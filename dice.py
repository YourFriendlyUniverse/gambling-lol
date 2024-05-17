import pygame
import random


class Dice:
    def __init__(self, sides, times_scaled):
        # basic functionality
        self.faces = []
        for i in range(sides):
            self.faces.append(i + 1)
        self.sides = sides
        self.side_up = random.randint(1, self.sides)
        self.face_up_symbol = self.faces[self.side_up - 1]  # gets the number that's face up
        self.image = pygame.image.load(f"{self.face_up_symbol}Dice.png")    # gets the image
        self.image_size = self.image.get_size()     # sets up image size for scaling later
        # scaling
        self.scale_factor = 2
        self.original_image = self.image    # sets the original image to be used for scaling
        self.times_scaled = times_scaled
        self.image = pygame.transform.scale(self.original_image, (self.image_size[0] / (self.scale_factor ** self.times_scaled), self.image_size[1] / (self.scale_factor ** self.times_scaled)))
        self.image_size = self.image.get_size()     # updates image size
        # rectangles for display
        self.rect = pygame.Rect(100, 100, self.image_size[0], self.image_size[1])   # sets location of dice
        self.rect.center = (100, 100)   # sets center of dice

    def roll_dice(self):
        self.side_up = random.randint(1, self.sides)
        self.face_up_symbol = self.faces[self.side_up - 1]
        self.image = pygame.image.load(f"{self.face_up_symbol}Dice.png")
        self.image = pygame.transform.scale(self.image, (self.image_size[0] / 1 + (self.scale_factor * self.times_scaled), self.image_size[1] / 1 + (self.scale_factor * self.times_scaled)))
        # updates image and rolls dice

    def position_correct(self, previous_x, previous_y, start, limit):
        # previous_x and previous_y are the x and y positions of the center of the previous dice
        if previous_x < limit[0] and previous_y < limit[1]:
            if not previous_x >= limit[0] - 100:
                # places dice to the right of the previous one
                self.rect.center = (previous_x + self.image_size[0], previous_y)
            elif previous_y <= limit[1]:
                # loops back around to beginning but one row down
                self.rect.center = (start[0], previous_y + self.image_size[1])
        else:
            return True
            # returns true to let program know to scale dice

    def scale_down(self):
        self.image = pygame.transform.scale(self.original_image, (self.image_size[0] / self.scale_factor, self.image_size[1] / self.scale_factor))
        self.rect = self.image.get_rect()
        self.image_size = self.image.get_size()

