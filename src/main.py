import pygame
import sys

from Entity.PaintBlobEnemyClass import OrangePBEnem, RedPBEnem, YellowPBEnem
from Entity.PygmyPaintEnemyClass import YellowPygmyEnem
from GUI.GameUIClass import GameUI
from Level.LevelManagerClass import Level, LevelManager
from Entity.PlayerClass import Player
from GUI.FontClass import Font
from SaveAndLoadManager import SaveAndLoadSystem
from Level.AreaManagerClass import AreaManager

# from UserInterface import UserInterface
menu_clock = pygame.time.Clock()
clock = pygame.time.Clock()
pygame.display.set_caption('Colour!')

pygame.init()

ui = GameUI()
save_load_sys = SaveAndLoadSystem('resources/data/save_data')

WINDOW_SIZE = (1280, 720)
GAME_WINDOW = (400, 225)
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
display = pygame.Surface(GAME_WINDOW)
main_display = pygame.Surface(GAME_WINDOW)
save_files_display = pygame.Surface(GAME_WINDOW)
options_display = pygame.Surface(GAME_WINDOW)
settings_display = pygame.Surface(GAME_WINDOW)
true_scroll = [0, 0]

# player init
player: Player = Player()
is_game_complete: bool = False
data: dict = {'player_x': 0, 'player_y': 0, 'game_complete': is_game_complete}

# levels
level_one: Level = Level('resources/data/maps/room1.txt')
font = Font('resources/textures/font_system/small_font.png')
level_one_manager: LevelManager = LevelManager(level_one)
level_one_manager.add_enem(OrangePBEnem([0, 0]))
level_one_manager.add_enem(RedPBEnem([300, 0]))
level_one_manager.add_enem(YellowPBEnem([150, 0]))
level_one_manager.add_enem(YellowPygmyEnem([150, 0]))
level_two: Level = Level('resources/data/maps/room2.txt')
level_two_manager: LevelManager = LevelManager(level_two)

rooms: list = [level_one_manager, level_two_manager]
tutorial: AreaManager = AreaManager(rooms)
cur_level: LevelManager = tutorial.cur_room

background: pygame.image = pygame.image.load('resources/textures/MapItems/background.png').convert_alpha()
background_parallax: pygame.image = pygame.image.load('background_parallax.png').convert_alpha()
foreground_parallax: pygame.image = pygame.image.load('foreground_parallax.png').convert_alpha()


# run game
def run_game(save_file: str) -> None:
    anim_count: int = 1
    idle_count: int = 0

    while True:
        display.blit(background, [0, 0])
        true_scroll[0] += (player.rect.x - true_scroll[0] - 204) / 10
        true_scroll[1] += (player.rect.y - true_scroll[1] - 120) / 10
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
        display.blit(background_parallax, [0 - int(0.5 * scroll[0]), 50 - int(0.1 * scroll[1])])

        cur_level.level_map.draw_map(display, scroll)
        player.update(anim_count, idle_count, level_one_manager.enemies)
        cur_level.update(anim_count, player.rect)
        cur_level.draw(display, scroll)

        player.rect, collisions = cur_level.level_map.map_collision(player.rect, player.player_movement)

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
                data['player_x'], data['player_y'], data[
                    'game_complete'] = player.rect.x, player.rect.y, is_game_complete
                save_load_sys.save_file(data, save_file)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                player.is_idle = False
                if keys[pygame.K_LSHIFT]:
                    player.is_changing_colour = True
                if keys[pygame.K_z]:
                    if player.air_timer < 6:
                        player.player_y_momentum = -7
                        player.is_jumping = True
                        player.is_idle = False
                if event.key == pygame.K_x:
                    player.is_attack = True
                if not player.is_changing_colour:
                    ui.cur_colour_line = ui.colour_line
                    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
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
                    options_menu(save_file)
            if event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_LSHIFT:
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
                if event.key == pygame.K_x:
                    player.is_attack = False
                if event.key == pygame.K_LSHIFT:
                    player.is_changing_colour = False
                    ui.cur_colour_line = ui.colour_line

        if player.player_y_momentum > 1.21:
            player.is_jumping = False
            player.is_falling = True
        elif player.player_y_momentum > 0:
            player.is_jumping = False
            if not player.moving_left and not player.moving_right:
                player.is_idle = True

        # display.blit(foreground_parallax, [-250 - 2 * scroll[0], 0 - scroll[1]])
        ui.change_health(player)
        ui.draw(display, player)
        surf: pygame.Surface = pygame.transform.scale(display, WINDOW_SIZE)
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


