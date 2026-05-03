from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from typing import Any


class Server():
    def create_app(self,
        debug: bool = True,
        title: str = '',
        description: str = '',
        version: str = ''
    ):
        """
        """
        self.app = FastAPI(
            debug = debug,
            title = title,
            description = description,
            version = version,
        )
        return self.app

    def set_templates_path(self, templates_path: str = 'templates'):
        """
        """
        self.templates = Jinja2Templates(directory=templates_path)     # this is the directory where we will store our html files

        # return self.templates

    def mount_assets(self,
        assets_url: str = '/assets',
        assets_path: str = 'assets',
        assets_app_name: str = 'assets'
    ):
        """
        """
        # includes frontend static files - css, js, img (if req)
        self.app.mount(assets_url, StaticFiles(directory=assets_path), name=assets_app_name)   # this will serve the static files from the assets directory and we can access them using /assets in the url


    def add_router(self, router: APIRouter):
        """
        """
        self.app.include_router(router)

    def serve_template(self,     # serve template on frontend (with required data)
        request: Request,
        template_name: str,
        template_data: dict
    ):
        """
        """
        return self.templates.TemplateResponse(request, template_name, template_data)



