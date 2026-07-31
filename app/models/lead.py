from typing import List, Optional

from pydantic import BaseModel


class Budget(BaseModel):
    min: Optional[int] = None
    max: Optional[int] = None
    currency: Optional[str] = None


class LeadExtraction(BaseModel):
    is_lead: bool = True
    reason: str | None = None
    company: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None

    project_type: Optional[str] = None
    deliverables: List[str] = []

    budget: Optional[Budget] = Budget()

    deadline: Optional[str] = None
    urgency: Optional[str] = None

    missing_fields: List[str] = []

    summary: Optional[str] = None