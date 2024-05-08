import pygame
import random
from menubutton import MenuButton
from dice import Dice


def screen_blit_die(die_list):
    for dice in die_list:
        screen.blit(dice.image, dice.rect)


pygame.init()
pygame.font.init()


settings = {
    "screen_size": (800, 600),
    "frames_per_second": 60,
    "font": "Comic Sans",
}

# initializing variables
my_font = pygame.font.SysFont(settings["font"], 20)
pygame.display.set_caption("Dice roller")
title_screen = True
size = settings["screen_size"]
screen_center = (size[0] / 2, size[1] / 2)
screen = pygame.display.set_mode(size)

# loop variables needed for it to run
run = True
clock = pygame.time.Clock()
frame = 0

# initializing menu buttons
dice_option = MenuButton("Dice", (screen_center[0], screen_center[1] - 100))
roll_button = MenuButton("Roll", (screen_center[0], screen_center[1] + (screen_center[1] / 2)))

# dice game variables
all_dice = []

while run:
    # --- Main event loop
    clock.tick(settings["frames_per_second"])  # sets fps

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("space")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if dice_option.rect.collidepoint(event.pos) and not dice_option.clicked:    # checks for a click on the dice gamemode option
                dice_option.clicked = True
                all_dice = [Dice(6)]    # starts game off with one D6
                # initializes button to roll dice
            if roll_button.rect.collidepoint(event.pos) and dice_option.clicked:
                for dice in all_dice:
                    dice.roll_dice()
            # elif slot_option.rect.collidepoint(event.pos):
            #     print("SLOTS")

    # do not blit above #
    screen.fill((0, 0, 0))
    # screen.blit(bg, (bg_x, 0))
    if dice_option.clicked:
        screen_blit_die(all_dice)
        screen.blit(roll_button.image, roll_button.rect)
    else:
        screen.blit(dice_option.image, dice_option.rect)


    pygame.display.update()
    frame += 1

# Once we have exited the main program loop we can stop the game engine
pygame.quit()
