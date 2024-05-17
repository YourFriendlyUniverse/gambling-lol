import pygame


class SubMenu:
    def __init__(self, name, screen_size):
        self.is_open = False
        if name == "testing":
            self.spacing = (125, 75)    # how far the centers of the buttons should be spaced x and y
            self.buttons = {
                "1": "AddDice",
                "2": "AddCurrency",
            }
            # the buttons and their positions
        elif name == "shop":
            self.spacing = (100, 100)   # how far the centers of the buttons should be spaced x and y
            self.buttons = {
                "1": "shop_l1"
            }
            # the buttons and their positions
        self.rect = pygame.Rect(0, 0, 250, screen_size[1])
        self.image = pygame.Surface((500, screen_size[1]))
        pygame.Surface.fill(self.image, (255, 255, 255))


    def open(self):
        if self.is_open:
            self.is_open = False
        else:
            self.is_open = True
