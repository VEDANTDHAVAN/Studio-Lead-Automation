from app.database.models import Lead
from app.database.session import SessionLocal

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