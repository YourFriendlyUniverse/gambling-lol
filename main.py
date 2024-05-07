import pygame
from menubutton import MenuButton

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
            if dice_option.rect.collidepoint(event.pos):
                print("DICE")
            # elif slot_option.rect.collidepoint(event.pos):
            #     print("SLOTS")
    # do not blit above #
    screen.fill((0, 0, 0))
    # screen.blit(bg, (bg_x, 0))
    screen.blit(dice_option.image, dice_option.rect)

    pygame.display.update()
    frame += 1

# Once we have exited the main program loop we can stop the game engine
pygame.quit()
