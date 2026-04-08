from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Tuple

ACTION_INDEX = {"approve": 0, "flag": 1, "block": 2}


@dataclass(frozen=True, slots=True)
class RuleConfig:
    review_amount: float = 4000.0
    elevated_amount: float = 12000.0
    block_amount: float = 15000.0
    foreign_block_amount: float = 6000.0
    review_user_risk: float = 0.6
    high_user_risk: float = 0.7
    very_high_user_risk: float = 0.75
    review_transaction_count: int = 3
    high_transaction_count: int = 4
    very_high_transaction_count: int = 5
    burst_transaction_count: int = 7

    home_locations: frozenset[str] = field(
        default_factory=lambda: frozenset({"IN", "US"})
    )
    block_locations: frozenset[str] = field(
        default_factory=lambda: frozenset({"NG"})
    )
    review_locations: frozenset[str] = field(
        default_factory=lambda: frozenset({"RU"})
    )


# 🚀 UPDATED FUNCTION
def decide(
    state: Mapping[str, Any], config: RuleConfig | None = None
) -> Tuple[int, float, str]:

    config = config or RuleConfig()

    amount = float(state.get("amount", 0.0))
    user_risk = float(state.get("user_risk", 0.0))
    tx_count = int(state.get("transaction_count_1hr", 0))
    location = str(state.get("location", "")).upper()

    is_foreign = _is_foreign(state, location, config)
    off_hours = _is_off_hours(state.get("time"))

    # -------------------------------
    # 🧠 RISK SCORE (NEW)
    # -------------------------------
    risk = 0.0
    reasons = []

    if amount >= config.block_amount:
        risk += 0.5
        reasons.append("Very high transaction amount")
    elif amount >= config.review_amount:
        risk += 0.3
        reasons.append("High transaction amount")

    if user_risk >= config.very_high_user_risk:
        risk += 0.3
        reasons.append("Very high user risk")
    elif user_risk >= config.review_user_risk:
        risk += 0.2
        reasons.append("Elevated user risk")

    if tx_count >= config.burst_transaction_count:
        risk += 0.3
        reasons.append("Too many transactions in short time")
    elif tx_count >= config.review_transaction_count:
        risk += 0.2
        reasons.append("High transaction frequency")

    if is_foreign:
        risk += 0.2
        reasons.append("Foreign transaction")

    if off_hours:
        risk += 0.1
        reasons.append("Odd transaction time")

    if location in config.block_locations:
        risk += 0.4
        reasons.append("Blocked country")

    if location in config.review_locations:
        risk += 0.2
        reasons.append("Suspicious location")

    risk = min(risk, 1.0)

    # -------------------------------
    # 🎯 ORIGINAL DECISION LOGIC (UNCHANGED)
    # -------------------------------

    if location in config.block_locations and amount >= config.review_amount:
        action = ACTION_INDEX["block"]

    elif _should_block(
        amount=amount,
        user_risk=user_risk,
        tx_count=tx_count,
        is_foreign=is_foreign,
        off_hours=off_hours,
        config=config,
    ):
        action = ACTION_INDEX["block"]

    elif (
        location in config.review_locations
        or _should_flag(
            amount=amount,
            user_risk=user_risk,
            tx_count=tx_count,
            is_foreign=is_foreign,
            off_hours=off_hours,
            config=config,
        )
    ):
        action = ACTION_INDEX["flag"]

    else:
        action = ACTION_INDEX["approve"]

    # -------------------------------
    # 🧾 FINAL REASON
    # -------------------------------
    if not reasons:
        reason = "Low risk transaction"
    else:
        reason = ", ".join(reasons)

    return action, risk, reason


# -------------------------------
# HELPERS (UNCHANGED)
# -------------------------------

def _is_foreign(
    state: Mapping[str, Any], location: str, config: RuleConfig
) -> bool:
    if "is_foreign" in state:
        return bool(state["is_foreign"])
    if location:
        return location not in config.home_locations
    return False


def _is_off_hours(hour: Any) -> bool:
    if hour is None:
        return False
    try:
        hour_int = int(hour)
    except (TypeError, ValueError):
        return False
    return hour_int >= 22 or hour_int <= 5


def _should_block(
    *,
    amount: float,
    user_risk: float,
    tx_count: int,
    is_foreign: bool,
    off_hours: bool,
    config: RuleConfig,
) -> bool:
    return any(
        (
            amount >= config.block_amount
            and (
                is_foreign
                or user_risk >= config.very_high_user_risk
                or tx_count >= config.very_high_transaction_count
            ),
            amount >= config.foreign_block_amount
            and is_foreign
            and user_risk >= config.high_user_risk
            and tx_count >= config.high_transaction_count,
            tx_count >= config.burst_transaction_count
            and user_risk >= config.very_high_user_risk,
            amount >= config.foreign_block_amount
            and is_foreign
            and off_hours
            and user_risk >= config.very_high_user_risk,
        )
    )


def _should_flag(
    *,
    amount: float,
    user_risk: float,
    tx_count: int,
    is_foreign: bool,
    off_hours: bool,
    config: RuleConfig,
) -> bool:
    return any(
        (
            amount >= config.elevated_amount,
            amount >= config.review_amount
            and (
                is_foreign
                or user_risk >= config.review_user_risk
                or tx_count >= config.high_transaction_count
            ),
            amount >= 2500.0 and user_risk >= config.review_user_risk,
            user_risk >= config.high_user_risk and is_foreign,
            tx_count >= config.review_transaction_count
            and user_risk >= config.review_user_risk,
            off_hours
            and (
                is_foreign
                or user_risk >= config.review_user_risk
                or tx_count >= config.very_high_transaction_count
            ),
        )
    )