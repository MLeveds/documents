from json import JSONDecodeError

from fastapi import APIRouter, Request, UploadFile, File as FastapiFile
from src.api.responses.api_response import ApiResponse

from src.database.session_manager import db_manager
from sqlalchemy.future import select

from src.database.models.file import File
from src.database.models.document_type import DocumentType
from src.config.app.config import settings_app
from src.utils.storage import storage

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
    res = get_prediction(image_path)

    """Отредактированную фотку (с выделенными полями) нужно будет сохранить с этим именем"""
    image_edited_path = settings_app.APP_PATH + '/storage/' + file.path + '_edited' + file.extension

    return ApiResponse.payload({
        'file_type_id': res['file_type_id'],
        'confidence': res['confidence'],
        'data': res['data'],
        'page': res['page'],
    })


@router.post('/detect')
async def detect(
        request: Request,
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
        path = storage.save_temp(image)
    else:
        try:
            path = storage.save_temp_from_base64(json_data['image'])
        except Exception as e:
            return ApiResponse.error(str(e), 400)

    """Путь к картинке - path"""
    """Всякое с предсказаниями..."""
    res = get_prediction(path)

    return ApiResponse.payload({
        'type': DocumentType.to_str(res['file_type_id']),
        'confidence': res['confidence'],
        'series': res['data']['series'],
        'number': res['data']['number'],
        'page': res['page'],
    })


def get_prediction(image_path: str):
    data = {
        'file_type_id': DocumentType.PASSPORT_RU,  # enum с id типа файла
        'confidence': 0.99,
        'data': {
            # поля прочитанные с картинки, произвольные названия, надо будет посмотреть, какие поля вы достаете, я потом у себя их обозначу, чтобы правильно выводиить
            'series': '0808',
            'number': '123321',
        },
        'page': 1,  # Страница документа nullable
    }
    return data
