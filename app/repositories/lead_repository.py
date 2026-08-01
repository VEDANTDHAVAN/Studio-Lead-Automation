from app.database.models import Lead
from app.database.session import SessionLocal

from sqlalchemy import func

class LeadRepository:
    def save(self, lead, qualification):
        db = SessionLocal()

        existing = (
            db.query(Lead).filter(
                Lead.contact_email == lead.contact_email
            ).first()
        )

        if existing:
            existing.company = lead.company
            existing.status = qualification.status.value
            existing.score = qualification.score

        else:
            db.add(
                Lead(
                    company=lead.company, contact_name=lead.contact_name,
                    contact_email=lead.contact_email, project_type=lead.project_type,
                    budget=str(lead.budget) if lead.budget else None, 
                    deadline=lead.deadline, summary=lead.summary,
                    status=qualification.status.value, score=qualification.score,
                )
            )

        db.commit()

        db.close()

    def get_all(self):
        db = SessionLocal()
        leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
        db.close()

        return leads

    def get_by_id(self, lead_id: int):
        db = SessionLocal()
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        db.close()

        return lead

    def get_statistics(self):
        db = SessionLocal()
        total = db.query(Lead).count()

        qualified = (
            db.query(Lead).filter(Lead.status == "qualified").count()
        )

        review = (
            db.query(Lead).filter(Lead.status == "needs_review").count()
        )

        declined = (
            db.query(Lead).filter(Lead.status == "declined").count()
        )

        avg_budget = db.query(func.avg(Lead.score)).scalar()

        db.close()

        return {
            "total": total,
            "qualified": qualified,
            "needs_review": review,
            "declined": declined,
            "average_score": avg_budget,
        }

    def search_by_company(self, company: str):
        db = SessionLocal()

        results = (
            db.query(Lead).filter(Lead.company.ilike(f"%{company}%")).all()
        )

        db.close()

        return results