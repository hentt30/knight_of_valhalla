"""
Init file for gamemodes module
"""
from .level import LevelGameMode
from .titlescreen import TitleScreen
from .endgame import EndGame
from .wingame import WinGame

modes = {
    'title_screen': TitleScreen,
    'level_main': LevelGameMode,
    'end_game': EndGame,
    'win_game': WinGame
}