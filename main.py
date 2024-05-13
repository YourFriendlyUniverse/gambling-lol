import pygame
import random
from menubutton import MenuButton
from dice import Dice


def screen_blit_die(die_list):
    for dice in die_list:
        screen.blit(dice.image, dice.rect)


def die_position_correct(die_list, screen_size):
    for i in range(len(die_list)):
        if i == 0:
            die_list[0].rect_center = (100, 100)
        elif die_list[i].position_correct(die_list[i - 1].rect.center[0], die_list[i - 1].rect.center[1], (100, 100), screen_size):
            for dice in die_list:
                dice.scale_down()
            return "rerun"


def add_dice_total(die_list):
    total = 0
    for dice in die_list:
        total += dice.face_up_symbol
    return total


pygame.init()
pygame.font.init()


settings = {
    "screen_size": (1600, 1000),
    "frames_per_second": 60,
    "font": "Comic Sans",
    "testing": True,
}

# initializing variables
display_font = pygame.font.SysFont(settings["font"], 20)
pygame.display.set_caption("Dice roller")
title_screen = True
size = settings["screen_size"]
screen_center = (size[0] / 2, size[1] / 2)
screen = pygame.display.set_mode(size)

# loop variables needed for it to run
run = True
clock = pygame.time.Clock()
frame = 0
new_die_added = False

# initializing menu buttons
dice_option = MenuButton("Dice", (screen_center[0], screen_center[1] - 100))
roll_button = MenuButton("Roll", (screen_center[0], screen_center[1] + (screen_center[1] / 2)))
if settings["testing"]:
    test_tools_button = MenuButton("TestTools", (100, size[1] - 100))
    add_dice_button = MenuButton("AddDice", (screen_center[0], screen_center[1] + (screen_center[1] / 2) + 100))
    add_dice_button.scale_down(1.5)

# dice game variables
all_dice = []
dice_total = 0
display_dice_total = display_font.render(f"{dice_total}", True, (255, 255, 255))
times_scaled = 0
displaying_testing_menu = False

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
                all_dice = [Dice(6, times_scaled)]    # starts game off with one D6
                # initializes button to roll dice
            if roll_button.rect.collidepoint(event.pos) and dice_option.clicked:
                for dice in all_dice:
                    dice.roll_dice()
                dice_total = add_dice_total(all_dice)
                display_dice_total = display_font.render(f"{dice_total}", True, (255, 255, 255))
            if add_dice_button.rect.collidepoint(event.pos) and dice_option.clicked and displaying_testing_menu:
                all_dice.append(Dice(6, times_scaled))
                new_die_added = True
            # elif slot_option.rect.collidepoint(event.pos):
            #     print("SLOTS")

    if new_die_added:
        if die_position_correct(all_dice, size) == "rerun":
            die_position_correct(all_dice, size)
            times_scaled += 1
            # preforms a rerun of correcting the positions of the die as they have then been scaled down
        new_die_added = False
    # do not blit above #
    screen.fill((0, 0, 0))
    # screen.blit(bg, (bg_x, 0))
    if dice_option.clicked:
        screen_blit_die(all_dice)
        screen.blit(roll_button.image, roll_button.rect)
        if settings["testing"]:
            screen.blit(test_tools_button.image, test_tools_button.rect)
            if displaying_testing_menu:
                screen.blit(add_dice_button.image, add_dice_button.rect)
                screen.blit(display_dice_total, (0, 0))
    else:
        screen.blit(dice_option.image, dice_option.rect)


    pygame.display.update()
    frame += 1

# Once we have exited the main program loop we can stop the game engine
pygame.quit()
