from fastapi import APIRouter, Request
from src.api.responses.api_response import ApiResponse
import asyncio

router = APIRouter()


@router.post("/predict")
async def predict(request: Request):
    await asyncio.sleep(5)
    return ApiResponse.payload({'message': 'hellow'})
