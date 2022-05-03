"""
Note: game is currently under development and is not currently functional as is
Enter the wonderful world of Wendyll the Wizard in his journey to purge the land of evil atrocities.
"""

import pygame
import random

# Font initialization
pygame.font.init()

# Set game window size
WIDTH, HEIGHT = 800, 800
FPS = 60
ACC = 0.5
window = pygame.display.set_mode((WIDTH, HEIGHT))
# Set the game name
pygame.display.set_caption("Wizards Save the World")
# Load all art assets
WIZARD = pygame.transform.scale(pygame.image.load("assets/wizard.png"), (WIDTH / 16, HEIGHT / 16))
BOMB_ENEMY = pygame.image.load("assets/enemy_bomb.png")
REAPER_ENEMY = pygame.image.load("assets/grim-reaper.png")
MINOTAUR_ENEMY = pygame.image.load("assets/minotaur.png")
GROUND = pygame.transform.scale(pygame.image.load("assets/soil.png"), (WIDTH, HEIGHT / 8))
FIRE = pygame.image.load("assets/fire.png")
LIGHTNING = pygame.image.load("assets/lightning.png")
WATER = pygame.image.load("assets/wave.png")
HEART = pygame.image.load("assets/heart.png")
MAIN_SCREEN = pygame.transform.scale(pygame.image.load("assets/main_screen.png"), (WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load("assets/fall-bg.png"), (WIDTH, HEIGHT))


def main_menu():
    title_font = pygame.font.SysFont("gothic", 80)
    running = True
    while running:
        # Place the background on the screen
        window.blit(MAIN_SCREEN, (0, 0))
        # Set up start screen
        title_label = title_font.render("Wizards Save the World", 1, (255, 255, 255))
        start_label = title_font.render("Click the mouse to begin...", 1, (255, 255, 255))
        window.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, title_label.get_height() / 2))
        window.blit(start_label, (WIDTH / 2 - start_label.get_width() / 2, HEIGHT - start_label.get_height() / 2 - 550))

        pygame.display.update()

        # Loop for starting or quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Change the game window from the title screen and call main
                window.blit(BG, (0, 0))
                main()

    pygame.quit()


class GameEntity:
    # 0.5 second cooldown
    COOLDOWN = 30

    def __init__(self, x, y, health=5):
        self.x = x
        self.y = y
        self.health = health
        self.image = None
        self.attack_img = None
        self.attacks = []
        # Limit on how fast shots can be fired
        self.cool_down_counter = 0

    # update on window, called win to avoid having 2 variables named windows
    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        for attack in self.attacks:
            attack.draw(win)

    def move_attacks(self, vel, obj):
        self.cooldown()
        for attack in self.attacks:
            attack.move(vel)
            if attack.off_screen(HEIGHT) or attack.off_screen(WIDTH):
                self.attacks.remove(attack)
            elif attack.collision(obj):
                obj.health -= 1
                self.attacks.remove(attack)

    def get_height(self):
        return self.image.get_height()

    def get_width(self):
        return self.image.get_width()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1


class Player(GameEntity):
    def __init__(self, x, y, health=5):
        super().__init__(x, y, health)
        self.image = WIZARD
        # Add list and add lightning and fire attacks
        self.attack_image = WATER
        self.num_hearts = health
        # Mask allows for better pixel collision (no more rectangular collision)
        self.mask = pygame.mask.from_surface(self.image)
        self.attack_type = ['fire', 'water', 'lightning']
        self.is_jumping = False
        self.is_falling = False

    # the hearts feature is currently not working here
    def draw(self, win):
        super().draw(window)
        # self.num_hearts(window)
        # Try adding jump methods here

    def attack(self):
        if self.cool_down_counter == 0:
            attack = ElementalAttack(self.x, self.y, self.attack_img)
            self.attacks.append(attack)
            self.cool_down_counter = 1

    def move_attacks(self, vel, objs):
        # Check against cooldown to see if wizard can fire an attack
        self.cooldown()
        for attack in self.attacks:
            attack.move(vel)
            if attack.off_screen(WIDTH):
                self.attacks.remove(attack)
            else:
                for obj in objs:
                    if attack.collision(obj):
                        objs.remove(obj)
                        if attack in self.attacks:
                            self.attacks.remove(attack)

    # add more code to add more hearts and make adjustable
    def health_bar(self, win):
        offset = 25  # Number of pixels to separate each heart by
        for heart, offset in enumerate(self.num_hearts):
            x, y = 50, 50
            x += offset
            pygame.blit(HEART, win, (x + offset, y))

    def jump(self):
        if self.is_jumping is False:
            self.is_falling = False
            self.is_jumping = True
            if self.is_jumping:
                self.y -= 20

    def gravity(self):
        if self.is_jumping:
            self.y += 3


