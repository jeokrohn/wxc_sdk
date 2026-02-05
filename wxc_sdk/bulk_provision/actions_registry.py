from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class ActionResult:
    remote_id: Optional[str]
    message: str


@dataclass(frozen=True)
class Action:
    entity_type: str
    step: str
    lookup: Callable
    upsert: Callable


class ActionsRegistry:
    def __init__(self) -> None:
        self._actions: dict[str, list[Action]] = {}

    def register(self, action: Action) -> None:
        self._actions.setdefault(action.entity_type, []).append(action)

    def actions_for(self, entity_type: str) -> list[Action]:
        return self._actions.get(entity_type, [])
