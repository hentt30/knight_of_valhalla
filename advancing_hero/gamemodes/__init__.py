"""
Init file for gamemodes module
"""
from .level import LevelGameMode
from .titlescreen import TitleScreen
from .endgame import EndGame

modes = {
    'title_screen': TitleScreen,
    'level_main': LevelGameMode,
    'end_game': EndGame
}