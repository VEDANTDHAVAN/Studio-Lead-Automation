from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Lead(Base):

    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    company: Mapped[str | None] = mapped_column(String)

    contact_name: Mapped[str | None] = mapped_column(String)

    contact_email: Mapped[str | None] = mapped_column(
        String,
        unique=True,
    )

    project_type: Mapped[str | None] = mapped_column(String)

    budget: Mapped[str | None] = mapped_column(String)

    deadline: Mapped[str | None] = mapped_column(String)

    status: Mapped[str] = mapped_column(String)

    score: Mapped[int] = mapped_column(Integer)

    summary: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )