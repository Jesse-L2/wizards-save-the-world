import pygame
import random
from constants import *
from helper_functions import load_img


WIZARD = load_img("assets/wizard.png", (WIDTH / 16, HEIGHT / 16))
BOMB_ENEMY = load_img("assets/enemy_bomb.png", (WIDTH / 16, HEIGHT / 16))
REAPER_ENEMY = load_img("assets/grim-reaper.png", (WIDTH / 16, HEIGHT / 16))
MINOTAUR_ENEMY = load_img("assets/minotaur.png", (WIDTH / 16, HEIGHT / 16))
GROUND = load_img("assets/soil.png", (WIDTH / 16, HEIGHT / 16))
FIRE = load_img("assets/fire.png", (WIDTH / 16, HEIGHT / 16))
LIGHTNING = load_img("assets/lightning.png", (WIDTH / 16, HEIGHT / 16))
WATER = load_img("assets/wave.png", (WIDTH / 16, HEIGHT / 16))
HEART = load_img("assets/heart.png", (WIDTH, HEIGHT))

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
        super().draw(win)
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
        self.vel = random.choice([1, -1])

    def move(self, vel):
        self.x += self.vel

        # Check if the enemy hits the left or right edge of the screen
        if self.x <= 0 or self.x +self.get_width() >WIDTH:
            self.vel = -self.vel
            # Flip the image to turn the enemy sprite around
            self.image = flip_image(self.image)


    def attack(self):
        pass


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.transform.scale(GROUND, (self.w, self.h))

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def flip_image(img):
    return pygame.transform.flip(img, True, False)
