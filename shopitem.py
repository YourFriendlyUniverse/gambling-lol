import pygame


class ShopItem:
    def __init__(self, name):
        self.name = name
        self.clicked = False
        self.image = pygame.image.load(f"ShopItems/{self.name}_ShopItem.png")
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(0, 0, self.image_size[0], self.image_size[1])
        self.rect.center = (100, 100)
        self.center = self.rect.center
        self.is_bought = False

    def buy(self):
        self.is_bought = True

    def change_pos(self, x, y):
        self.rect.center = (x, y)
