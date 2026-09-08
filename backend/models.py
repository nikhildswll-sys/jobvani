"""
JobVani - Pydantic Request & Response Schemas
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List

class JobBase(BaseModel):
    title: str
    organization: str
    org_logo: Optional[str] = None
    category: str
    job_type: str
    location: str = "All India"
    vacancies: str
    qualification: str
    age_limit: Optional[str] = None
    application_fee: Optional[str] = None
    posted_date: str
    last_date: str
    salary: Optional[str] = None
    selection_process: Optional[str] = None
    exam_pattern: Optional[str] = None
    syllabus_summary: Optional[str] = None
    how_to_apply: Optional[str] = None
    official_notification_url: Optional[str] = None
    official_apply_url: Optional[str] = None
    official_website_url: Optional[str] = None
    status_badge: Optional[str] = "New"
    is_trending: Optional[int] = 0
    trending_score: Optional[int] = 0

class JobCreate(JobBase):
    pass

class SubscriberCreate(BaseModel):
    email: str

class BookmarkToggle(BaseModel):
    job_id: int
    user_id: Optional[str] = "guest"

class SettingsUpdate(BaseModel):
    active_jobs_stat: Optional[str] = None
    exam_categories_stat: Optional[str] = None
    happy_users_stat: Optional[str] = None
    updated_info_stat: Optional[str] = None
    closing_soon_days: Optional[str] = None
