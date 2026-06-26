from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class PredictionAudit(Base):
    __tablename__ = "prediction_audit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    age: Mapped[int] = mapped_column(Integer, nullable=False)
    annual_income: Mapped[float] = mapped_column(Float, nullable=False)
    employment_years: Mapped[int] = mapped_column(Integer, nullable=False)
    loan_amount: Mapped[float] = mapped_column(Float, nullable=False)
    loan_term_months: Mapped[int] = mapped_column(Integer, nullable=False)
    credit_score: Mapped[int] = mapped_column(Integer, nullable=False)
    existing_debt: Mapped[float] = mapped_column(Float, nullable=False)
    debt_to_income: Mapped[float] = mapped_column(Float, nullable=False)

    default_probability: Mapped[float] = mapped_column(Float, nullable=False)
    default_label: Mapped[int] = mapped_column(Integer, nullable=False)
    threshold: Mapped[float] = mapped_column(Float, nullable=False)


def create_session_factory(database_url: str) -> sessionmaker[Session]:
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


def save_prediction_audit(
    session: Session,
    application_data: dict[str, float | int],
    default_probability: float,
    default_label: int,
    threshold: float,
) -> PredictionAudit:
    audit = PredictionAudit(
        **application_data,
        default_probability=default_probability,
        default_label=default_label,
        threshold=threshold,
    )

    session.add(audit)
    session.commit()
    session.refresh(audit)

    return audit