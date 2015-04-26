#######################################################################
# LegoBatmanFan					8 November 2014
#
# For our last mini-project, we will complete the implementation of 
# RiceRocks, an updated version of Asteroids,  that we began last week.  
# You may start with either your code or the program template which 
# includes a full implementation of Spaceship and will be released 
# immediately after the deadline for the Spaceship mini-project (by 
# making the preceding link live).  If you start with your own code, 
# you should add the splash screen image that you dismiss with a mouse 
# click before starting this mini-project.  We strongly recommend using 
# Chrome for this mini-project since Chrome's superior performance will 
# become apparent when your program attempts to draw dozens of sprites. 
#
# This program can be executed using Code Skulptor in Chrome at the following link:
# http://www.codeskulptor.org/#user39_bc73ek8eL8q0Hpd_0.py
#######################################################################

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3

# global variables for the rocks, missiles, and ship
time = 0.5
friction_constant = 0.05
acceleration_constant = 0.5
ship_turn_constant = 0.05
missile_velocity = 10

# global variables for the status
started = False
game_status = " "
SOUNDTRACK_PLAY = False
soundtrack_message = " "


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
soundtrack.set_volume(.5)
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if not self.thrust:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0]*2+self.image_size[0]/2, self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
            
    def thrust_operation(self, thruster):
        self.thrust = thruster
        if self.thrust:
            ship_thrust_sound.play()
            print "thrusters on..."
        else:
            ship_thrust_sound.rewind()
            print "thrusters off..."
    
    def rotate(self, angular_velocity):
        # this is code from the lecture
        self.angle_vel = angular_velocity
    
    def fire_missile(self):
        global missile
        
        print "shooting a missile..."
        ship_orientation = angle_to_vector(self.angle)
        x_pos_missile = self.pos[0] + ship_orientation[0] * self.radius
        y_pos_missile = self.pos[1] + ship_orientation[1] * self.radius
        missile = Sprite([x_pos_missile, y_pos_missile], [self.vel[0]+ ship_orientation[0]*missile_velocity, self.vel[1]+ ship_orientation[1]*missile_velocity], 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(missile)
        
    def update(self):
        # this is the code from the lecture
        self.angle += self.angle_vel
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        self.vel[0] *= (1 - friction_constant)
        self.vel[1] *= (1 - friction_constant)
        
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0] * acceleration_constant
            self.vel[1] += forward[1] * acceleration_constant

    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
            
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    # this draws the sprite image (the missle or the rock)
    # or it will draw an explosion
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + (self.age * self.image_size[0]), self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    # this is the code from the lecture
    def update(self):
        remove = False
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT  
        self.age += 1
        if self.age == self.lifespan:
            remove = True
        return remove

    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    # detect a collision
    def collide(self, other_object):
        collision = False
        if dist(self.get_position(), other_object.get_position()) < (self.get_radius() + other_object.get_radius()):
            collision = True
        return collision  
    

# detect a collision and draw an explosion if there is a
# collision
def group_collide(group, other_object):
    
    object_collision = 0
    for thing in set(group):
        if thing.collide(other_object):
            object_collision += 1
            group.remove(thing)
            explosion = Sprite(thing.get_position(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion) 
            print "explosion..."
    return object_collision     


# detect a collision
def group_group_collide(group1, group2):
    object_collision = 0
    for thing in set(group1):
        if group_collide(group2, thing) > 0:
            object_collision += 1
            group1.remove(thing)
    return object_collision     


# draw and update the sprites
def draw_sprite_group(group, canvas):
    for sprite_object in set(group):
        sprite_object.draw(canvas)
        if sprite_object.update():
            group.remove(sprite_object)
        
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, game_status, SOUNDTRACK_PLAY
    
    SOUNDTRACK_PLAY = True
    soundtrack.play()
    soundtrack_message = "soundtrack on..."
    label.set_text(str(soundtrack_message)) 
    print "soundtrack on..."
    game_status = "  "
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
   
        
# keydown handlers
# right arrow: clockwise
# left arrow: counter-clockwise
# up arrow: thruster rockets on
# space bar: fire missile
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.rotate(-ship_turn_constant)
        print "rotating counter-clockwise..."
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.rotate(ship_turn_constant)
        print "rotating clockwise..."
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_operation(True)
    elif key == simplegui.KEY_MAP["down"]:
        my_ship.thrust_operation(False)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.fire_missile()

        
# keyup handlers
# left and right arrow keys up: rotation stops
# up arrow key up: thrusters off
def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.rotate(0)
        print "rotation stopped..."
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.rotate(0)
        print "rotation stopped..."
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_operation(False)
    
    
# timer handler that spawns a rock   
# i used the rock_spawner code from the template for this part
def rock_spawner():
    global rock_group
    
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    rock_avel = random.random() * .2 - .1
    rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
    if len(rock_group) < 6 and started:
        if (dist(rock.get_position(), my_ship.get_position())) >(rock.get_radius() + (1.5 * my_ship.get_radius()) + 100):
            rock_group.add(rock)  
            
    # this bit of code came from the forum. it stops the soundtrack
    # when the window is closed. this will cause an error
    if frame.get_canvas_textwidth('stop soundtrack',50) < 10:
        soundtrack.pause()
    

# this allows the user to turn the soundtrack off while
# playing the game
def play_soundtrack():
    
    global SOUNDTRACK_PLAY, soundtrack_message
    if started:
        if SOUNDTRACK_PLAY:
            soundtrack.pause()
            SOUNDTRACK_PLAY = False
            soundtrack_message = "soundtrack off..."
            label.set_text(str(soundtrack_message)) 
            print "soundtrack off..."
        else:
            soundtrack.play()
            SOUNDTRACK_PLAY = True
            soundtrack_message = "soundtrack on..."
            label.set_text(str(soundtrack_message)) 
            print "soundtrack on..."

            
# draw the ship, rocks, score, and lives
def draw(canvas):
    global time, score, lives, started, rock_group, game_status, SOUNDTRACK_PLAY, soundtrack_message    
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    canvas.draw_text("lives: "+str(lives), [55,55], 25, "white")
    canvas.draw_text("score: "+str(score), [655,55], 25, "white")
    canvas.draw_text(str(game_status), (250,55), 50, "white")
    
    # draw ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    
    
    # update ship, sprites, score, and lives
    draw_sprite_group(rock_group, canvas)
    draw_sprite_group(missile_group, canvas)
    draw_sprite_group(explosion_group, canvas)
    
    lives -= group_collide(rock_group, my_ship)
    score += group_group_collide(rock_group, missile_group)
    
    # if lives = 0, reset everything and display the splash screen
    # this means the game is over
    if lives == 0:
        started = False
        lives = 3
        score = 0
        game_status = "GAME OVER"
        rock_group = set()
        SOUNDTRACK_PLAY = False
        soundtrack_message = "soundtrack off..."
        label.set_text(str(soundtrack_message)) 
        soundtrack.pause()
        
    # this is the splash screen. display it if the game 
    # has not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
frame.add_button("soundtrack", play_soundtrack)


timer = simplegui.create_timer(1000.0, rock_spawner)

# draw labels that explain the controls
label = frame.add_label('---------------------------------') 
label = frame.add_label('keyboard controls')
label = frame.add_label('---------------------------------') 
label = frame.add_label('right arrow: clockwise')
label = frame.add_label('left arrow: counter-clockwise')
label = frame.add_label('up arrow: thruster rockets on')
label = frame.add_label('space bar: fire missile')
label = frame.add_label('---------------------------------')
label = frame.add_label(' ')

# get things rolling
timer.start()
frame.start()
