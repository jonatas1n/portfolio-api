from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date
from database.base import Base


class Experiences(Base):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), unique=True)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=True)
    company_name: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(String(2048), nullable=True)
    technologies: Mapped[list[str]] = mapped_column(String(32), nullable=True)
