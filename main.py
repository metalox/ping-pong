# Import the pygame library and initialise the game engine
import pygame
from modules.paddle import Paddle
from modules.ball import Ball

pygame.init()

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,200)

# Define sounds
batSound = pygame.mixer.Sound('sounds/hit01.wav')
scoreSound = pygame.mixer.Sound('sounds/beee01.wav')

# Open a new window
size = (800,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 30 
paddleA.rect.y = 250
 
paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 760 
paddleB.rect.y = 250

ball = Ball(WHITE, 10, 10)
ball.rect.x = 395
ball.rect.y = 295

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()
 
# Add the paddles to the list of sprites
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

# The loop will cary on until the user exits the game (e.g clicks the close button)
carryOn = True

# the closk will be used to control how fast the screen updates
clock = pygame.time.Clock()

# Initialise player scrores
scoreA = 0
scoreB = 0

# -------- Main Program Loop --------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            carryOn = False # Flag that we are done, so we exit this loop
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                while True: # Infinite loop that will be broken when the user presses space again
                    event = pygame.event.wait()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        break #Exit infinite loop
            elif event.key==pygame.K_x: # Pressing the x key will quit the game
                carryOn = False

    # Moving the paddles when keys are pressed
    # Player A:  Q/A - Player B: P/L
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        paddleA.moveUp(10)
    if keys[pygame.K_a]:
        paddleA.moveDown(10)
    if keys[pygame.K_p]:
        paddleB.moveUp(10)
    if keys[pygame.K_l]:
        paddleB.moveDown(10)

    # --- Game Logic should go here...
    all_sprites_list.update()

    # Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x >= 790:
        scoreSound.play()
        scoreA += 1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 10:
        scoreSound.play()
        scoreB += 1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 590:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1] 
 
 # Detect collisions between the ball and the paddles  
    if pygame.sprite.collide_mask(ball, paddleA):
        if ball.velocity[0] < 0 : 
            batSound.play()
            ball.bounce()
    elif pygame.sprite.collide_mask(ball, paddleB):
        if ball.velocity[0] > 0 : 
            batSound.play()
            ball.bounce()

    # --- Drawing Code should go here
    # First clear the screen to black
    screen.fill(BLACK)
    
    # Draw the net
    pygame.draw.line(screen, WHITE, [398,0],[398, 600], 5 )
    # Draw the walls
    pygame.draw.line(screen, WHITE, [20,0],[20, 600], 1 )
    pygame.draw.line(screen, WHITE, [780,0],[780, 600], 1 )
    
    # Draw all the sprites in one go.
    all_sprites_list.draw(screen) 

    # Display scores
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (180, 10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (520, 10))

    # --- Go ahead and update the screen with what we've drawn
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine
pygame.quit()
