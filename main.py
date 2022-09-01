import pygame
import sys

from EnemyClass import Orange_PB_Enem
from GameUIClass import GameUI
from LevelManagerClass import Level, LevelManager
from PlayerClass import Player

# from UserInterface import UserInterface
menu_clock = pygame.time.Clock()
clock = pygame.time.Clock()
pygame.display.set_caption('Colour!')

pygame.init()

ui = GameUI()

WINDOW_SIZE = (1280, 720)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((320, 180))
main_display = pygame.Surface((320, 180))
options_display = pygame.Surface((320, 180))
settings_display = pygame.Surface((320, 180))
true_scroll = [0, 0]

# player init
player = Player()

# levels
level_one = Level('map.txt')
level_one.load_map()

level_one_manager = LevelManager(level_one)
level_one_manager.enemies.append(Orange_PB_Enem())

player.becomes_colourful()

background = pygame.image.load('background.png').convert_alpha()
background_parallax = pygame.image.load('background_parallax.png').convert_alpha()
foreground_parallax = pygame.image.load('foreground_parallax.png').convert_alpha()


# run game
def run_game():
    anim_count = 1
    idle_count = 0
    while True:
        display.blit(background, [0, 0])
        true_scroll[0] += (player.rect.x - true_scroll[0] - 154) / 10
        true_scroll[1] += (player.rect.y - true_scroll[1] - 98) / 10
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
        display.blit(background_parallax, [0 - int(0.5 * scroll[0]), 50 - int(0.1 * scroll[1])])

        level_one.draw_map(display, scroll)
        player.update(anim_count, idle_count, level_one_manager.enemies)
        level_one_manager.update(anim_count)
        level_one_manager.draw(display, scroll)

        player.rect, collisions = level_one.map_collision(player.rect, player.player_movement)

        if collisions['top']:
            player.player_y_momentum = 1
            player.is_jumping = False
            player.is_falling = True
        if collisions['bottom']:
            player.player_y_momentum = 0
            player.air_timer = 0
            player.is_falling = False
        else:
            player.air_timer += 1

        player.draw(display, scroll)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                player.is_idle = False
                if keys[pygame.K_LSHIFT] and player.is_colourful:
                    player.is_changing_colour = True
                if keys[pygame.K_z]:
                    if player.air_timer < 6:
                        player.player_y_momentum = -7
                        player.is_jumping = True
                        player.is_idle = False
                if not player.is_changing_colour:
                    ui.cur_colour_line = ui.colour_line
                    if keys[pygame.K_LEFT] and keys[
                        pygame.K_RIGHT]:  # event.key == pygame.K_LEFT and event.key == pygame.K_RIGHT:
                        player.is_idle = True
                        player.moving_right, player.moving_left = False, False
                    if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                        player.moving_right = True
                        player.moving_left = False
                        player.is_idle = False
                        player.facing_right, player.facing_left = True, False
                        player.init_move = player.moving_right
                    elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                        player.moving_left = True
                        player.moving_right = False
                        player.is_idle = False
                        player.facing_left, player.facing_right = True, False
                        player.init_move = player.moving_left
                else:
                    player.moving_left, player.moving_right = False, False
                    if event.key == pygame.K_LEFT:
                        if player.colour_index >= 2:
                            player.colour_index = 0
                        else:
                            player.colour_index += 1
                        player.change_colour()
                        ui.change_colour(player, player.colour_index)
                        idle_count = 0
                    elif event.key == pygame.K_RIGHT:
                        if player.colour_index <= 0:
                            player.colour_index = 2
                        else:
                            player.colour_index -= 1
                        player.change_colour()
                        ui.change_colour(player, player.colour_index)
                        idle_count = 0
                    ui.cur_colour_line = ui.changing_colour_ui[ui.colour_index]
                if event.key == pygame.K_ESCAPE:
                    options_menu()
            if event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                player.is_idle = True
                if event.key == pygame.K_RIGHT:
                    player.moving_right = False
                    if keys[pygame.K_LEFT]:
                        player.moving_left = True
                        player.facing_left, player.facing_right = True, False
                        player.is_idle = False
                        if player.init_move == player.moving_right:
                            player.init_move = player.moving_left
                    else:
                        player.moving_left = False
                        player.facing_right, player.facing_left = True, False
                        player.init_move = player.moving_right
                if event.key == pygame.K_LEFT:
                    player.moving_left = False
                    if keys[pygame.K_RIGHT]:
                        player.moving_right = True
                        player.facing_right, player.facing_left = True, False
                        player.is_idle = False
                        if player.init_move == player.moving_left:
                            player.init_move = player.moving_right
                    else:
                        player.moving_right = False
                        player.facing_left, player.facing_right = True, False
                        player.is_idle = True
                        player.init_move = player.moving_left
                if event.key == pygame.K_LEFT and event.key == pygame.K_RIGHT:
                    player.is_idle = True
                    player.moving_left, player.moving_right = False
                if event.key == pygame.K_z:
                    player.is_jumping = False
                    if collisions['bottom']:
                        player.is_idle = True
                        player.is_falling = False
                        player.is_jumping = False
                    else:
                        if player.is_idle:
                            player.is_falling = False
                        else:
                            player.is_falling = True
                        player.is_idle = False
                if event.key == pygame.K_LSHIFT and player.is_colourful:
                    player.is_changing_colour = False
                    ui.cur_colour_line = ui.colour_line

        if player.player_y_momentum > 1.21:
            player.is_jumping = False
            player.is_falling = True
        elif player.player_y_momentum > 0:
            player.is_jumping = False
            if not player.moving_left and not player.moving_right:
                player.is_idle = True

        display.blit(foreground_parallax, [-250 - 2 * scroll[0], 0 - int(0.5 * scroll[1])])
        ui.change_health(player)
        ui.draw(display, player)
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(60)
        if anim_count >= 5:
            anim_count = 0
        anim_count += 1
        if not player.is_idle:
            idle_count = 0
        elif player.is_idle:
            if idle_count <= 240:
                idle_count += 1


