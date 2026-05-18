from .managers import InputManager
from .managers import ResourceManager
from .managers import SceneManager
from .managers import SoundManager
from .managers import GameManager

input_manager = InputManager()
resource_manager = ResourceManager()
scene_manager = SceneManager()
sound_manager = SoundManager(resource_manager)
