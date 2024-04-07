from fastapi import APIRouter, Request
from src.api.responses.api_response import ApiResponse

from src.database.session_manager import db_manager
from sqlalchemy.future import select

from src.database.models.file import File
from src.database.models.document_type import DocumentType
from src.config.app.config import settings_app

router = APIRouter()


@router.post("/predict")
async def predict(request: Request):
    data = await request.json()
    if 'image_id' not in data:
        return ApiResponse.error('image_id must be present.')

    async with db_manager.get_session() as session:
        q = select(File).where(File.id == data['image_id'])
        res = await session.execute(q)
        file: File = res.scalar()

    if not file:
        return ApiResponse.error('Image does not exist', 404)

    """Путь к картинке"""
    image_path = settings_app.APP_PATH + '/storage/' + file.path + file.extension

    """Всякое с предсказаниями..."""

    """Отредактированную фотку (с выделенными полями) нужно будет сохранить с этим именем"""
    image_edited_path = settings_app.APP_PATH + '/storage/' + file.path + '_edited' + file.extension

    """"""
    response_data = {
        'file_type_id': DocumentType.PASSPORT_RU,  # enum с id типа файла
        'data': {  # поля прочитанные с картинки, произвольные названия, надо будет посмотреть, какие поля вы достаете, я потом у себя их обозначу, чтобы правильно выводиить
            'series': '0808',
            'number': '123321',
        },
        'page': 1,  # Страница документа
    }

    return ApiResponse.payload(response_data)
