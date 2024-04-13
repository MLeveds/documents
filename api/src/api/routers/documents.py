from json import JSONDecodeError
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
from sqlalchemy import update, desc
from sqlalchemy.orm import joinedload

from src.utils.storage import storage

import json
import aiohttp
import datetime

router = APIRouter(prefix="/documents")


@router.get("")
async def index():
    async with db_manager.get_session() as session:
        q = select(Document) \
            .options(joinedload(Document.type)) \
            .options(joinedload(Document.status)) \
            .options(joinedload(Document.file)) \
            .order_by(desc(Document.created_at))
        res = await session.execute(q)
        documents: List[Document] = res.unique().scalars().all()

    return ApiResponse.payload(transform(
        documents,
        DocumentTransformer()
    ))


@router.post("")
async def store(
        request: Request,
        queue: BackgroundTasks,
        image: UploadFile = FastapiFile(None)
):
    json_data = {}
    if not image:
        try:
            json_data = await request.json()
        except JSONDecodeError:
            pass

        if 'image' not in json_data and not image:
            return ApiResponse.error('Image must be present in form data or in json payload encoded with base64.', 400)

    if image:
        filename, extension = storage.save(image)
    else:
        try:
            filename, extension = storage.save_from_base64(image)
        except Exception as e:
            return ApiResponse.error('Image must be a valid base64 string.', 400)
    return filename + extension
    async with db_manager.get_session() as session:
        file = File(path=filename, extension=extension)

        session.add(file)
        await session.commit()
        await session.refresh(file)
        document = Document(
            type_id=None,
            file_id=file.id,
            status_id=DocumentStatus.CREATED,
            page=None,
            data=None,
            created_at=datetime.datetime.now()
        )

        session.add(document)
        await session.commit()
        await session.refresh(document)

        await session.commit()

    async def send_to_ml(document: Document):
        async with aiohttp.ClientSession() as client:
            try:
                async with client.post('http://docs_ml:8000/predict', json={
                    'image_id': document.file_id,
                }) as response:
                    data = await response.json()

                    async with db_manager.get_session() as session:
                        q = update(Document)\
                            .filter(Document.id == document.id)\
                            .values(
                            status_id=DocumentStatus.PROCESSED,
                            data=json.dumps(data['data']) if 'data' in data else None,
                            type_id=data['file_type_id'] if 'file_type_id' in data else None,
                            page=data['page'] if 'page' in data else None,
                        )
                        await session.execute(q)
                        await session.commit()
            except:
                async with db_manager.get_session() as session:
                    q = update(Document)\
                        .filter(Document.id == document.id)\
                        .values(status_id=DocumentStatus.FAILED)
                    await session.execute(q)
                    await session.commit()



    queue.add_task(send_to_ml, document)

    async with db_manager.get_session() as session:
        q = update(Document).filter(Document.id == document.id).values(status_id=DocumentStatus.WAIT)
        await session.execute(q)
        await session.commit()

    return ApiResponse.success('Document is sent to processing.')
