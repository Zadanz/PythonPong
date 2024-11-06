# Built off of: https://www.geeksforgeeks.org/create-a-pong-game-in-python-pygame/

import pygame

pygame.init()

# Text font
font20 = pygame.font.Font('freesansbold.ttf', 20)
font40 = pygame.font.Font('freesansbold.ttf', 40)

# RGB Colours
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Screen parameters
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Framerate
clock = pygame.time.Clock()
Framerate = 120

paused = False

debug = False

# Paddle Class
class Paddle:

    # Paddle parameters & constructor
    def __init__(self, posx, posy, width, height, speed, colour):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.colour = colour
        # Create paddle to draw
        self.playRect = pygame.Rect(posx, posy, width, height)
        self.player = pygame.draw.rect(screen,self.colour, self.playRect)

    # Function to draw the paddle
    def display(self):
        self.player = pygame.draw.rect(screen, self.colour, self.playRect)

    # Function to update position of the paddle
    # Y Factor (yFac) represents the vertical movement of the paddle
    # -1 up, 1 down, 0 no movement
    def update(self, yFac, delta):
        self.posy = self.posy + self.speed*yFac*delta

        # Limit the movement area
        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT-self.height

        self.playRect = (self.posx, self.posy, self.width, self.height)

    # Function to display the score
    def displayScore(self, text, score, x, y, colour):
        text = font20.render(text+str(score), True, colour)
        textRect = text.get_rect()
        textRect.center = (x,y)

        screen.blit(text, textRect)

    def getRect(self):
        return self.playRect
    
# Ball Class
class Ball:
    def __init__(self, posx, posy, radius, speed, colour):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.colour = colour
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(screen, self.colour, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    def display(self):
        self.ball = pygame.draw.circle(screen, self.colour, (self.posx, self.posy), self.radius)

    def update(self, delta):
        self.posx += self.speed*self.xFac*delta
        self.posy += self.speed*self.yFac*delta

        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0
        
    def reset(self):
        self.posx = WIDTH//2
        self.posy = HEIGHT//2
        self.xFac *= -1
        self.firstTime = 1

    def hit(self):
        self.xFac *= -1

    def getBall(self):
        return self.ball
    
def pauseGame():
    global paused

    Pausedtext = font20.render("Paused, press P to unpause or ESC to quit", True, WHITE)
    TextRect = Pausedtext.get_rect()
    TextRect.center = ((WIDTH/2),(HEIGHT/2))
    screen.blit(Pausedtext, TextRect)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        pygame.display.update()
        clock.tick(15) 

def main_menu():
    running = True

    while running:
        screen.fill(BLACK)

        MenuText = font40.render("Pong", True, GREEN)
        MenuRect = MenuText.get_rect()
        MenuRect.center = ((WIDTH/2), (HEIGHT*(1/4)))
        screen.blit(MenuText, MenuRect)

        StartText = font20.render("Press SPACE to start", True, WHITE)
        StartRect = StartText.get_rect()
        StartRect.center = ((WIDTH/2), (HEIGHT/2))
        screen.blit(StartText, StartRect)

        QuitText = font20.render("Press ESC to quit", True, WHITE)
        QuitRect = QuitText.get_rect()
        QuitRect.center = ((WIDTH/2), (HEIGHT*(3/4)))
        screen.blit(QuitText, QuitRect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game()
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.update()


# Game Manager
def game():
    running = True
    
    # Defining Objects
    player1 = Paddle(20, HEIGHT//2-50, 10, 100, 1000, GREEN)
    player2 = Paddle(WIDTH-30, HEIGHT//2-50, 10, 100, 1000, GREEN)
    ball = Ball(WIDTH//2, HEIGHT//2, 7, 700, WHITE)

    players = [player1, player2]

    player1Score, player2Score = 0, 0
    player1YFac, player2YFac = 0, 0

    while running:
        screen.fill(BLACK)
        
        dt = clock.tick(Framerate) / 1000

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player2YFac = -1
                if event.key == pygame.K_DOWN:
                    player2YFac = 1
                if event.key == pygame.K_w:
                    player1YFac = -1
                if event.key == pygame.K_s:
                    player1YFac = 1
                if event.key == pygame.K_p:
                    global paused 
                    paused = True
                    pauseGame()
                if event.key == pygame.K_b:
                    global debug
                    if debug:
                        debug = False
                    else:
                        debug = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1YFac = 0

        for player in players:
            if pygame.Rect.colliderect(ball.getBall(), player.getRect()):
                ball.hit()

        player1.update(player1YFac, dt)
        player2.update(player2YFac, dt)
        point = ball.update(dt)

        # point = -1: Player 1 scored
        # point = 1: Player 2 scored
        # point = 0: No one scored
        if point == -1:
            player1Score += 1
        elif point == 1:
            player2Score += 1
        
        if point:
            ball.reset()

        player1.display()
        player2.display()
        ball.display()

        player1.displayScore("Player 1: ", player1Score, 100, 20, WHITE)
        player2.displayScore("Player 2: ", player2Score, WIDTH-100, 20, WHITE)

        # Display FPS
        if debug:
            FPStext = font20.render("FPS: "+str(round(clock.get_fps(), 1))+" Frametime: "+str(round(dt, 7)), True, WHITE)
            FPStextRect = FPStext.get_rect()
            FPStextRect.center = (WIDTH/2,20)
            screen.blit(FPStext, FPStextRect)

        pygame.display.update()
        #clock.tick()

if __name__ == "__main__":
    main_menu()
    pygame.quit()

        

