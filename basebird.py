import pygame
import random
import time

pygame.init()

fps = pygame.time.Clock()

# window
screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Base Bird")
bg = pygame.image.load("imgs/bg.png")
bg = pygame.transform.scale(bg, (screen_width, screen_height))
floor = pygame.image.load("imgs/base.png")
floor = pygame.transform.scale(floor, (screen_width, 100))

# physics
flap = -10
gravity = 1
velocity = 0

# classes
class Bird:
    def __init__(self):
        self.image = pygame.image.load("imgs/bird2.png")
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.velocity = 0

    def update(self, gravity):
        self.velocity += gravity
        self.y += self.velocity
        self.rect.center = (self.x, self.y)

# main loop
running = True
game_live = False
game_over = False
score = 0

bird = Bird()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.velocity = flap
                if not game_live:
                    game_live = True

    screen.blit(bg, (0, 0))
    screen.blit(floor, (0, screen_height - 100))
        
    if game_live and not game_over:
        bird.update(gravity)

    screen.blit(bird.image, bird.rect)

    fps.tick(60)

    pygame.display.flip()

pygame.quit()   