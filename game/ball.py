import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1

    def check_collision(self, player, ai):
    # Store old position before movement
        old_x = self.x - self.velocity_x
        old_y = self.y - self.velocity_y

        # Create line segments for ball motion
        ball_path = pygame.Rect(min(old_x, self.x), min(old_y, self.y),
                                abs(self.velocity_x) + self.width,
                                abs(self.velocity_y) + self.height)

        # Check if the motion path intersects a paddle
        if ball_path.colliderect(player.rect()):
            self.x = player.rect().right  # place ball just outside paddle
            self.velocity_x = abs(self.velocity_x)
        elif ball_path.colliderect(ai.rect()):
            self.x = ai.rect().left - self.width
            self.velocity_x = -abs(self.velocity_x)

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
