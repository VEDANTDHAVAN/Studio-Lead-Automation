from enum import Enum

from pydantic import BaseModel

class LeadStatus(str, Enum):
    QUALIFIED = "qualified"
    NEEDS_REVIEW = "needs_review"
    DECLINED = "declined"

class LeadQualification(BaseModel):
    score: int
    status: LeadStatus
    reasons: list[str]