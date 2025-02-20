from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, JSON, Text
from database.base import Base


class Experiences(Base):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(primary_key=True)
    position: Mapped[str] = mapped_column(String(30), unique=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=True)
    company_name: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    technologies: Mapped[list[str]] = mapped_column(JSON, nullable=True)
