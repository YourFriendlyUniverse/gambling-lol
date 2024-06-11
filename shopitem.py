import pygame
import random


class ShopItem:
    def __init__(self, name, multiplier):
        self.name = name
        self.clicked = False
        self.image = pygame.image.load(f"ShopItems/{self.name}_ShopItem.png")
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(0, 0, self.image_size[0], self.image_size[1])
        self.rect.center = (100, 100)
        self.center = self.rect.center
        self.multiplier = multiplier
        self.price = 1 * multiplier

    def set_price(self, original_price):
        self.multiplier = int(self.multiplier)
        self.price = (original_price * self.multiplier) + round(random.randint(1, 10) * self.multiplier / random.randint(1, round((self.multiplier / 2) + 1)))