from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager  # import for fastapi lifespan

from typing import Any


class Server():
    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        """
        """
        # Start the database connection
        await self.on_startup_fnc(app)
        yield
        # Close the database connection
        await self.on_shutdown_fnc(app)

    def create_app(self,
        debug: bool = True,
        title: str = '',
        description: str = '',
        version: str = '',
        lifespan: dict[str, Any] | None = None,
    ) -> FastAPI:
        """
        """
        if lifespan:
            self.on_startup_fnc = lifespan['on_startup_fnc']
            self.on_shutdown_fnc = lifespan['on_shutdown_fnc']

        self.app = FastAPI(
            debug = debug,
            title = title,
            description = description,
            version = version,
            lifespan = lifespan and self._lifespan
        )
        return self.app

    def set_templates_path(self, templates_path: str = 'templates'):
        """
        """
        self.templates = Jinja2Templates(directory=templates_path)     # this is the directory where we will store our html files

    def mount_assets(self,
        assets_url: str = '/assets',
        assets_path: str = 'assets',
        assets_app_name: str = 'assets'
    ):
        """
        Includes frontend static files - css, js, img (if req)
        """
        self.app.mount(
            assets_url,
            StaticFiles(directory = assets_path),
            name = assets_app_name
        )   # this will serve the static files from the assets directory and we can access them using /assets in the url


    def add_router(self, router: APIRouter):
        """
        """
        self.app.include_router(router)


    def serve_template(self,
        request: Request,
        template_name: str,
        template_data: dict
    ):
        """
        Serve template on frontend (with required data)
        """
        return self.templates.TemplateResponse(request, template_name, template_data)



