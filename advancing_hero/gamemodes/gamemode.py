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
        pass

    def loop(self, events):
        pass
