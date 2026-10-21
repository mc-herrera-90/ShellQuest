
import pygame

from shellquest.settings import (
    WIDTH, HEIGHT, BACKGROUND, PANEL,
    GREEN, WHITE, GRAY
)


class MenuScene:
    def __init__(self):
        self.title_font = pygame.font.SysFont("consolas", 56, bold=True)
        self.font = pygame.font.SysFont("consolas", 25)
        self.small_font = pygame.font.SysFont("consolas", 17)

        self.buttons = {
            "play": pygame.Rect(WIDTH // 2 - 130, 300, 260, 58),
            "quit": pygame.Rect(WIDTH // 2 - 130, 380, 260, 58),
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "quit"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.buttons["play"].collidepoint(event.pos):
                return "game"

            if self.buttons["quit"].collidepoint(event.pos):
                return "quit"

        return None

    def draw(self, screen):
        screen.fill(BACKGROUND)

        title = self.title_font.render(
            "SHELLQUEST", True, GREEN
        )
        screen.blit(
            title, title.get_rect(center=(WIDTH // 2, 150))
        )

        subtitle = self.small_font.render(
            "APRENDE LINUX JUGANDO", True, GRAY
        )
        screen.blit(
            subtitle, subtitle.get_rect(center=(WIDTH // 2, 205))
        )

        mouse_pos = pygame.mouse.get_pos()

        for key, label in [
            ("play", "JUGAR"),
            ("quit", "SALIR"),
        ]:
            rect = self.buttons[key]
            hovered = rect.collidepoint(mouse_pos)

            color = PANEL if not hovered else (43, 58, 74)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(
                screen, GREEN if hovered else GRAY,
                rect, width=2, border_radius=10
            )

            text = self.font.render(label, True, WHITE)
            screen.blit(text, text.get_rect(center=rect.center))

        footer = self.small_font.render(
            "Explora. Aprende. Domina la terminal.",
            True, GRAY
        )
        screen.blit(
            footer, footer.get_rect(center=(WIDTH // 2, 540))
        )
