#############################################################################
# LegoBatmanFan					4 October 2014
#
# Mini-project 2 — “Guess the number” game 
# the program generates a random number and the player tries to guess the 
# secret number. based on the range (100 or 1000), the player will have a set
# number of guesses. if the player has not run out of guesses and if the guess
# is greater than the secret number, the program prints the message "higher." 
# if the guess is lower than the secret number, the program prints the messge 
# "lower." if the player guesses the number (before running out of guesses),
# the player wins. if the player runs out of guesses, the player loses. in 
# either case, the game restarts with an upper range of 100 (with 7 total 
# guesses). the player can also start a new game by clicking on the button 
# "range is [0, 100)" or "range is [0, 1000)." clicking on "range is [0, 100)"
# starts the game with an upper range of 100 and 7 total guesses. clicking on 
# "range is [0, 1000)" starts the game with an upper range of 1000 and 10
# total guesses.
#
# This program can be executed using Code Skulptor at the following link:
#  http://www.codeskulptor.org/#user39_BXGDJg6shr_0.py
#############################################################################

import simplegui
import random
import math

# initialization of global variables 
secret_number = 0
count_guess = 0

# helper function to start and restart the game
# new_game() takes the value from range_high (100 or 1000) as the upper limit 
# of a range. the value of range_high is used to calculate secret_number and
# count_guess. count_guess is the number of guesses. if the upper limit of the 
# range is 100, the player gets 7 guesses. if the upper limit of the range is 
# 1000, the player gets 10 guesses. secret_number and count_guess are global
# variables because they will be used in the function input_guess()
def new_game(range_high):
    global secret_number, count_guess
    
    print" "
    print"=========================================="
    print "THIS IS THE UPPER RANGE >>>>> " +str(range_high)
    print"------------------------------------------"
    secret_number = random.randrange(0, range_high)
    
    # the line below calculates the number of guesses using math.log and 
    # math.ceil
    x = math.ceil(((math.log(range_high - (0 + 1)))/(math.log(2))))
    count_guess = int(x)
    
    print "total number of guesses >>>>> "+str(count_guess)
    print"------------------------------------------"
    

# button that changes the range to [0,100) and starts a new game 
# by calling the function "new_game and passing the value "100"
# to the function new_game()
def range100(): 
    print " "
    print "...StArTiNg A nEw GaMe..."
    new_game(100) 
    
    
# button that changes the range to [0,1000) and starts a new game 
# by calling the function "new_game and passing the value "1000"
# to the function new_game()     
def range1000():
    print " "
    print "...StArTiNg A nEw GaMe..."
    new_game(1000)    
    
    
# this function takes the number from the gui and compares it to the secret
# number. while the number of guesses is greater than zero, this function
# will compare the guess to the secret number. the game will print a message 
# if the number is higher or lower than the secret number. if the player 
# guesses the number and the number of guesses is greater than zero the player
# wins. if the player runs out of guesses, the player will see a message 
# stating the game is over. if the player runs out of guesses or the player 
# wins, the game restarts and a value of 100 is passed to the function 
# new_game()
def input_guess(guess):
    global count_guess
    
    # now here's something interesting...this little bit of code checks to see
    # if the user has entered valid input. if the user enters characters, a 
    # combination of numbers and characters, or enters nothing, and error message
    # will be printed and the user will be prompted to enter another number.
    # the number of alowed/total guesses decreases by 1
    try: 
            print "++ guess was " +guess
            number_guess = int(guess)
    except ValueError:
            if count_guess > 1:
                count_guess = count_guess - 1
                print "inavlid input. try again..." 
                print "number of guesses left: "+str(count_guess)
                print"------------------------------------------"
                return input_guess
        
    if count_guess > 1:
        count_guess = count_guess - 1
        if number_guess > secret_number:
            print "lower!!!!!  number of guesses left: "+str(count_guess)
            print"------------------------------------------"
        elif number_guess < secret_number:
            print "HIGHER!!!!! number of guesses left: "+str(count_guess)  
            print"------------------------------------------"
        else:
            print "we have a WINNER!!!" 
            print "you guessed it! the secret number is "+str(secret_number)
            print"=========================================="
            count_guess = -100
    else:
        print "max number tries!!!"
        print "the secret number is "+str(secret_number)
        print "<<<GAME OVER>>>"
        print"=========================================="
        count_guess = 0 
        
    # start a new game    
    if count_guess < 1:        
        print " "
        print "...StArTiNg A nEw GaMe..."
        new_game(100)

    
# create the frame
f = simplegui.create_frame("guess the number", 200, 200)

# register event handlers for control elements and start frame
f.add_button("range is [0, 100)", range100, 150)
f.add_button("range is [0, 1000)",range1000, 150)
f.add_input("enter a guess", input_guess, 150)

# call new_game and pass the value of 100
new_game(100)

