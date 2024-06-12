import pygame
import random
from menubutton import MenuButton
from dice import Dice
from submenu import SubMenu
from shopitem import ShopItem


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


def get_shop_item_multipliers():
    shop_item_multiplier = {}
    shop_item_names = open("shopitemnames", "r")
    for line in shop_item_names:
        line = line[:-1]    # removes the "\n"
        is_value = False
        item_name = ""
        multiplier_value = ""
        for character in line:
            if character != ":" and not is_value:
                item_name += character
            elif is_value:
                multiplier_value += character
            else:
                is_value = True
        shop_item_multiplier.update({f"{item_name}": multiplier_value})
    return shop_item_multiplier


def get_shop_items():
    shop_item_names = open("shopitemnames", "r")
    item_name_list = []
    for line in shop_item_names:
        line = line[:-1]  # removes the "\n"
        is_value = False
        item_name = ""
        for character in line:
            if character != ":" and not is_value:
                item_name += character
            else:
                is_value = True
        # FIX THIS
        item_name_list.append(item_name)
    return item_name_list


def screen_blit_shop_items(items):
    for item in items:
        screen.blit(item.image, item.rect)


def pick_random_shop_item(items, item_multiplier):
    shop_item_index = random.randint(0, len(items) - 1)
    item_name = items[shop_item_index]
    return ShopItem(item_name, item_multiplier[item_name])


def realign_shop(current_items, shop_submenu):
    x = 100
    y = 100
    for item in current_items:
        item.rect.center = (x, y)
        x += shop_submenu.spacing[0]
        if x >= shop_submenu.slot_close[0]:
            y += shop_submenu.spacing[0]
            x = 100


def adjust_prices(current_items, scaler):
    for item in current_items:
        item.set_price(scaler)
    return current_items


def blit_prices(prices_list, current_items):
    for i in range(len(prices_list)):
        x = current_items[i].rect.center[0]
        y = current_items[i].rect.center[1]
        screen.blit(prices_list[i], (x - 50, y + 40))


def update_prices(shop_items):
    display_shop_prices = []
    for item in shop_items:
        display_shop_prices.append(display_font.render(f"${item.price}", True, (0, 0, 0)))
    return display_shop_prices


def add_money(dice_list, j_mult, e_mult, o_mult):
    dice_values = []
    final_add = 0
    for dice in dice_list:
        final_mult = 1
        if dice.face_up_symbol % 2 == 0:
            final_mult = final_mult * e_mult
        else:
            final_mult = final_mult * o_mult
        if dice.face_up_symbol == 6:
            final_mult = final_mult * j_mult
        dice_values.append(dice.face_up_symbol * final_mult)
    for value in dice_values:
        final_add += value
    return final_add


def take_money(bet, money_taken_mult):
    return -(round(bet * money_taken_mult))


def gamble(money, dice_list, bet, j_mult, e_mult, o_mult, money_taken_mult):
    for dice in dice_list:
        dice.roll_dice()
    money += add_money(dice_list, j_mult, e_mult, o_mult) + take_money(bet, money_taken_mult)
    return money


pygame.init()
pygame.font.init()


