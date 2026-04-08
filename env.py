from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Dict


@dataclass
class StepResult:
    next_state: Dict[str, Any] | None
    reward: float
    done: bool
    info: Dict[str, Any] = field(default_factory=dict)


class FraudEnv:
    ACTIONS = ["approve", "flag", "block"]
    REWARDS = {"correct": 1.0, "flag": 0.5, "wrong": -1.0}
    LABEL_KEY = "label"

    def __init__(self, transactions: List[Dict[str, Any]]) -> None:
        if not transactions:
            raise ValueError("transactions must be non-empty")

        self._transactions = transactions
        self._index = 0
        self._total_reward = 0.0

    # ---------- public API ----------

    def reset(self) -> Dict[str, Any]:
        self._index = 0
        self._total_reward = 0.0
        return self._state

    def step(self, action: int) -> StepResult:
        if action not in range(len(self.ACTIONS)):
            raise ValueError(f"action must be 0-{len(self.ACTIONS)-1}, got {action}")

        reward = self._reward_for(action)
        self._total_reward += reward
        self._index += 1

        done = self._index >= len(self._transactions)

        return StepResult(
            next_state=None if done else self._state,
            reward=reward,
            done=done,
        )

    # ---------- private helpers ----------

    @property
    def _state(self) -> Dict[str, Any]:
        return {
            k: v
            for k, v in self._transactions[self._index].items()
            if k != self.LABEL_KEY
        }

    def _reward_for(self, action: int) -> float:
        current = self._transactions[self._index]
        action_str = self.ACTIONS[action]
        correct_str = current[self.LABEL_KEY]

        if action_str == correct_str:
            return self.REWARDS["correct"]
        if action_str == "flag":
            return self.REWARDS["flag"]
        return self.REWARDS["wrong"]