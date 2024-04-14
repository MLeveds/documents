from src.database.models.document_type import DocumentType
from src.database.seeders.generic_seeder import GenericSeeder


class DocumentTypeSeeder(GenericSeeder):
    def __init__(self):
        super().__init__()
        self.initial_data = {
            DocumentType: {
                DocumentType.DRIVERS_LICENSE_BACK: {"name": "Водительское удостоверение"},
                DocumentType.DRIVERS_LICENSE_FACE: {"name": "Водительское удостоверение"},
                DocumentType.PASSPORT_MAIN: {"name": "Паспорт"},
                DocumentType.PASSPORT_REGISTER: {"name": "Паспорт"},
                DocumentType.PTS_FACE: {"name": "ПТС"},
                DocumentType.SERIAL: {"name": "Серия и номер"},
                DocumentType.STS_BACK: {"name": "СТС"},
                DocumentType.STS_FACE: {"name": "СТС"},
            }
        }
