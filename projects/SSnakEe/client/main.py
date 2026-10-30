"""Pygame logs, izvēlne, spēles cilpa. Palaist:
    python -m client.main
"""

import math
import sys
import pygame

pygame.init()

from game.game import Game
from game.constants import (
    GRID_OPTIONS, SPEED_OPTIONS,
    DEFAULT_GRID_SIZE, DEFAULT_SPEED_INDEX,
    INVERT_P1_AD,
    BG_COLOR, GRID_COLOR,
    FOOD_COLOR, FOOD_BORDER,
    MAGNET_COLOR, MAGNET_BORDER,
    P1_BODY, P2_BODY,
)
from game.storage import load_scores, save_score


BASE_SIZE = 750
FPS = 120

MENU_BG = (28, 28, 42)
BUTTON = (60, 60, 90)
BUTTON_HOVER = (95, 95, 145)
GOLD = (255, 200, 50)
TEXT = (240, 240, 240)
GRAY = (140, 140, 155)
LIGHT_GRAY = (185, 185, 195)
GREEN = (0, 200, 90)
RED = (225, 55, 55)

FONT_LARGE = pygame.font.SysFont("Arial", 64, bold=True)
FONT_MED = pygame.font.SysFont("Arial", 32, bold=True)
FONT_SMALL = pygame.font.SysFont("Arial", 24)
FONT_TINY = pygame.font.SysFont("Arial", 18)


class Button:
    def __init__(self, x, y, w, h, text, font=FONT_MED):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font

    def draw(self, surf, mouse_pos, selected=False):
        hover = self.rect.collidepoint(mouse_pos)
        if selected:
            color = GOLD
        elif hover:
            color = BUTTON_HOVER
        else:
            color = BUTTON
        pygame.draw.rect(surf, color, self.rect, border_radius=10)
        pygame.draw.rect(surf, LIGHT_GRAY, self.rect, 2, border_radius=10)
        color_text = (0, 0, 0) if selected else TEXT
        t = self.font.render(self.text, True, color_text)
        surf.blit(t, t.get_rect(center=self.rect.center))


