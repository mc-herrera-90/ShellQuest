
import pygame

from shellquest.settings import (
    WIDTH, HEIGHT, BACKGROUND, PANEL, GREEN, WHITE, GRAY, BLUE
)
from shellquest.entities.player import Player
from shellquest.systems.terminal import TerminalUI


class GameScene:
    def __init__(self):
        self.font = pygame.font.SysFont("consolas", 22)
        self.small_font = pygame.font.SysFont("consolas", 15)
        self.title_font = pygame.font.SysFont("consolas", 25, bold=True)

        # Mapa a la izquierda
        self.world = pygame.Rect(20, 110, 570, 570)

        # Terminal visible a la derecha
        self.terminal = TerminalUI((610, 110, WIDTH - 630, 570))

        # Jerarquia del sistema de archivos.
        # Las coordenadas son relativas a la pantalla.
        self.folders = [
            {"name": "/", "path": "/", "parent": None,
             "rect": pygame.Rect(230, 140, 140, 50)},

            {"name": "home", "path": "/home", "parent": "/",
             "rect": pygame.Rect(230, 245, 140, 50)},

            {"name": "player", "path": "/home/player", "parent": "/home",
             "rect": pygame.Rect(230, 350, 140, 50)},

            {"name": "documents", "path": "/home/player/documents",
             "parent": "/home/player",
             "rect": pygame.Rect(45, 485, 150, 55)},

            {"name": "downloads", "path": "/home/player/downloads",
             "parent": "/home/player",
             "rect": pygame.Rect(225, 485, 150, 55)},

            {"name": "missions", "path": "/home/player/missions",
             "parent": "/home/player",
             "rect": pygame.Rect(405, 485, 150, 55)},
        ]

        # Empezamos en la raiz
        self.current_path = "/"
        self.player = Player(280, 155)
        self.completed = False

        self.message = "Llega a /home/player/missions"
        self.history = []

    def handle_event(self, event):
        # Los eventos del teclado se envian primero a la terminal.
        command = self.terminal.handle_event(event)

        if command:
            self.run_command(command)

        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
            and not self.terminal.active
        ):
            return "menu"

        return None

    def run_command(self, command):
        parts = command.strip().split()

        if not parts:
            return

        if parts[0] == "pwd":
            self.terminal.add_output(self.current_path)
            return

        if parts[0] == "ls":
            children = [
                folder["name"]
                for folder in self.folders
                if folder["parent"] == self.current_path
            ]

            self.terminal.add_output(
                "  ".join(children) if children else "(directorio vacio)"
            )
            return

        if parts[0] == "cd":
            if len(parts) < 2:
                self.terminal.add_output("Uso: cd <directorio>")
                return

            target = parts[1]

            if target == "/":
                new_path = "/"
            elif target == "..":
                if self.current_path == "/":
                    new_path = "/"
                else:
                    new_path = self.current_path.rsplit("/", 1)[0] or "/"
            elif target.startswith("/"):
                new_path = target.rstrip("/") or "/"
            else:
                new_path = (
                    self.current_path.rstrip("/") + "/" + target
                )

            valid_paths = {folder["path"] for folder in self.folders}

            if new_path not in valid_paths:
                self.terminal.add_output(
                    f"cd: no existe el directorio: {target}"
                )
                return

            self.current_path = new_path
            self.terminal.add_output(f"Directorio actual: {new_path}")

            # Mover el personaje a la carpeta seleccionada
            target_folder = next(
                folder for folder in self.folders
                if folder["path"] == new_path
            )

            self.player.rect.center = target_folder["rect"].center

            if new_path == "/home/player/missions":
                self.completed = True
                self.message = "¡MISION COMPLETADA!"
                self.terminal.add_output(
                    "¡Excelente! Has llegado a missions."
                )
            else:
                self.message = f"Ubicacion actual: {new_path}"

            return

        if parts[0] == "help":
            self.terminal.add_output("Comandos: pwd, ls, cd, help")
            return

        self.terminal.add_output(
            f"{parts[0]}: comando no encontrado"
        )

    def update(self):
        # El personaje se mueve por el mapa cuando la terminal
        # no esta activa.
        if not self.terminal.active and not self.completed:
            keys = pygame.key.get_pressed()
            self.player.update(keys, self.world)

            # La posicion del jugador actualiza la carpeta seleccionada
            for folder in self.folders:
                if self.player.rect.colliderect(folder["rect"]):
                    self.current_path = folder["path"]
                    self.message = f"Ubicacion actual: {self.current_path}"

                    if self.current_path == "/home/player/missions":
                        self.completed = True
                        self.message = "¡MISION COMPLETADA!"
                        self.terminal.add_output(
                            "¡Has encontrado la carpeta missions!"
                        )
                    break

    def draw_connections(self, screen):
        by_path = {folder["path"]: folder for folder in self.folders}

        for folder in self.folders:
            parent_path = folder["parent"]

            if parent_path is None:
                continue

            parent = by_path[parent_path]["rect"]
            child = folder["rect"]

            start = (parent.centerx, parent.bottom)
            end = (child.centerx, child.top)
            middle_y = (start[1] + end[1]) // 2

            pygame.draw.lines(
                screen,
                (75, 88, 107),
                False,
                [start, (start[0], middle_y),
                 (end[0], middle_y), end],
                3,
            )

    def draw_folder(self, screen, folder):
        rect = folder["rect"]
        path = folder["path"]

        if path == self.current_path:
            fill = (27, 100, 65)
            border = GREEN
        elif path == "/home/player/missions":
            fill = (68, 57, 30)
            border = (255, 196, 75)
        else:
            fill = (38, 48, 63)
            border = (105, 130, 160)

        pygame.draw.rect(screen, fill, rect, border_radius=8)
        pygame.draw.rect(screen, border, rect, 2, border_radius=8)

        # Pestaña de carpeta dibujada con geometria
        tab = pygame.Rect(rect.x + 10, rect.y - 7, 45, 10)
        pygame.draw.rect(screen, border, tab, border_radius=3)

        label = self.small_font.render(folder["name"], True, WHITE)
        screen.blit(label, label.get_rect(center=rect.center))

    def draw(self, screen):
        screen.fill(BACKGROUND)

        title = self.title_font.render(
            "NIVEL 1: EXPLORA EL SISTEMA DE ARCHIVOS",
            True, GREEN
        )
        screen.blit(title, (20, 25))

        hint = self.small_font.render(self.message, True, WHITE)
        screen.blit(hint, (20, 70))

        # Mapa
        pygame.draw.rect(screen, PANEL, self.world, border_radius=10)
        pygame.draw.rect(screen, GRAY, self.world, 2, border_radius=10)

        self.draw_connections(screen)

        for folder in self.folders:
            self.draw_folder(screen, folder)

        self.player.draw(screen)

        # Terminal siempre visible a la derecha
        self.terminal.draw(screen)
