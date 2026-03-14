import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.const import WIN_WIDTH, C_ORANGE, MENU_OPTION, C_WHITE


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load("./asset/MenuIBG.png").convert_alpha()
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self, menu_option=0):
        pygame.mixer.init()  # correção pequena
        pygame.mixer.music.load("./asset/menu.mp3")
        pygame.mixer.music.play(-1)

        while True:
            self.window.blit(source=self.surf, dest=self.rect)

            self.menu_text(
                50, "Mountain",
                text_color=C_WHITE,
                text_center_pos=((WIN_WIDTH / 2), 70)
            )
            self.menu_text(
                50, "Shooter",
                text_color=C_WHITE,
                text_center_pos=((WIN_WIDTH / 2), 120)
            )

            for i in range(len(MENU_OPTION)):
                if i == menu_option:
                    self.menu_text(20, MENU_OPTION[i], C_ORANGE, ((WIN_WIDTH / 2), 200 + 25 * i))
                else:
                    self.menu_text(20, MENU_OPTION[i], C_WHITE, ((WIN_WIDTH / 2), 200 + 25 * i))

            pygame.display.flip()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_DOWN:
                        if menu_option < len(MENU_OPTION) - 1:
                            menu_option += 1
                        else:
                            menu_option = 0

                    if ev.key == pygame.K_UP:
                        if menu_option > 0:
                            menu_option -= 1
                        else:
                            menu_option = len(MENU_OPTION) - 1
                    if ev.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
