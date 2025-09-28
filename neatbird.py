import pygame
import neat
import random

pygame.init()

# window
screen_width = 500
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird NEAT")
bg = pygame.image.load("imgs/bg.png")
bg = pygame.transform.scale(bg, (screen_width, screen_height))

bird_image = pygame.image.load("imgs/bird2.png")
pipe_image = pygame.transform.scale(pygame.image.load("imgs/pipe_img.png"), (50, 400))

# physics
flap = -10      # upward velocity when bird jumps
gravity = 0.75
pipe_gap = 125
pipe_velocity = 4

GENERATION = 0

# -------------------------
# Bird Class
# -------------------------
class Bird:
    def __init__(self, x, y):
        self.image = bird_image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.velocity = 0
        self.last_y = y

    def update(self, gravity):
        """Apply gravity and move the bird"""
        self.velocity += gravity
        self.y += self.velocity
        self.rect.center = (self.x, self.y)

# -------------------------
# Pipe Class
# -------------------------
class Pipe:
    def __init__(self, x, y, position):
        self.image = pipe_image
        self.x = x
        self.y = y
        self.position = position
        self.image = pygame.transform.scale(self.image, (50, 400))

        if self.position == "top":
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(bottomleft=(self.x, self.y))
        elif self.position == "bottom":
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.passed = False

    def update(self):
        self.x -= pipe_velocity
        self.rect.x = self.x

# -------------------------
# Genetic Algorithm (NEAT)
# -------------------------
def eval_genomes(genomes, config):
    global GENERATION
    GENERATION += 1

    nets = []
    birds = []
    ge = []

    # create neural networks and birds
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(screen_width // 2, screen_height // 2))
        genome.fitness = 0
        ge.append(genome)

    pipes = []
    pipe_time = 0
    score = 0
    clock = pygame.time.Clock()

    while len(birds) > 0:
        clock.tick(60)
        screen.blit(bg, (0, 0))

        # spawn pipes
        pipe_time += 1
        if pipe_time > 90:
            pipe_height = random.randint(100, 400)
            top_pipe = Pipe(screen_width, pipe_height, "top")
            bottom_pipe = Pipe(screen_width, pipe_height + pipe_gap, "bottom")
            pipes.append(top_pipe)
            pipes.append(bottom_pipe)
            pipe_time = 0

        # move and draw pipes
        for pipe in pipes:
            pipe.update()
            screen.blit(pipe.image, pipe.rect)

        # remove off-screen pipes
        i = 0
        while i < len(pipes):
            if pipes[i].rect.right <= 0:
                del pipes[i]
            else:
                i += 1

        # loop through birds
        i = 0
        while i < len(birds):
            bird = birds[i]
            bird.update(gravity)
            screen.blit(bird.image, bird.rect)

            ge[i].fitness += 0.01  # reward for staying alive

            if abs(bird.y - bird.last_y) < 1:  # hovering penalty
                ge[i].fitness -= 0.05
            bird.last_y = bird.y

            # find nearest pipes
            top_pipe = None
            bottom_pipe = None
            for pipe in pipes:
                if pipe.x + pipe.rect.width > bird.x:
                    if pipe.position == "top" and top_pipe is None:
                        top_pipe = pipe
                    elif pipe.position == "bottom" and bottom_pipe is None:
                        bottom_pipe = pipe
                if top_pipe and bottom_pipe:
                    break

            # inputs for neural net
            if top_pipe and bottom_pipe:
                dist_to_top = abs(bird.y - top_pipe.rect.bottom) / screen_height
                dist_to_bottom = abs(bird.y - bottom_pipe.rect.top) / screen_height
                inputs = (bird.y / screen_height, dist_to_top, dist_to_bottom)
            else:
                inputs = (bird.y / screen_height, 0, 0)

            # decision (jump or not)
            output = nets[i].activate(inputs)
            if output[0] > 0.5:
                bird.velocity = flap   # directly set velocity (no flap function)

            # collision with pipe
            hit = False
            for pipe in pipes:
                if bird.rect.colliderect(pipe.rect):
                    ge[i].fitness -= 1
                    del birds[i], nets[i], ge[i]
                    hit = True
                    break
            if hit:
                continue

            # collision with screen edges
            if bird.rect.top <= 0 or bird.rect.bottom >= screen_height:
                ge[i].fitness -= 1
                del birds[i], nets[i], ge[i]
                continue

            # score and reward
            for pipe in pipes:
                if pipe.position == "bottom":
                    if not pipe.passed and bird.rect.left > pipe.rect.right:
                        score += 1
                        pipe.passed = True
                        ge[i].fitness += 200
            i += 1

        # draw HUD
        font = pygame.font.SysFont(None, 36)
        screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (10, 10))
        screen.blit(font.render(f"Gen: {GENERATION}", True, (0, 0, 0)), (10, 40))
        screen.blit(font.render(f"Population: {len(birds)}", True, (0, 0, 0)), (10, 70))

        pygame.display.update()

# -------------------------
# NEAT Setup
# -------------------------
def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )
    p = neat.Population(config)
    p.run(eval_genomes, 1000)

if __name__ == "__main__":
    run("neatconfig.txt")