settings = {
    "screen_size": (1600, 1000),
    "frames_per_second": 60,
    "font": "Comic Sans",
    "testing": False,
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
display_money = display_font.render(f"${money}", True, (150, 150, 150))
display_current_bet = display_font.render(f"Current Bet: ${current_bet}", True, (150, 150, 150))
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

# change bet buttons
change_bet_button = MenuButton("ChangeBet", (size[0] - 200, size[1] - 100))
change_bet_submenu = SubMenu("change_bet", settings["screen_size"])
change_bet_back = MenuButton("ChangeBetBack", (screen_center[0] - 60, screen_center[1] + 50))
change_bet_confirm = MenuButton("ChangeBetConfirm", (screen_center[0] + 60, screen_center[1] + 50))

# shop buttons + submenu + variables
shop_button = MenuButton("Shop", (100, size[1] - 250))
shop_submenu = SubMenu("shop", settings["screen_size"])
shop_close_button = MenuButton("Close", shop_submenu.slot_close)
shop_bought = []
shop_item_multipliers = get_shop_item_multipliers()
shop_items = get_shop_items()
current_shop_items = []
price_scaler = 1
for i in range(15):
    current_shop_items.append(pick_random_shop_item(shop_items, shop_item_multipliers))
realign_shop(current_shop_items, shop_submenu)
current_shop_items = adjust_prices(current_shop_items, price_scaler)
display_shop_prices = update_prices(current_shop_items)

# testing stuff
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

# variables that the shop items will adjust
jackpot_multiplier = 1
odd_multiplier = 1
even_multiplier = 1
money_taken_multiplier = 1

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
                    display_current_bet = display_font.render(f"Current Bet: ${current_bet}", True, (150, 150, 150))
                    # updates the current bet

            # checks for mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if change_bet_confirm.rect.collidepoint(event.pos):
                    change_bet_submenu.open()
                    current_bet = int(change_bet)
                    display_current_bet = display_font.render(f"Current Bet: ${current_bet}", True, (150, 150, 150))
                    # updates the current bet
                elif change_bet_back.rect.collidepoint(event.pos):
                    change_bet_submenu.open()
                    # closes the menu without updating the bet

        elif event.type == pygame.TEXTINPUT:
            if event.text == " " and dice_option.clicked:  # checks if space is held down
                money = gamble(money, all_dice, current_bet, jackpot_multiplier, even_multiplier, odd_multiplier, money_taken_multiplier)
                display_money = display_font.render(f"${money}", True, (150, 150, 150))
                dice_total = add_dice_total(all_dice)
                display_dice_total = display_font.render(f"{dice_total}", True, (100, 100, 100))

        elif shop_submenu.is_open:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shop_close_button.rect.collidepoint(event.pos):
                    shop_submenu.open()
                # buying items
                for i in range(len(current_shop_items)):
                    if current_shop_items[i].rect.collidepoint(event.pos):
                        if current_shop_items[i].price < money:

                            money -= current_shop_items[i].price    # updates money
                            display_money = display_font.render(f"${money}", True, (150, 150, 150))

                            shop_bought.append(current_shop_items[i])   # appends the item to the bought items
                            item_bought = current_shop_items[i]
                            current_shop_items.pop(i)   # removes it from the shop
                            current_shop_items.append(pick_random_shop_item(shop_items, shop_item_multipliers))    # adds new item
                            realign_shop(current_shop_items, shop_submenu)


                            price_scaler += random.randint(0, 100)        # readjusts prices
                            current_shop_items = adjust_prices(current_shop_items, price_scaler)
                            display_shop_prices = update_prices(current_shop_items)     # updates shop item prices

                            # effects of bought item
                            if "Dice_Add" in item_bought.name:
                                if item_bought.name == "Dice_Add1":
                                    all_dice.append(Dice(6, times_scaled))
                                elif item_bought.name == "Dice_Add2":
                                    for i in range(2):
                                        all_dice.append(Dice(6, times_scaled))
                                elif item_bought.name == "Dice_Add3":
                                    for i in range(3):
                                        all_dice.append(Dice(6, times_scaled))
                                elif item_bought.name == "Dice_Add10":
                                    for i in range(10):
                                        all_dice.append(Dice(6, times_scaled))
                                new_die_added = True
                            elif "Jackpot_" in item_bought.name:
                                if item_bought.name == "Jackpot_x2":
                                    jackpot_multiplier += 2
                                elif item_bought.name == "Jackpot_x3":
                                    jackpot_multiplier += 3
                                elif item_bought.name == "Jackpot_x5":
                                    jackpot_multiplier += 5
                                elif item_bought.name == "Jackpot_x10_MoneyTaken_x2":
                                    jackpot_multiplier += 10
                                    money_taken_multiplier = money_taken_multiplier * 2
                            elif "MoneyTaken" in item_bought.name:
                                if item_bought.name == "MoneyTaken_Divide2":
                                    money_taken_multiplier = money_taken_multiplier / 2
                            elif "Number_" in item_bought.name:
                                if item_bought.name == "OddNumber_x2":
                                    odd_multiplier += 2
                                elif item_bought.name == "EvenNumber_x2":
                                    even_multiplier += 2

        # checks for mouse button clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if dice_option.clicked:
                # rolls dice
                if roll_button.rect.collidepoint(event.pos):
                    money = gamble(money, all_dice, current_bet, jackpot_multiplier, even_multiplier, odd_multiplier, money_taken_multiplier)
                    display_money = display_font.render(f"${money}", True, (150, 150, 150))
                    dice_total = add_dice_total(all_dice)
                    display_dice_total = display_font.render(f"{dice_total}", True, (100, 100, 100))

                elif shop_button.rect.collidepoint(event.pos) and not shop_submenu.is_open:
                    shop_submenu.open()

                # opens and closes the change_bet submenu
                elif change_bet_button.rect.collidepoint(event.pos):
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
        elif shop_submenu.is_open:
            screen.blit(shop_submenu.image, shop_submenu.rect)
            screen.blit(shop_close_button.image, shop_close_button.rect)
            screen_blit_shop_items(current_shop_items)
            blit_prices(display_shop_prices, current_shop_items)
        # testing stuff
        if settings["testing"]:
            if testing_submenu.is_open:
                screen.blit(testing_submenu.image, testing_submenu.rect)
                screen.blit(add_dice_button.image, add_dice_button.rect)
            screen.blit(test_tools_button.image, test_tools_button.rect)

        screen.blit(display_current_bet, (screen_center[0], 0))
        screen.blit(display_money, (screen_center[0], 20))
        screen.blit(display_dice_total, (30, 30))
    # shows the menu screen
    else:
        screen.blit(dice_option.image, dice_option.rect)



    pygame.display.update()
    frame += 1

# Once we have exited the main program loop we can stop the game engine
pygame.quit()
