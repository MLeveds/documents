from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.api.responses.api_response import ApiResponse
from src.config.app.config import settings_app

router = APIRouter(prefix="/files")


@router.get('/{path}')
async def get_file(path: str):
    try:
        image_path = settings_app.APP_PATH + '/storage/' + path
        return FileResponse(image_path)
    except Exception as e:
        return ApiResponse.error(str(e))
