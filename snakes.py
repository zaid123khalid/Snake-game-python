import pygame
import pygame_menu
import random
import time
import sqlite3

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

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

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


def pause():

    paused = True

    while paused:
        pygame.mixer.music.pause()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                    pygame.mixer.music.unpause()
                if event.key == pygame.K_ESCAPE:
                    return main_menu()
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

        game_window.fill(black)
        message_screen("Paused", white, -100, size="small")
        message_screen("Press c to Continue or q to Quit", white, 25, size="small")
        message_screen("Escape to return to main menu", white, 50, size="small")
        pygame.display.update()
        fps.tick(5)


def easy():
    snake_speed = 10

    snake_position = [100, 50]

    snake_body = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]
                  ]

    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True

    direction = 'RIGHT'
    change_to = direction

    easy_score = 0

    def show_score(choice, color, font, size):

        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(easy_score), True, color)
        score_rect = score_surface.get_rect()
        game_window.blit(score_surface, score_rect)

    def game_over():

        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render('Your Score is : ' + str(easy_score), True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.center = (window_x / 2, window_y / 4)
        game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(2)

        return main_menu()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    return main_menu()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pause()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            easy_score += 1
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]

        fruit_spawn = True
        game_window.fill(black)

        for pos in snake_body:
            pygame.draw.rect(game_window, green,
                             pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, red, pygame.Rect(
            fruit_position[0], fruit_position[1], 10, 10))

        if snake_position[0] < 0 or snake_position[0] > window_x - 10:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > window_y - 10:
            game_over()

        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        show_score(1, white, 'times new roman', 20)
        pygame.display.update()
        fps.tick(snake_speed)

        conn = sqlite3.connect('snake.db')
        c = conn.cursor()

        c.execute("SELECT score FROM snake WHERE id = 1")
        rec = c.fetchone()
        if rec == None:
            score1 = 0
        else:
            score1 = int(rec[0])
        if score1 < easy_score:
            c.execute("DELETE FROM snake WHERE id = 1")
            c.execute("INSERT INTO snake VALUES(:id, :name, :score)",
                      {"id":1, "name": "Easy", "score":easy_score})

        conn.commit()
        conn.close()


def medium():
    snake_speed = 20

    snake_position = [100, 50]

    snake_body = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]
                  ]

    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True

    direction = 'RIGHT'
    change_to = direction

    medium_score = 0

    def show_score(choice, color, font, size):

        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(medium_score), True, color)
        score_rect = score_surface.get_rect()
        game_window.blit(score_surface, score_rect)

    def game_over():

        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render('Your Score is : ' + str(medium_score), True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.center = (window_x / 2, window_y / 4)
        game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(2)

        return main_menu()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    return main_menu()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pause()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            medium_score += 1
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]

        fruit_spawn = True
        game_window.fill(black)

        for pos in snake_body:
            pygame.draw.rect(game_window, green,
                             pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, red, pygame.Rect(
            fruit_position[0], fruit_position[1], 10, 10))

        if snake_position[0] < 0 or snake_position[0] > window_x - 10:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > window_y - 10:
            game_over()

        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        show_score(1, white, 'times new roman', 20)
        pygame.display.update()
        fps.tick(snake_speed)

        conn = sqlite3.connect('snake.db')
        c = conn.cursor()

        c.execute("SELECT score FROM snake WHERE id = 2")
        rec = c.fetchone()
        if rec == None:
            score2 = 0
        else:
            score2 = int(rec[0])
        if score2 < medium_score:
            c.execute("DELETE FROM snake WHERE id = 2")
            c.execute("INSERT INTO snake VALUES(:id, :name, :score)",
                      {"id": 2, "name": "Medium", "score": medium_score})

        conn.commit()
        conn.close()


def hard():
    snake_speed = 30

    snake_position = [100, 50]

    snake_body = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]
                  ]

    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True

    direction = 'RIGHT'
    change_to = direction

    hard_score = 0

    def show_score(choice, color, font, size):

        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(hard_score), True, color)
        score_rect = score_surface.get_rect()
        game_window.blit(score_surface, score_rect)

    def game_over():

        my_font = pygame.font.SysFont('times new roman', 50)
        game_over_surface = my_font.render('Your Score is : ' + str(hard_score), True, red)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.center = (window_x / 2, window_y / 4)
        game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        time.sleep(2)

        return main_menu()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    return main_menu()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pause()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            hard_score += 1
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]

        fruit_spawn = True
        game_window.fill(black)

        for pos in snake_body:
            pygame.draw.rect(game_window, green,
                             pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, red, pygame.Rect(
            fruit_position[0], fruit_position[1], 10, 10))

        if snake_position[0] < 0 or snake_position[0] > window_x - 10:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > window_y - 10:
            game_over()

        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        show_score(1, white, 'times new roman', 20)
        pygame.display.update()
        fps.tick(snake_speed)

        conn = sqlite3.connect('snake.db')
        c = conn.cursor()
        c.execute("SELECT score FROM snake WHERE id = 3")
        rec = c.fetchone()
        if rec == None:
            score2 = 0
        else:
            score2 = int(rec[0])
        if score2 < hard_score:
            c.execute("DELETE FROM snake WHERE id = 3")
            c.execute("INSERT INTO snake VALUES(:id, :name, :score)",
                      {"id": 3, "name": "Hard", "score": hard_score})

        conn.commit()
        conn.close()

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