class Enemy(GameEntity):
    def __init__(self, x, y, enemy_type, health=5):
        super().__init__(x, y, health)

        enemy_map = {
            "bomb": BOMB_ENEMY,
            "minotaur": MINOTAUR_ENEMY,
            "reaper": REAPER_ENEMY,
        }

        self.image = enemy_map[enemy_type]
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, vel):
        self.x += vel

    def attack(self):
        pass


class ElementalAttack:
    def __init__(self, x, y, element, image):

        elemental_type_map = {
            "lightning": LIGHTNING,
            "water": WATER,
            "fire": FIRE,
        }

        self.x = x
        self.y = y
        self.elemental_type = elemental_type_map[element]
        self.image = image
        # Mask makes collision with the object match the image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    #  TODO: Figure out how to set angle attack is fired at
    def move(self, vel):
        self.x += vel

    def collision(self, obj):
        return collide(self, obj)

    def off_screen(self, width):
        # if off-screen - True, if on screen - False
        return not (width >= self.x >= 0)


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.x
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    running = True
    dead = False
    # player_jumping = False
    level = 0
    hearts = 5
    dead_count = 0

    enemies = []
    enemy_vel = 2
    enemy_wave_count = 0

    player_vel = 4
    player_attack_vel = 7

    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("Gothic", 50)
    lost_font = pygame.font.SysFont("Gothic", 75)

    player = Player(WIDTH / 2, HEIGHT - 125)

    def redraw_window():
        # Drawing the window at 0,0 (top left)
        window.blit(BG, (0, 0))
        # Drawing the ground, dynamically assigned per resolution
        window.blit(GROUND, (0, HEIGHT - HEIGHT / 9))
        # Drawing lives_label
        lives_label = main_font.render(f"Hearts: {player.num_hearts}", 1, (255, 255, 255))
        window.blit(lives_label, (50, 50))
        # taking the enemies list and drawing those enemies on the window
        for enemy in enemies:
            enemy.draw(window)

        if dead:
            lost_label = lost_font.render("You DIED", 1, (255, 0, 0))
            window.blit(lost_label, ((WIDTH / 2) - lost_label.get_width() / 2, 350))

        player.draw(window)

        pygame.display.update()

    while running:
        # Check and refresh everything at 60FPS
        clock.tick(FPS)

        if hearts <= 0:
            dead = True
            dead_count += 1

        if dead:
            # If the dead timer is up for over 5 seconds
            if dead_count > FPS * 5:
                running = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            enemy_wave_count += 2
            for _ in range(enemy_wave_count):
                enemy = Enemy(random.randrange(WIDTH, WIDTH + 300), HEIGHT,
                              random.choice(["bomb", "minotaur", "reaper"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Returns a dictionary of the keys and tells if they are pressed
        keys = pygame.key.get_pressed()
        # key assignment
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.jump()

        if keys[pygame.K_SPACE]:
            player.attack()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            if collide(enemy, player):
                player.health -= 1
                # enemy dies if they collide with player
                # should probably add a collision timer and not kill the enemy
                enemies.remove(enemy)

        player.move_attacks(player_attack_vel, enemies)

        redraw_window()


if __name__ == "__main__":
    main_menu()
