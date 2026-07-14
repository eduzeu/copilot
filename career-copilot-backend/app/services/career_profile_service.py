from sqlalchemy.orm import Session

from app.models.career_profile import CareerProfile
from app.schemas.career_profile import CareerProfileUpdate


def calculate_completeness(profile: CareerProfile) -> int:
    checks = [
        bool(profile.status),
        bool(profile.school or profile.current_role),
        bool(profile.major or profile.current_industry),
        bool(profile.experiences),
        bool(profile.technical_skills),
        profile.dsa_level != "not_started",
        profile.system_design_level != "not_started",
        bool(profile.target_roles),
        bool(profile.target_companies or profile.target_industries),
        bool(profile.primary_goal),
    ]
    return round(sum(checks) / len(checks) * 100)


def get_or_create_profile(db: Session, user_id: int) -> CareerProfile:
    profile = db.query(CareerProfile).filter(CareerProfile.user_id == user_id).first()
    if not profile:
        profile = CareerProfile(user_id=user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


def update_profile(db: Session, user_id: int, req: CareerProfileUpdate) -> CareerProfile:
    profile = get_or_create_profile(db, user_id)
    for field, value in req.model_dump().items():
        if field == "experiences":
            value = [entry.model_dump() for entry in req.experiences]
        setattr(profile, field, value)
    db.commit()
    db.refresh(profile)
    return profile


def profile_response(profile: CareerProfile) -> dict:
    return {
        column.name: getattr(profile, column.name)
        for column in CareerProfile.__table__.columns
    } | {"completeness": calculate_completeness(profile)}
