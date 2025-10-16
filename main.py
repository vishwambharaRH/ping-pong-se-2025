import pygame
from game.game_engine import GameEngine
import sys

# Initialize pygame/Start application
pygame.init()

# Initialize mixer (before creating GameEngine/ball so sounds can load)
try:
    pygame.mixer.init()
except Exception:
    # If mixer init fails (no audio device), continue without sound
    pass

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop setup
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)
        engine.check_game_over(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    # Quit cleanly
    try:
        pygame.mixer.quit()
    except Exception:
        pass
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
