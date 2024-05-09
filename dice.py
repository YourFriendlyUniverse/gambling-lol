import pygame
import random


class Dice:
    def __init__(self, sides):
        self.faces = []
        for i in range(sides):
            self.faces.append(i + 1)
        self.sides = sides
        self.side_up = random.randint(1, self.sides)
        self.face_up_number = self.faces[self.side_up - 1]  # gets the number that's face up
        self.image = pygame.image.load(f"{self.face_up_number}Dice.png")    # gets the image
        self.image_size = self.image.get_size()
        self.rect = pygame.Rect(100, 100, self.image_size[0], self.image_size[1])   # sets location of dice
        self.rect.center = (100, 100)   # sets center of dice

    def roll_dice(self):
        self.side_up = random.randint(1, self.sides)
        self.face_up_number = self.faces[self.side_up - 1]
        self.image = pygame.image.load(f"{self.face_up_number}Dice.png")
        # updates image and rolls dice

    def position_correct(self, previous_x, previous_y, start, limit):
        # previous_x and previous_y are the x and y positions of the center of the previous dice
        if not previous_x >= limit[0] - 100:
            self.rect.center = (previous_x + self.image_size[0], previous_y)
        elif previous_y <= limit[1]:
            # loops back around to beginning but one row down
            self.rect.center = (start[0], previous_y + self.image_size[1])
