import pygame
import random
import time

pygame.init()

fps = pygame.time.Clock()

# music + sound effects
"""
Music: Tobu & Itro - Sunburst
http://youtube.com/tobuofficial
https://www.youtube.com/user/officialitro
Released by NCS https://www.youtube.com/NoCopyrightSounds
"""
pygame.mixer.music.load("audio/Tobu & Itro - Sunburst.mp3") 
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)
flappy = pygame.mixer.Sound("audio/wing.wav")
flappy.set_volume(0.5)
point = pygame.mixer.Sound("audio/point.wav")
point.set_volume(0.5)

# window
screen_width = 500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Base Bird")
bg = pygame.image.load("imgs/bg.png")
bg = pygame.transform.scale(bg, (screen_width, screen_height))

# physics
flap = -10
gravity = 0.75
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

class Pipe:
    def __init__(self, x, y, position):
        self.image = pygame.image.load("imgs/pipe_img.png")
        self.passed = False
        self.x = x
        self.y = y
        self.position = position
        # scale pipes
        self.image = pygame.transform.scale(self.image, (50, 400))
        if self.position == "top":
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(bottomleft=(self.x, self.y))
        elif self.position == "bottom":
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

# main loop
running = True
game_live = False
game_over = False
score = 0

# pipe variables
pipe_gap = 125
pipe_time = 0
pipes = []

# main bird
bird1 = Bird()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird1.velocity = flap
                flappy.play()

                if not game_live:
                    game_live = True
            
            if event.key == pygame.K_SPACE and game_over:
                bird1 = Bird()
                pipes = []            
                game_over = False
                score = 0
                game_live = False
                pipe_time = 0

    screen.blit(bg, (0, 0))

    if game_live and not game_over:

        bird1.update(gravity)

        # pipe spawn
        pipe_time += 1
        if pipe_time > 90:
            pipe_height = random.randint(100, 400)
            top_pipe = Pipe(screen_width, pipe_height, "top")
            bottom_pipe = Pipe(screen_width, pipe_height + pipe_gap, "bottom")
            pipes.append(top_pipe)
            pipes.append(bottom_pipe)
            pipe_time = 0

        for pipe in pipes:
            pipe.x -= 4
            pipe.rect.x = pipe.x                
            (pipe.image, pipe.rect)
            screen.blit(pipe.image, pipe.rect)

        for pipe in pipes[:]:
            if pipe.rect.right <= 0:
                pipes.remove(pipe)

        # detect screen edge collision
        if bird1.rect.top <= 0 or bird1.rect.bottom >= screen_height:
            game_over = True

        # detect pipe collision
        for pipe in pipes:
            if bird1.rect.colliderect(pipe.rect):
                game_over = True

        # adding to score
        for pipe in pipes:
            if pipe.position == "bottom":
                if not pipe.passed and bird1.rect.left > pipe.rect.right:
                    score += 1
                    pipe.passed = True
                    point.play()

    if game_over:
        font = pygame.font.SysFont(None, 48)
        text = font.render("Game Over!", True, (0 , 0, 0))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, 100))

    screen.blit(bird1.image, bird1.rect)
    score_font = pygame.font.SysFont(None, 36)
    score_text = score_font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    fps.tick(60)

    pygame.display.flip()

pygame.quit()   