class Client:
    def __init__(self):
        
        self.screen = pygame.display.set_mode((BASE_SIZE, BASE_SIZE))
        pygame.display.set_caption("SsnakEe")
        self.clock = pygame.time.Clock()
        self.state = "MENU"
        self.game = None
        self.mode = 1

        self.grid_size = DEFAULT_GRID_SIZE
        self.multi_food = True
        self.speed_index = DEFAULT_SPEED_INDEX

        cx = BASE_SIZE // 2

        self.btn_1p = Button(cx - 180, 300, 360, 70, "1 Player")
        self.btn_2p = Button(cx - 180, 390, 360, 70, "2 Players (local)")
        self.btn_settings = Button(cx - 180, 480, 360, 70, "Settings")
        self.btn_quit = Button(cx - 180, 570, 360, 70, "Quit")

        self.btn_back = Button(cx - 90, 650, 180, 55, "Back")

        self.speed_buttons = []
        total = 4 * 130 + 3 * 12
        sx = (BASE_SIZE - total) // 2
        for i, (label, _) in enumerate(SPEED_OPTIONS):
            self.speed_buttons.append(
                (i, Button(sx + i * 142, 200, 130, 55, label, FONT_SMALL))
            )

        self.grid_buttons = []
        total = 4 * 120 + 3 * 12
        sx = (BASE_SIZE - total) // 2
        for i, n in enumerate(GRID_OPTIONS):
            self.grid_buttons.append(
                (n, Button(sx + i * 132, 320, 120, 55, f"{n}x{n}", FONT_SMALL))
            )

        self.food_single = Button(cx - 160, 440, 150, 55, "Single", FONT_SMALL)
        self.food_multi = Button(cx + 10, 440, 150, 55, "Multi", FONT_SMALL)

        self.btn_restart = Button(cx - 150, 470, 300, 65, "Restart")
        self.btn_menu = Button(cx - 150, 550, 300, 65, "Main Menu")

        pygame.key.set_repeat(60, 40)
        self.scores = load_scores()

    def start_game(self, mode):
        self.mode = mode
        self.game = Game(
            grid_size=self.grid_size,
            multi_food=self.multi_food,
            speed_index=self.speed_index,
            player_count=mode,
        )
        self.state = "PLAYING"

    def _p1_map(self):
        a_dir = (1, 0) if INVERT_P1_AD else (-1, 0)
        d_dir = (-1, 0) if INVERT_P1_AD else (1, 0)
        return {
            pygame.K_w: (0, -1),
            pygame.K_s: (0, 1),
            pygame.K_a: a_dir,
            pygame.K_d: d_dir,
        }

    def _p2_map(self):
        return {
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
        }

    def handle_click(self, pos):
        if self.state == "MENU":
            if self.btn_1p.rect.collidepoint(pos):
                self.start_game(1)
            elif self.btn_2p.rect.collidepoint(pos):
                self.start_game(2)
            elif self.btn_settings.rect.collidepoint(pos):
                self.state = "SETTINGS"
            elif self.btn_quit.rect.collidepoint(pos):
                pygame.quit()
                sys.exit()

        elif self.state == "SETTINGS":
            for i, b in self.speed_buttons:
                if b.rect.collidepoint(pos):
                    self.speed_index = i
            for n, b in self.grid_buttons:
                if b.rect.collidepoint(pos):
                    self.grid_size = n
            if self.food_single.rect.collidepoint(pos):
                self.multi_food = False
            if self.food_multi.rect.collidepoint(pos):
                self.multi_food = True
            if self.btn_back.rect.collidepoint(pos):
                self.state = "MENU"

        elif self.state == "GAME_OVER":
            if self.btn_restart.rect.collidepoint(pos):
                self.start_game(self.mode)
            elif self.btn_menu.rect.collidepoint(pos):
                self.state = "MENU"

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == "MENU":
                    pygame.quit()
                    sys.exit()
                else:
                    self.state = "MENU"
                    pygame.event.clear(pygame.KEYDOWN)
                return

            if self.state == "PLAYING" and self.game:
                if event.key == pygame.K_p:
                    self.state = "PAUSED"
                    return
                p1 = self._p1_map()
                p2 = self._p2_map()
                if event.key in p1:
                    self.game.set_direction(0, p1[event.key])
                elif self.mode == 2 and event.key in p2:
                    self.game.set_direction(1, p2[event.key])

            elif self.state == "PAUSED":
                if event.key == pygame.K_p:
                    self.state = "PLAYING"

            elif self.state == "GAME_OVER":
                if event.key == pygame.K_r:
                    self.start_game(self.mode)
                elif event.key == pygame.K_m:
                    self.state = "MENU"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_click(event.pos)

    def update(self, dt):
        if self.state == "PLAYING" and self.game:
            self.game.update(dt)
            if self.game.game_over:
                self._on_game_over()

    def _on_game_over(self):
        if self.game.player_count == 1:
            score = self.game.snakes[0].score
        else:
            score = max(s.score for s in self.game.snakes)
        save_score("1p" if self.mode == 1 else "2p", score)
        self.scores = load_scores()
        self.state = "GAME_OVER"

    def draw_menu(self):
        self.screen.fill(MENU_BG)
        title = FONT_LARGE.render("SsnakEe", True, GREEN)
        self.screen.blit(title, title.get_rect(center=(BASE_SIZE // 2, 130)))
        sub = FONT_SMALL.render("Piepildi laukumu. Neieskrien sevī.", True, GRAY)
        self.screen.blit(sub, sub.get_rect(center=(BASE_SIZE // 2, 200)))

        mp = pygame.mouse.get_pos()
        self.btn_1p.draw(self.screen, mp)
        self.btn_2p.draw(self.screen, mp)
        self.btn_settings.draw(self.screen, mp)
        self.btn_quit.draw(self.screen, mp)

        hs1 = FONT_TINY.render(f"1P Highscore: {self.scores.get('1p', 0)}", True, GOLD)
        hs2 = FONT_TINY.render(f"2P Highscore: {self.scores.get('2p', 0)}", True, GOLD)
        self.screen.blit(hs1, (20, BASE_SIZE - 50))
        self.screen.blit(hs2, (20, BASE_SIZE - 25))
        hint = FONT_TINY.render("ESC - quit", True, GRAY)
        self.screen.blit(hint, (BASE_SIZE - hint.get_width() - 15, BASE_SIZE - 25))

    def draw_settings(self):
        self.screen.fill(MENU_BG)
        title = FONT_LARGE.render("Settings", True, TEXT)
        self.screen.blit(title, title.get_rect(center=(BASE_SIZE // 2, 80)))
        mp = pygame.mouse.get_pos()

        lbl = FONT_MED.render("Speed:", True, TEXT)
        self.screen.blit(lbl, lbl.get_rect(center=(BASE_SIZE // 2, 160)))
        for i, b in self.speed_buttons:
            b.draw(self.screen, mp, selected=(i == self.speed_index))

        lbl = FONT_MED.render("Grid Size:", True, TEXT)
        self.screen.blit(lbl, lbl.get_rect(center=(BASE_SIZE // 2, 280)))
        for n, b in self.grid_buttons:
            b.draw(self.screen, mp, selected=(n == self.grid_size))

        lbl = FONT_MED.render("Food:", True, TEXT)
        self.screen.blit(lbl, lbl.get_rect(center=(BASE_SIZE // 2, 400)))
        self.food_single.draw(self.screen, mp, selected=not self.multi_food)
        self.food_multi.draw(self.screen, mp, selected=self.multi_food)

        self.btn_back.draw(self.screen, mp)

    def draw_game(self):
        self.screen.fill(BG_COLOR)
        g = self.game
        cell = BASE_SIZE // g.grid_size

        for i in range(g.grid_size + 1):
            pygame.draw.line(self.screen, GRID_COLOR,
                             (i * cell, 0), (i * cell, BASE_SIZE))
            pygame.draw.line(self.screen, GRID_COLOR,
                             (0, i * cell), (BASE_SIZE, i * cell))

        for f in g.foods:
            rect = pygame.Rect(f.x * cell + 2, f.y * cell + 2, cell - 4, cell - 4)
            pygame.draw.rect(self.screen, FOOD_COLOR, rect, border_radius=6)
            pygame.draw.rect(self.screen, FOOD_BORDER, rect, 2, border_radius=6)

        t = pygame.time.get_ticks() / 1000.0
        for m in g.magnets:
            cx = m.x * cell + cell // 2
            cy = m.y * cell + cell // 2
            pulse = 1.0 + 0.2 * math.sin(t * 8)
            r = max(4, int(cell * 0.38 * pulse))
            pygame.draw.circle(self.screen, MAGNET_COLOR, (cx, cy), r)
            pygame.draw.circle(self.screen, MAGNET_BORDER, (cx, cy), r, 2)
            letter = FONT_SMALL.render("M", True, (255, 255, 255))
            self.screen.blit(letter, letter.get_rect(center=(cx, cy)))

        for s in g.snakes:
            if not s.alive:
                continue
            for i, (sx, sy) in enumerate(s.body):
                rect = pygame.Rect(
                    sx * cell + 1, sy * cell + 1, cell - 2, cell - 2
                )
                if i == 0:
                    pygame.draw.rect(self.screen, s.head_color, rect, border_radius=6)
                    dx, dy = s.direction
                    ex = sx * cell + cell // 2 + dx * cell // 4
                    ey = sy * cell + cell // 2 + dy * cell // 4
                    pygame.draw.circle(
                        self.screen, (0, 0, 0), (ex, ey), max(2, cell // 7)
                    )
                else:
                    pygame.draw.rect(self.screen, s.body_color, rect, border_radius=4)

        self._draw_hud()

    def _draw_hud(self):
        g = self.game
        p1 = g.snakes[0]
        p1_text = FONT_SMALL.render(f"P1: {p1.score}", True, p1.body_color)
        self.screen.blit(p1_text, (12, 8))

        if g.player_count == 2:
            p2 = g.snakes[1]
            p2_text = FONT_SMALL.render(f"P2: {p2.score}", True, p2.body_color)
            self.screen.blit(p2_text, (BASE_SIZE - p2_text.get_width() - 12, 8))

        info = FONT_TINY.render(
            f"Time: {int(g.elapsed)}s  Level: {g.level()}  "
            f"Food: {len(g.foods)}  Speed: {SPEED_OPTIONS[g.speed_index][0]}",
            True, LIGHT_GRAY,
        )
        self.screen.blit(info, info.get_rect(center=(BASE_SIZE // 2, 15)))

        if g.multi_food and g.magnet_spawns < 2:
            m_left = 2 - g.magnet_spawns
            mt = FONT_TINY.render(f"Magnet left: {m_left}", True, MAGNET_COLOR)
            self.screen.blit(mt, (12, BASE_SIZE - 25))

    def draw_paused(self):
        self.draw_game()
        overlay = pygame.Surface((BASE_SIZE, BASE_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        t = FONT_LARGE.render("PAUSED", True, GOLD)
        self.screen.blit(t, t.get_rect(center=(BASE_SIZE // 2, BASE_SIZE // 2 - 40)))
        h = FONT_SMALL.render("P - resume   ESC - menu", True, TEXT)
        self.screen.blit(h, h.get_rect(center=(BASE_SIZE // 2, BASE_SIZE // 2 + 40)))

    def draw_game_over(self):
        self.screen.fill(MENU_BG)
        g = self.game

        if g.won_by_fill:
            t = FONT_LARGE.render("YOU WIN!", True, GOLD)
            self.screen.blit(t, t.get_rect(center=(BASE_SIZE // 2, 110)))
            sub = FONT_SMALL.render("Piepildīji visu laukumu!", True, GREEN)
            self.screen.blit(sub, sub.get_rect(center=(BASE_SIZE // 2, 180)))
        else:
            t = FONT_LARGE.render("Game Over", True, RED)
            self.screen.blit(t, t.get_rect(center=(BASE_SIZE // 2, 110)))

        if self.mode == 1:
            s = g.snakes[0]
            line = f"Score: {s.score}"
            rec = self.scores.get("1p", 0)
        else:
            p1 = g.snakes[0]
            p2 = g.snakes[1]
            line = f"P1: {p1.score}    P2: {p2.score}"
            rec = self.scores.get("2p", 0)
            if g.winner:
                win = FONT_MED.render(f"Winner: {g.winner.name}", True, GOLD)
                self.screen.blit(win, win.get_rect(center=(BASE_SIZE // 2, 260)))

        score_text = FONT_MED.render(line, True, TEXT)
        self.screen.blit(score_text, score_text.get_rect(center=(BASE_SIZE // 2, 340)))

        rec_text = FONT_SMALL.render(f"Highscore: {rec}", True, GOLD)
        self.screen.blit(rec_text, rec_text.get_rect(center=(BASE_SIZE // 2, 400)))

        mp = pygame.mouse.get_pos()
        self.btn_restart.draw(self.screen, mp)
        self.btn_menu.draw(self.screen, mp)

        hint = FONT_TINY.render("R - restart   M - menu", True, GRAY)
        self.screen.blit(hint, hint.get_rect(center=(BASE_SIZE // 2, BASE_SIZE - 30)))

    def draw(self):
        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "SETTINGS":
            self.draw_settings()
        elif self.state == "PLAYING":
            self.draw_game()
        elif self.state == "PAUSED":
            self.draw_paused()
        elif self.state == "GAME_OVER":
            self.draw_game_over()
        pygame.display.flip()

    def run(self):
        pygame.event.clear()
        self.clock.tick(FPS)
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                self.handle_event(event)
            self.update(dt)
            self.draw()


if __name__ == "__main__":
    Client().run()