import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player_sprite = pygame.image.load("sprite_sprite.png").convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (50, 65))

coin_sprite = pygame.image.load("cola.png").convert_alpha()
coin_sprite = pygame.transform.scale(coin_sprite, (50, 50))

player_rect = pygame.Rect(400, 100, 50, 65)
player_speed = 5
velocity_y = 0

gravity = 1
color = (255, 0, 0)

floor = pygame.Rect(0, 500, 800, 100)
floor_color = (202, 122, 233)
on_floor = True

coins_left = 5
coin_color = (255, 255, 100)

lava = pygame.Rect(300, 470, 150, 30)
lava_color = (255, 100, 0)
start_pos = (400, floor.y - player_rect.height)

lives = 2

coins = []
for i in range(5):
    x = random.randint(50, 750)
    y = random.randint(200, 450)
    coins.append(pygame.Rect(x, y, 50, 50))

def spawn_lava():
    while True:
        x = random.randint(0, 600)
        lava_rect = pygame.Rect(x, 470, 150, 30)

        if not lava_rect.colliderect(player_rect): 
            return lava_rect

game_won = False
game_lose = False
font = pygame.font.SysFont("Arial", 36)

def reset_game():
    global coins, coins_left, game_won, game_lose, lava, lives

    player_rect.topleft = start_pos

    coins = []
    for i in range(5):
        x = random.randint(50, 750)
        y = random.randint(200, 450)
        coins.append(pygame.Rect(x, y, 50, 50))

    coins_left = 5
    game_won = False
    game_lose = False

    lives = 2

    lava = spawn_lava()
    
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

    if player_rect.colliderect(lava):
        lives -= 1
        player_rect.topleft = start_pos
        velocity_y = 0

        if lives <= 0:
            game_lose = True

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

    if not game_won and not game_lose:

        lives_text = font.render("Lives: " + str(lives), True, (0,0,0))
        screen.blit(lives_text, (50, 50))
        text_surface = font.render("Coins Left: " + str(coins_left), True, (0,0,0))
        screen.blit(text_surface, (300,100))

        screen.blit(player_sprite, player_rect)
        pygame.draw.rect(screen, floor_color, floor)
        pygame.draw.rect(screen, lava_color, lava)

        for coin in coins:
            screen.blit(coin_sprite, coin)

    elif game_won:
        win_text = font.render("YOU WIN!", True, (0,0,0))
        restart_text = font.render("Press R to Restart", True, (0,0,0))
        screen.blit(win_text, (330,250))
        screen.blit(restart_text, (290,300))

    elif game_lose:
        lose_text = font.render("YOU DIED!", True, (0,0,0))
        restart_text = font.render("Press R to Restart", True, (0,0,0))
        screen.blit(lose_text, (330,250))
        screen.blit(restart_text, (290,300))

    pygame.display.flip()

    clock.tick(60)