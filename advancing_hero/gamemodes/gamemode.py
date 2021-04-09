"""
Base class to implement gamemodes
"""
import pygame
import os


class GameMode:
    """
    General class that represents a gamemode. All the classes
    have to inherit from this class
    """

    def __init__(self, screen) -> None:
        self.screen = screen
        self.font_path = os.path.abspath('advancing_hero/fonts/zerovelo.ttf')
        pass

    def loop(self, events):
        pass
