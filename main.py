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
FALL_SPEED = 1
MAX_FALL_SPEED = 20
JUMP_HEIGHT = 75

MENU, PLAYING, PAUSE, GAME_OVER = "menu", "playing", "pause", "game_over"

window = pygame.display.set_mode((WIDTH, HEIGHT))



# Set the game name
pygame.display.set_caption("Wizards Save the World")
# Load all art assets
def load_img(path, size=None):
    try:
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as err:
        print(f"Error loading image {path}: {err}")

WIZARD = load_img("assets/wizard.png", (WIDTH / 16, HEIGHT / 16))
BOMB_ENEMY = load_img("assets/enemy_bomb.png", (WIDTH / 16, HEIGHT / 16))
REAPER_ENEMY = load_img("assets/grim-reaper.png", (WIDTH / 16, HEIGHT / 16))
MINOTAUR_ENEMY = load_img("assets/minotaur.png", (WIDTH / 16, HEIGHT / 16))
GROUND = load_img("assets/soil.png", (WIDTH / 16, HEIGHT / 16))
FIRE = load_img("assets/fire.png", (WIDTH / 16, HEIGHT / 16))
LIGHTNING = load_img("assets/lightning.png", (WIDTH / 16, HEIGHT / 16))
WATER = load_img("assets/wave.png", (WIDTH / 16, HEIGHT / 16))
HEART = load_img("assets/heart.png", (WIDTH, HEIGHT))
MAIN_SCREEN = load_img("assets/main_screen.png", (WIDTH, HEIGHT))
BG = load_img("assets/fall-bg.png", (WIDTH, HEIGHT))


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

class GameEntity:
    COOLDOWN = 60  # 1 second cooldown - 60/60FPS = 1 sec

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
        self.attack_img = LIGHTNING
        self.num_hearts = health
        # Mask allows for better pixel collision (no more rectangular collision)
        self.mask = pygame.mask.from_surface(self.image)
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
        x, y = 50, 50
        for heart in range(self.num_hearts):
            win.blit(HEART, (x + num_hearts * 25, y))

    def jump(self):
        # Can only jump when not currently jumping
        if not self.is_jumping and not self.is_falling:
            self.is_falling = True
            self.is_jumping = True
            if self.is_jumping:
                self.y -= JUMP_HEIGHT

    def gravity(self):
        if self.is_falling:
            self.y += FALL_SPEED

        if self.y >= HEIGHT - 125:
            # Hit the ground
            self.y = HEIGHT - 125
            self.is_falling, self.is_jumping = False, False
        else:
            self.is_falling = True


    def change_attack_element(self):
        if self.attack_img == LIGHTNING:
            self.attack_img = WATER
        elif self.attack_img == WATER:
            self.attack_img = FIRE
        else:
            self.attack_img = LIGHTNING



class ElementalAttack:
    # TODO: Add elemental attacks affecting certain enemy types more than others
    def __init__(self, x, y, attack_img):
        # elemental_attacks = [
        #     LIGHTNING,
        #     FIRE,
        #     WATER,
        # ]
        self.x = x
        self.y = y
        self.attack_img = attack_img
        # Mask makes collision with the object match the image
        self.mask = pygame.mask.from_surface(self.attack_img)

    def draw(self, win):
        win.blit(self.attack_img, (self.x, self.y))

    #  TODO: Figure out how to set angle attack is fired at
    def move(self, vel):
        self.x += vel

    def collision(self, obj):
        return collide(self, obj)

    def off_screen(self, width):
        # if off-screen - True, if on screen - False
        return not (width >= self.x >= 0)


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


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


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
        lives_label = main_font.render(f"Hearts: {player.num_hearts}", True, (255, 255, 255))
        window.blit(lives_label, (50, 50))

        # take the enemies list and draw/update those enemies on the window
        for enemy in enemies:
            enemy.draw(window)

        if game_state == GAME_OVER:
            lost_label = lost_font.render("You DIED", True, (255, 0, 0))
            window.blit(lost_label, ((WIDTH / 2) - lost_label.get_width() / 2, 350))

        player.draw(window)

        pygame.display.update()


    while running:
        # Check and refresh everything at 60FPS
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

            if len(enemies) == 0:
                level += 1
                enemy_wave_count += 2
                for _ in range(enemy_wave_count):
                    enemy = Enemy(random.randrange(0, WIDTH), HEIGHT-125,
                                  random.choice(["bomb", "minotaur", "reaper"]))
                    enemies.append(enemy)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player.x - player_vel > 0:  # left
                player.x -= player_vel
            if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
                player.x += player_vel
            if keys[pygame.K_w]:  # up
                player.jump()
            if keys[pygame.K_SPACE]:
                player.attack()

            player.gravity()

            for enemy in enemies[:]:
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
