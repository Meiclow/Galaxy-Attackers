import pygame
import pymongo

from GameObjects.Position import Position
from GameObjects.Player import Player
from GameObjects.Map import Map

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["galaxy-attackers"]
highscores_col = db["highscores"]
title = "Galaxy Attackers"
title_up = "GALAXY ATTACKERS"

pygame.init()
size = (1200, 900)
screen = pygame.display.set_mode(size)
model = 0
game_map = Map(screen, False, 0, model, 0)
pygame.display.set_caption(title, title)
pygame.display.set_icon(pygame.transform.scale(pygame.image.load("ufo (1).png"), (16, 16)))
player_position = Position(game_map.player_rect.centerx, game_map.player_rect.centery)
player = Player.spawn(player_position, model)
game_map.set_player(player)
clock = pygame.time.Clock()


def get_name():
    global game_on
    name_input = ""
    font = pygame.font.Font(None, 50)
    while True and game_on:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.unicode.isalpha():
                    name_input += evt.unicode
                elif evt.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                elif evt.key == pygame.K_RETURN:
                    return name_input
                elif evt.key == pygame.K_ESCAPE:
                    game_on = False
                    return name_input
            elif evt.type == pygame.QUIT:
                game_on = False
                return name_input
        screen.fill((0, 0, 0))

        text_font_1 = pygame.font.Font("freesansbold.ttf", 32)
        text_1 = text_font_1.render("Your name, my grace?", True, (255, 255, 255))
        text_1_rect = text_1.get_rect()
        text_1_rect.center = (size[0] / 2, size[1] / 2 - 80)

        block = font.render(name_input, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)

        screen.blit(text_1, text_1_rect)
        pygame.display.flip()


def add_score(score):
    highscores_col.insert_one({"username": name, "score": score})


def get_top_ten():
    return highscores_col.find({}).sort({"score"}, pymongo.DESCENDING)


def reset(current_map):
    new_map = Map(current_map.screen, False, current_map.difficulty, model, 0)
    new_map.set_player(Player.spawn(player_position, model))
    return new_map


def game_intro():
    global game_on
    intro = True
    while intro and game_on:
        clock.tick(120)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_on = False
                intro = False
        text_font_1 = pygame.font.Font("freesansbold.ttf", 64)
        text_1 = text_font_1.render(title_up, True, (255, 255, 255))
        text_1_rect = text_1.get_rect()
        text_1_rect.center = (size[0] / 2, size[1] / 2 - 40)
        text_font_2 = pygame.font.Font("freesansbold.ttf", 32)
        text_2 = text_font_2.render("Click SPACE to start the game", True, (255, 255, 255))
        text_2_rect = text_2.get_rect()
        text_2_rect.center = (size[0] / 2, size[1] / 2 + 20)
        screen.blit(text_1, text_1_rect)
        screen.blit(text_2, text_2_rect)
        pygame.display.update()


def menu():
    global game_on
    menu_on = True
    highlight = [48, 32]
    while menu_on and game_on:
        clock.tick(120)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                menu_on = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_on = False
                if event.key == pygame.K_DOWN and highlight[1] == 32:
                    highlight[0] = 32
                    highlight[1] = 48
                if event.key == pygame.K_UP and highlight[0] == 32:
                    highlight[1] = 32
                    highlight[0] = 48
                if event.key == pygame.K_RETURN:
                    menu_on = False
        text_font_1 = pygame.font.Font("freesansbold.ttf", 96)
        text_1 = text_font_1.render("MENU", True, (255, 255, 255))
        text_1_rect = text_1.get_rect()
        text_1_rect.center = (size[0] / 2, size[1] / 2 - 180)
        text_font_3 = pygame.font.Font("freesansbold.ttf", 16)
        text_3 = text_font_3.render("Choose your game mode", True, (255, 255, 255))
        text_3_rect = text_3.get_rect()
        text_3_rect.center = (size[0] / 2, size[1] / 2 - 120)
        text_font_2 = pygame.font.Font("freesansbold.ttf", highlight[0])
        text_2 = text_font_2.render("Level Mode", True, (255, 255, 255))
        text_2_rect = text_2.get_rect()
        text_2_rect.center = (size[0] / 2, size[1] / 2 - 5)
        text_font_4 = pygame.font.Font("freesansbold.ttf", highlight[1])
        text_4 = text_font_4.render("Endless Mode", True, (255, 255, 255))
        text_4_rect = text_4.get_rect()
        text_4_rect.center = (size[0] / 2, size[1] / 2 + 96)
        screen.blit(text_1, text_1_rect)
        screen.blit(text_2, text_2_rect)
        screen.blit(text_3, text_3_rect)
        screen.blit(text_4, text_4_rect)
        pygame.display.update()
    if highlight[0] == 48:
        return False
    return True


