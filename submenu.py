import pygame


class SubMenu:
    def __init__(self, name, screen_size):
        self.is_open = False
        if name == "testing":
            self.slot_1 = (100, 100)
            self.spacing = (125, 75)    # how far the centers of the buttons should be spaced x and y
            self.rect = pygame.Rect(0, 0, 250, screen_size[1])
            self.image = pygame.Surface((500, screen_size[1]))
            pygame.Surface.fill(self.image, (255, 255, 255))

        elif name == "shop":
            self.slot_1 = (100, 100)
            self.spacing = (125, 150)   # how far the centers of the buttons should be spaced x and y
            # can buy stuff like multipliers/jackpot size increase etc
            # also stuff with dice total
            self.slot_close = (400, 25)
            self.rect = pygame.Rect(0, 0, 250, screen_size[1])
            self.image = pygame.Surface((500, screen_size[1]))
            pygame.Surface.fill(self.image, (255, 255, 255))

        elif name == "change_bet":
            self.bet = ""
            self.rect = pygame.Rect(0, 0, 250, 150)
            self.image = pygame.Surface((250, 150))
            pygame.Surface.fill(self.image, (255, 255, 255))
            self.rect.center = (screen_size[0] / 2, screen_size[1] / 2)




    def open(self):
        if self.is_open:
            self.is_open = False
        else:
            self.is_open = True
