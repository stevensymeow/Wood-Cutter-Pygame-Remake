from __future__ import annotations
import pygame as pg

from src.utils import GameSettings
from src.core.services import input_manager, sound_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
from .whshape import WHShape
from src.interface.components import Text, Overlay, Rectangle, Text
from src.core import GameManager, Game
from src.data.info import GameInfo

class FallingObject(WHShape):
    # Pos and size
    x_left: int
    x_right: int
    pos: int
    
    # Color
    color: tuple[int, int, int]
    hitbox_color: tuple[int, int, int]
    
    # Fall
    y_dropped: int
    
    # Is falling
    falling: bool
    
    # Game manager
    game_manager: GameManager
    
    # Lv2: Move
    do_move: bool = False
    moved: bool
    started_moving: bool
    
    # Lv3: Emerge
    do_emerge: bool = False
    emerged: bool
    started_emerging: bool
    y_dropped_emerged: int # y_dropped when fully emerged
    
    # Lv4
    been_hit: bool = False
    
    def __init__(self, game_manager: GameManager, 
                 width: int, height: int,
                 color: tuple[int, int, int], hitbox_color: tuple[int, int, int],
                 can_drag: bool = False, pos: int = -1):
        """
        Yes, this is the tree branch
        """
        # Game manager
        self.game_manager = game_manager
        
        # Pos and size
        pcx, pcy = GameSettings.SCREEN_WIDTH / 2, GameSettings.SCREEN_HEIGHT / 2
        
        self.width = width
        self.height = height
        
        self.x_left = pcx - GameInfo.bark_width/2 - GameInfo.branch_width/2
        self.x_right = pcx + GameInfo.bark_width/2 + GameInfo.branch_width/2
        self.pos = pos
        
        # pos init
        if self.pos == -1:
            self.x = self.x_left
        elif self.pos == 1:
            self.x = self.x_right
        else: # should not happen
            self.x = pcx
        
        # Color
        self.color = color
        self.hitbox_color = hitbox_color
        
        # Is Falling
        self.falling = True
        
        # Fall
        self.y_dropped = 0
        
        # Lv2: Move
        self.moved = False
        self.started_moving = False
        
        # Lv3: Emerge
        self.emerged = False
        self.started_emerging = False
        self.y_dropped_emerged = 0
        
        self.pos_init()
        
        super().__init__(color=color, 
                         x=self.x, y=self.y, 
                         width=self.width, height=self.height, 
                         can_drag=can_drag,
                         alpha=self.alpha)
    
    def pos_init(self):
        hy = GameSettings.SCREEN_HEIGHT
        # Gravity
        curr_lv = self.game_manager.curr_lv
        if curr_lv.gravity > 0:
            self.y = 0
        else:
            self.y = hy
        self.set_pos(self.x, self.y)
        self.y_dropped = 0
        # Lv3: Emerge
        emerge = self.do_emerge and self.game_manager.curr_lv.branch_emerge
        if emerge:
            self.set_alpha(0)
        else:
            self.set_alpha(255)
    
    @property
    def y_at_init(self) -> bool:
        hy = GameSettings.SCREEN_HEIGHT
        if self.game_manager.curr_lv.gravity > 0:
            return self.y == 0
        else:
            return self.y == hy
    
    @property
    def y_is_falling(self) -> bool:
        hy = GameSettings.SCREEN_HEIGHT
        if self.game_manager.curr_lv.gravity > 0:
            return self.y < hy
        else:
            return self.y > 0
    
    @property
    def y_hit_ground(self) -> bool:
        hy = GameSettings.SCREEN_HEIGHT
        if self.game_manager.curr_lv.gravity > 0:
            return self.y >= hy
        else:
            return self.y <= 0
    
    @property
    def fully_emergered(self) -> bool:
        return self.alpha == 255
    
    @property
    def y_dist_from_init(self) -> int:
        hy = GameSettings.SCREEN_HEIGHT
        gravity = self.game_manager.curr_lv.gravity
        if gravity > 0:
            return self.y
        else:
            return hy - self.y
    
    def check_hit(self) -> bool:
        if self.been_hit:
            return True
        if self.game_manager.wood_cutter.invincible and self.fully_emergered or input_manager.key_down(pg.K_t) or input_manager.mouse_down(3):
            if not self.been_hit:
                #Logger.info("Player used his invincibility!!!!!!")
                sound_manager.play_sound("Punch1.wav")
                self.been_hit = True
            return True
        return False
    
    def been_hit_fly_away(self):
        if self.game_manager.state == Game.Playing:
            if self.been_hit:
                wx = GameSettings.SCREEN_WIDTH
                if (self.pos == -1 and self.x > 0) or (self.pos == 1 and self.x < wx):
                    self.move_by(20*self.pos, 0)
                else:
                    self.falling = False
    
    @override
    def update(self, dt: float) -> None:
        match (self.game_manager.state):
            case Game.Entered:
                pass
            case Game.Playing:
                curr_lv = self.game_manager.curr_lv
                
                if self.y_at_init and (self.fully_emergered):
                    #sound_manager.play_sound("pop.wav")
                    pass
                if self.y_is_falling:
                    # Fall
                    drop = curr_lv.gravity*curr_lv.fall_speed
                    if not self.been_hit:
                        self.move_by(0, drop)
                        self.y_dropped += abs(drop)
                    # Hit the player
                    if self.hitbox.colliderect(self.game_manager.wood_cutter.hitbox):
                        if self.fully_emergered: # fully shown
                            if not self.check_hit():
                                self.when_hit_player()
                else:
                    if self.falling:
                        if self.y_hit_ground:
                            self.when_hit_ground()
                
                # -- Been hit --
                self.been_hit_fly_away()
                
                # --- Features ---
                if self.been_hit:
                    super().update(dt)
                    return
                
                screen_height = GameSettings.SCREEN_HEIGHT
                name = self.__class__.__name__
                # Lv2: Move to left or right
                if self.y_dropped >= screen_height/2:
                    d_drop = 0 # Lv3: Move after emerged
                    move = self.do_move and self.game_manager.curr_lv.branch_move \
                        and self.fully_emergered \
                        and (self.y_dropped >= self.y_dropped_emerged+d_drop)
                    if move and ((not self.moved) or (self.x != self.x_left and self.x != self.x_right)):
                        if (not self.started_moving) and self.fully_emergered:
                            self.started_moving = True
                            sound_manager.play_sound(self.game_manager.curr_lv.move_sound)
                            if self.pos == -1:
                                Logger.info(f"{name} moving right!")
                            elif self.pos == 1:
                                Logger.info(f"{name} moving left!")
                        branch_move_speed = self.game_manager.curr_lv.branch_move_speed
                        if self.pos == -1:
                            if self.x < self.x_right:
                                self.move_by(branch_move_speed, 0)
                            else:
                                self.x = self.x_right
                                self.pos = 1
                                self.moved = True
                                self.set_pos(self.x, self.y)
                                Logger.info(f"{name} finished moving!")
                        elif self.pos == 1:
                            if self.x > self.x_left:
                                self.move_by(-branch_move_speed, 0)
                            else:
                                self.x = self.x_left
                                self.pos = -1
                                self.moved = True
                                self.set_pos(self.x, self.y)
                                Logger.info(f"{name} finished moving!")
                
                # Lv3: Emerge
                if self.y_dropped >= screen_height/3:
                    emerge = self.do_emerge and self.game_manager.curr_lv.branch_emerge
                    if emerge and ((not self.emerged) or 0 < self.alpha < 255):
                        if not self.started_emerging:
                            self.started_emerging = True
                            sound_manager.play_sound(self.game_manager.curr_lv.emerge_sound)
                            Logger.info(f"{name} is emerging!")
                        if self.alpha < 255:
                            self.change_alpha(self.game_manager.curr_lv.branch_emerge_speed)
                            if self.alpha >= 255:
                                self.emerged = True
                                Logger.info(f"{name} finished emerging!")
                                self.y_dropped_emerged = self.y_dropped
                        else:
                            self.emerged = True
                            Logger.info(f"{name} finished emerging!")

        super().update(dt)
    
    def when_hit_ground(self):
        """When tounch the ground"""
        pass
    
    def when_hit_player(self):
        """When hit(touch) the player(wood cutter)"""
        pass
     
    @override
    def draw(self, screen: pg.Surface, show: bool = True) -> None:
        if self.falling and show:
            super().draw(screen)
        
        if GameSettings.DRAW_HITBOXES and self.fully_emergered:
            pg.draw.rect(screen, self.hitbox_color, self.hitbox, 2)