def main_menu() -> None:
    click: bool = False
    play_button: pygame.image = pygame.image.load('resources/textures/main_menu_buttons/play_button.png').convert_alpha()
    play_button_rect: pygame.Rect = pygame.Rect(100, 60, play_button.get_width(), play_button.get_height())
    quit_button: pygame.image = pygame.image.load('resources/textures/main_menu_buttons/quit_button.png').convert_alpha()
    quit_button_rect: pygame.Rect = pygame.Rect(100, 120, quit_button.get_width(), quit_button.get_height())
    while True:
        main_display.fill('black')

        m_x, m_y = pygame.mouse.get_pos()

        main_display.blit(play_button, (play_button_rect.x, play_button_rect.y))
        main_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))

        play_button_rect_scaled = pygame.Rect(scale_loc(play_button_rect.x, play_button_rect.y),
                                              scale_size(play_button.get_width(), play_button.get_height()))
        quit_button_rect_scaled = pygame.Rect(scale_loc(quit_button_rect.x, quit_button_rect.y),
                                              scale_size(quit_button.get_width(), quit_button.get_height()))
        if play_button_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                save_files_menu()
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


def save_files_menu() -> None:
    click = False
    save_files_bg = pygame.image.load('resources/textures/save_files_buttons/save_files.png').convert_alpha()
    empty_file = pygame.image.load('resources/textures/save_files_buttons/empty_save_file.png').convert_alpha()
    delete_button = pygame.image.load('resources/textures/save_files_buttons/delete_file_button.png').convert_alpha()
    delete_rect_1 = pygame.Rect(250, 58, delete_button.get_width(), delete_button.get_height())
    delete_rect_2 = pygame.Rect(250, 108, delete_button.get_width(), delete_button.get_height())
    delete_rect_3 = pygame.Rect(250, 158, delete_button.get_width(), delete_button.get_height())
    delete_highlight = pygame.image.load(
        'resources/textures/save_files_buttons/delete_highlight.png').convert_alpha()
    save_file_1 = pygame.image.load('resources/textures/save_files_buttons/save_file_1_button.png').convert_alpha()
    file_1_rect = pygame.Rect(50, 50, save_file_1.get_width(), save_file_1.get_height())
    save_file_2 = pygame.image.load('resources/textures/save_files_buttons/save_file_2_button.png').convert_alpha()
    file_2_rect = pygame.Rect(50, 100, save_file_2.get_width(), save_file_2.get_height())
    save_file_3 = pygame.image.load('resources/textures/save_files_buttons/save_file_3_button.png').convert_alpha()
    file_3_rect = pygame.Rect(50, 150, save_file_3.get_width(), save_file_3.get_height())
    hover_highlight = pygame.image.load(
        'resources/textures/save_files_buttons/save_file_highlight.png').convert_alpha()
    if not save_load_sys.check_for_file('file_1'):
        save_file_1 = empty_file
    if not save_load_sys.check_for_file('file_2'):
        save_file_2 = empty_file
    if not save_load_sys.check_for_file('file_3'):
        save_file_3 = empty_file
    while True:
        save_files_display.blit(save_files_bg, [0, 0])
        save_files_display.blit(save_file_1, (file_1_rect.x, file_1_rect.y))
        save_files_display.blit(save_file_2, (file_2_rect.x, file_2_rect.y))
        save_files_display.blit(save_file_3, (file_3_rect.x, file_3_rect.y))
        m_x, m_y = pygame.mouse.get_pos()

        file_1_rect_scaled = pygame.Rect(scale_loc(file_1_rect.x, file_1_rect.y),
                                         scale_size(save_file_1.get_width(), save_file_1.get_height()))
        file_2_rect_scaled = pygame.Rect(scale_loc(file_2_rect.x, file_2_rect.y),
                                         scale_size(save_file_2.get_width(), save_file_2.get_height()))
        file_3_rect_scaled = pygame.Rect(scale_loc(file_3_rect.x, file_3_rect.y),
                                         scale_size(save_file_3.get_width(), save_file_3.get_height()))
        delete_rect_1_scaled = pygame.Rect(scale_loc(delete_rect_1.x, delete_rect_1.y),
                                           scale_size(delete_button.get_width(), delete_button.get_height()))
        delete_rect_2_scaled = pygame.Rect(scale_loc(delete_rect_2.x, delete_rect_2.y),
                                           scale_size(delete_button.get_width(), delete_button.get_height()))
        delete_rect_3_scaled = pygame.Rect(scale_loc(delete_rect_3.x, delete_rect_3.y),
                                           scale_size(delete_button.get_width(), delete_button.get_height()))
        if file_1_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                if delete_rect_1_scaled.collidepoint((m_x, m_y)):
                    save_load_sys.delete_save('file_1')
                    save_file_1 = empty_file
                elif save_load_sys.check_for_file('file_1'):
                    loaded_data = save_load_sys.load_save('file_1')
                    if loaded_data is not None:
                        player.rect.x, player.rect.y = loaded_data['player_x'], loaded_data['player_y']
                        run_game('file_1')
                else:
                    run_game('file_1')
            else:
                save_files_display.blit(save_files_bg, [0, 0])
                save_files_display.blit(save_file_1, (file_1_rect.x, file_1_rect.y))
                save_files_display.blit(save_file_2, (file_2_rect.x, file_2_rect.y))
                save_files_display.blit(save_file_3, (file_3_rect.x, file_3_rect.y))
                save_files_display.blit(hover_highlight, (file_1_rect.x, file_1_rect.y))
                if save_load_sys.check_for_file('file_1'):
                    save_files_display.blit(delete_button, (delete_rect_1.x, delete_rect_1.y))
                    if delete_rect_1_scaled.collidepoint((m_x, m_y)):
                        if click:
                            save_load_sys.delete_save('file_1')
                        else:
                            save_files_display.blit(delete_highlight, (delete_rect_1.x, delete_rect_1.y))
        elif file_2_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                if delete_rect_2_scaled.collidepoint((m_x, m_y)):
                    save_load_sys.delete_save('file_2')
                    save_file_2 = empty_file
                elif save_load_sys.check_for_file('file_2'):
                    loaded_data = save_load_sys.load_save('file_2')
                    if loaded_data is not None:
                        player.rect.x, player.rect.y = loaded_data['player_x'], loaded_data['player_y']
                    run_game('file_2')
                else:
                    run_game('file_2')
            else:
                save_files_display.blit(save_files_bg, [0, 0])
                save_files_display.blit(save_file_1, (file_1_rect.x, file_1_rect.y))
                save_files_display.blit(save_file_2, (file_2_rect.x, file_2_rect.y))
                save_files_display.blit(save_file_3, (file_3_rect.x, file_3_rect.y))
                save_files_display.blit(hover_highlight, (file_2_rect.x, file_2_rect.y))
                if save_load_sys.check_for_file('file_2'):
                    save_files_display.blit(delete_button, (delete_rect_2.x, delete_rect_2.y))
                    if delete_rect_2_scaled.collidepoint((m_x, m_y)):
                        if click:
                            save_load_sys.delete_save('file_2')
                        else:
                            save_files_display.blit(delete_highlight, (delete_rect_2.x, delete_rect_2.y))
        elif file_3_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                if delete_rect_3_scaled.collidepoint((m_x, m_y)):
                    save_load_sys.delete_save('file_3')
                    save_file_3 = empty_file
                elif save_load_sys.check_for_file('file_3'):
                    loaded_data = save_load_sys.load_save('file_3')
                    if loaded_data is not None:
                        player.rect.x, player.rect.y = loaded_data['player_x'], loaded_data['player_y']
                    run_game('file_3')
                else:
                    run_game('file_3')
            else:
                save_files_display.blit(save_files_bg, [0, 0])
                save_files_display.blit(save_file_1, (file_1_rect.x, file_1_rect.y))
                save_files_display.blit(save_file_2, (file_2_rect.x, file_2_rect.y))
                save_files_display.blit(save_file_3, (file_3_rect.x, file_3_rect.y))
                save_files_display.blit(hover_highlight, (file_3_rect.x, file_3_rect.y))
                if save_load_sys.check_for_file('file_3'):
                    save_files_display.blit(delete_button, (delete_rect_3.x, delete_rect_3.y))
                    if delete_rect_3_scaled.collidepoint((m_x, m_y)):
                        if click:
                            save_load_sys.delete_save('file_3')
                        else:
                            save_files_display.blit(delete_highlight, (delete_rect_3.x, delete_rect_3.y))

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        surf = pygame.transform.scale(save_files_display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        menu_clock.tick(60)


def options_menu(save_file: str) -> None:
    click = False
    options_bg = pygame.image.load('resources/textures/options_buttons/options_bg.png').convert_alpha()
    pause_bg = pygame.image.load('resources/textures/options_buttons/pause_bg.png').convert_alpha()
    resume_button = pygame.image.load('resources/textures/options_buttons/resume_button.png').convert_alpha()
    resume_button_rect = pygame.Rect(100, 60, resume_button.get_width(), resume_button.get_height())
    settings_button = pygame.image.load('resources/textures/options_buttons/settings_button.png').convert_alpha()
    settings_button_rect = pygame.Rect(100, 80, settings_button.get_width(), settings_button.get_height())
    exit_to_menu_button = pygame.image.load(
        'resources/textures/options_buttons/exit_to_menu_button.png').convert_alpha()
    exit_to_menu_button_rect = pygame.Rect(100, 100, exit_to_menu_button.get_width(), exit_to_menu_button.get_height())
    quit_button = pygame.image.load('resources/textures/options_buttons/quit_button.png').convert_alpha()
    quit_button_rect = pygame.Rect(100, 120, quit_button.get_width(), quit_button.get_height())
    while True:
        options_display.blit(display, [0, 0])
        options_display.blit(pause_bg, [0, 0])
        # options_display.blit(options_bg, [0, 0])
        m_x, m_y = pygame.mouse.get_pos()
        options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y))
        options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))
        options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y))
        options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))

        resume_button_rect_scaled = pygame.Rect(scale_loc(resume_button_rect.x, resume_button_rect.y),
                                                scale_size(resume_button.get_width(), resume_button.get_height()))
        settings_button_rect_scaled = pygame.Rect(scale_loc(settings_button_rect.x, settings_button_rect.y),
                                                  scale_size(settings_button.get_width(), settings_button.get_height()))
        exit_to_menu_button_rect_scaled = pygame.Rect(scale_loc(exit_to_menu_button_rect.x, exit_to_menu_button_rect.y),
                                                      scale_size(exit_to_menu_button.get_width(),
                                                                 exit_to_menu_button.get_height()))

        if resume_button_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                break
            else:
                options_display.blit(display, [0, 0])
                options_display.blit(pause_bg, [0, 0])
                options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y - 5))
                options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))
                options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y))
                options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))
        elif settings_button_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                settings()
            else:
                options_display.blit(display, [0, 0])
                options_display.blit(pause_bg, [0, 0])
                options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y))
                options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y - 5))
                options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y))
                options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))
        elif exit_to_menu_button_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                confirm_quit(options_display, save_file)
            else:
                options_display.blit(display, [0, 0])
                options_display.blit(pause_bg, [0, 0])
                options_display.blit(resume_button, (resume_button_rect.x, resume_button_rect.y))
                options_display.blit(settings_button, (settings_button_rect.x, settings_button_rect.y))
                options_display.blit(exit_to_menu_button, (exit_to_menu_button_rect.x, exit_to_menu_button_rect.y - 5))
                options_display.blit(quit_button, (quit_button_rect.x, quit_button_rect.y))
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run_game(save_file)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        surf = pygame.transform.scale(options_display, WINDOW_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        menu_clock.tick(60)


def settings() -> None:
    click = False
    while True:
        settings_display.blit('black', [0, 0])
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


def confirm_quit(cur_display: pygame.Surface, save_file: str) -> None:
    click = False
    confirm_quit_screen = pygame.image.load('resources/textures/confirm_quit/confirm_quit_bg.png')
    yes_button = pygame.image.load('resources/textures/confirm_quit/confirm_quit_yes.png')
    yes_button_rect = pygame.Rect(100, 10, yes_button.get_width(), yes_button.get_height())
    no_button = pygame.image.load('resources/textures/confirm_quit/confirm_quit_no.png')
    no_button_rect = pygame.Rect(100, 20, no_button.get_width(), no_button.get_height())
    while True:
        cur_display.blit(confirm_quit_screen, [0, 0])
        cur_display.blit(yes_button, (yes_button_rect.x, yes_button_rect.y))
        cur_display.blit(no_button, (no_button_rect.x, no_button_rect.y))
        m_x, m_y = pygame.mouse.get_pos()
        yes_button_rect_scaled = pygame.Rect(scale_loc(yes_button_rect.x, yes_button_rect.y),
                                             scale_size(yes_button.get_width(), yes_button.get_height()))
        no_button_rect_scaled = pygame.Rect(scale_loc(no_button_rect.x, no_button_rect.y),
                                            scale_size(no_button.get_width(), no_button.get_height()))

        if yes_button_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                data['player_x'], data['player_y'] = player.rect.x, player.rect.y
                save_load_sys.save_file(data, save_file)
                main_menu()
            else:
                cur_display.blit(confirm_quit_screen, [0, 0])
                cur_display.blit(yes_button, (yes_button_rect.x, yes_button_rect.y - 1))
                cur_display.blit(no_button, (no_button_rect.x, no_button_rect.y))
        elif no_button_rect_scaled.collidepoint((m_x, m_y)):
            if click:
                break
            else:
                cur_display.blit(confirm_quit_screen, [0, 0])
                cur_display.blit(yes_button, (yes_button_rect.x, yes_button_rect.y))
                cur_display.blit(no_button, (no_button_rect.x, no_button_rect.y - 1))
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


def scale_loc(x: int, y: int) -> (int, int):
    scaled_x = (x / GAME_WINDOW[0]) * WINDOW_SIZE[0]
    scaled_y = (y / GAME_WINDOW[1]) * WINDOW_SIZE[1]
    return scaled_x, scaled_y


def scale_size(w: int, h: int) -> (int, int):
    scaled_w = (w / GAME_WINDOW[0]) * WINDOW_SIZE[0]
    scaled_h = (h / GAME_WINDOW[1]) * WINDOW_SIZE[1]
    return scaled_w, scaled_h


main_menu()
