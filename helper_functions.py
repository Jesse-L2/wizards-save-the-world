import pygame

def load_img(path, size=None):
    try:
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as err:
        print(f"Error loading image {path}: {err}")