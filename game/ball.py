import pygame
import random
import os

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        # position & size
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # screen bounds
        self.screen_width = screen_width
        self.screen_height = screen_height

        # velocities
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # store start coords for resets
        self.start_x = x
        self.start_y = y

        # Sound handles — loaded only if mixer is initialized
        self.hit_sound = None
        self.wall_sound = None
        self.score_sound = None
        if pygame.mixer.get_init():
            try:
                SOUND_DIR = os.path.join(os.path.dirname(__file__), "../sounds")
                self.hit_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "hit.wav"))
                self.wall_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "wall.wav"))
                self.score_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, "score.wav"))
            except Exception:
                # If sounds fail to load, leave them as None (non-fatal)
                self.hit_sound = None
                self.wall_sound = None
                self.score_sound = None

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # wall (top/bottom) bounce
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            if self.wall_sound:
                self.wall_sound.play()
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            if self.wall_sound:
                self.wall_sound.play()

    def check_collision(self, player, ai):
        """
        Robust collision: construct a swept rect from previous to current position
        to avoid tunneling. If collision with a paddle is detected, set the
        ball just outside the paddle and reverse X velocity.
        Play hit sound if available.
        """
        old_x = self.x - self.velocity_x
        old_y = self.y - self.velocity_y

        ball_path = pygame.Rect(
            min(old_x, self.x),
            min(old_y, self.y),
            abs(self.velocity_x) + self.width,
            abs(self.velocity_y) + self.height
        )

        # Player paddle collision
        if ball_path.colliderect(player.rect()):
            # place ball to the right of player paddle
            self.x = player.rect().right
            self.velocity_x = abs(self.velocity_x)
            if self.hit_sound:
                self.hit_sound.play()

        # AI paddle collision
        elif ball_path.colliderect(ai.rect()):
            # place ball to the left of ai paddle
            self.x = ai.rect().left - self.width
            self.velocity_x = -abs(self.velocity_x)
            if self.hit_sound:
                self.hit_sound.play()

    def reset(self):
        """Reset to original center position and flip X velocity (serve)."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        # optional: small pause handled by game engine

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def reset_position(self):
        """Compatibility helper (previous name used in code)."""
        self.reset()
