import pygame
from .paddle import Paddle
from .ball import Ball
import sys
import os

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Default target score (first to this wins)
        self.target_score = 5

        # Entities
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        # Scores
        self.player_score = 0
        self.ai_score = 0

        # Font
        self.font = pygame.font.SysFont("Arial", 30)

        # Try to use ball's loaded sounds (Ball loads them if mixer initialized)
        self.hit_sound = getattr(self.ball, "hit_sound", None)
        self.wall_sound = getattr(self.ball, "wall_sound", None)
        self.score_sound = getattr(self.ball, "score_sound", None)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move ball and check collisions
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Check for scoring (left or right beyond screen)
        # Left side (player missed)
        if self.ball.x + self.ball.width < 0:
            self.ai_score += 1
            if self.score_sound:
                self.score_sound.play()
            self.ball.reset()

        # Right side (ai missed)
        elif self.ball.x > self.width:
            self.player_score += 1
            if self.score_sound:
                self.score_sound.play()
            self.ball.reset()

        # Move AI paddle
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
        if self.player_score >= self.target_score or self.ai_score >= self.target_score:
            if self.player_score >= self.target_score:
                message = "Player Wins!"
            else:
                message = "AI Wins!"

            # Display winner text
            game_over_text = self.font.render(message, True, WHITE)
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 3))

            # Draw final frame and overlay text + options
            self.render(screen)
            screen.blit(game_over_text, text_rect)

            # Display replay options
            small_font = pygame.font.Font(None, 48)
            options_text = [
                small_font.render("Press 3 for Best of 3", True, WHITE),
                small_font.render("Press 5 for Best of 5", True, WHITE),
                small_font.render("Press 7 for Best of 7", True, WHITE),
                small_font.render("Press ESC to Exit", True, WHITE),
            ]

            for i, text in enumerate(options_text):
                rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 60))
                screen.blit(text, rect)

            pygame.display.flip()

            # Wait for user choice
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_3:
                            # Best of 3 => first to 2
                            self.target_score = 2
                            waiting = False
                        elif event.key == pygame.K_5:
                            # Best of 5 => first to 3
                            self.target_score = 3
                            waiting = False
                        elif event.key == pygame.K_7:
                            # Best of 7 => first to 4
                            self.target_score = 4
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

            # Reset game state for replay
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()
            pygame.time.wait(500)  # slight pause before restarting
