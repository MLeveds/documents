from src.database.models.document_type import DocumentType
from src.database.seeders.generic_seeder import GenericSeeder


class PermissionsSeeder(GenericSeeder):
    def __init__(self):
        super().__init__()
        self.initial_data = {
            DocumentType: {
                DocumentType.DRIVERS_LICENSE: {"name": "Водительское удостоверение"},
                DocumentType.VEHICLE_REGISTRATION: {"name": "Свидетельство о регистрации транспортного средства"},
                DocumentType.PTS: {"name": "ПТС"},
                DocumentType.PASSPORT_RU: {"name": "Паспорт РФ"},
            }
        }
