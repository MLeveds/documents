from fastapi import APIRouter, Request
from src.api.responses.api_response import ApiResponse

router = APIRouter()


@router.post("/predict")
async def predict(request: Request):
    return ApiResponse.payload({'message': 'hellow'})
