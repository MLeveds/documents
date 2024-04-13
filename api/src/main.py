from fastapi import FastAPI

from src.config.app.config import settings_app

from src.api.routers.documents import router as docs_router
from src.api.routers.files import router as files_router


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings_app.APP_NAME,
        debug=settings_app.DEBUG,
        version=settings_app.APP_VERSION
    )

    application.include_router(docs_router)
    application.include_router(files_router)

    return application


app = get_application()
