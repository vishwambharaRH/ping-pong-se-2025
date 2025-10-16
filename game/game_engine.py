import pygame
from .paddle import Paddle
from .ball import Ball
import time as time
import sys

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
    # When either player reaches 5 points, show game over text
        if self.player_score >= 5 or self.ai_score >= 5:
            # Determine winner message
            if self.player_score >= 5:
                message = "Player Wins!"
            else:
                message = "AI Wins!"

            # Render the message using the same font and color
            game_over_text = self.font.render(message, True, WHITE)
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))

            # Draw everything once more to keep paddles/ball visible behind text
            self.render(screen)

            # Overlay the message
            screen.blit(game_over_text, text_rect)
            pygame.display.flip()

            # Short pause before quitting
            pygame.time.wait(3000)  # 3 seconds
            pygame.quit()
            sys.exit()


