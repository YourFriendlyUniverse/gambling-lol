import pygame
import random
from menubutton import MenuButton
from dice import Dice
from submenu import SubMenu


# displays all the dice on the screen
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
    "max_die": 100
}

# initializing variables
display_font = pygame.font.SysFont(settings["font"], 20)
pygame.display.set_caption("Dice roller")
title_screen = True
size = settings["screen_size"]
screen_center = (size[0] / 2, size[1] / 2)
screen = pygame.display.set_mode(size)
current_bet = 1
change_bet = ""
money = 100
display_money = display_font.render(f"${money}", True, (255, 255, 255))
display_current_bet = display_font.render(f"Current Bet: ${current_bet}", True, (255, 255, 255))
display_change_bet = display_font.render(f"{change_bet}", True, (0, 0, 0))


# loop variables needed for it to run
run = True
clock = pygame.time.Clock()
frame = 0
new_die_added = False
dice_points = 0

# initializing menu buttons
dice_option = MenuButton("Dice", (screen_center[0], screen_center[1] - 100))
roll_button = MenuButton("Roll", (screen_center[0], screen_center[1] + (screen_center[1] / 2)))
shop_button = MenuButton("Shop", (100, size[1] - 250))
# change bet buttons
change_bet_button = MenuButton("ChangeBet", (size[0] - 200, size[1] - 100))
change_bet_submenu = SubMenu("change_bet", settings["screen_size"])
change_bet_back = MenuButton("ChangeBetBack", (screen_center[0] - 60, screen_center[1] + 50))
change_bet_confirm = MenuButton("ChangeBetConfirm", (screen_center[0] + 60, screen_center[1] + 50))
if settings["testing"]:
    testing_submenu = SubMenu("testing", settings["screen_size"])
    test_tools_button = MenuButton("TestTools", (100, size[1] - 100))
    add_dice_button = MenuButton("AddDice", testing_submenu.slot_1)
    add_dice_button.scale_down(2)



# dice game variables
all_dice = []
dice_total = 0
display_dice_total = display_font.render(f"{dice_total}", True, (100, 100, 100))
times_scaled = 0
displaying_testing_menu = False

while run:
    # --- Main event loop
    clock.tick(settings["frames_per_second"])  # sets fps

    # quitting game
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            run = False

        # when the change_bet submenu is open
        if change_bet_submenu.is_open:
            if event.type == pygame.TEXTINPUT:
                if event.text.isdigit():    # checks if the text inputted was a number
                    change_bet += event.text
                    display_change_bet = display_font.render(f"{change_bet}", True, (0, 0, 0))
                    # updates the screen to show number
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:        # checks for esc key
                    change_bet_submenu.open()   # closes menu
                elif event.key == pygame.K_BACKSPACE:     # checks for backspace
                    change_bet = change_bet[:-1]  # removes last character
                    display_change_bet = display_font.render(f"{change_bet}", True, (0, 0, 0))
                    # updates the screen to show number
                elif event.key == pygame.K_RETURN:
                    change_bet_submenu.open()
                    current_bet = int(change_bet)
                    display_current_bet = display_font.render(f"Current Bet: ${current_bet}", True, (255, 255, 255))
                    # updates the current bet

            # checks for mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if change_bet_confirm.rect.collidepoint(event.pos):
                    change_bet_submenu.open()
                    current_bet = int(change_bet)
                    display_current_bet = display_font.render(f"Current Bet: ${current_bet}", True, (255, 255, 255))
                    # updates the current bet
                elif change_bet_back.rect.collidepoint(event.pos):
                    change_bet_submenu.open()
                    # closes the menu without updating the bet


        # rolling dice using space
        elif event.type == pygame.TEXTINPUT:
            if event.text == " " and dice_option.clicked:  # checks if space is held down
                for dice in all_dice:
                    dice.roll_dice()
                    if dice.face_up_symbol == 6:
                        money += current_bet * 2
                        display_money = display_font.render(f"${money}", True, (255, 255, 255))
                dice_total = add_dice_total(all_dice)
                display_dice_total = display_font.render(f"{dice_total}", True, (100, 100, 100))

        # checks for mouse button clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if dice_option.clicked:
                # rolls dice
                if roll_button.rect.collidepoint(event.pos):
                    for dice in all_dice:
                        dice.roll_dice()
                        if dice.face_up_symbol == 6:
                            money += current_bet * 2
                            display_money = display_font.render(f"${money}", True, (255, 255, 255))
                    dice_total = add_dice_total(all_dice)
                    display_dice_total = display_font.render(f"{dice_total}", True, (100, 100, 100))

                # opens and closes the change_bet submenu
                if change_bet_button.rect.collidepoint(event.pos):
                    change_bet_submenu.open()
                    change_bet = ""
                    display_change_bet = display_font.render(f"{change_bet}", True, (0, 0, 0))

            # initializing dice game
            elif dice_option.rect.collidepoint(event.pos):  # checks for a click on the dice gamemode option
                dice_option.clicked = True
                all_dice = [Dice(6, times_scaled)]  # starts game off with one D6
                # initializes button to roll dice

            # testing settings
            if settings["testing"]:
                # opens/closes testing submenu when button is clicked
                if test_tools_button.rect.collidepoint(event.pos):
                    testing_submenu.open()

                # adds dice within the testing menu
                elif add_dice_button.rect.collidepoint(event.pos) and dice_option.clicked and testing_submenu.is_open:
                    if len(all_dice) < settings["max_die"]:     # caps die that can be in game
                        all_dice.append(Dice(6, times_scaled))
                        new_die_added = True

            # elif slot_option.rect.collidepoint(event.pos):
            #     print("SLOTS")

    # corrects die positions and scales die
    if new_die_added:
        if die_position_correct(all_dice, size) == "rerun":
            die_position_correct(all_dice, size)
            times_scaled += 1
            # preforms a rerun of correcting the positions of the die as they have then been scaled down
        new_die_added = False

    # do not blit above #
    screen.fill((0, 0, 0))
    # screen.blit(bg, (bg_x, 0))
    # shows on screen the dice game buttons when the dice option is clicked
    if dice_option.clicked:
        screen_blit_die(all_dice)
        screen.blit(roll_button.image, roll_button.rect)
        screen.blit(shop_button.image, shop_button.rect)
        screen.blit(change_bet_button.image, change_bet_button.rect)
        if change_bet_submenu.is_open:
            screen.blit(change_bet_submenu.image, change_bet_submenu.rect)
            screen.blit(change_bet_back.image, change_bet_back.rect)
            screen.blit(change_bet_confirm.image, change_bet_confirm.rect)
            screen.blit(display_change_bet, change_bet_submenu.rect)
            # change bet submenu to input text
        # testing stuff
        if settings["testing"]:
            if testing_submenu.is_open:
                screen.blit(testing_submenu.image, testing_submenu.rect)
                screen.blit(add_dice_button.image, add_dice_button.rect)
            screen.blit(test_tools_button.image, test_tools_button.rect)
            screen.blit(display_dice_total, (30, 30))
        screen.blit(display_current_bet, (screen_center[0], 0))
        screen.blit(display_money, (screen_center[0], 20))
    # shows the menu screen
    else:
        screen.blit(dice_option.image, dice_option.rect)



    pygame.display.update()
    frame += 1

# Once we have exited the main program loop we can stop the game engine
pygame.quit()
