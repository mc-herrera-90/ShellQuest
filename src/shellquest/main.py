
import pygame

from shellquest.settings import WIDTH, HEIGHT, TITLE, FPS
from shellquest.scenes.menu import MenuScene
from shellquest.scenes.game import GameScene


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    current_scene = "menu"
    scenes = {
        "menu": MenuScene(),
        "game": GameScene(),
    }

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            result = scenes[current_scene].handle_event(event)

            if result == "quit":
                running = False
                break

            if result in scenes and result != current_scene:
                current_scene = result

        if not running:
            break

        scene = scenes[current_scene]

        if hasattr(scene, "update"):
            scene.update()

        scene.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
