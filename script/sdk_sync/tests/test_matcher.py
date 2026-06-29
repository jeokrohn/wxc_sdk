"""Regression tests for stub-to-SDK matching."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from script.sdk_sync import aliases, matcher
from script.sdk_sync.differ import ChangeRecord
from script.sdk_sync.ir import extract_from_text


def _point_matcher_at_tmp_sdk(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, source: str) -> Path:
    """Create a temporary SDK root and point the matcher index at it.

    :param tmp_path: Temporary directory from pytest.
    :type tmp_path: pathlib.Path
    :param monkeypatch: Pytest helper used to reset matcher globals.
    :type monkeypatch: pytest.MonkeyPatch
    :param source: Python source for ``wxc_sdk/common.py``.
    :type source: str
    :return: Path to the temporary SDK root.
    :rtype: pathlib.Path
    """
    sdk_root = tmp_path / 'wxc_sdk'
    sdk_root.mkdir()
    (sdk_root / 'common.py').write_text(textwrap.dedent(source))
    monkeypatch.setattr(matcher, '_SDK_ROOT', sdk_root)
    monkeypatch.setattr(matcher, '_index', matcher._SDKIndex())
    return sdk_root


def test_method_match_finds_non_last_api_class_in_sdk_module(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Ensure endpoint matching searches every API class in an SDK module.

    The regression case is a module whose last ``ApiChild`` subclass is not the
    class that owns the matching endpoint. The matcher must still find the
    earlier class by HTTP method and endpoint template.

    :param tmp_path: Temporary project root used for a synthetic SDK module.
    :param monkeypatch: Pytest helper used to point the matcher at that module.
    """
    # Build a minimal SDK module with two API classes. The endpoint we need is
    # intentionally on the non-last class to guard against old indexing behavior.
    sdk_root = tmp_path / 'wxc_sdk'
    sdk_root.mkdir()
    sdk_file = sdk_root / 'jobs.py'
    sdk_file.write_text(
        textwrap.dedent("""\
        from wxc_sdk.api_child import ApiChild


        class ManageNumbersJobsApi(ApiChild, base='telephony/config/jobs/numbers'):
            def initiate_job(self):
                url = self.ep('manageNumbers')
                return super().post(url)


        class JobsApi(ApiChild, base='telephony/config/jobs'):
            pass
        """)
    )

    # Point the matcher at the synthetic SDK root and reset the cached index so
    # the test only observes the fixture module above.
    monkeypatch.setattr(matcher, '_SDK_ROOT', sdk_root)
    monkeypatch.setattr(matcher, '_index', matcher._SDKIndex())

    # The generated stub uses a different class and method name but the same
    # effective POST endpoint, which is the contract the matcher joins on.
    stub_ir = extract_from_text(
        textwrap.dedent("""\
        from wxc_sdk.api_child import ApiChild


        class NumbersApi(ApiChild, base='telephony/config'):
            def initiate_number_jobs(self):
                url = self.ep('jobs/numbers/manageNumbers')
                return super().post(url)
        """),
        'open_api/generated/Webex-Suite/Webex-Calling/Webex-Cloud-Calling/All-APIs/numbers_auto.py',
    )
    record = ChangeRecord(
        kind='method_param_added',
        qualname='NumbersApi.initiate_number_jobs',
        old=None,
        new={'name': 'initiate_number_jobs'},
        severity='review',
    )

    match = matcher.match(record, stub_ir, aliases.AliasStore())

    assert match is not None
    assert match.sdk_class == 'ManageNumbersJobsApi'
    assert match.sdk_member == 'initiate_job'
    assert match.matched_by == 'exact'