def main_menu():
    click = False
    play_button = pygame.image.load('main_menu_buttons/play_button.png').convert_alpha()
    play_button_rect = pygame.Rect(100, 60, play_button.get_width(), play_button.get_height())
    quit_button = pygame.image.load('main_menu_buttons/quit_button.png').convert_alpha()
    quit_button_rect = pygame.Rect(100, 120, quit_button.get_width(), quit_button.get_height())
    while True:
        main_display.fill('black')

        m_x, m_y = pygame.mouse.get_pos()

        main_display.blit(play_button, (play_button_rect.x, play_button_rect.y))
        main_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))

        play_button_rect_scaled = pygame.Rect(400, 240, 400, 200)
        quit_button_rect_scaled = pygame.Rect(400, 480, 400, 200)
        if play_button_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                run_game()
            main_display.fill('black')
            main_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))
            main_display.blit(play_button, (play_button_rect.x, play_button_rect.y - 5))
        elif quit_button_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                pygame.quit()
                sys.exit()
            main_display.fill('black')
            main_display.blit(play_button, (play_button_rect.x, play_button_rect.y))
            main_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y - 5))

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        surf = pygame.transform.scale(main_display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        menu_clock.tick(60)


def options_menu():
    click = False
    resume_button = pygame.image.load('options_buttons/resume_button.png').convert_alpha()
    resume_button_rect = pygame.Rect(100, 60, resume_button.get_width(), resume_button.get_height())
    settings_button = pygame.image.load('options_buttons/settings_button.png').convert_alpha()
    settings_button_rect = pygame.Rect(100, 80, settings_button.get_width(), settings_button.get_height())
    exit_to_menu_button = pygame.image.load('options_buttons/exit_to_menu_button.png').convert_alpha()
    exit_to_menu_button_rect = pygame.Rect(100, 100, exit_to_menu_button.get_width(), exit_to_menu_button.get_height())
    quit_button = pygame.image.load('options_buttons/quit_button.png').convert_alpha()
    quit_button_rect = pygame.Rect(100, 120, quit_button.get_width(), quit_button.get_height())
    while True:
        options_display.fill('black')
        m_x, m_y = pygame.mouse.get_pos()
        options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y))
        options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))
        options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y))
        options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))

        if resume_button_rect.collidepoint((m_x, m_y)):
            if click:
                break
            else:
                options_display.fill('black')
                options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y - 5))
                options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))
                options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y))
                options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))
        elif exit_to_menu_button_rect.collidepoint((m_x, m_y)):
            if click:
                main_menu()
            else:
                options_display.fill('black')
                options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y))
                options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))
                options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y - 5))
                options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))
        elif quit_button_rect.collidepoint((m_x, m_y)):
            if click:
                pygame.quit()
                sys.exit()
            else:
                options_display.fill('black')
                options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y))
                options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))
                options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y))
                options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y - 5))
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        surf = pygame.transform.scale(options_display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        menu_clock.tick(60)


def settings():
    click = False
    while True:
        settings_display.blit('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        surf = pygame.transform.scale(settings_display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        menu_clock.tick(60)

def confirm_quit(cur_display):
    click = False
    yes_button = None
    yes_button_rect = None
    no_button = None
    no_button_rect = None
    confirm_quit_screen = None
    while True:
        cur_display.blit('black')
        m_x, m_y = pygame.mouse.get_pos()

        if yes_button_rect.collidepoint((m_x, m_y)):
            if click:
                pygame.quit()
                sys.exit()
            else:
                cur_display.blit(yes_button, [0,0])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        surf = pygame.transform.scale(cur_display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        menu_clock.tick(60)



main_menu()
