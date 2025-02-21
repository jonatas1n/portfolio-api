from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from database.base import Base


class Skills(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), unique=True)
    skill_type: Mapped[str] = mapped_column(
        String(64), nullable=False, default="Programming Languages"
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
