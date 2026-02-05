import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from wxc_sdk import WebexSimpleApi
from wxc_sdk.locations import Location
from wxc_sdk.people import Person
from wxc_sdk.workspaces import Workspace

from .action_helpers import build_person, build_workspace
from .batch_iterator import iter_batches
from .config import Config
from .data_pipeline import DataPipelineResult, DeviceRow, SiteBundle, UserRow, WorkspaceRow, build_pipeline
from .error_handling import ErrorInfo, ReasonCode, classify_http_status, map_exception
from .state_store import CheckpointStore
from .writers import Writers

log = logging.getLogger(__name__)


@dataclass
class ExecutorContext:
    config: Config
    api: WebexSimpleApi
    site_bundle: SiteBundle
    writers: Writers
    checkpoint: CheckpointStore
    run_dir: Path
    location_cache: dict[str, dict[str, Any]]


class Executor:
    def __init__(self, config: Config) -> None:
        self.config = config

    def run(self) -> None:
        pipeline = build_pipeline(self.config.input_dir)
        run_dir = self._run_dir()
        writers = Writers(
            results_path=run_dir / "results.csv",
            pending_path=run_dir / "pending_rows.csv",
            rejected_path=run_dir / "rejected_rows.csv",
        )
        for rejected in pipeline.rejected:
            writers.write_rejected(
                row_id=rejected.row_id,
                reason_code=rejected.reason_code.value,
                reason_message=rejected.reason_message,
                raw_row_minified=rejected.raw_row_minified,
            )
        checkpoint = CheckpointStore(run_dir / "checkpoint.json")
        api = self._build_api()
        context = ExecutorContext(
            config=self.config,
            api=api,
            site_bundle=pipeline.site_bundle,
            writers=writers,
            checkpoint=checkpoint,
            run_dir=run_dir,
            location_cache={},
        )
        self._process_locations(context)
        self._process_users(context, pipeline)
        self._process_workspaces(context, pipeline)
        self._process_devices(context, pipeline)

    def _run_dir(self) -> Path:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        run_dir = self.config.output_dir / f"run_{timestamp}_{self.config.environment}"
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def _build_api(self) -> WebexSimpleApi:
        api = WebexSimpleApi(
            tokens=self.config.webex_token,
            retry_429=False,
            concurrent_requests=1,
        )
        api.session.BASE = self.config.webex_base_url
        return api

    def _process_locations(self, context: ExecutorContext) -> None:
        locations = list(context.site_bundle.locations.values())
        for batch in iter_batches(
            locations,
            batch_size=self.config.batch_size_users,
            max_rows=self.config.max_rows_users,
            max_batches=self.config.max_rows_users // self.config.batch_size_users + 1,
        ):
            self._log_batch_start(batch.batch_id, "location")
            for index, location_payload in enumerate(batch.items, 1):
                row_id = index
                location_key = location_payload.get("location_key", f"location_{row_id}")
                try:
                    location_id = self._lookup_location(context, location_payload)
                    if location_id:
                        self._update_location(context, location_id, location_payload)
                        context.writers.write_result(
                            batch_id=batch.batch_id,
                            row_id=row_id,
                            entity_type="location",
                            entity_key=location_key,
                            step="update",
                            status="success",
                            http_status=200,
                            message="updated",
                            remote_id=location_id,
                        )
                    else:
                        location_id = self._create_location(context, location_payload)
                        context.writers.write_result(
                            batch_id=batch.batch_id,
                            row_id=row_id,
                            entity_type="location",
                            entity_key=location_key,
                            step="create",
                            status="success",
                            http_status=200,
                            message="created",
                            remote_id=location_id,
                        )
                    self._write_checkpoint(context, "location", row_id)
                except Exception as exc:
                    info = map_exception(exc)
                    context.writers.write_pending(
                        batch_id=batch.batch_id,
                        row_id=row_id,
                        entity_type="location",
                        entity_key=location_key,
                        step="location",
                        reason_code=info.reason_code.value,
                        reason_message=info.reason_message,
                        http_status=info.http_status,
                        raw_row_minified=json.dumps({"location_key": location_key}),
                    )
            self._log_batch_end(batch.batch_id, "location")

    def _process_users(self, context: ExecutorContext, pipeline: DataPipelineResult) -> None:
        for batch in iter_batches(
            pipeline.users,
            batch_size=self.config.batch_size_users,
            max_rows=self.config.max_rows_users,
            max_batches=self.config.max_rows_users // self.config.batch_size_users + 1,
        ):
            self._log_batch_start(batch.batch_id, "user")
            for row in batch.items:
                self._process_user_row(context, batch.batch_id, row)
            self._log_batch_end(batch.batch_id, "user")

    def _process_workspaces(self, context: ExecutorContext, pipeline: DataPipelineResult) -> None:
        for batch in iter_batches(
            pipeline.workspaces,
            batch_size=self.config.batch_size_users,
            max_rows=self.config.max_rows_users,
            max_batches=self.config.max_rows_users // self.config.batch_size_users + 1,
        ):
            self._log_batch_start(batch.batch_id, "workspace")
            for row in batch.items:
                self._process_workspace_row(context, batch.batch_id, row)
            self._log_batch_end(batch.batch_id, "workspace")

    def _process_devices(self, context: ExecutorContext, pipeline: DataPipelineResult) -> None:
        for batch in iter_batches(
            pipeline.devices,
            batch_size=self.config.batch_size_users,
            max_rows=self.config.max_rows_users,
            max_batches=self.config.max_rows_users // self.config.batch_size_users + 1,
        ):
            self._log_batch_start(batch.batch_id, "device")
            for row in batch.items:
                context.writers.write_pending(
                    batch_id=batch.batch_id,
                    row_id=row.row_id,
                    entity_type="device",
                    entity_key=row.entity_key,
                    step="device",
                    reason_code=ReasonCode.out_of_scope.value,
                    reason_message="Device operations not implemented",
                    http_status=None,
                    raw_row_minified=json.dumps(
                        {"device_type": row.data.get("device_type"), "owner_key": row.data.get("owner_key")}
                    ),
                )
            self._log_batch_end(batch.batch_id, "device")

    def _process_user_row(self, context: ExecutorContext, batch_id: int, row: UserRow) -> None:
        location_id = self._resolve_location_id(context, row.location_key)
        if not location_id:
            context.writers.write_pending(
                batch_id=batch_id,
                row_id=row.row_id,
                entity_type="user",
                entity_key=row.entity_key,
                step="lookup_location",
                reason_code=ReasonCode.ambiguous_match.value,
                reason_message=f"Unknown location_key {row.location_key}",
                http_status=None,
                raw_row_minified=json.dumps({"email": row.entity_key, "location_key": row.location_key}),
            )
            return
        licenses = self._resolve_profile_list(context.site_bundle, "licenses", row.data.get("licenses"))
        person = build_person(email=row.entity_key, location_id=location_id, licenses=licenses)
        try:
            remote = self._lookup_person(context, row.entity_key)
            if remote:
                self._update_person(context, remote.person_id, person)
                status = "update"
                remote_id = remote.person_id
            else:
                created = context.api.people.create(person)
                status = "create"
                remote_id = created.person_id
            context.writers.write_result(
                batch_id=batch_id,
                row_id=row.row_id,
                entity_type="user",
                entity_key=row.entity_key,
                step=status,
                status="success",
                http_status=200,
                message="ok",
                remote_id=remote_id,
            )
            self._write_checkpoint(context, "user", row.row_id)
        except Exception as exc:
            info = map_exception(exc)
            context.writers.write_pending(
                batch_id=batch_id,
                row_id=row.row_id,
                entity_type="user",
                entity_key=row.entity_key,
                step="user",
                reason_code=info.reason_code.value,
                reason_message=info.reason_message,
                http_status=info.http_status,
                raw_row_minified=json.dumps({"email": row.entity_key}),
            )

    def _process_workspace_row(self, context: ExecutorContext, batch_id: int, row: WorkspaceRow) -> None:
        location_id = self._resolve_location_id(context, row.location_key)
        if not location_id:
            context.writers.write_pending(
                batch_id=batch_id,
                row_id=row.row_id,
                entity_type="workspace",
                entity_key=row.entity_key,
                step="lookup_location",
                reason_code=ReasonCode.ambiguous_match.value,
                reason_message=f"Unknown location_key {row.location_key}",
                http_status=None,
                raw_row_minified=json.dumps({"workspace_display_name": row.entity_key}),
            )
            return
        licenses = self._resolve_profile_list(context.site_bundle, "licenses", row.data.get("licenses"))
        workspace = build_workspace(
            display_name=row.entity_key,
            location_id=location_id,
            external_id=row.data.get("workspace_external_id"),
            licenses=licenses,
        )
        try:
            remote = self._lookup_workspace(context, row.entity_key)
            if remote:
                self._update_workspace(context, remote.workspace_id, workspace)
                status = "update"
                remote_id = remote.workspace_id
            else:
                created = context.api.workspaces.create(workspace)
                status = "create"
                remote_id = created.workspace_id
            context.writers.write_result(
                batch_id=batch_id,
                row_id=row.row_id,
                entity_type="workspace",
                entity_key=row.entity_key,
                step=status,
                status="success",
                http_status=200,
                message="ok",
                remote_id=remote_id,
            )
            self._write_checkpoint(context, "workspace", row.row_id)
        except Exception as exc:
            info = map_exception(exc)
            context.writers.write_pending(
                batch_id=batch_id,
                row_id=row.row_id,
                entity_type="workspace",
                entity_key=row.entity_key,
                step="workspace",
                reason_code=info.reason_code.value,
                reason_message=info.reason_message,
                http_status=info.http_status,
                raw_row_minified=json.dumps({"workspace_display_name": row.entity_key}),
            )

    def _lookup_location(self, context: ExecutorContext, payload: dict[str, Any]) -> Optional[str]:
        name = payload.get("location_name") or payload.get("name")
        external_id = payload.get("location_external_id") or payload.get("external_id")
        cache_key = external_id or name
        if cache_key and cache_key in context.location_cache:
            return context.location_cache[cache_key]["location_id"]
        locations = list(context.api.locations.list())
        for location in locations:
            if external_id and getattr(location, "external_id", None) == external_id:
                context.location_cache[cache_key] = {"location_id": location.location_id}
                return location.location_id
            if name and location.name == name:
                context.location_cache[cache_key] = {"location_id": location.location_id}
                return location.location_id
        return None

    def _create_location(self, context: ExecutorContext, payload: dict[str, Any]) -> str:
        return context.api.locations.create(
            name=payload["name"],
            time_zone=payload["time_zone"],
            preferred_language=payload["preferred_language"],
            announcement_language=payload["announcement_language"],
            address1=payload["address1"],
            city=payload["city"],
            state=payload["state"],
            postal_code=payload["postal_code"],
            country=payload["country"],
            address2=payload.get("address2"),
            latitude=payload.get("latitude"),
            longitude=payload.get("longitude"),
            notes=payload.get("notes"),
            org_id=context.config.org_id,
        )

    def _update_location(self, context: ExecutorContext, location_id: str, payload: dict[str, Any]) -> None:
        settings = Location.model_validate(payload)
        context.api.locations.update(location_id=location_id, settings=settings, org_id=context.config.org_id)

    def _lookup_person(self, context: ExecutorContext, email: str) -> Optional[Person]:
        people = list(context.api.people.list(email=email))
        return people[0] if people else None

    def _update_person(self, context: ExecutorContext, person_id: str, person: Person) -> None:
        context.api.people.update(person_id=person_id, settings=person)

    def _lookup_workspace(self, context: ExecutorContext, display_name: str) -> Optional[Workspace]:
        workspaces = list(context.api.workspaces.list(display_name=display_name))
        return workspaces[0] if workspaces else None

    def _update_workspace(self, context: ExecutorContext, workspace_id: str, workspace: Workspace) -> None:
        context.api.workspaces.update(workspace_id=workspace_id, settings=workspace)

    def _resolve_location_id(self, context: ExecutorContext, location_key: str) -> Optional[str]:
        location_payload = context.site_bundle.locations.get(location_key)
        if not location_payload:
            return None
        return self._lookup_location(context, location_payload)

    def _resolve_profile_list(self, site_bundle: SiteBundle, profile_key: str, profile_name: Optional[str]) -> list[str]:
        if not profile_name:
            return []
        profiles = site_bundle.payload.get("profiles", {})
        profile = profiles.get(profile_key, {}).get(profile_name)
        if not profile:
            return []
        return profile if isinstance(profile, list) else []

    def _write_checkpoint(self, context: ExecutorContext, phase: str, last_item_id: int) -> None:
        payload = {
            "pipeline_version": context.config.pipeline_version,
            "input_hash": context.site_bundle.input_hash,
            "phase": phase,
            "last_item_id": last_item_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        context.checkpoint.write(payload)

    def _log_batch_start(self, batch_id: int, entity_type: str) -> None:
        log.info(
            "batch_start",
            extra={"batch_id": batch_id, "entity_type": entity_type},
        )

    def _log_batch_end(self, batch_id: int, entity_type: str) -> None:
        log.info(
            "batch_end",
            extra={"batch_id": batch_id, "entity_type": entity_type},
        )
