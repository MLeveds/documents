import asyncio
from typing import List, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.seeders.generic_seeder import GenericSeeder
from src.database.seeders.document_types_seeder import DocumentTypeSeeder
from src.database.seeders.document_statuses_seeder import DocumentStatusSeeder
from src.database.session_manager import db_manager


class DatabaseSeeder:

    def __init__(self):
        self.session_factory: AsyncSession = db_manager.session_factory
        self.seeders: List[Any[GenericSeeder]] = [
            DocumentTypeSeeder,
            DocumentStatusSeeder,
        ]

    async def run(self):
        try:
            if self.seeders:
                for seeder in self.seeders:
                    await seeder().run(self.session_factory)
        except Exception as e:
            print(e)


async def run_seeders(*args, **kwargs):
    db_s = DatabaseSeeder()
    await db_s.run()


if __name__ == "__main__":
    asyncio.run(run_seeders())
