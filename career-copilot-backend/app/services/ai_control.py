import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Callable

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.metrics import increment
from app.models.ai_control import AIRequestLog, AIResponseCache


def enforce_daily_quota(db: Session, user_id: int, feature: str) -> None:
    start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    used = (
        db.query(func.count(AIRequestLog.id))
        .filter(AIRequestLog.user_id == user_id, AIRequestLog.created_at >= start)
        .scalar()
        or 0
    )
    if used >= settings.ai_daily_requests_per_user:
        raise HTTPException(
            status_code=429,
            detail="You reached today's AI request limit. Cached results and non-AI features remain available.",
            headers={"Retry-After": "3600"},
        )


def record_ai_request(db: Session, user_id: int, feature: str, status: str = "completed") -> None:
    db.add(AIRequestLog(user_id=user_id, feature=feature, status=status))
    db.commit()
    increment("ai.requests", tags=[f"feature:{feature}", f"status:{status}"])


def run_cached_json(
    db: Session,
    user_id: int,
    feature: str,
    operation: Callable[..., dict],
    *args,
) -> dict:
    material = json.dumps(
        {"feature": feature, "args": args, "model": settings.ai_model, "prompt": settings.prompt_version},
        sort_keys=True,
        default=str,
    )
    cache_key = hashlib.sha256(material.encode("utf-8")).hexdigest()
    now = datetime.now(timezone.utc)
    cached = (
        db.query(AIResponseCache)
        .filter(AIResponseCache.cache_key == cache_key, AIResponseCache.expires_at > now)
        .first()
    )
    if cached:
        increment("ai.cache", tags=[f"feature:{feature}", "result:hit"])
        return {**cached.response, "cached": True}

    increment("ai.cache", tags=[f"feature:{feature}", "result:miss"])
    enforce_daily_quota(db, user_id, feature)
    try:
        result = operation(*args)
    except Exception:
        record_ai_request(db, user_id, feature, "failed")
        raise
    record_ai_request(db, user_id, feature)
    expires = now + timedelta(seconds=settings.ai_cache_ttl_seconds)
    db.add(AIResponseCache(cache_key=cache_key, feature=feature, response=result, expires_at=expires))
    db.commit()
    return {**result, "cached": False}
