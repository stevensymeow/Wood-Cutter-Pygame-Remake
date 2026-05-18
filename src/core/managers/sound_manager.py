import pygame as pg
from src.utils import load_sound, GameSettings

# Before initialization, force Pygame to use the dummy audio driver or switch the driver order
# This is the most common trick to solve "WASAPI can't find requested audio endpoint"
from src.utils import Logger
import os
os.environ['SDL_AUDIODRIVER'] = 'dsound'  # Use the DirectSound driver instead of WASAPI

# Resource for sound
from src.core.managers import ResourceManager

class SoundManager:
    resource_manager: ResourceManager
    
    def __init__(self, resource_manager: ResourceManager):
        # Resource manager
        self.resource_manager = resource_manager
        
        try:
            # Increasing the buffer size helps reduce latency errors in WASAPI/DirectSound
            pg.mixer.pre_init(buffer=1024)
            pg.mixer.init()
            Logger.info("SoundManager successfully init with dsound")
        except pg.error as pg_err:
            # If dsound also fails, try disabling audio completely to allow the program to run (even without sound)
            os.environ['SDL_AUDIODRIVER'] = 'dummy'
            pg.mixer.init()
            Logger.warning(pg_err)
            Logger.info("Mute all instead")
        
        pg.mixer.set_num_channels(GameSettings.MAX_CHANNELS)
        self.current_bgm = None
        
    def play_bgm(self, filepath: str):
        if self.current_bgm:
            self.current_bgm.stop()
        audio = load_sound(filepath)
        if not GameSettings.AUDIO_MUTE: # Imply MUTE
            audio.set_volume(GameSettings.AUDIO_VOLUME)
        else:
            audio.set_volume(0)
        audio.play(-1)
        self.current_bgm = audio
    
    def toggle_mute(self): # Imply MUTE
        GameSettings.toggle_mute()
        if not GameSettings.AUDIO_MUTE: # Imply MUTE
            self.current_bgm.set_volume(GameSettings.AUDIO_VOLUME)
        else:
            self.current_bgm.set_volume(0)
    
    def set_volume(self, volume: float): # Imply VOLUME
        GameSettings.set_volume(volume)
        if not GameSettings.AUDIO_MUTE:
            self.current_bgm.set_volume(GameSettings.AUDIO_VOLUME)
        else:
            self.current_bgm.set_volume(0)
    
    def pause_all(self):
        pg.mixer.pause()

    def resume_all(self):
        pg.mixer.unpause()
        
    def play_sound(self, filepath, volume=0.7):
        #sound = load_sound(filepath)
        sound = self.resource_manager.get_sound(filepath)
        sound.set_volume(volume)
        sound.play()

    def stop_all_sounds(self):
        pg.mixer.stop()
        self.current_bgm = None
    
    def stop_bgm(self):
        if self.current_bgm:
            self.current_bgm.stop()