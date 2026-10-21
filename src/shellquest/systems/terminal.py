
import pygame

from shellquest.settings import GREEN, WHITE


class TerminalUI:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)

        # Paleta visual
        self.background = (17, 19, 24)
        self.titlebar = (41, 43, 50)
        self.border = (58, 62, 72)
        self.text_color = (225, 228, 236)
        self.muted = (139, 145, 158)
        self.green = (114, 229, 162)
        self.blue = (133, 191, 255)
        self.input_bg = (27, 32, 40)

        self.title_font = pygame.font.SysFont(
            "menlo", 13
        )
        self.font = pygame.font.SysFont(
            "menlo", 14
        )
        self.small_font = pygame.font.SysFont(
            "menlo", 11
        )

        self.active = False
        self.command = ""
        self.scroll = 0

        self.history = [
            ("system", "SHELLQUEST TERMINAL"),
            ("system", "Sesion de aprendizaje iniciada."),
            ("system", "Escribe help para ver los comandos."),
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

            if event.button == 4 and self.active:
                self.scroll = min(
                    self.scroll + 3,
                    len(self.history)
                )

            elif event.button == 5 and self.active:
                self.scroll = max(0, self.scroll - 3)

        if not self.active or event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_RETURN:
            command = self.command.strip()
            self.command = ""

            if command:
                self.history.append(("input", command))
                self.scroll = 0
                return command

        elif event.key == pygame.K_BACKSPACE:
            self.command = self.command[:-1]

        elif event.key == pygame.K_ESCAPE:
            self.active = False

        elif event.key == pygame.K_UP:
            self.scroll = min(
                self.scroll + 1,
                len(self.history)
            )

        elif event.key == pygame.K_DOWN:
            self.scroll = max(0, self.scroll - 1)

        elif event.unicode.isprintable():
            self.command += event.unicode

        return None

    def add_output(self, text):
        for line in str(text).splitlines() or [""]:
            self.history.append(("output", line))

        self.scroll = 0

    def draw(self, screen):
        r = self.rect

        # Sombra exterior
        shadow = r.move(0, 5)
        pygame.draw.rect(
            screen,
            (10, 11, 15),
            shadow,
            border_radius=12,
        )

        # Cuerpo de la terminal
        pygame.draw.rect(
            screen,
            self.background,
            r,
            border_radius=12,
        )

        # Barra superior
        bar = pygame.Rect(r.x, r.y, r.width, 42)
        pygame.draw.rect(
            screen,
            self.titlebar,
            bar,
            border_top_left_radius=12,
            border_top_right_radius=12,
        )

        # Botones de ventana macOS
        buttons = [
            (255, 95, 87),
            (254, 188, 46),
            (40, 200, 64),
        ]

        for i, color in enumerate(buttons):
            pos = (r.x + 18 + i * 20, r.y + 21)
            pygame.draw.circle(screen, color, pos, 6)

        # Titulo centrado
        title = self.title_font.render(
            "Terminal — zsh",
            True,
            (218, 220, 228),
        )

        screen.blit(
            title,
            title.get_rect(
                center=(r.centerx, r.y + 21)
            ),
        )

        # Borde exterior
        pygame.draw.rect(
            screen,
            self.green if self.active else self.border,
            r,
            width=1,
            border_radius=12,
        )

        # Historial: solo se dibuja dentro de su zona
        content = pygame.Rect(
            r.x + 14,
            r.y + 55,
            r.width - 28,
            r.height - 112,
        )

        screen.set_clip(content)

        line_height = 22
        lines = []

        for kind, message in self.history:
            if kind == "input":
                lines.append(("prompt", "player@quest:~$ "))
                lines.append(("input", message))
            else:
                lines.append((kind, message))

        visible_count = max(
            1, content.height // line_height
        )

        end = max(0, len(lines) - self.scroll)
        start = max(0, end - visible_count)
        visible = lines[start:end]

        y = content.y

        for kind, message in visible:
            if kind == "prompt":
                color = self.green
            elif kind == "input":
                color = self.text_color
            elif kind == "system":
                color = self.muted
            elif kind == "directory":
                color = self.blue
            else:
                color = self.text_color

            # Ajuste de texto para no salir de la ventana
            words = message.split(" ")
            current_line = ""

            for word in words:
                candidate = (
                    word if not current_line
                    else current_line + " " + word
                )

                if (
                    self.font.size(candidate)[0] > content.width
                    and current_line
                ):
                    rendered = self.font.render(
                        current_line, True, color
                    )
                    screen.blit(rendered, (content.x, y))
                    y += line_height
                    current_line = word
                else:
                    current_line = candidate

            rendered = self.font.render(
                current_line, True, color
            )
            screen.blit(rendered, (content.x, y))
            y += line_height

        screen.set_clip(None)

        # Separador superior de la entrada
        input_y = r.bottom - 49

        pygame.draw.line(
            screen,
            self.border,
            (r.x + 12, input_y),
            (r.right - 12, input_y),
            1,
        )

        # Prompt y comando actual
        prompt = "player@quest:~$ "
        prompt_surface = self.font.render(
            prompt, True, self.green
        )

        command_surface = self.font.render(
            self.command, True, self.text_color
        )

        x = r.x + 14
        y = r.bottom - 35

        screen.blit(prompt_surface, (x, y))
        x += prompt_surface.get_width()

        # Evitar que la entrada desborde por la derecha
        max_width = r.right - x - 12
        if command_surface.get_width() > max_width:
            self.command = self.command[-max(1, len(self.command) - 1):]
            command_surface = self.font.render(
                self.command, True, self.text_color
            )

        screen.blit(command_surface, (x, y))

        # Cursor
        cursor_x = x + command_surface.get_width()
        if self.active and (pygame.time.get_ticks() // 500) % 2 == 0:
            pygame.draw.line(
                screen,
                self.green,
                (cursor_x + 2, y + 2),
                (cursor_x + 2, y + 17),
                2,
            )
