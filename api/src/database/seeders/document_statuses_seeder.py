from src.database.models.document_status import DocumentStatus
from src.database.seeders.generic_seeder import GenericSeeder


class DocumentStatusSeeder(GenericSeeder):
    def __init__(self):
        super().__init__()
        self.initial_data = {
            DocumentStatus: {
                DocumentStatus.CREATED: {"name": "Создан"},
                DocumentStatus.WAIT: {"name": "Обрабатывается"},
                DocumentStatus.PROCESSED: {"name": "Обработан"},
                DocumentStatus.FAILED: {"name": "Ошибка"},
            }
        }
