from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database.base import Base


class Skills(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str] = mapped_column(String(2048), nullable=True)
