"""
Note: game is currently under development and is not currently functional as is
Enter the wonderful world of Wendyll the Wizard in his journey to purge the land of evil atrocities.
"""

import pygame
import random
from entities import GameEntity, Player, Enemy, ElementalAttack, Platform, GROUND, collide
from constants import WIDTH, HEIGHT, FPS, ACC, FALL_SPEED, MAX_FALL_SPEED, JUMP_HEIGHT
from helper_functions import load_img
import level_data

# Font initialization
pygame.font.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))


# Set the game name
pygame.display.set_caption("Wizards Save the World")
# Load all art assets

MAIN_SCREEN = load_img("assets/main_screen.png", (WIDTH, HEIGHT))
BG = load_img("assets/fall-bg.png", (WIDTH, HEIGHT))
MENU, PLAYING, PAUSE, GAME_OVER = "menu", "playing", "pause", "game_over"

GROUND_HEIGHT = 100
GROUND_IMG = load_img("assets/soil.png", (WIDTH, GROUND_HEIGHT))


def main_menu():
    title_font = pygame.font.SysFont("gothic", 80)
    window.blit(MAIN_SCREEN, (0, 0))
    title_label = title_font.render("Wizards Save the World", True, (255, 255, 255))
    start_label = title_font.render("Click the mouse to begin...", True, (255, 255, 255))
    window.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, title_label.get_height() / 2))
    window.blit(start_label, (WIDTH / 2 - start_label.get_width() / 2, HEIGHT - start_label.get_height() / 2 - 550))
    pygame.display.update()

def play_game():
    pygame.display.update()

def pause_menu():
    window.fill((50, 50, 50))  # Darker background to signify pause
    font = pygame.font.SysFont("Gothic", 80)
    pause_text = font.render("Paused", True, (255, 255, 255))
    resume_text = font.render("Press P to Resume", True, (255, 255, 255))

    window.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3))
    window.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2))

    pygame.display.update()

def game_over_screen():
    window.fill((100, 0, 0))
    font = pygame.font.SysFont("Gothic", 80)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    restart_text = font.render("Press Enter to Restart", True, (255, 255, 255))

    window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    window.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

    pygame.display.update()

def flip_image(img):
    """Flip sprite across Y plane"""
    return pygame.transform.flip(surface=img, flip_x=True, flip_y=False)


def main():
    global game_state
    running = True
    game_state = MENU

    level = 0
    hearts = 5
    dead_count = 0
    player_vel = 4
    player_attack_vel = 7

    enemies = []
    enemy_vel = 1
    enemy_wave_count = 0

    platforms = []
    new_wave = True

    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("Gothic", 50)
    lost_font = pygame.font.SysFont("Gothic", 75)

    player = Player(WIDTH / 2, HEIGHT - 300)

    def redraw_window():
        window.blit(BG, (0, 0))
        # Drawing the ground, dynamically assigned per resolution
        window.blit(GROUND_IMG, (0, HEIGHT - HEIGHT / 9))
        # Drawing lives_label
        lives_label = main_font.render(f"Hearts: {player.num_hearts}", True, (255, 255, 255))
        window.blit(lives_label, (50, 50))

        # Draw platforms
        for platform in platforms:
            platform.draw(window)

        # Draw enemies
        for enemy in enemies:
            enemy.draw(window)

        if game_state == GAME_OVER:
            lost_label = lost_font.render("You DIED", True, (255, 0, 0))
            window.blit(lost_label, ((WIDTH / 2) - lost_label.get_width() / 2, 350))

        player.draw(window)

        pygame.display.update()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle input based on game state
            if game_state == MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = PLAYING

            elif game_state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_state = PAUSE
                    elif event.key == pygame.K_r:
                        player.change_attack_element()

            elif game_state == PAUSE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    game_state = PLAYING

            elif game_state == GAME_OVER:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = MENU

        # Handle drawing and updating based on game state
        if game_state == MENU:
            main_menu()

        elif game_state == PLAYING:
            if hearts <= 0:
                game_state = GAME_OVER
                dead_count += 1

            # Check if all enemies are defeated to start a new wave
            if len(enemies) == 0:
                level += 1
                enemy_wave_count += 2

                # Spawn new enemies for the next wave
                for _ in range(enemy_wave_count):
                    enemy = Enemy(random.randrange(0, WIDTH), HEIGHT - 125,
                                  random.choice(["bomb", "minotaur", "reaper"]))
                    enemies.append(enemy)

                # Set the flag to true to generate new platforms
                new_wave = True

            # Generate new platforms at the start of each wave
            if new_wave:
                platforms = level_data.generate_platforms()  # Clear old platforms and generate new ones
                new_wave = False  # Prevent further generation until next wave

            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player.x - player_vel > 0:  # left
                player.x -= player_vel
            if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
                player.x += player_vel
            if keys[pygame.K_w]:  # up
                player.jump()
            if keys[pygame.K_SPACE]:
                player.attack()

            # Apply gravity and check for platform collisions
            player.gravity(platforms)

            # Move and update enemies
            for enemy in enemies:
                enemy.move(enemy_vel)

                if collide(enemy, player):
                    player.health -= 1
                    enemies.remove(enemy)

            player.move_attacks(player_attack_vel, enemies)

            redraw_window()

        elif game_state == PAUSE:
            pause_menu()

        elif game_state == GAME_OVER:
            game_over_screen()

    pygame.quit()


if __name__ == "__main__":
    main()
