from fastapi import APIRouter, Request

from src.api.responses.api_response import ApiResponse
from src.utils.transformer import transform

router = APIRouter(prefix="/documents")


@router.get("/me")
async def get_my(request: Request):
    pass

