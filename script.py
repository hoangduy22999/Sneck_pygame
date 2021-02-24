import pygame
import sys
import random

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = SNAKE
        # Special thanks to YouTubers Mini - Cafetos and Knivens Beast for raising this issue!
        # Code adjustment courtesy of YouTuber Elija de Hoog
        self.score = 0
        self.start = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0
        self.start = 0

    def draw(self,surface):
        for p in self.positions:
            if ( p.index == 0):
                pygame.draw.circle(surface, self.color, (p[0]+ gridsize/2, p[1] + gridsize/2), gridsize/2)
            else:
                r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
                pygame.draw.rect(surface, self.color, r)
                pygame.draw.rect(surface, SNAKEBD, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = FOOD
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, FOODBD, r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, GRID, r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, GRIDBD, rr)

screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

SNAKE = (17, 24, 47)
SNAKEBD = (93,216, 228)
FOOD = (255, 0, 0)
FOODBD = (93, 216, 228)
GRID = (93,216,228)
GRIDBD = (84,194,205)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147, 153, 35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)

COLOR = [RED,GREEN,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace",16)
    welcomefont =  pygame.font.SysFont("monospace",25)
    best_Sorce = 0
    start_game = 0 

    while (True):
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        while (snake.start == 0):
            welcometxt = welcomefont.render("Press Space to Play",1, random.choice(COLOR))
            screen.blit(welcometxt, (110,230))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        snake.start = 1
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
        else:
            snake.move()
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                if snake.score > best_Sorce:
                    best_Sorce = snake.score
                food.randomize_position()
            snake.draw(surface)
            food.draw(surface)
            screen.blit(surface, (0,0))
            text = myfont.render("Score {0}".format(snake.score), 1, BLACK)
            best_txt = myfont.render("High Socre {0}".format(best_Sorce), 1, BLACK)
            screen.blit(text, (5,10))
            screen.blit(best_txt, (5, 30))
            pygame.display.update()

    pygame.quit()
main()