from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class DocumentType(Base):
    __tablename__ = "document_types"

    DRIVERS_LICENSE: str = 1
    VEHICLE_REGISTRATION: str = 2
    PTS: str = 3
    PASSPORT_RU: str = 4

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
