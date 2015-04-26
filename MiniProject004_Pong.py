###############################################################
# LegoBatManFan							18 October 2014
#
# Implementation of classic arcade game Pong
# When the game is "stopped" when it first opens. Press
# the "start/restart game" button to start the game.
# the ball turns red when it hits the top of the screen
# and turns green when it hits the bottom of the screen.
# if the game is reset, the ball turns white.
#
# messages about key presses, ball direction, player scores,
# and the walls hit by the ball are printed out to the console.
# these messages were part of the debugging of the code
#
# This program can be executed using Code Skulptor at the following link:
# http://www.codeskulptor.org/#user39_xgLhMcPEvRjxxwX_0.py
###############################################################

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
PAD_SPEED = 5
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
HORIZONTAL = WIDTH/2
VERTICAL = HEIGHT/2
ball_pos = [HORIZONTAL, VERTICAL]
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0 
paddle2_vel = 0
player1_score = 0
player2_score = 0
ball_vel = [0,0]
ball_color = "white"
radius_color = "white"


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_vel, ball_pos # these are vectors stored as lists
    global ball_color, radius_color
    
    ball_color = "white"
    radius_color = "white"
    ball_pos = [HORIZONTAL, VERTICAL]
    print direction
    h_velocity = random.randrange(120, 240) / 60.0
    v_velocity = -random.randrange(60, 180) / 60.0
    ball_vel = [h_velocity, v_velocity]
    if not direction:
        ball_vel[0] = -ball_vel[0]

        
# define event handlers
# start a new game
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos  # these are numbers
    global player1_score, player2_score  # these are ints
    
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    player1_score = 0
    player2_score = 0
    spawn_ball(random.choice([LEFT, RIGHT]))

    
# move the paddles    
def move_paddles():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    
    paddle1_pos += paddle1_vel
    if paddle1_pos < HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
        
    paddle2_pos += paddle2_vel
    if paddle2_pos < HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT    
    

# move the ball    
def move_ball():
    global ball_pos, ball_vel, player1_score, player2_score
    global ball_color, radius_color
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]  
    
    # if the ball hits the gutter, increment the other player's 
    # score by 1. print different messages to the console based
    # on if the ball hits the paddle or the gutter
    if ball_pos[0] < BALL_RADIUS + PAD_WIDTH:
        if paddle1_pos - HALF_PAD_HEIGHT - BALL_RADIUS <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT + BALL_RADIUS:
            ball_pos[0] = BALL_RADIUS + PAD_WIDTH
            ball_vel[0] = -(ball_vel[0] + (ball_vel[0] * 0.1))
            print "ball bounced off left paddle"
        else:
            print "ball bounced off left gutter"
            player2_score += 1
            print "score for player 2 >>>"+str(player2_score)
            for x in range(0, 4):
                print " "
            print "spawning new game"
            spawn_ball(random.choice([LEFT, RIGHT]))
   
    elif ball_pos[0] > WIDTH - BALL_RADIUS - PAD_WIDTH:
        if paddle2_pos - HALF_PAD_HEIGHT - BALL_RADIUS <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT + BALL_RADIUS:
            ball_pos[0] = WIDTH - BALL_RADIUS - PAD_WIDTH
            ball_vel[0] = -(ball_vel[0] + (ball_vel[0] * 0.1))
            print "ball bounced off right paddle"
        else:
            print "ball bounced off right gutter"
            player1_score += 1
            print "score for player 1 >>>"+str(player1_score)
            for x in range(0, 4):
                print " "
            print "spawning new game"
            spawn_ball(random.choice([LEFT, RIGHT]))
    
    # bounce the ball off the top of the screen
    if ball_pos[1] < BALL_RADIUS:
            ball_pos[1] = BALL_RADIUS 
            ball_vel[1] = -ball_vel[1]
            print "ball bounced off top of screen"
            ball_color = "red"
            radius_color = "red"
    # bounce the ball off the top of the screen    
    elif ball_pos[1] > HEIGHT - BALL_RADIUS:
            ball_pos[1] = HEIGHT - BALL_RADIUS 
            ball_vel[1] = -ball_vel[1]
            print "ball bounced off bottom of the screen"
            ball_color = "green"
            radius_color = "green"
        
        
def draw(canvas):
    global player1_score, player2_score, paddle1_pos, paddle2_pos
    global ball_pos, ball_vel, ball_color
         
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # move ball
    move_ball()
    
    # draw the ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, radius_color, ball_color)
    
    # move the paddle sup and down
    move_paddles()
    
    # draw paddles
    #this part draws the paddles as a thick line (PAD_WIDTH)
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], 
                     [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], 
                     PAD_WIDTH, "white")   
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], 
                     [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], 
                     PAD_WIDTH, "white")
    
    # draw scores
    canvas.draw_text("player 1", [120,25], 20, "white")
    canvas.draw_text("player 2", [420,25], 20, "white")
    canvas.draw_text(str(player1_score), [150,55], 30, "white")
    canvas.draw_text(str(player2_score), [450,55], 30, "white")

    
# restart the game
def restart():
    
    for x in range(0, 4):
        print " "
    print "reset..."
    new_game()
    
    
# if the keys have been pressed, the velocity of the paddles 
# should not be zero, so update the position   
# w key - moves the paddle for player1 up
# s key - moves the paddle for player1 down
# up arrow - moves the paddle for player1 up
# down arrow - moves the paddle for player2 down
def keydown(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -PAD_SPEED
        print "w key >>"+str(paddle1_vel)
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = PAD_SPEED
        print "s key >>"+str(paddle1_vel)
       
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PAD_SPEED
        print "up arrow key >>"+str(paddle2_vel)       
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PAD_SPEED
        print "down arrow key >>"+str(paddle2_vel)
        
    
# if the keys have been released, the velocity of the paddles should be zero,
# so don't update the position   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0

    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.add_button("start/restart game", restart, 100)
# draw labels that explain the controls
label = frame.add_label('---------------------------------') 
label = frame.add_label('keyboard controls')
label = frame.add_label('---------------------------------') 
label = frame.add_label('player 1')
label = frame.add_label('w: moves the left paddle up')
label = frame.add_label('s: moves the left paddle down')
label = frame.add_label(' ')
label = frame.add_label('player 2')
label = frame.add_label('up arrow: moves the right paddle up')
label = frame.add_label('down arrow: moves the right paddle down')
label = frame.add_label('--------------------------------')
label = frame.add_label(' ')
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
#new_game()
frame.start()
