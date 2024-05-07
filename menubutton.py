import pygame


class MenuButton:
    def __init__(self, name, pos):
        self.name = name
        self.x = pos[0]
        self.y = pos[1]
        self.clicked = False
        self.image = pygame.image.load(f"{self.name}MenuButton.png")
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
        self.rect.center = (self.x, self.y)
