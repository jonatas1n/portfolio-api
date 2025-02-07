from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database.base import Base


class Projects(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), unique=True)
    technologies: Mapped[list[str]] = mapped_column(String(32), nullable=True)
    description: Mapped[str] = mapped_column(String(2048), nullable=True)
    images: Mapped[list[str]] = mapped_column(String(2048), nullable=True)
