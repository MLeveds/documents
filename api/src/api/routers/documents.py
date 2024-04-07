from typing import List

from fastapi import APIRouter, Request, UploadFile, File
from src.api.responses.api_response import ApiResponse
from src.api.transformers.document_transformer import DocumentTransformer

from src.database.models.document import Document
from src.database.session_manager import db_manager
from src.utils.transformer import transform
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

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
async def store(request: Request, image: UploadFile = File(...)):
    import json
    return {
        'type': str(type(request.values())),
        'len': len(request.values()),
        'vals': json.dumps(dict(request.values())),
    }
    return request.values()
    return {'filename': image.filename, 'data': request.values()}
    async with aiohttp.ClientSession() as session:
        async with session.post('http://docs_ml:8000/predict') as response:
        # async with session.post('https://ml.rwfsh39.ru/predict') as response:
            res = await response.json()

    return res


@router.post('/callback')
async def callback():
    pass
