import random
import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player
from code.const import C_WHITE, WIN_HEIGHT, MENU_OPTION, EVENT_ENEMY, SPAWN_TIME, C_GREEN, C_CIAN


class Level:
    def __init__(self, window, name, game_mode):
        self.timeout = 60000
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.entity_list.extend(EntityFactory.get_entity('Level1Bg'))
        self.entity_list.append(EntityFactory.get_entity('Player1'))
        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            self.entity_list.append(EntityFactory.get_entity('Player2'))
        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)

    def run(self):
        pygame.mixer.music.load('./asset/Level1.mp3')
        pygame.mixer.music.play(-1)
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if ev.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))

            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()
                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

                if ent.name == 'Player1':
                    self.level_text(text_size=14,
                                    text=f'Player 1 - Health:{ent.health} | Score: {ent.score} ',
                                    text_color=C_CIAN, text_pos=(10, 25))

                if ent.name == 'Player2':
                    self.level_text(text_size=14,
                                    text=f'Player 2 - Health:{ent.health} | Score: {ent.score} ',
                                    text_color=C_GREEN, text_pos=(10, 45))

            self.level_text(
                text_size=14,
                text=f'{self.name} - Timeout: {self.timeout / 1000:.1f}s',
                text_color=C_WHITE,
                text_pos=(10, 5)
            )

            self.level_text(
                text_size=14,
                text=f'FPS: {clock.get_fps():.0f}',
                text_color=C_WHITE,
                text_pos=(10, WIN_HEIGHT - 35)
            )

            self.level_text(
                text_size=14,
                text=f'Entidades: {len(self.entity_list)}',
                text_color=C_WHITE,
                text_pos=(10, WIN_HEIGHT - 20)
            )

            pygame.display.flip()

            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)
            pass

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(source=text_surf, dest=text_rect)
