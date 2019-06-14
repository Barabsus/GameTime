
#import required directories
import pygame
import random
import sys

#Start new pygame project
pygame.init()

#game window size
WIDTH = 800
HEIGHT = 600

#game window colors/player 1 figure dimensions
RED = (0,255,247)
YELLOW = (255, 255, 0)
BLUE = (255, 147,0)
BACKGROUND_COLOR = (0,0,0)
player_size = 10
player_pos = [WIDTH/2, HEIGHT-3*player_size]

#Enemy dimensions
enemy_size = 10
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)


def set_level(score, SPEED):
    if score < 20:
        SPEED = 5
    elif score < 40:
        SPEED = 8
    elif score < 60:
        SPEED = 12
    elif score < 100:
        SPEED = 15
    else:
        SPEED = 20
    return SPEED

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])
        
def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_position(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
           enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score +=1
    return score 
def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if e_x >= p_x and e_x < (p_x + player_size) or p_x >= e_x and (p_x <(e_x+enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
            return True
    return False

while not game_over:
    for event in pygame.event.get():
        x = player_pos[0]
        y = player_pos[1]
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size

            player_pos = [x,y]
    screen.fill(BACKGROUND_COLOR)
    if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
        enemy_pos[1]+= SPEED
    else:
        enemy_pos[0] = random.randint(0, WIDTH-enemy_size)
        enemy_pos[1]=0
    if detect_collision(player_pos, enemy_pos):
        game_over = True
        break
    drop_enemies(enemy_list)
    score = update_enemy_position(enemy_list, score)
    SPEED = set_level(score, SPEED)

    text = "Score:" + str(score)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH-200, HEIGHT-40))


    if collision_check(enemy_list, player_pos):
        game_over = True
    draw_enemies(enemy_list)
    pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(60)
    pygame.display.update()
    
    
