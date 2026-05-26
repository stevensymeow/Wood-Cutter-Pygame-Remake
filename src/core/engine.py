import pygame as pg

from src.utils import GameSettings, Logger
from .services import scene_manager, input_manager, resource_manager
#from src.data.info import Info
from src.data.info import GameInfo

from src.scenes.menu_scene import MenuScene
from src.scenes.game_scene import GameScene
#from src.scenes.setting_scene import SettingScene

class Engine:

    screen: pg.Surface              # Screen Display of the Game
    clock: pg.time.Clock            # Clock for FPS control
    running: bool                   # Running state of the game

    def __init__(self):
        Logger.info("Initializing Engine")

        pg.init()
        
        # By me: For resize (pg.RESIZABLE)
        #self.screen = pg.display.set_mode((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT), pg.RESIZABLE)
        self.screen = pg.display.set_mode((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        
        # By me: Window icon
        self.window_icon = resource_manager.get_image("window_icon/mochicat.png")
        pg.display.set_icon(self.window_icon)

        # By me: do some initializing of GameSettings here
        #GameSettings.json_path_init()
        GameSettings.save_config()
        #GameSettings.load_config()
        
        # Get version
        GameSettings.get_version()
        
        # By me: initialize GameInfo here
        #GameInfo.load_info()
        
        # Scene register
        scene_manager.register_scene("game", GameScene())
        scene_manager.register_scene("menu", MenuScene())
        
        scene_manager.change_scene("menu")
        
        # Set the caption
        curr_lv = scene_manager.game_manager.curr_lv
        pg.display.set_caption(f"{GameSettings.TITLE}: {curr_lv.level_label} {curr_lv.level_name}")
        
    def run(self):
        Logger.info("Running the Game Loop ...")
        
        try:
            while self.running:
                dt = self.clock.tick(GameSettings.FPS) / 1000.0
                self.handle_events()
                self.update(dt)
                self.render()
        except KeyboardInterrupt:
            Logger.warning("Don't kill me like that if not necessary!")
            self.end()

    def handle_events(self):
        input_manager.reset()
        # Events
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                #self.running = False
                self.end()
            input_manager.handle_events(event)
            
            # By me: screen resizing
            if event.type == pg.WINDOWMAXIMIZED:
                Logger.info("The window is maximized!")
                GameSettings.SCREEN_MAXIMIZED = True
            elif event.type == pg.WINDOWRESTORED:
                Logger.info("The window size is restored!")
                GameSettings.SCREEN_MAXIMIZED = False
            
            if event.type == pg.VIDEORESIZE:
                screen_width, screen_height = event.size
                GameSettings.set_screen_size(screen_width, screen_height)
                self.screen = pg.display.set_mode((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT), pg.RESIZABLE)
                Logger.info(f"New screen size: {screen_width}x{screen_height}")
            
            if input_manager.key_down(pg.K_r) and input_manager.key_pressed(pg.K_u) and not(GameSettings.SCREEN_MAXIMIZED):
                Logger.info("Change game screen size back to default")
                GameSettings.default_screen_size()
                self.screen = pg.display.set_mode((GameSettings.SCREEN_WIDTH, GameSettings.SCREEN_HEIGHT), pg.RESIZABLE)
        
        # Level set caption
        curr_lv = scene_manager.game_manager.curr_lv
        pg.display.set_caption(f"{GameSettings.TITLE}: {curr_lv.level_label} {curr_lv.level_name}")
        
        # Temp: switch level
        """
        if GameSettings.LEVEL_SWITCHED:
            self.end()
        """

    # By me: engine end
    def end(self):
        Logger.info("Bye")
             
           
        # Auto save
        if GameSettings.AUTO_SAVE:
            if scene_manager.is_game_scene:
                scene_manager.game_manager.set_record()
            scene_manager.game_manager.save()
            Logger.info("Auto save on, file loaded, auto saved")
        else:
            Logger.info("Auto save off, changes not saved")
                
        
        GameSettings.save_config()
        self.running = False
    
    # By me: online switched
    def online_switched(self):
        Logger.info("Switched online, close window")
        self.end()
    
    # By me: IP set
    def IP_set(self):
        Logger.info("Server new IP set, close window")
        self.end()
    
    def update(self, dt: float):
        scene_manager.update(dt)

    def render(self):
        self.screen.fill((0, 0, 0))     # Make sure the display is cleared
        scene_manager.draw(self.screen) # Draw the current scene
        pg.display.flip()               # Render the display
