import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player_sprite = pygame.image.load("sprite_sprite.png").convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (50, 65))

player_rect = pygame.Rect(400, 300, 50, 65)
player_speed = 5
velocity_y = 0
gravity = 1
color = (255, 0, 0)
floor = pygame.Rect(0, 500, 800, 100)
floor_color = (202, 122, 233)
on_floor = True
coins_left = 5
coin_color = (255, 255, 100)

coins = []
for i in range(5):
    x = random.randint(50, 750)
    y = random.randint(200, 450)
    coins.append(pygame.Rect(x, y, 25, 25))

game_won = False
font = pygame.font.SysFont("Arial", 36)

def reset_game():
    global player_rect, velocity_y, coins, coins_left, game_won

    player_rect = pygame.Rect(400, 300, 50, 50)
    velocity_y = 0

    coins = []
    for i in range(5):
        x = random.randint(50, 750)
        y = random.randint(200, 450)
        coins.append(pygame.Rect(x, y, 25, 25))

    coins_left = 5
    game_won = False
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player_rect.x > 0:
            player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        if player_rect.x < 750:
            player_rect.x += player_speed

    if keys[pygame.K_r]:
            reset_game()

    if player_rect.colliderect(floor):
        on_floor = True
        velocity_y = 0
    else:
        on_floor = False
        velocity_y += gravity

    if keys[pygame.K_UP]:
        if on_floor:
            velocity_y -= 24

    player_rect.y += velocity_y

    for coin in coins[:]: 
        if player_rect.colliderect(coin):
            coins.remove(coin)
            coins_left -= 1

    font = pygame.font.SysFont("Arial", 36)
    text_surface = font.render(str(coins_left), True, (0, 0, 0))
    
    if coins_left == 0:
        game_won = True

    screen.fill((135, 206, 235))

    if not game_won:

        text_surface = font.render(str(coins_left), True, (0,0,0))
        screen.blit(text_surface, (400,100))

        screen.blit(player_sprite, player_rect)
        pygame.draw.rect(screen, floor_color, floor)

        for coin in coins:
            pygame.draw.ellipse(screen, coin_color, coin)

    else:
        win_text = font.render("YOU WIN!", True, (0,0,0))
        restart_text = font.render("Press R to Restart", True, (0,0,0))
        screen.blit(win_text, (330,250))
        screen.blit(restart_text, (290,300))

    pygame.display.flip()

    clock.tick(60)