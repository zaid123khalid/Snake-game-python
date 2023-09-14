import pygame
import random
import time
import sqlite3

import consts

class Board:
    fps = pygame.time.Clock()
    game_window = pygame.display.set_mode((consts.window_x, consts.window_y))
    
    def mode(self, speed, scr, main_menu, difficulty):
        self.snake_speed = speed

        snake_position = [100, 50]

        snake_body = [[100, 50],
                    [90, 50],
                    [80, 50],
                    [70, 50]
                    ]

        fruit_position = [random.randrange(1, (consts.window_x // 10)) * 10,
                        random.randrange(1, (consts.window_y // 10)) * 10]

        fruit_spawn = True

        direction = 'RIGHT'
        change_to = direction

        self.score = scr

        def show_score(choice, color, font, size):

            score_font = pygame.font.SysFont(font, size)
            score_surface = score_font.render('Score : ' + str(self.score), True, color)
            score_rect = score_surface.get_rect()
            self.game_window.blit(score_surface, score_rect)

        def game_over():

            my_font = pygame.font.SysFont('times new roman', 50)
            game_over_surface = my_font.render('Your Score is : ' + str(self.score), True, consts.red)
            game_over_rect = game_over_surface.get_rect()
            game_over_rect.center = (consts.window_x / 2, consts.window_y / 4)
            self.game_window.blit(game_over_surface, game_over_rect)
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
                        return main_menu
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
                self.score += 1
                fruit_spawn = False
            else:
                snake_body.pop()

            if not fruit_spawn:
                fruit_position = [random.randrange(1, (consts.window_x // 10)) * 10,
                                random.randrange(1, (consts.window_y // 10)) * 10]

            fruit_spawn = True
            self.game_window.fill(consts.black)

            for pos in snake_body:
                pygame.draw.rect(self.game_window, consts.green,
                                pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(self.game_window, consts.red, pygame.Rect(
                fruit_position[0], fruit_position[1], 10, 10))

            if snake_position[0] < 0 or snake_position[0] > consts.window_x - 10:
                game_over()
            if snake_position[1] < 0 or snake_position[1] > consts.window_y - 10:
                game_over()

            for block in snake_body[1:]:
                if snake_position[0] == block[0] and snake_position[1] == block[1]:
                    game_over()

            show_score(1, consts.white, 'times new roman', 20)
            pygame.display.update()
            self.fps.tick(self.snake_speed)


            if difficulty == 1:

                conn = sqlite3.connect('snake.db')
                c = conn.cursor()

                c.execute("SELECT score FROM snake WHERE id = 1")
                rec = c.fetchone()
                if rec == None:
                    score2 = 0
                else:
                    score2 = int(rec[0])
                if score2 < self.score:
                    c.execute("DELETE FROM snake WHERE id = 1")
                    c.execute("INSERT INTO snake VALUES(:id, :name, :score)",
                            {"id": 1, "name": "Easy", "score": self.score})

                conn.commit()
                conn.close()

            elif difficulty == 2:

                conn = sqlite3.connect('snake.db')
                c = conn.cursor()

                c.execute("SELECT score FROM snake WHERE id = 2")
                rec = c.fetchone()
                if rec == None:
                    score2 = 0
                else:
                    score2 = int(rec[0])
                if score2 < self.score:
                    c.execute("DELETE FROM snake WHERE id = 2")
                    c.execute("INSERT INTO snake VALUES(:id, :name, :score)",
                            {"id": 2, "name": "Medium", "score": self.score})

                conn.commit()
                conn.close()

            elif difficulty == 1:

                conn = sqlite3.connect('snake.db')
                c = conn.cursor()

                c.execute("SELECT score FROM snake WHERE id = 3")
                rec = c.fetchone()
                if rec == None:
                    score2 = 0
                else:
                    score2 = int(rec[0])
                if score2 < self.score:
                    c.execute("DELETE FROM snake WHERE id = 3")
                    c.execute("INSERT INTO snake VALUES(:id, :name, :score)",
                            {"id": 3, "name": "Hard", "score": self.score})

                conn.commit()
                conn.close()