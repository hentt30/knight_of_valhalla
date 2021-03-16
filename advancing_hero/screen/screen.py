import pygame
from advancing_hero import settings


class Screen():
    def __init__(
        self,
        background_path: str = "advancing-hero/images/Sample_fantasy.png"
    ) -> None:
        self.background = pygame.image.load(background_path).convert()

    def render(self) -> None:

        #Display refresh
        pygame.display.flip()