def game_outro():
    game_not_over = True
    while game_not_over:
        clock.tick(120)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_not_over = False
            if event.type == pygame.KEYDOWN:
                game_not_over = False
        text_font_1 = pygame.font.Font("freesansbold.ttf", 64)
        text_1 = text_font_1.render(title_up, True, (255, 255, 255))
        text_1_rect = text_1.get_rect()
        text_1_rect.center = (size[0] / 2, size[1] / 2 - 40)
        text_font_2 = pygame.font.Font("freesansbold.ttf", 32)
        text_2 = text_font_2.render("Press any key to end it all.", True, (255, 255, 255))
        text_2_rect = text_2.get_rect()
        text_2_rect.center = (size[0] / 2, size[1] / 2 + 20)
        text_font_3 = pygame.font.Font("freesansbold.ttf", 16)
        text_3 = text_font_3.render("Autors: Michał Dronka, Emilia Kwolek", True, (255, 255, 255))
        text_3_rect = text_2.get_rect()
        text_3_rect.center = (size[0] / 2, size[1] / 2 + 60)
        screen.blit(text_1, text_1_rect)
        screen.blit(text_2, text_2_rect)
        screen.blit(text_3, text_3_rect)
        pygame.display.update()


def level_over(text):
    global game_on
    intro = True
    while intro:
        clock.tick(120)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_on = False
                intro = False
        text_font_1 = pygame.font.Font("freesansbold.ttf", 64)
        text_1 = text_font_1.render(text + "level " + str(game_map.difficulty), True, (255, 255, 255))
        text_1_rect = text_1.get_rect()
        text_1_rect.center = (size[0] / 2, size[1] / 2 - 40)
        text_font_2 = pygame.font.Font("freesansbold.ttf", 32)
        text_2 = text_font_2.render("Click SPACE to continue", True, (255, 255, 255))
        text_2_rect = text_2.get_rect()
        text_2_rect.center = (size[0] / 2, size[1] / 2 + 20)
        screen.blit(text_1, text_1_rect)
        screen.blit(text_2, text_2_rect)
        pygame.display.update()


def game():
    global game_on
    win = False
    play = True
    while play and game_on:
        clock.tick(120)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game_map.player.speed_vector.x = -1
                if event.key == pygame.K_RIGHT:
                    game_map.player.speed_vector.x = 1
                if event.key == pygame.K_DOWN:
                    game_map.player.speed_vector.y = 1
                if event.key == pygame.K_UP:
                    game_map.player.speed_vector.y = -1
                if event.key == pygame.K_SPACE:
                    game_map.player_shoot()
                if event.key == pygame.K_ESCAPE:
                    game_on = False
                    break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    game_map.player.speed_vector.x = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    game_map.player.speed_vector.y = 0
        game_map.update()
        if game_map.game_over():
            win = False
            play = False
        if game_map.game_won():
            win = True
            play = False
        pygame.display.update()
    return win


# START OF THE GAME CODE
game_on = True
game_intro()
game_map.is_endless = menu()
pygame.display.set_mode(size, pygame.FULLSCREEN)
if not game_map.is_endless:
    for i in range(10):
        if game_on:
            game_map.difficulty = i
            success = False
            while not success and game_on:
                game_map = reset(game_map)
                success = game()
                if success is None:
                    break
                if game_on:
                    if success:
                        level_over("You won ")
                    else:
                        level_over("You lost ")
else:
    game_map = Map(screen, True, 0, model, 0)
    game_map.set_player(player)
    endless_win = True
    while endless_win and game_on:
        endless_win = game()
        if game_on:
            if endless_win:
                game_map.ascend()
                level_over("You won ")
            else:
                level_over("You lost on endless ")
                name = get_name()
                score = game_map.score
                add_score(score)

game_outro()
