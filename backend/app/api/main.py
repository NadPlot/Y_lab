from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core import config, tasks

from app.api.routes import menu


def get_application():
    app = FastAPI(
        title=config.PROJECT_NAME,
        version=config.VERSION,
        description=config.DESCRIPTION,
        openapi_tags=config.TAGS_METADATA,
        docs_url='/api/openapi',
        redoc_url='/api/redoc',
        # В формате OpenAPI
        openapi_url='/api/v1/openapi.json',
        debug='true',)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(menu.router)

    return app


app = get_application()
