from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class DocumentType(Base):
    __tablename__ = "document_types"

    DRIVERS_LICENSE: str = 1
    VEHICLE_REGISTRATION: str = 2
    PTS: str = 3
    PASSPORT_RU: str = 4

    @staticmethod
    def to_str(key: int):
        descriptions = {
            DocumentType.DRIVERS_LICENSE: 'driver_license',
            DocumentType.VEHICLE_REGISTRATION: 'vehicle_certificate',
            DocumentType.PTS: 'vehicle_passport',
            DocumentType.PASSPORT_RU: 'personal_passport',
        }
        return descriptions[key] if key in descriptions else None

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
