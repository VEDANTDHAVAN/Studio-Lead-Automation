from fastapi import APIRouter, HTTPException

from app.repositories.lead_repository import LeadRepository

router = APIRouter(prefix="/leads", tags=["Leads"])
repo = LeadRepository()

@router.get("/")
def list_leads():
    return repo.get_all()

@router.get("/{lead_id}")
def get_lead(lead_id: int):
    lead = repo.get_by_id(lead_id)

    if not lead:
        raise HTTPException(
            status_code=404, detail="Lead not found",
        )

    return lead

@router.get("/analytics/summary")
def analytics():
    return repo.get_statistics()

@router.get("/search/{company}")
def search(company: str):
    return repo.search_by_company(company)