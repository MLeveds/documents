from typing import List

from fastapi import APIRouter, Request, UploadFile, File as FastapiFile, BackgroundTasks
from src.api.responses.api_response import ApiResponse
from src.api.transformers.document_transformer import DocumentTransformer

from src.database.models.document import Document
from src.database.models.document_status import DocumentStatus
from src.database.models.file import File
from src.database.session_manager import db_manager
from src.utils.transformer import transform
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload

from src.utils.storage import storage

import aiohttp

router = APIRouter(prefix="/documents")


@router.get("")
async def index():
    async with db_manager.get_session() as session:
        q = select(Document) \
            .options(joinedload(Document.type)) \
            .options(joinedload(Document.file))
        res = await session.execute(q)
        documents: List[Document] = res.unique().scalars().all()

    return ApiResponse.payload(transform(
        documents,
        DocumentTransformer()
    ))


@router.post("")
async def store(request: Request, queue: BackgroundTasks, image: UploadFile = FastapiFile(...)):
    data = await request.form()

    if 'image' not in data:
        return ApiResponse.errors({
            'image': ['image is required'],
        })

    filename, extension = storage.save(image)

    async with db_manager.get_session() as session:
        file = File(path=filename, extension=extension)
        session.begin()

        session.add(file)
        await session.refresh(file)
        document = Document(
            type_id=None,
            file_id=file.id,
            status_id=DocumentStatus.CREATED,
            page=None,
            data=None,
        )

        session.add(document)
        await session.refresh(document)

        await session.commit()

    async def send_to_ml(document: Document):
        async with aiohttp.ClientSession() as client:
            try:
                async with client.post('http://docs_ml:8000/predict') as response:
                    res = await response.json()
                    status_id = DocumentStatus.PROCESSED
            except aiohttp.ClientConnectorError:
                status_id = DocumentStatus.FAILED

            async with db_manager.get_session() as session:
                q = update(Document).filter(Document.id == document.id).update({'status_id': status_id})
                await session.execute(q)

    queue.add_task(send_to_ml, document)

    async with db_manager.get_session() as session:
        q = update(Document).filter(Document.id == document.id).update({'status_id': DocumentStatus.WAIT})
        await session.execute(q)

    return ApiResponse.success('Document is sent to processing.')
