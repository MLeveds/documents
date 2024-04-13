from typing import Optional
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.models.base import Base
from src.database.models.document_status import DocumentStatus


# TODO: ADD TO ADMIN
class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("document_types.id"), nullable=True)
    file_id: Mapped[Optional[int]] = mapped_column(ForeignKey("files.id"), nullable=False)
    status_id: Mapped[Optional[int]] = mapped_column(ForeignKey("document_statuses.id"), nullable=False, default=DocumentStatus.CREATED)
    page: Mapped[Optional[int]] = mapped_column(nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(nullable=True)
    data: Mapped[str] = mapped_column(nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now())

    file: Mapped["File"] = relationship(uselist=False, lazy="selectin")
    type: Mapped["DocumentType"] = relationship(uselist=False, lazy="selectin")
    status: Mapped["DocumentStatus"] = relationship(uselist=False, lazy="selectin")

    @property
    def link(self):
        return self.file.link

    @property
    def edited_link(self):
        return self.file.edited_link
