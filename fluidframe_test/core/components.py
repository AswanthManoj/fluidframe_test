import os
from typing import List, Optional
from abc import ABC, abstractmethod
from starlette.routing import Route
from fluidframe_test.core.dependency import requires
from fluidframe_test.utilities.helper import UniqueIDGenerator
from typing import Optional, Any, Callable, Dict, Tuple, Union
from fluidframe_test.config import TITLE, SCRIPTS, STYLES, HOT_RELOAD_SCRIPT
from fluidframe_test.core import html, body, meta, script, link, div, head, title

class State:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_state(self, key, value):
        setattr(self, key, value)
        
    def get_state(self, key, default=None):
        return getattr(self, key, default)

    def remove_state(self, key):
        if hasattr(self, key):
            delattr(self, key)
  
  
  
class Root:
    def __init__(self, title: Optional[str]=None, reload: bool=True) -> None:
        self.path = "root"
        self.reload = reload
        self.title = title or TITLE
        self.routes: Dict[str, Route] = {}
        self.children: List[Component] = []
        self.id_generator = UniqueIDGenerator()
        
    def get_id(self, path: List[str]):
        return self.id_generator.generate_unique_id(path)
    
    def get_route_id(self, path: List[str]):
        return "/".join(path)
    
    def add_child(self, child):
        self.children.append(child)
    
    def add_children(self, children):
        self.children.extend(children)
        
    def register_route(self, route: str, handler: Callable):
        self.routes[route] = handler
        
    def get_routes(self) -> Dict[str, Route]:
        return self.routes
    
    def render(self) -> str:
        return ''.join(["<!DOCTYPE html>",
            html(lang="eng",
                i=[
                    head(
                        title(self.title),
                        meta(charset="UTF-8"),
                        [script(src=s) for s in SCRIPTS],
                        requires(HOT_RELOAD_SCRIPT) if self.reload else "",
                        [link(href=stl, rel="stylesheet") for stl in STYLES],
                    ),
                    body(
                        div(id="root",
                            i=[child.render() for child in self.children]
                        ),
                        cls="relative dark:bg-gray-800 bg-white text-sm text-gray-900 dark: text-white"
                    )
                ]
            )
        ])



class Component(ABC):
    def __init__(self, key: Optional[str] = None, **kwargs) -> None:
        self.path = []
        self.key = key
        self.root = None
        self.styles = []
        self.scripts = []
        self.id_generator = UniqueIDGenerator()
        self.type = self.__class__.__name__.lower()
        self.id = key if key is not None else 'undefined'
        self.parent: Optional[Union['Component', Root]] = None
        
        self.path.append(self.type)
        self.id = self.get_pseudo_id(self.path) if self.key is None else key
        
        for k, v in kwargs.items():
            if hasattr(self, k):
                raise (f"Attribute conflict! attribute `{k}` already exists as part of the component `{self.type}` with id `{self.id}`")
            setattr(self, k, v)
        
    def get_pseudo_id(self, path: List[str]):
        return self.id_generator.generate_unique_id(path)
        
    def get_id(self, path: List[str]) -> str:
        return self.parent.get_id(path)
    
    def add_child(self, component: 'Component') -> 'Component':
        component.path
        
    def set_parent(self, parent: Union['Component', Root]):
        self.parent = parent
        self.path.append(self.type)
    
    @abstractmethod
    def render(self, **kwargs) -> str:
        pass
    
    
    
class StatelessComponent(Component):
    """For simple display components that don't need to manage state.

    - text
    - markdown
    - latex
    - title
    - header
    - subheader
    - caption
    - code
    - image
    - audio
    - video
    - diagram
    """
    def __init__(self, parent: Union[Component, Root], key: Optional[str] = None, **kwargs) -> None:
        super().__init__(parent, key, **kwargs)



class StatefulComponent(Component):
    """For components that need to manage and update their own state and respond to user interactions.

    - text_input
    - text_area
    - number_input
    - slider
    - select_box
    - multiselect
    - checkbox
    - radio
    - date_input
    - time_input
    - file_uploader
    - color_picker
    - button
    - download_button
    - form
    - progress
    - spinner
    - status
    """
    def __init__(self, parent: Union[Component, Root], key: Optional[str] = None, on_change: Optional[Callable] = None, **kwargs) -> None:
        super().__init__(parent, key, **kwargs)
        self.state = State()
        self.on_change = on_change
       
    def get_route_id(self, path: List[str]) -> str:
        return self.root_component.get_route_id(path)
        
    def set_state(self, new_state: Dict[str, Any]):
        for key, value in new_state.items():
            self.state.set_state(key, value)
        if self.on_change:
            self.on_change(self)

    def get_state(self, key: str, default: Any = None) -> Any:
        return self.state.get_state(key, default)

    @abstractmethod
    def handle_update(self, new_data: Any) -> None:
        pass
    


class LayoutComponent(StatelessComponent):
    """For components that can contain other components.

    - sidebar
    - columns
    - expander
    - container
    - empty
    """
    def __init__(self, parent: Union[Component, Root], key: Optional[str] = None, children: List[Component] = None, **kwargs) -> None:
        super().__init__(parent, key, **kwargs)
        self.children = children or []
        
    def __enter__(self):
        # Any setup code if needed
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        # Any teardown code if needed
        pass

    def add_child(self, child: Component):
        self.children.append(child)
        
    def get_childrens(self):
        return self.children
    
    # StatelessComponent
    def text(self, body: str, help: Optional[str]=None) -> Component:
        pass
    
    # LayoutComponent
    def container(self) -> Component:
        pass
    
    # StatefulComponent
    def button(self, label: str, key: Optional[str]=None, help: Optional[str]=None, on_click: Optional[Callable]=None, args: Optional[Tuple[Any]]=None, kwargs: Optional[Dict[str, Any]]=None, type: str="secondary", disabled: bool=False, use_container_width: bool=False) -> Component:
        pass

    def checkbox(self, label: str, value: bool=False, key: Optional[str]=None, help: Optional[str]=None, on_click: Optional[Callable]=None, args: Optional[Tuple[Any]]=None, kwargs: Optional[Dict[str, Any]]=None, type: str="secondary", disabled: bool=False, label_visibility: str="visible") -> Component:
        pass
 


