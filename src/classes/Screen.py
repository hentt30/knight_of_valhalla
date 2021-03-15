import pygame 

from pygame.locals import *
from settings import *


class Screen():

    def __init__(self, background = "img/Sample_fantasy.png"):
        self.background = pygame.image.load(background).convert()

    def run_screen(self, gm):

        #Display refresh
        pygame.display.flip()

