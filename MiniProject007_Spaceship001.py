#######################################################################
# LegoBatmanFan					8 November 2014
#
# From the assignment:
# In our last two mini-projects, we will build a 2D space game RiceRocks 
# that is inspired by the classic arcade game Asteroids (1979). Asteroids
# is a relatively simple game by today's standards, but was still 
# immensely popular during its time. (Joe spent countless quarters 
# playing it.) In the game, the player controls a spaceship via four 
# buttons: two buttons that rotate the spaceship clockwise or 
# counterclockwise (independent of its current velocity), a thrust 
# button that accelerates the ship in its forward direction and a fire 
# button that shoots missiles. Large asteroids spawn randomly on the 
# screen with random velocities. The player's goal is to destroy these 
# asteroids before they strike the player's ship. In the arcade version, 
# a large rock hit by a missile split into several fast moving small 
# asteroids that themselves must be destroyed. Occasionally, a flying 
# saucer also crosses the screen and attempts to destroy the player's 
# spaceship. Searching for "asteroids arcade" yields links to multiple 
# versions of Asteroids that are available on the web (including an 
# updated version by Atari, the original creator of Asteroids).
#
# This program can be executed using Code Skulptor in Chrome at the following link:
# http://www.codeskulptor.org/#user39_I3L2evqWDgIragy_0.py
#######################################################################

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
friction_constant = 0.05
acceleration_constant = 0.5
ship_turn_constant = 0.05
missile_velocity = 10


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
        global a_missile
        
        print "shooting a missile..."
        ship_orientation = angle_to_vector(self.angle)
        x_pos_missile = self.pos[0] + ship_orientation[0] * self.radius
        y_pos_missile = self.pos[1] + ship_orientation[1] * self.radius
        a_missile = Sprite([x_pos_missile, y_pos_missile], [self.vel[0]+ ship_orientation[0]*missile_velocity, self.vel[1]+ ship_orientation[1]*missile_velocity], 0, 0, missile_image, missile_info, missile_sound)
        
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
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    # this is the code from the lecture
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT        


# draw the ship, rocks, score, and lives
def draw(canvas):
    global time, score, lives
    
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
    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()


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
def rock_spawner():
    global a_rock
    
    random_width = random.randrange(0,11)
    random_height = random.randrange(0,11)
    random_x = random.randrange(-20,20)
    random_y = random.randrange(-30,30)
    random_radian = random.randrange(-3,3)
    a_rock = Sprite([WIDTH * (random_width/10), HEIGHT * (random_height/10)], [3  * (random_x/10), 3 * (random_y/10)], 0, random_radian/75, asteroid_image, asteroid_info)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

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

# get things rolling
timer.start()
frame.start()
