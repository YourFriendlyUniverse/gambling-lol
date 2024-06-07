import pygame


class MenuButton:
    def __init__(self, name, pos):
        self.name = name
        self.x = pos[0]
        self.y = pos[1]
        self.clicked = False
        self.original_image = pygame.image.load(f"MenuButtons/{self.name}MenuButton.png")
        self.image = self.original_image
        self.original_image_size = self.original_image.get_size()
        self.image_size = self.original_image_size
        self.rect = pygame.Rect(self.x, self.y, self.image_size[0], self.image_size[1])
        self.rect.center = (self.x, self.y)
        self.center = self.rect.center

    def scale_down(self, factor):
        self.center = self.rect.center
        length = self.original_image_size[0]
        height = self.original_image_size[1]
        self.image = pygame.transform.scale(self.original_image, (length / factor, height / factor))
        # scales the image
        self.image_size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = self.center  # keeps the center of the button the same

    def click(self):
        if self.clicked:
            self.clicked = False
        else:
            self.clicked = True