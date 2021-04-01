"""
Init file for gamemodes module
"""
from .level import LevelGameMode
from .titlescreen import TitleScreen

modes = {
    'title_screen': TitleScreen,
    'level_main': LevelGameMode,
}