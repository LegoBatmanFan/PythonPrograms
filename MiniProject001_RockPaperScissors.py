#################################################################
# LegoBatmanFan	
# Rock-paper-scissors-lizard-Spock Mini-project 1
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors
#
# This program can be executed using Code Skulptor at the following link:
# http://www.codeskulptor.org/#user39_leWeeX0RDM_0.py
#################################################################

# import random
import random

# nameToNumber: changes the name to a number.
# if given an invalid name, the function prints an error message
# and returns the number 5
def nameToNumber(name):
    if name == "rock":
        number = 0
    elif name == "Spock":
        number = 1
    elif name == "paper":
        number = 2
    elif name == "lizard":
        number = 3
    elif name == "scissors":
        number = 4
    else:
        number = 5
        print "invalid name"
    return number

# numberToName: chnages the number to a name.
# if given a number greater than 4, the function returns the string
# "invalid function" as the name
def numberToName(number):
    if number == 0:
        name = "rock"
    elif number == 1:
        name = "Spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    elif number == 4:
        name = "scissors"
    else:
        name = "invalid name"
    return name

def rpsls(playerChoice): 
    
    # print a blank line to separate consecutive games
    print " "
    
    # convert the player's choice to playerNumber using the function nameToNumber() 
    playerNumber = nameToNumber(playerChoice)
    
    # compute random guess for computerNumber using random.randrange()
    computerNumber = random.randrange(0, 5)
    
    # convert computerNumber to computerChoice using the function numberToName()
    computerChoice = numberToName(computerNumber)
    
    # print out the message for the choices made by the computer and the player
    print "player chooses " + playerChoice
    print "computer chooses " + computerChoice
    
    # compute difference of computerNumber and playerNumber modulo five
    difference = (computerNumber - playerNumber) % 5
    
    # if the playerNumber or computerNumber is greater than 4, set difference to 1000
    if (playerNumber > 4 or computerNumber > 4):
        difference = 1000
    
    # use if/elif/else to determine winner, print winner message   
    # if difference is 1 or 2, the computer wins
    # if difference is 3 or 4, the player wins
    # if difference is 0, it's a tie
    # an invalid name causes difference to have a very high value and 
    # this will throw an error message
    if (difference == 1 or difference == 2):
        print "computer wins!"
    elif (difference == 3 or difference == 4):
        print "player wins!"
    elif (difference == 0):
        print "it's a tie!"
    else:
        print "too many errors. GAME OVER"
        
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

#this entry tests the error message
rpsls("moose")

# always remember to check your completed program against the grading rubric


