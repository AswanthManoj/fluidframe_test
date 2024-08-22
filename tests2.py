from uuid import uuid4
import uvicorn, inspect
from abc import ABC, abstractmethod
from starlette.requests import Request
from fluidframe_test import get_lib_path
from starlette.responses import Response
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from fluidframe_test.core.dependency import requires
from starlette.middleware.sessions import SessionMiddleware
from fluidframe_test.utilities.helper import UniqueIDGenerator
from starlette.websockets import WebSocketDisconnect, WebSocket
from fluidframe_test.config import PUBLIC_DIR, HOT_RELOAD_SCRIPT
from typing import Awaitable, Optional, Any, Callable, Dict, List, Union
from fluidframe_test.core import html, body, meta, script, link, div, head, title, div, h1, button, p



class FluidFrame(Starlette):
    def __init__(self, reload: bool=True) -> None:
        super().__init__()
        self.id = "root"
        self.reload = reload
        self.children: List[Component] = []
        self.add_fluidroute("/", self.render)
        self.add_websocket_route("/ws", self.hot_reload_socket)
        self.add_middleware(SessionMiddleware, secret_key='your-secret-key')
        self.mount(f'/{PUBLIC_DIR}', StaticFiles(directory=str(get_lib_path() / "public")))
    
    def child(self, component: 'Component') -> 'Component':
        if isinstance(component, Component):
            component.root = self
            component.__parent__=self
        self.children.append(component)
        return component
    
    def __wrap_render__(self, func: Callable) -> Callable:
        async def wrapped_func(request: Request) -> HTMLResponse:
            result = await func() if inspect.iscoroutinefunction(func) else func()
            return HTMLResponse(result) if isinstance(result, str) else result
        return wrapped_func
    
    def add_fluidroute(self, path: str, endpoint: Callable, **kwargs) -> None:
        wrapped_endpoint = self.__wrap_render__(endpoint)
        self.add_route(path, wrapped_endpoint, **kwargs)
        
    async def hot_reload_socket(self, ws: WebSocket):
        await ws.accept()
        try:
            while True:
                data = await ws.receive_text()
                if data == "ping":
                    await ws.send_text("pong")
        except WebSocketDisconnect:
            print('Client connection closed')
    
    def add_event_route(self, path: str, handler: Callable):
        self.add_fluidroute(path, handler)
    
    def render(self) -> str:
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
                        div(
                            id=self.id,
                            i=[child.render() if isinstance(child, Component) else child for child in self.children]
                        ),
                        cls="relative dark:bg-gray-800 bg-white text-sm text-gray-900 dark: text-white"
                    )
                ]
            )
        ])
    


class Component(ABC):
    def __init__(self) -> None:
        self.root = None
        self.styles = []
        self.scripts = []
        self.children = []
        self.htmx_attributes: Dict[str, str] = {}
        self.type = self.__class__.__name__.lower()
        self.__parent__: Optional['Component'] = None
        self.id = self.get_id()
    
    def get_id(self) -> str:
        id_ = str(uuid4())
        return f"{self.type}-{id_[-8:]}"
    
    def child(self, component: 'Component') -> 'Component':
        if isinstance(component, Component):
            component.__parent__=self
            component.root = self.root
        self.children.append(component)
        return component
    
    @abstractmethod
    def render(self) -> str:
        pass
    
    def on_change(self, trigger: str, target: 'Component'|List['Component'], action: str, cache: bool = False) -> Callable:
        def decorator(func: Callable):
            route_path = f"/{self.id}/{trigger}"
            # Add HTMX attributes to the component
            self.htmx_attributes.update({
                "hx-swap": action,
                "hx-get": route_path,
                "hx-trigger": f"{trigger} once" if cache else trigger,
                "hx-target": f"#{target.id}" if isinstance(target, Component) else f"{', '.join([f'#{t.id}' for t in target])}",
            })

            # Wrap the original render method to include HTMX attributes
            original_render = self.render
            def wrapped_render(*args, **kwargs) -> str:
                rendered_content = original_render(*args, **kwargs)
                htmx_div = div(i=[rendered_content], **self.htmx_attributes)
                return htmx_div
            self.render = wrapped_render

            # Register the route
            self.root.add_event_route(route_path, func)
            return func
        return decorator


# def get_client_state(request: Request) -> Dict[str, int]:
#     client_id = request.cookies.get('client_id')
#     if not client_id:
#         client_id = str(uuid4())
#         response = Response()  # Creating an empty response to set cookies
#         response.set_cookie('client_id', client_id)
#         return {'client_id': client_id, 'response': response}
    
#     # Retrieve client state based on client_id (implement your state store here)
#     client_state = STATE_STORE.get(client_id, {'n': 0})
#     return {'client_id': client_id, 'state': client_state}

# def save_client_state(client_id: str, state: Dict[str, int]) -> None:
#     # Save state based on client_id (implement your state store here)
#     STATE_STORE[client_id] = state

# STATE_STORE = {}

class Header(Component):
    def __init__(self, title:str) -> None:
        super().__init__()
        self.title = title
        
    def render(self) -> str:
        return div(h1(self.title), id=self.id, cls="text-2xl font-bold m-5")
    
    
class Text(Component):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
    
    def render(self) -> str:
        return p(self.text, id=self.id, cls="m-5 border border-gray-300 p-5 rounded-lg")   
       
        
class Button(Component):
    def __init__(self, label: str) -> None:
        super().__init__()
        self.label = label

    def render(self) -> str:
        return button(self.label, cls="bg-blue-500 m-5 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded", id=self.id)



app = FluidFrame(reload=True)


###########################
# Increment and Decrement #
#############################################################
increment_btn: Button = app.child(Button("Increment"))      #
header = app.child(Header("Here we show a dynamic number")) #
decrement_btn: Button = app.child(Button("Decrement"))      #
                                                            #
n=0                                                         #
                                                            #################################################
@increment_btn.on_change(trigger="click", target=header, action="innerHTML transition:true", cache=False)   #
def increment() -> str:                                                                                     #
    global n                                                                                                #
    n+=1                                                                                                    #
    return f"You have clicked the button to increment {n}"                                                  #
                                                                                                            #
@decrement_btn.on_change(trigger="click", target=header, action="innerHTML transition:true", cache=False)   #
def decrement() -> str:                                                                                     #
    global n                                                                                                #
    n-=1                                                                                                    #            
    return f"You have clicked the button to decrement {n}"                                                  #
#############################################################################################################


###################
# Loading content #
#############################################
btn = app.child(Button("Load More"))        #
t1 = app.child(Text("Loaded Section "))     #
t2 = app.child(Text("Loded Section"))       #
                                            #
                                            ########################################################
@btn.on_change(trigger="click", target=[t1, t2], action="outerHTML transition:true", cache=False)  #
def load_more() -> str:                                                                            #
    return t1.render() + t2.render()                                                               #
                                                                                                   #
####################################################################################################

if __name__ == '__main__':
    uvicorn.run("tests2:app", host='127.0.0.1', port=8000, reload=True)