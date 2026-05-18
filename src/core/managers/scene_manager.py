import pygame as pg

from src.scenes.scene import Scene
from src.utils import Logger

from src.core.managers import GameManager

from enum import Enum

from src.scenes.overlay_scene import OverlayScene

"""
Process:
overlay show
scene exit
switch scene
overlay hide
scene enter
"""

class State(Enum):
    Init = -1           #
    OverlayShowing = 0  # overlay show
    SceneExiting = 1    # scene exit, scene switch
    OverlayHiding = 2   # overlay hide
    SceneEntering = 3   # scene enter
    SceneRunning = 4    #

class SceneManager:
    
    _scenes: dict[str, Scene]
    _current_scene: Scene | None = None
    _current_scene_name: str | None = None
    _next_scene_name: str | None = None
    
    # Overlay effect
    overlay: OverlayScene
    overlay_showing: bool
    overlay_hiding: bool
    
    # State
    state: State
    changing_scene: bool
    
    def __init__(self):
        Logger.info("Initializing SceneManager")
        self._scenes = {}
        self._current_scene = None
        self._current_scene_name
        self._next_scene_name = None
        
        # Scene args kwargs
        self._args = []
        self._kwargs = {}
        
        # Overlay effect
        self.overlay = OverlayScene((0, 0, 0), 255)
        self.overlay_showing = False
        self.overlay_hiding = False
        
        # State
        self.state = State.Init
        self.changing_scene = False
    
    @property
    def scenes(self) -> dict[str, Scene]:
        return self._scenes
    
    @property
    def game_scene(self) -> Scene | None:
        return self._scenes.get("game")
    
    @property
    def current_scene(self) -> Scene | None:
        return self._current_scene
    
    @property
    def game_manager(self) -> GameManager | None:
        if self.game_scene is not None:
            return self.game_scene.game_manager
        return None
     
    def register_scene(self, name: str, scene: Scene) -> None:
        self._scenes[name] = scene
        
    def change_scene(self, scene_name: str, *args, **kwargs) -> None:
        # Scene args kwargs
        if args: self._args = args
        if kwargs: self._kwargs = kwargs
        
        if scene_name in self._scenes:
            Logger.info(f"Changing scene to '{scene_name}'")
            self._next_scene_name = scene_name
            
            # Overlay effect, scene state
            if not self._current_scene:
                self.state = State.SceneEntering
            else:
                self.state = State.OverlayShowing
            self.changing_scene = True
            self.overlay.set_alpha(0)
        else:
            raise ValueError(f"Scene '{scene_name}' not found")
            
    def update(self, dt: float) -> None:
        # Handle scene transition
        if self._next_scene_name is not None:
            self._perform_scene_switch()
            
        # Update current scene
        if self._current_scene:
            self._current_scene.update(dt)
            
    def draw(self, screen: pg.Surface) -> None:
        if self._current_scene:
            self._current_scene.draw(screen)
        
        # Overlay effect
        if self.changing_scene:
            self.overlay.draw(screen)
            
    def _perform_scene_switch(self) -> None:
        if self._next_scene_name is None:
            return
            
        # Overlay effect
        dalpha = 15
        if self.state == State.OverlayShowing:
            if self.overlay.alpha < 255:
                self.overlay.change_alpha(dalpha)
            else:
                self.state = State.SceneExiting
        elif self.state == State.OverlayHiding:
            if self.overlay.alpha > 0:
                self.overlay.change_alpha(-dalpha)
            else:
                self.state = State.SceneEntering
        
        # Exit current scene
        if self.state == State.SceneExiting:
            if self._current_scene:
                Logger.info(f"Exiting scene '{self._current_scene_name}'")
                self._current_scene.exit()
        
        # Switch scene
        if self.state == State.SceneExiting or (self.state == State.SceneEntering and self._current_scene is None):
            self._current_scene = self._scenes[self._next_scene_name]
            self.state = State.OverlayHiding
        
        # Enter new scene
        if self.state == State.SceneEntering:
            if self._current_scene:
                Logger.info(f"Entering {self._next_scene_name} scene")
                # Scene kwargs
                if self._args:
                    if self._kwargs:
                        self._current_scene.enter(*self._args, **self._kwargs)
                    else:
                        self._current_scene.enter(*self._args)
                elif self._kwargs:
                    self._current_scene.enter(**self._kwargs)
                else:
                    self._current_scene.enter()
                # Clear args and kwargs
                self._args = []
                self._kwargs = {}
                
            # Clear the transition request
            self._current_scene_name = self._next_scene_name
            self._next_scene_name = None
            self.changing_scene = False
        