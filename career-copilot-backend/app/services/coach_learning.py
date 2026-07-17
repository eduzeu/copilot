import math

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.coach_learning import CoachInteraction, CoachPolicy


STRATEGIES = (
    "direct_action",
    "structured_plan",
    "diagnostic",
    "socratic",
)

STRATEGY_INSTRUCTIONS = {
    "direct_action": "Lead with the answer and give the smallest set of high-impact actions.",
    "structured_plan": "Organize the response as a sequenced plan with measurable checkpoints.",
    "diagnostic": "Briefly diagnose the strongest evidence, then connect each action to that evidence.",
    "socratic": "When a missing decision-critical fact exists, ask one sharp question; otherwise give advice and one reflective question.",
}


def _get_policy(db: Session, user_id: int) -> CoachPolicy:
    policy = db.query(CoachPolicy).filter(CoachPolicy.user_id == user_id).first()
    if not policy:
        policy = CoachPolicy(user_id=user_id, state={})
        db.add(policy)
        db.flush()
    return policy


def choose_strategy(db: Session, user_id: int, mode: str) -> str:
    """Select a coaching strategy with a mode-specific UCB1 online bandit."""
    policy = _get_policy(db, user_id)
    mode_state = policy.state.get(mode, {})

    # Explore every strategy once before optimizing from feedback.
    for strategy in STRATEGIES:
        if int(mode_state.get(strategy, {}).get("count", 0)) == 0:
            return strategy

    total = sum(int(mode_state[s]["count"]) for s in STRATEGIES)
    scores = {}
    for strategy in STRATEGIES:
        arm = mode_state[strategy]
        count = int(arm["count"])
        average_reward = float(arm["reward_sum"]) / count
        exploration_bonus = math.sqrt(2 * math.log(total) / count)
        scores[strategy] = average_reward + exploration_bonus
    return max(STRATEGIES, key=lambda item: scores[item])


def record_interaction(
    db: Session, user_id: int, mode: str, strategy: str, message: str, response: str
) -> CoachInteraction:
    interaction = CoachInteraction(
        user_id=user_id,
        mode=mode,
        strategy=strategy,
        user_message=message,
        response=response,
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


def train_from_feedback(
    db: Session, user_id: int, interaction_id: int, helpful: bool
) -> CoachInteraction:
    interaction = (
        db.query(CoachInteraction)
        .filter(CoachInteraction.id == interaction_id, CoachInteraction.user_id == user_id)
        .first()
    )
    if not interaction:
        raise HTTPException(status_code=404, detail="Coach interaction not found")

    reward = 1 if helpful else 0
    previous_reward = interaction.feedback
    policy = _get_policy(db, user_id)
    state = dict(policy.state or {})
    mode_state = dict(state.get(interaction.mode, {}))
    arm = dict(mode_state.get(interaction.strategy, {"count": 0, "reward_sum": 0.0}))

    if previous_reward is None:
        arm["count"] = int(arm["count"]) + 1
        arm["reward_sum"] = float(arm["reward_sum"]) + reward
    else:
        arm["reward_sum"] = float(arm["reward_sum"]) - previous_reward + reward

    mode_state[interaction.strategy] = arm
    state[interaction.mode] = mode_state
    policy.state = state
    interaction.feedback = reward
    db.commit()
    db.refresh(interaction)
    return interaction
