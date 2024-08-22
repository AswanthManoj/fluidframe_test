from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from typing import Union, List, Callable, Optional
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocketDisconnect
from fluidframe_test.core.dependency import requires
from fluidframe_test.utilities.helper import UniqueIDGenerator
from fluidframe_test.config import PUBLIC_DIR, HOT_RELOAD_SCRIPT
from fluidframe_test.core import html, body, meta, script, link, div, head, title
from fluidframe_test.core.components import Component, StatefulComponent, StatelessComponent, Root



class FluidFrame(Starlette):
    def __init__(self, reload: bool=True, **kwargs):
        super().__init__(**kwargs)
        self.path = "root"
        self.reload = reload
        self.add_route("/", self.render)
        self.childrens: List[Component] = []
        self.id_generator = UniqueIDGenerator()
        
    def __render__(self) -> str:
        return ''.join(["<!DOCTYPE html>",
            html(lang="eng",
                i=[
                    head(
                        title("Fluidframe App"),
                        meta(charset="UTF-8"),
                        script(src=f"{PUBLIC_DIR}/scripts/dependency_manager.js"),
                        script(src="https://cdnjs.cloudflare.com/ajax/libs/htmx/2.0.2/htmx.min.js"),
                        link(href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css", rel="stylesheet"),
                        requires(HOT_RELOAD_SCRIPT) if self.reload else "",
                    ),
                    body(
                        div(id=self.path,
                            i=[child.render() for child in self.childrens]
                        ),
                        cls="relative dark:bg-gray-800 bg-white text-sm text-gray-900 dark: text-white"
                    )
                ]
            )
        ])
        
    def render(self) -> HTMLResponse:
        return HTMLResponse(self.__render__())


