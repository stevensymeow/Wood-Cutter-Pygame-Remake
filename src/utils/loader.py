import pygame as pg
from pathlib import Path
from .logger import Logger

# For exe convert
import json # By me
import sys
import os

# --- ADD THIS HELPER FUNCTION ---
def get_resource_path(relative_path: str) -> Path:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except Exception:
        # If not running as EXE, use the current directory
        base_path = Path(os.path.abspath("."))

    return base_path / relative_path

def get_persistent_path(relative_path: str) -> Path:
    """ Get path to the actual folder where the EXE is (Read-Write) """
    if getattr(sys, 'frozen', False):
        # Path to the folder containing the .exe
        base_path = Path(sys.executable).parent
    else:
        # Path to the folder containing the script
        base_path = Path(os.path.abspath("."))
    return base_path / relative_path

# --- MODIFY ASSETS_DIR ---
# Instead of Path("assets"), use the helper
ASSETS_DIR = get_resource_path("assets")
SAVES_DIR = get_persistent_path("saves")

# [MAKEDIR] Try make saves dir if not exist
if not os.path.exists(SAVES_DIR):
    Logger.info("The directory 'saves' does not exist")
    SAVES_DIR.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(SAVES_DIR):
        Logger.error("The directory 'saves' does not exist")
    else:
        Logger.info("Successfully maked the directory")

CONFIG_DIR = get_persistent_path("")
#ASSETS_DIR = Path("assets")

# By me, loading for exe
def load_data(path: str) -> dict:
    Logger.info(f"Loading data: {path}")
    direct_path = ASSETS_DIR / path
    with open(direct_path, "r") as f:
        data = json.load(f)
    if not data:
        Logger.error(f"Failed to load data: {path}")
    return data

def load_img(path: str) -> pg.Surface:
    Logger.info(f"Loading image: {path}")
    direct_path = str(ASSETS_DIR / "images" / path)
    if not os.path.exists(direct_path):
        Logger.error(f"Image path not exist: {path}")
    img = pg.image.load(direct_path)
    if not img:
        Logger.error(f"Failed to load image: {path}")
    return img.convert_alpha()

def load_sound(path: str) -> pg.mixer.Sound:
    Logger.info(f"Loading sound: {path}")
    direct_path = str(ASSETS_DIR / "sounds" / path)
    if not os.path.exists(direct_path):
        Logger.error(f"Sound path not exist: {path}")
    sound = pg.mixer.Sound(direct_path)
    if not sound:
        Logger.error(f"Failed to load sound: {path}")
    return sound

def load_font(path: str, size: int) -> pg.font.Font:
    Logger.info(f"Loading font: {path}")
    direct_path = str(ASSETS_DIR / "fonts" / path)
    if not os.path.exists(direct_path):
        Logger.error(f"Font path not exist: {path}")
    font = pg.font.Font(direct_path, size)
    if not font:
        Logger.error(f"Failed to load font: {path}")
    return font
