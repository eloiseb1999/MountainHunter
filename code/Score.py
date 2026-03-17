import datetime

import pygame
from pygame import Surface, Rect
from pygame.constants import KEYDOWN, K_RETURN, K_BACKSPACE, K_ESCAPE
from pygame.font import Font

from code.DBProxy import DBProxy
from code.const import C_YELLOW, SCORE_POS, MENU_OPTION, C_WHITE


class Score:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load("./asset/ScoreBg.png").convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)
        pass

    def save_score(self, game_mode: str, player_score: list[int]):
        pygame.mixer.music.load("./asset/Score.mp3")
        pygame.mixer.music.play(-1)
        db_proxy = DBProxy('DBScore')
        name = ''

        while True:
            self.window.blit(source=self.surf, dest=self.rect)

            self.score_text(48, 'You Win!', C_YELLOW, SCORE_POS['Title'])

            if game_mode == MENU_OPTION[0]:
                score = player_score[0]
                text = 'PLAYER 1 ENTER YOUR NAME (4 CHARACTERS):'

            if game_mode == MENU_OPTION[1]:
                score = (player_score[0] + player_score[1]) // 2
                text = 'ENTER YOUR TEAM NAME (4 CHARACTERS):'

            if game_mode == MENU_OPTION[2]:
                if player_score[0] >= player_score[1]:
                    score = player_score[0]
                    text = 'PLAYER 1 ENTER YOUR NAME (4 CHARACTERS):'
                else:
                    score = player_score[1]
                    text = 'PLAYER 2 ENTER YOUR NAME (4 CHARACTERS):'

            self.score_text(20, text, C_WHITE, SCORE_POS['EnterName'])

            self.score_text(20, name, C_YELLOW, SCORE_POS['Name'])

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    db_proxy.close()
                    pygame.quit()
                    raise SystemExit

                elif ev.type == KEYDOWN:

                    if ev.key == K_RETURN and len(name) == 4:
                        db_proxy.save({"name": name,
                                       "score": score,
                                       "date": get_formatted_date()})

                        self.show()
                        return
                        db_proxy.close()
                        return

                    elif ev.key == K_BACKSPACE:
                        name = name[:-1]

                    else:
                        if len(name) < 4:
                            name += ev.unicode

            pygame.display.flip()
            pass

        pass

    def show(self):
        pygame.mixer.music.load('./asset/Score.mp3')
        pygame.mixer.music.play(-1)
        self.window.blit(source=self.surf, dest=self.rect)

        self.score_text(48, 'TOP 10 SCORE', C_YELLOW, SCORE_POS['Title'])
        self.score_text(20, 'NAME        SCORE        DATE', C_YELLOW, SCORE_POS['Label'])

        db_proxy = DBProxy('DBScore')
        list_score = db_proxy.retrieve_top10()
        db_proxy.close()

        for player_score in list_score:
            id_, name, score, date = player_score

            self.score_text(
                20,
                f'{name}      {score:05d}      {date}',
                C_YELLOW,
                SCORE_POS[list_score.index(player_score)]
            )

        while True:
            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        return
            pygame.display.flip()

    def score_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple, text_rect=None):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)

        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()

        text_rect: Rect = text_surf.get_rect(center=text_center_pos)

        self.window.blit(source=text_surf, dest=text_rect)


def get_formatted_date():
    current_datetime = datetime.datetime.now()
    current_time = current_datetime.strftime("%H:%M")
    current_date = current_datetime.strftime("%d/%m/%y")

    return f"{current_time} - {current_date}"