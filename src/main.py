import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routers.main_router import router
from resources.config import settings
from resources.logs.config import logging_config


logging.config.dictConfig(logging_config)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Zimran Quiz",
        version="1.0.0",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app


app = create_app()
