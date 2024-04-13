from fastapi import FastAPI

from src.config.app.config import settings_app

from src.api.routers.predictions import router as predictions_router


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings_app.APP_NAME,
        debug=settings_app.DEBUG,
        version=settings_app.APP_VERSION
    )

    application.include_router(predictions_router)

    return application


app = get_application()
