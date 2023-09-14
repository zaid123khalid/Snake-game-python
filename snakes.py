import pygame
import pygame_menu

import sqlite3

from game_board import Board

conn = sqlite3.connect("snake.db")
c = conn.cursor()

c.execute("""CREATE TABLE if not exists snake(
            id integer, name text, score integer)
            """)

conn.commit()
conn.close()

pygame.init()
pygame.display.set_caption('Snakes')
window_x = 720
window_y = 480

surface = pygame.display.set_mode((window_x, window_y))

game_window = pygame.display.set_mode((window_x, window_y))

smallfont = pygame.font.SysFont("Algerian", 25)
mediumfont = pygame.font.SysFont("Algerian", 50)
largefont = pygame.font.SysFont("Algerian", 80)


def text_objects(text, color, size):
    if size == "small":
        textsurface = smallfont.render(text, True, color)
    if size == "medium":
        textsurface = mediumfont.render(text, True, color)
    if size == "large":
        textsurface = largefont.render(text, True, color)
    return textsurface, textsurface.get_rect()


def message_screen(text, color, y_displace, size="large"):
    textSurf, textRect = text_objects(text, color, size)
    textRect.center = (window_x / 2), (window_y / 2) + y_displace
    game_window.blit(textSurf, textRect)


def easy():

    Board().mode(speed=10,scr=0,main_menu=main_menu,difficulty=1)


def medium():
    Board().mode(speed=20,scr=0,main_menu=main_menu,difficulty=2)


def hard():
    Board().mode(speed=30,scr=0,main_menu=main_menu,difficulty=3)

def Back():
    return main_menu()


def start_game():
    difficulty_menu = pygame_menu.Menu('Select Difficulty', 500, 400, theme=pygame_menu.themes.THEME_DARK)
    difficulty_menu.add.button('Easy', easy, selection_color=[200,50,70], font_color="black")
    difficulty_menu.add.button('Medium', medium, selection_color=[200,50,70], font_color="black")
    difficulty_menu.add.button('Hard', hard, selection_color=[200,50,70], font_color="black")
    difficulty_menu.add.button('Back', Back, selection_color=[200,50,70], font_color="black")
    difficulty_menu.mainloop(surface)


def Help():
    Help_menu = pygame_menu.Menu('Help', 500, 400, theme=pygame_menu.themes.THEME_DARK)
    HELP = "Use arrow keys to control snake" \
           "\nPress p to pause or c to continue" \
           "\nPress Escape to return to Menu" \
           "\nWhile paused Press q to quit the game" \
           "\nWhile In-game Press Esc to get back to main menu instantly"
    Help_menu.add.label(HELP, max_char=-1, font_size=20, font_name="georgia", font_color="black")
    Help_menu.add.button('Back', Back, selection_color=[200,50,70], font_color="black")
    Help_menu.mainloop(surface)


def score():
    conn = sqlite3.connect('snake.db')
    c = conn.cursor()
    c.execute("SELECT score FROM snake WHERE id = 1")
    recs = c.fetchone()
    c.execute("SELECT score FROM snake WHERE id = 2")
    recs1 = c.fetchone()
    c.execute("SELECT score FROM snake WHERE id = 3")
    recs2 = c.fetchone()
    if recs == None:
        recs = [0]
    if recs1 == None:
        recs1 = [0]
    if recs2 == None:
        recs2 = [0]
    conn.commit()
    conn.close()

    score_menu = pygame_menu.Menu('Hi-Score', 500, 400, theme=pygame_menu.themes.THEME_DARK)
    score_menu.add.label(f"Easy : {recs[0]}", max_char=-1, font_size=30, font_name="georgia", font_color="black")
    score_menu.add.label(f"Medium : {recs1[0]}", max_char=-1, font_size=30, font_name="georgia", font_color="black")
    score_menu.add.label(f"Hard : {recs2[0]}", max_char=-1, font_size=30, font_name="georgia", font_color="black")
    score_menu.add.button('Back', Back, selection_color=[200,50,70], font_color="black")
    score_menu.mainloop(surface)


def Reset_score():
    conn = sqlite3.connect('snake.db')
    c = conn.cursor()

    c.execute("SELECT score FROM snake WHERE id = 1")
    recs = c.fetchone()
    c.execute("SELECT score FROM snake WHERE id = 2")
    recs1 = c.fetchone()
    c.execute("SELECT score FROM snake WHERE id = 3")
    recs2 = c.fetchone()
    if recs != None:
        recs = 0
        c.execute("DELETE FROM snake WHERE id = 1")
        c.execute("INSERT INTO snake VALUES(:id, :name, :score)",
                  {"id": 1, "name": "Easy", "score": recs})
    if recs1 != None:
        recs1 = 0
        c.execute("DELETE FROM snake WHERE id = 2")
        c.execute("INSERT INTO snake VALUES(:id, :name, :score)",
                  {"id": 2, "name": "Medium", "score": recs1})
    if recs2 != None:
        recs2 = 0
        c.execute("DELETE FROM snake WHERE id = 3")
        c.execute("INSERT INTO snake VALUES(:id, :name, :score)",
                  {"id": 3, "name": "Hard", "score": recs2})
    conn.commit()
    conn.close()


def Quit():
    quit_menu = pygame_menu.Menu('Good luck', 500, 400, theme=pygame_menu.themes.THEME_DARK)
    quit_menu.add.button('Yes', pygame_menu.events.EXIT, selection_color=[200,50,70], font_color="black")
    quit_menu.add.button('No', Back, selection_color=[200,50,70], font_color="black")
    quit_menu.mainloop(surface)


def main_menu():
    pygame.mixer.music.load('Snake Game - Theme Song.mp3')
    pygame.mixer.music.play(-1)
    menu = pygame_menu.Menu('Welcome', 500, 400, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Play', start_game, selection_color=[200,50,70], font_color="black")
    menu.add.button('Help', Help, selection_color=[200,50,70], font_color="black")
    menu.add.button('Hi-Score', score, selection_color=[200, 50, 70], font_color="black")
    menu.add.button('Reset Score', Reset_score, selection_color=[200, 50, 70], font_color="black")
    menu.add.button('Quit', Quit, selection_color=[200,50,70], font_color="black")
    menu.mainloop(surface)


main_menu()