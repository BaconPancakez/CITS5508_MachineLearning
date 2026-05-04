import pygame
from pygame.locals import *
import random
pygame.init()
clock = pygame.time.Clock()
fps = 60

screen_width = 860
screen_height = 940

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy bird')

# define font
font = pygame.font.SysFont('Bauhaus 93', 60)

# define colours
white = (255, 255, 255)

# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 225
pipe_freq = 1500 #1.5s
last_pipe = pygame.time.get_ticks() - pipe_freq
score = 0
pass_pipe = False


# Load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score


def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y))


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            self.images.append(pygame.image.load(f'img/bird{num}.png'))
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        self.clicked = False
    
    def update(self):
        # Gravity
        if flying:
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom < 770:
                self.rect.y += int(self.velocity)

        if game_over == False:
            # Jumping
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity = - 10
            if pygame.mouse.get_pressed()[0] != 1 and self.clicked == True:
                self.clicked = False

            # Handle animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # Rotation
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        # position 1 is from top, -1 is bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, img):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        # get mouse pos
        pos = pygame.mouse.get_pos()

        # check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        
        # draw button
        screen.blit(self.img, (self.rect.x, self.rect.y))
        
        return action
    
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100,int(screen_height / 2))

bird_group.add(flappy)

# Create restart button instance
button = Button(screen_width//2 - 50, screen_height//2 - 100, button_img)

run = True
while run:

    clock.tick(fps)

    # draw background
    screen.blit(bg, (0,0))

    # bird
    bird_group.draw(screen)
    bird_group.update()

    # Pipe
    pipe_group.draw(screen)

    # draw the ground
    screen.blit(ground_img, (ground_scroll, 760))

    # Check for score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
            and pass_pipe == False:
                pass_pipe = True
        if pass_pipe:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                pass_pipe = False
                score += 1
    
    draw_text(f'Score = {int(score)}', font, white, 5, 20)


    # Check if bird hit the ground
    if flappy.rect.bottom >= 760:
        game_over = True
        flying = False

    # Check if bird hit the pipe
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    if game_over == False and flying == True:
        #draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        # generate new pipe
        curr_time = pygame.time.get_ticks()
        if curr_time - last_pipe > pipe_freq:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = curr_time

        pipe_group.update()

    # check for game over and reset
    if game_over:
        if button.draw():
            game_over = False
            score = reset_game()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying=True
        
    pygame.display.update()


pygame.quit()
