from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class DocumentStatus(Base):
    __tablename__ = "document_statuses"

    CREATED: str = 1
    WAIT: str = 2
    PROCESSED: str = 3
    FAILED: str = 4

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
