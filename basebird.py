import pygame
import random
import time

pygame.init()

# window
screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Base Bird")
bg = pygame.image.load("imgs/bg.png")
bg = pygame.transform.scale(bg, (screen_width, screen_height))
floor = pygame.image.load("imgs/base.png")
floor = pygame.transform.scale(floor, (screen_width, 100))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(bg, (0, 0))
    screen.blit(floor, (0, screen_height - 100))

    pygame.display.flip()

pygame.quit()   