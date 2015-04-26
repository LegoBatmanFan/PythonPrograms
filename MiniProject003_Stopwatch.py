#############################################################################
# LegoBatmanFan					12 October 2014
#
# Stopwatch: The Game
# the stopwatch keeps track of time in tenths of seconds. the stopwatch has
# contain "Start", "Stop" and "Reset" buttons. "start" starts the watch,
# "stop" stops the watch, and "reset" stopd the watch and resets the time.
# the stopwatch keeps track of the number of times the watch is stopped.
# if the watch is stopped on the whole second (1.0, 2.0, 3.0, 4.0, etc), a
# counter is incremented. the total number of times the watch has been 
# stopped and the number of times the watch was stopped on the whole second
# are "printed" in the top right corner of the canvas.
#
# the stopwatch time is printed in the format A:BC.D, where C and D are 
# integers in the range 0-9 and B is in the range 0-5. 
#
# This program can be executed using Code Skulptor at the following link:
# http://www.codeskulptor.org/#user39_jSTJp2DSGtg68US_0.py
#############################################################################

import simplegui
total_time = 0
total_stopped = 0
stop_on_second = 0
timer_running = 0

# a function to format the time into A:BC:D, C and D are integers in the range 
# 0-9 and B is in the range 0-5. now A can goes up to 9. this function will 
# return the formatted string
def format(time):
    global hour, total_time
    
    A = time // 600
    B = ((time //10) % 60) // 10
    C = ((time // 10) % 10) % 10
    D = time % 10
    
    # something different: if A > 10, then set the total_time to 0 and the
    # function format is called again
    if A > 9:
        total_time = 0
        format(total_time)
    return str(A)+":"+str(B)+str(C)+"."+str(D)

# start the timer
def start_timer(): 
    global timer_running
    
    # print "starting..."
    timer.start()
    timer_running = 1
    return

# stop the timer. if the timer was running when the stop button was placed,
# increment the variable total_stopped by 1. if the timer was stopped on the
# whole second, increment stop_on_second by 1
def stop_timer():
    global total_stopped
    global stop_on_second
    global timer_running
    global total_time
              
    # print "stopping..."
         
    if timer_running:
        total_stopped += 1
        if total_time % 10 == 0:
            stop_on_second += 1
      #  print "the total stops "+str(total_stopped)
    timer.stop() 
    timer_running = 0
    return

# reset the global variables total_time, total_stopped, stop_on_second,
# timer_running to 0. stop the timer
def reset_timer():
    global total_time
    global total_stopped
    global stop_on_second
    global timer_running
    
    # print "reseting..."
    timer.stop() 
    total_time = 0
    total_stopped = 0
    stop_on_second = 0
    timer_running = 0

    return

# draw the background image on the canvas. now place the formated text (total_time),
# the hour, and the number of times the timer was stopped on a whole second, and 
# the total number of times the timer was stopped on the canvas
def draw_handler(canvas):
    canvas.draw_image(image, (300 / 2, 175 / 2), (300, 175), (150, 150), (300, 230))
    canvas.draw_text(format(total_time), (65, 160), 50, 'Yellow', 'monospace')
    canvas.draw_text(str(stop_on_second)+" / "+str(total_stopped), (220,20), 15, 'Yellow', 'monospace')

def timer_handler():
    global total_time
    
    total_time += 1
    return
  
# load an image from the internet. this is an image of the batman logo from www.automopedia.org
image = simplegui.load_image('http://www.automopedia.org/wp-content/uploads/2008/07/batman-logo.jpg')

# create the frame
frame = simplegui.create_frame("stopwatch game", 300, 300)

# register event handlers for control elements and start frame
timer = simplegui.create_timer(10, timer_handler)
frame.add_button("start", start_timer, 50)
frame.add_label(" ")
frame.add_button("stop", stop_timer, 50)
frame.add_label(" ")
frame.add_button("reset", reset_timer, 50)
frame.set_draw_handler(draw_handler)

# start the frame
frame.start()


