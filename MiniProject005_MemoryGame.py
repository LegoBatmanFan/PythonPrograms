######################################################
# LegoBatmanFan						25 October 2014
#
# Mini Porject #5: Memory game
#
# in this game, there are 16 "cards" with the values
# of 0 - 7. the user lcicks on a cards, "flipping it 
# over," showing the card's value. when two cards are
# "exposed," their values are compared. if the values 
# are the same, the cards remain exposed and the user 
# can click on other cards. if the values of the two 
# cards are not the same, then the two exposed cards 
# are flipped over when the user clicks on a third
# card. the number of moved are counted. moves are not
# counted when the user clicks on a card (or cards)
# that have been exposed. messages are printed out to
# the console
# 
# This program can be executed using Code Skulptor at the following link:
# http://www.codeskulptor.org/#user39_ojjmIgvNSbMwZ3s_0.py
######################################################

import simplegui
import random

# simple state example for Memory
WIDTH = 100
HEIGHT = 100
state = 0
moves = 0
exposed_cards = []
card_values = []
card_value_list = []
card_values_list2 = []

     
# define event handlers
def new_game():
    global state, exposed_cards, card_values, moves
    
    for i in range(5):
        print " "
    print "STARTING NEW GAME"
    state = 0
    moves = 0
    index = 0
    exposed_cards = []
    card_values = []
    
    # shuffle the cards
    card_value_list = range(8)
    random.shuffle(card_value_list)
    card_values_list2 = range(8)
    random.shuffle(card_values_list2)
    card_value_list.extend(card_values_list2)
    
    # create four lists for the exposed cards
    for a in range(4):
        exposed_cards.append([])

    # set their "exposed" values to "False," meaning that
    # the cards are turned over and you cannot see their
    # values
    for b in range(4):
        for c in range(4):
            exposed_cards[c].append(False) 

    # create four lists for the card values        
    for x in range(4):
        card_values.append([])
    
    # set the card values
    for y in range(4):
        for z in range(4):
            card_values[y].append(card_value_list[index])
            index += 1
    label.set_text("# of moves = "+str(moves))
    # print the state of the exposed cards to the console
    print exposed_cards
  
    
def mouse_handler(position):
    global state, exposed_cards, moves
    global card1_index1, card1_index2
    global card2_index1, card2_index2
    
    print "mouse position>>>>> "+str(position)
    print "position[0]>>> "+str(position[0])
    print "position[1]>>> "+str(position[1])
    
    # get the card. the cards are set up in a 4x4
    # arrangement
    index1= position[0]//WIDTH
    index2= position[1]//WIDTH
    print "clicked on the card at position ["+str(index1)+","+str(index2)+"]"
    
    # explanation of the states
    # state 0: no cards have been clicked, no cards
    #			have been exposed
    # state 1: there are a few conditions where state = 1
    #			a. first card has been clicked and exposed
    #			b. you have two cards that don't match and
    #				you click on a third card. the first
    #				two cards are flipped over
    #			c. you have two cards that match and you
    #				click on a third card. the first two cards
    #				remain exposed
    # state 2: second card has been clicked
 
    if state == 0:
        state = 1
        card1_index1 = index1
        card1_index2 = index2
        exposed_cards[index1][index2] = True
    elif state == 1:
        if not exposed_cards[index1][index2]:
            state = 2
            card2_index1 = index1
            card2_index2 = index2
            exposed_cards[index1][index2] = True
            moves += 1
            label.set_text("# of moves = "+str(moves))
    else:
        if not exposed_cards[index1][index2]:
            state = 1
            if card_values[card1_index1][card1_index2] != card_values[card2_index1][card2_index2]:
                exposed_cards[card1_index1][card1_index2] = False
                exposed_cards[card2_index1][card2_index2] = False
            card1_index1 = index1
            card1_index2 = index2
            exposed_cards[index1][index2] = True
    print "state>>>>> "+str(state)
    
    
def draw(canvas):
    # create a 4 x 4 arrangement of the cards
    for i in range(0, 4):
        for j in range(0, 4):
            if not exposed_cards[j][i]:
                canvas.draw_polygon([(WIDTH*(j),HEIGHT*i), (WIDTH*(j+1), HEIGHT*i), (WIDTH*(j+1), HEIGHT*(i+1)),(WIDTH*(j),HEIGHT*(i+1))],3,"Black","Blue");
            else:
                canvas.draw_text(str(card_values[j][i]),[WIDTH*j+35,HEIGHT*(i+1)-30],50,"White");

# create frame and add a button and labels
frame = simplegui.create_frame("Memory states", 400,400)
frame.add_button("restart game", new_game, 150)
label = frame.add_label("# of moves = 0")


# register event handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse_handler)

# get things rolling
new_game()
frame.start()
