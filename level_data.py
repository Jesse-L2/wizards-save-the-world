import random
from entities import Platform
import pygame

WIDTH, HEIGHT = 800, 800

def generate_platforms():
    platforms = []
    max_platforms = 6
    platform_width = 150  # Example width of a platform
    platform_height = 20  # Example height of a platform
    max_attempts = 100  # Limit the number of attempts to place a platform

    for _ in range(max_platforms):
        valid_position = False
        attempts = 0

        while not valid_position and attempts < max_attempts:
            # Generate random position for the platform
            x = random.randint(0, WIDTH - platform_width)
            y = random.randint(100, HEIGHT - 150)  # Random y position, avoiding the bottom ground area

            new_platform_rect = pygame.Rect(x, y, platform_width, platform_height)

            # Check if the new platform overlaps with any existing platforms
            overlap = False
            for platform in platforms:
                existing_platform_rect = pygame.Rect(platform.x, platform.y, platform.w, platform.h)
                if new_platform_rect.colliderect(existing_platform_rect):
                    overlap = True
                    break

            if not overlap:
                valid_position = True
                platforms.append(Platform(x, y, platform_width, platform_height))

            attempts += 1

    return platforms
