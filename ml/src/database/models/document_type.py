from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class DocumentType(Base):
    __tablename__ = "document_types"

    DRIVERS_LICENSE_BACK: str = 0
    DRIVERS_LICENSE_FACE: str = 1
    PASSPORT_MAIN: str = 2
    PASSPORT_REGISTER: str = 3
    PTS_FACE: str = 4
    SERIAL: str = 5
    STS_BACK: str = 6
    STS_FACE: str = 7

    @staticmethod
    def to_str(key: int):
        descriptions = {
            DocumentType.DRIVERS_LICENSE_BACK: 'Водительское удостоверение',
            DocumentType.DRIVERS_LICENSE_FACE: 'Водительское удостоверение',
            DocumentType.PASSPORT_MAIN: 'Паспорт',
            DocumentType.PASSPORT_REGISTER: 'Паспорт',
            DocumentType.PTS_FACE: 'ПТС',
            DocumentType.SERIAL: 'Серия и номер',
            DocumentType.STS_BACK: 'СТС',
            DocumentType.STS_FACE: 'СТС'
        }
        return descriptions[key] if key in descriptions else None

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
