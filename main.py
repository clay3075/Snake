import pygame
from   pygame.locals import *
from   random import randint

RED   = (220, 20, 60)
BLACK = (0, 0, 0)
GREEN = (110, 139, 61)
WHITE = (255, 255, 255)

LEFT, RIGHT, UP, DOWN = 0, 1, 2, 3

CREATE_APPLE_EVENT = 22
 
class Snake_Game:
    def __init__(self):
        self.running  = True
        self.screen   = None
        self.clock    = None
        self.size     = self.width, self.height = 640, 400
        self.gameOver = False 
        self.snake    = None
        self.food     = None
 
    def init(self):
        pygame.init()
        self.screen     = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock      = pygame.time.Clock()
        self.snake      = Player(self.screen)
        self.food       = Apples(self.screen, self.snake)
        self.UI_manager = UI_Manager(self.screen)
        self.running    = True
        self.snake.create()
        pygame.time.set_timer(CREATE_APPLE_EVENT, 3000)
 
    def event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == CREATE_APPLE_EVENT and not self.gameOver:
            self.food.create()

    def loop(self):
        
        if not self.gameOver:
            self.snake.move()
            self.checkCollision()        
            self.checkGameOver()
        else:
            self.checkPlayAgain()


    def render(self):

        self.screen.fill(BLACK)

        if not self.gameOver:
            self.snake.show()
            self.food.show()
            self.clock.tick(8)
            self.UI_manager.update_score(self.snake.get_links())
        else:
            self.UI_manager.show_gameOverScreen()

        pygame.display.update()

    def checkGameOver(self):
        if not self.screen.get_rect().contains(self.snake.get_links()[0]):
            self.gameOver = True 


    def checkCollision(self):

        for link in self.snake.get_links():
            for food in self.food.get_food():
                colision = pygame.sprite.collide_rect(link, food)
                if colision == True:
                    self.food.remove(food)
                    self.snake.grow()

    def checkPlayAgain(self):

        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            self.reset()

    def reset(self):

        self.snake      = Player(self.screen)
        self.food       = Apples(self.screen, self.snake)
        self.UI_manager = UI_Manager(self.screen)
        self.snake.create()
        self.gameOver   = False 

    def cleanup(self):
        pygame.quit()
 
    def execute(self):
        if self.init() == False:
            self.running = False
 
        while( self.running ):
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            self.render()
        self.cleanup()

class UI_Manager:
    def __init__(self, screen):
        self.screen = screen
        self.score  = 0

    def show_gameOverScreen(self):

        # If game over is true, draw game over
        font   = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, RED)
        text_rect = text.get_rect()
        text_x = self.screen.get_width() / 2 - text_rect.width / 2
        text_y = self.screen.get_height() / 2 - text_rect.height / 2
        self.screen.blit(text, [text_x, text_y])
        font   = pygame.font.Font(None, 26)
        text = font.render("Score: " + self.score, True, WHITE)
        text_rect = text.get_rect()
        text_x += 30
        text_y += 35
        self.screen.blit(text, [text_x, text_y])
        font   = pygame.font.Font(None, 16)
        text = font.render("Press ENTER to play again.", True, WHITE)
        text_rect = text.get_rect()
        text_x -= 35
        text_y += 35
        self.screen.blit(text, [text_x, text_y])

    def update_score(self, snake_links):
        font   = pygame.font.Font(None, 16)
        self.score = str(len(snake_links))
        text = font.render("Score: " + self.score, True, WHITE)
        text_rect = text.get_rect()
        text_x = self.screen.get_width() - text_rect.width - 50
        text_y = text_rect.height + 5
        self.screen.blit(text, [text_x, text_y])

class Apples:
    def __init__(self, screen, snake):
        self.screen = screen
        self.apples  = []
        self.snake  = snake

    def get_food(self):
        return self.apples

    def remove(self, apple):
        self.apples.remove(apple)

    def generate(self):
        if randint(0, 100) == 50:
            self.create()

    def create(self):
        success = False

        while not success:
            x = randint(0, self.screen.get_width() - 16)
            y = randint(0, self.screen.get_height() - 16)

            for link in self.snake.get_links():
                if (x > (link.x + 16) and y > (link.y + 16)) or (x < (link.x - 16) and y < (link.y - 16)):
                    success = True

        self.apples.append(Apple(RED, 16, 16, (x, y)))

    def show(self):
        for apple in self.apples:
            apple.draw(self.screen);

class Player:
    def __init__(self, screen):
        self.snake   = []
        self.direction    = None
        self.oldDirection = None
        self.screen  = screen

    def get_links(self):
        return self.snake 

    def show(self):
        for link in self.snake:
            link.draw(self.screen)

    def create(self):
        self.snake.append(Snake_Link(GREEN, 16, 16))

    def get_direction(self):

        key = pygame.key.get_pressed()

        if key[pygame.K_DOWN] and self.oldDirection != UP: # down key
            self.direction = DOWN
        elif key[pygame.K_UP] and self.oldDirection != DOWN: # up key
            self.direction = UP
        elif key[pygame.K_RIGHT] and self.oldDirection != LEFT: # right key
            self.direction = RIGHT
        elif key[pygame.K_LEFT] and self.oldDirection != RIGHT: # left key
            self.direction = LEFT

        self.oldDirection = self.direction

    def move(self):

        self.get_direction()
        self.move_forward()          

    def move_forward(self):
        dist = 17

        for linkNum in range(len(self.snake) - 1, 0, -1):
            self.snake[linkNum].x = self.snake[linkNum - 1].x
            self.snake[linkNum].y = self.snake[linkNum - 1].y
            
        if self.direction == DOWN:
            self.snake[0].y += dist
        elif self.direction == UP:
            self.snake[0].y -= dist
        elif self.direction == LEFT:
            self.snake[0].x -= dist
        elif self.direction == RIGHT:
            self.snake[0].x += dist


    def grow(self):

        x = self.snake[len(self.snake) - 1].x 
        y = self.snake[len(self.snake) - 1].y
        if self.direction == DOWN:
            self.snake.append(Snake_Link(GREEN, 16, 16, (x, y - 17)))
        elif self.direction == UP:
            self.snake.append(Snake_Link(GREEN, 16, 16, (x, y + 17)))
        elif self.direction == LEFT:
            self.snake.append(Snake_Link(GREEN, 16, 16, (x + 17, y)))
        elif self.direction == RIGHT:
            self.snake.append(Snake_Link(GREEN, 16, 16, (x - 17, y)))

class Snake_Link(pygame.sprite.Sprite):

    def __init__(self, color, width, height, location=(0,0)):
       pygame.sprite.Sprite.__init__(self)
       self.x = location[0]
       self.y = location[1]

       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

    #Add this draw function so we can draw individual sprites
    def draw(self, screen):
        self.rect.topleft = (self.x, self.y)
        screen.blit(self.image, (self.x, self.y))

class Apple(pygame.sprite.Sprite):

    def __init__(self, color, width, height, location=(0,0)):
       pygame.sprite.Sprite.__init__(self)
       self.x = location[0]
       self.y = location[1]
       print("X:{}\nY:{}\n".format(self.x, self.y))

       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()

    #Add this draw function so we can draw individual sprites
    def draw(self, screen):
        self.rect.topleft = (self.x, self.y)
        screen.blit(self.image, (self.x, self.y))
 
if __name__ == "__main__" :
    game = Snake_Game()
    game.execute() 
