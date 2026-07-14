from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Level = Literal["not_started", "beginner", "intermediate", "advanced"]
CareerStatus = Literal["college", "recent_graduate", "professional"]


class ExperienceEntry(BaseModel):
    category: Literal[
        "internship", "professional", "project", "hackathon",
        "research_open_source_volunteering", "club_organization"
    ]
    title: str
    organization: str = ""
    start_date: str = ""
    end_date: str = ""
    description: str = ""
    skills: list[str] = Field(default_factory=list)
    url: str = ""


class CareerProfileUpdate(BaseModel):
    status: CareerStatus = "college"
    school: str | None = None
    degree: str | None = None
    major: str | None = None
    current_year: str | None = None
    graduation_year: int | None = Field(default=None, ge=1900, le=2200)
    current_role: str | None = None
    years_experience: int | None = Field(default=None, ge=0, le=80)
    current_industry: str | None = None
    experiences: list[ExperienceEntry] = Field(default_factory=list)
    technical_skills: list[str] = Field(default_factory=list)
    dsa_level: Level = "not_started"
    system_design_level: Level = "not_started"
    behavioral_confidence: Level = "not_started"
    preferred_language: str | None = None
    improvement_areas: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    target_roles: list[str] = Field(default_factory=list)
    target_companies: list[str] = Field(default_factory=list)
    target_industries: list[str] = Field(default_factory=list)
    target_locations: list[str] = Field(default_factory=list)
    position_types: list[str] = Field(default_factory=list)
    workplace_preferences: list[str] = Field(default_factory=list)
    application_timeline: str | None = None
    primary_goal: str | None = None
    salary_expectations: str | None = None


class CareerProfileOut(CareerProfileUpdate):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    completeness: int = 0

    model_config = {"from_attributes": True}
