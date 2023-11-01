import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score Time: {current_time}', False, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(450, 100))
    screen.blit(score_surface, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 479:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 475:
        player_surf = player_jump_scaled
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]
    # play walking animation if player is on the floor
    # display the jump surface when player is not on the floor


# initializing pygame
pygame.init()

# screen display settings/configuration
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Snail Runner")
clock = pygame.time.Clock()  # framerate initializer
test_font = pygame.font.Font('../../OneDrive/Desktop/Pixeltype.ttf', 100)
game_active = False
start_time = 0
score = 0

# static images/sprites

sky_surface = pygame.image.load('NightSky.png')
ground_surface = pygame.image.load('ground(1).png')
sky_scaled = pygame.transform.scale(sky_surface, (1200, 550))  # Scaling the Sky image
ground_surface_scaled = pygame.transform.scale(ground_surface, (1000, 176))
# score_surface = test_font.render('Hello World', False, 'White')
# score_rect = score_surface.get_rect(center = (450,100))
"""
---------------------------------------------------------------------------------------------------
                                  Special Sprites Configuration
---------------------------------------------------------------------------------------------------
"""
# Obstacles
# Snail
snail_frame_1 = pygame.image.load('Snail1.png')
snail_frame_2 = pygame.image.load('Snail2.png')
snail_frame1_scaled = pygame.transform.scale(snail_frame_1, (60, 70))
snail_frame2_scaled = pygame.transform.scale(snail_frame_2, (60, 70))
snail_frames = [snail_frame1_scaled, snail_frame2_scaled]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = pygame.image.load('Fly1.png')
fly_frame_2 = pygame.image.load('Fly2.png')
fly_frame1_scaled = pygame.transform.scale(fly_frame_1, (60, 70))
fly_frame2_scaled = pygame.transform.scale(fly_frame_2, (60, 70))
fly_frames = [fly_frame1_scaled, fly_frame2_scaled]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

# Green player
player_walk_1 = pygame.image.load('UserWalk1.png')
player_walk1_scaled = pygame.transform.scale(player_walk_1, (80, 90))
player_walk_2 = pygame.image.load('UserWalk2.png')
player_walk2_scaled = pygame.transform.scale(player_walk_2, (80, 90))
player_walk = [player_walk1_scaled, player_walk2_scaled]
player_jump = pygame.image.load('jump.png')
player_jump_scaled = pygame.transform.scale(player_jump, (80, 90))
player_index = 0

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(120, 385))
player_gravity = 0

# Intro Screen
player_stand = pygame.image.load('UserStand.png')
player_stand_scaled = pygame.transform.scale(player_stand, (160, 175))
player_stand_rect = player_stand_scaled.get_rect(center=(450, 270))

game_name = test_font.render('Snailman Run', False, (255, 255, 255))
game_name_rect = game_name.get_rect(center=(450, 100))

game_message = test_font.render('Press SPACE to continue', False, (255, 255, 255))
game_message_rect = game_message.get_rect(center=(450, 450))
game_creators = test_font.render('Code: Michael S. Art: Ethan A.', False, (255, 255, 255))
game_creators_rect = game_creators.get_rect(center=(450, 530))
# Timer1
# pygame
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 479:
                    player_gravity = -21

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 479:
                    player_gravity = -21
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer and game_active:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 479)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 374)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game_active:
        # positioning & setting static images on screen
        screen.blit(sky_scaled, (0, 0))
        screen.blit(ground_surface_scaled, (-50, 479))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 479: player_rect.bottom = 479
        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((63, 109, 162))
        screen.blit(player_stand_scaled, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (120, 480)
        player_gravity = 0

        screen.blit(game_name, game_name_rect)

        score_message = test_font.render(f'Last Score: {score}', False, (255, 255, 255))
        score_message_rect = score_message.get_rect(center=(450, 450))

        if score == 0:
            screen.blit(game_message, game_message_rect)
            screen.blit(game_creators, game_creators_rect)

        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
