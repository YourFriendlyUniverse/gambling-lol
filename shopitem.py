import pygame


class ShopItem:
    def __init__(self, name):
        self.name = name
        self.clicked = False
        self.image = pygame.image.load(f"{self.name}ShopItem.png")
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
        self.rect.center = (self.x, self.y)
        self.center = self.rect.center
        self.is_bought = False

    def buy(self):
        self.is_bought = True