def test_docstring_enum_value_structural_match_by_value_overlap(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Resolve a renamed SDK enum by structural value/name overlap.

    :param tmp_path: Temporary directory used for the synthetic SDK package.
    :type tmp_path: pathlib.Path
    :param monkeypatch: Pytest helper used to reset matcher globals.
    :type monkeypatch: pytest.MonkeyPatch
    :return: Nothing.
    :rtype: None
    """
    _point_matcher_at_tmp_sdk(
        tmp_path,
        monkeypatch,
        """\
        class OwnerType(str, Enum):
            #: The PSTN phone number's owner is a workspace.
            place = 'PLACE'
            #: The PSTN phone number's owner is a person.
            people = 'PEOPLE'
            #: The PSTN phone number's owner is a virtual line.
            virtual_line = 'VIRTUAL_LINE'
            #: The PSTN phone number's owner is an auto-attendant.
            auto_attendant = 'AUTO_ATTENDANT'
            #: The PSTN phone number's owner is a call queue.
            call_queue = 'CALL_QUEUE'
            #: The PSTN phone number's owner is a hunt group.
            hunt_group = 'HUNT_GROUP'
        """,
    )
    stub_ir = extract_from_text(
        textwrap.dedent("""\
        class NumberOwnerType(str, Enum):
            #: Number's owner is a workspace.
            place = 'PLACE'
            #: Number's owner is a person.
            people = 'PEOPLE'
            #: Number's owner is a Virtual Profile.
            virtual_line = 'VIRTUAL_LINE'
            #: Number's owner is an auto-attendant.
            auto_attendant = 'AUTO_ATTENDANT'
            #: Number's owner is a call queue.
            call_queue = 'CALL_QUEUE'
            #: Number's owner is a hunt group.
            hunt_group = 'HUNT_GROUP'
        """),
        'open_api/generated/features-auto-attendant_auto.py',
    )
    record = ChangeRecord(
        kind='docstring_changed',
        qualname='NumberOwnerType.call_queue',
        old={'doc_comment': "PSTN phone number's owner is a call queue."},
        new={'doc_comment': "Number's owner is a call queue."},
        severity='trivial',
    )

    match = matcher.match(record, stub_ir, aliases.AliasStore())

    assert match is not None
    assert match.sdk_class == 'OwnerType'
    assert match.sdk_member == 'call_queue'
    assert match.matched_by == 'structural-enum'


def test_docstring_model_field_structural_match_by_wire_alias(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Resolve a reused SDK model field using ``Field(alias=...)`` wire names.

    :param tmp_path: Temporary directory used for the synthetic SDK package.
    :type tmp_path: pathlib.Path
    :param monkeypatch: Pytest helper used to reset matcher globals.
    :type monkeypatch: pytest.MonkeyPatch
    :return: Nothing.
    :rtype: None
    """
    _point_matcher_at_tmp_sdk(
        tmp_path,
        monkeypatch,
        """\
        class OwnerType(str, Enum):
            people = 'PEOPLE'


        class NumberOwner(ApiModel):
            #: Unique identifier of the owner.
            owner_id: Optional[str] = Field(alias='id', default=None)
            #: Type of the owner.
            owner_type: Optional[OwnerType] = Field(alias='type', default=None)
            #: First name.
            first_name: Optional[str] = None
            #: Last name.
            last_name: Optional[str] = None
            #: Display name.
            display_name: Optional[str] = None
        """,
    )
    stub_ir = extract_from_text(
        textwrap.dedent("""\
        class NumberOwnerType(str, Enum):
            people = 'PEOPLE'


        class AutoAttendantCallForwardAvailableNumberObjectOwner(ApiModel):
            #: Unique identifier of the owner.
            id: Optional[str] = None
            #: Type of the owner.
            type: Optional[NumberOwnerType] = None
            #: First name.
            first_name: Optional[str] = None
            #: Last name.
            last_name: Optional[str] = None
            #: Display name.
            display_name: Optional[str] = None
        """),
        'open_api/generated/features-auto-attendant_auto.py',
    )
    record = ChangeRecord(
        kind='docstring_changed',
        qualname='AutoAttendantCallForwardAvailableNumberObjectOwner.type',
        old={'doc_comment': 'Type of the PSTN phone number owner.'},
        new={'doc_comment': 'Type of the number owner.'},
        severity='trivial',
    )

    match = matcher.match(record, stub_ir, aliases.AliasStore())

    assert match is not None
    assert match.sdk_class == 'NumberOwner'
    assert match.sdk_member == 'owner_type'
    assert match.matched_by == 'structural-model'


def test_model_field_added_structural_match_by_pre_add_wire_shape(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Resolve an added field to a reused SDK model by pre-addition shape.

    The added field itself is expected to be absent from the SDK. The safe
    class-level evidence is the already-shared wire fields plus the matched
    endpoint return type: the generated stranded-calls response maps to SDK
    ``StrandedCalls``.

    :param tmp_path: Temporary directory used for the synthetic SDK package.
    :type tmp_path: pathlib.Path
    :param monkeypatch: Pytest helper used to reset matcher globals.
    :type monkeypatch: pytest.MonkeyPatch
    :return: Nothing.
    :rtype: None
    """
    _point_matcher_at_tmp_sdk(
        tmp_path,
        monkeypatch,
        """\
        class StrandedCalls(ApiModel):
            #: The call processing action type.
            action: Optional[StrandedCallsAction] = None
            #: Call gets transferred to this number when action is set to TRANSFER.
            transfer_phone_number: Optional[str] = None
            #: The type of announcement to be played.
            audio_message_selection: Optional[Greeting] = None
            #: List of Announcement Audio Files when audioMessageSelection is CUSTOM.
            audio_files: Optional[list[AnnAudioFile]] = None


        class CQPolicyApi(ApiChild, base='telephony/config/locations'):
            def stranded_calls_details(self, location_id: str, queue_id: str) -> StrandedCalls:
                url = self.ep(f'{location_id}/queues/{queue_id}/strandedCalls')
                return self.get(url=url)
        """,
    )
    stub_ir = extract_from_text(
        textwrap.dedent("""\
        class GetCallQueueStrandedCallsObject(ApiModel):
            #: The call processing action type.
            action: Optional[GetCallQueueStrandedCallsObjectAction] = None
            #: Call gets transferred to this number when action is set to `TRANSFER`.
            transfer_phone_number: Optional[str] = None
            #: The type of announcement to be played.
            audio_message_selection: Optional[CallQueueQueueSettingsGetObjectOverflowGreeting] = None
            #: List of Announcement Audio Files when `audioMessageSelection` is `CUSTOM`.
            audio_files: Optional[list[AudioAnnouncementFileFeatureGetObject]] = None
            #: Trigger stranded calls queue policy when all agents are unreachable.
            trigger_policy_when_all_agents_are_unreachable_enabled: Optional[bool] = None


        class FeaturesCallQueueApi(ApiChild, base='telephony/config'):
            def get_call_queue_stranded_calls(
                self,
                location_id: str,
                queue_id: str,
            ) -> GetCallQueueStrandedCallsObject:
                url = self.ep(f'locations/{location_id}/queues/{queue_id}/strandedCalls')
                return self.get(url=url)
        """),
        'open_api/generated/features-call-queue_auto.py',
    )
    record = ChangeRecord(
        kind='model_field_added',
        qualname='GetCallQueueStrandedCallsObject.trigger_policy_when_all_agents_are_unreachable_enabled',
        old=None,
        new={
            'name': 'trigger_policy_when_all_agents_are_unreachable_enabled',
            'annotation': 'Optional[bool]',
            'default': 'None',
            'doc_comment': 'Trigger stranded calls queue policy when all agents are unreachable.',
        },
        severity='trivial',
    )

    match = matcher.match(record, stub_ir, aliases.AliasStore())

    assert match is not None
    assert match.sdk_class == 'StrandedCalls'
    assert match.sdk_member == 'trigger_policy_when_all_agents_are_unreachable_enabled'
    assert match.matched_by == 'structural-model-add'
    assert match.confidence == pytest.approx(1.0)


def test_model_field_added_ambiguous_structural_matches_are_not_accepted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Report tied added-field candidates instead of choosing arbitrarily.

    :param tmp_path: Temporary directory used for the synthetic SDK package.
    :type tmp_path: pathlib.Path
    :param monkeypatch: Pytest helper used to reset matcher globals.
    :type monkeypatch: pytest.MonkeyPatch
    :return: Nothing.
    :rtype: None
    """
    _point_matcher_at_tmp_sdk(
        tmp_path,
        monkeypatch,
        """\
        class FirstWidget(ApiModel):
            id: Optional[str] = None
            name: Optional[str] = None


        class SecondWidget(ApiModel):
            id: Optional[str] = None
            name: Optional[str] = None
        """,
    )
    stub_ir = extract_from_text(
        textwrap.dedent("""\
        class GeneratedWidget(ApiModel):
            id: Optional[str] = None
            name: Optional[str] = None
            color: Optional[str] = None
        """),
        'open_api/generated/widgets_auto.py',
    )
    record = ChangeRecord(
        kind='model_field_added',
        qualname='GeneratedWidget.color',
        old=None,
        new={
            'name': 'color',
            'annotation': 'Optional[str]',
            'default': 'None',
            'doc_comment': 'The widget color.',
        },
        severity='trivial',
    )
    store = aliases.AliasStore()

    match = matcher.match(record, stub_ir, store)

    assert match is None
    assert [candidate['sdk_class'] for candidate in store.unmatched[0].candidates[:2]] == [
        'FirstWidget',
        'SecondWidget',
    ]
    assert 'added target field absent as expected' in store.unmatched[0].candidates[0]['detail']


def test_docstring_enum_value_partial_mismatch_reports_candidate_without_match(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Do not auto-map enum values whose Python name and wire value both differ.

    :param tmp_path: Temporary directory used for the synthetic SDK package.
    :type tmp_path: pathlib.Path
    :param monkeypatch: Pytest helper used to reset matcher globals.
    :type monkeypatch: pytest.MonkeyPatch
    :return: Nothing.
    :rtype: None
    """
    _point_matcher_at_tmp_sdk(
        tmp_path,
        monkeypatch,
        """\
        class OwnerType(str, Enum):
            place = 'PLACE'
            people = 'PEOPLE'
            paging_group = 'PAGING_GROUP'
        """,
    )
    stub_ir = extract_from_text(
        textwrap.dedent("""\
        class NumberOwnerType(str, Enum):
            place = 'PLACE'
            people = 'PEOPLE'
            group_paging = 'GROUP_PAGING'
        """),
        'open_api/generated/features-auto-attendant_auto.py',
    )
    record = ChangeRecord(
        kind='docstring_changed',
        qualname='NumberOwnerType.group_paging',
        old={'doc_comment': "PSTN phone number's owner is a group paging."},
        new={'doc_comment': "Number's owner is a group paging."},
        severity='trivial',
    )
    store = aliases.AliasStore()

    match = matcher.match(record, stub_ir, store)

    assert match is None
    assert store.unmatched
    assert store.unmatched[0].candidates[0]['sdk_class'] == 'OwnerType'
    assert 'no same name or wire value' in store.unmatched[0].candidates[0]['detail']


def test_docstring_enum_value_ambiguous_structural_matches_are_not_accepted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Report tied enum candidates instead of choosing arbitrarily.

    :param tmp_path: Temporary directory used for the synthetic SDK package.
    :type tmp_path: pathlib.Path
    :param monkeypatch: Pytest helper used to reset matcher globals.
    :type monkeypatch: pytest.MonkeyPatch
    :return: Nothing.
    :rtype: None
    """
    _point_matcher_at_tmp_sdk(
        tmp_path,
        monkeypatch,
        """\
        class FirstColor(str, Enum):
            red = 'RED'
            blue = 'BLUE'


        class SecondColor(str, Enum):
            red = 'RED'
            blue = 'BLUE'
        """,
    )
    stub_ir = extract_from_text(
        textwrap.dedent("""\
        class GeneratedColor(str, Enum):
            red = 'RED'
            blue = 'BLUE'
        """),
        'open_api/generated/colors_auto.py',
    )
    record = ChangeRecord(
        kind='docstring_changed',
        qualname='GeneratedColor.red',
        old={'doc_comment': 'Old red.'},
        new={'doc_comment': 'New red.'},
        severity='trivial',
    )
    store = aliases.AliasStore()

    match = matcher.match(record, stub_ir, store)

    assert match is None
    assert [candidate['sdk_class'] for candidate in store.unmatched[0].candidates[:2]] == ['FirstColor', 'SecondColor']


def test_docstring_enum_value_exact_name_match_still_wins(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Keep the existing exact class/member match behavior.

    :param tmp_path: Temporary directory used for the synthetic SDK package.
    :type tmp_path: pathlib.Path
    :param monkeypatch: Pytest helper used to reset matcher globals.
    :type monkeypatch: pytest.MonkeyPatch
    :return: Nothing.
    :rtype: None
    """
    _point_matcher_at_tmp_sdk(
        tmp_path,
        monkeypatch,
        """\
        class NumberOwnerType(str, Enum):
            call_queue = 'CALL_QUEUE'
        """,
    )
    stub_ir = extract_from_text(
        textwrap.dedent("""\
        class NumberOwnerType(str, Enum):
            call_queue = 'CALL_QUEUE'
        """),
        'open_api/generated/features-auto-attendant_auto.py',
    )
    record = ChangeRecord(
        kind='docstring_changed',
        qualname='NumberOwnerType.call_queue',
        old={'doc_comment': 'Old.'},
        new={'doc_comment': 'New.'},
        severity='trivial',
    )

    match = matcher.match(record, stub_ir, aliases.AliasStore())

    assert match is not None
    assert match.sdk_class == 'NumberOwnerType'
    assert match.sdk_member == 'call_queue'
    assert match.matched_by == 'exact'
