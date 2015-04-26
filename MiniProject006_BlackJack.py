#######################################################
# LegoBatmanFan					BlackJack Mini-Project
#
# from the assignment:
# The game logic for our simplified version of Blackjack 
# is as follows. The player and the dealer are each dealt 
# two cards initially with one of the dealer's cards being
# dealt faced down (his hole card). The player may then 
# ask for the dealer to repeatedly "hit" his hand by 
# dealing him another card. If, at any point, the value 
# of the player's hand exceeds 21, the player is "busted" 
# and loses immediately. At any point prior to busting, 
# the player may "stand" and the dealer will then hit his 
# hand until the value of his hand is 17 or more. (For 
# the dealer, aces count as 11 unless it causes the 
# dealer's hand to bust). If the dealer busts, the player 
# wins. Otherwise, the player and dealer then compare the 
# values of their hands and the hand with the higher value
#wins. The dealer wins ties in our version.
#
# what's different:
# 1. messages are printed to the console (as a log)
# 2. the game tracks the score, wins, and losses for the
#	player.
# 3. if the player clicks on the "hit me" or "stand"
#	buttons after the game is over, they will receive a
# 	message stating they should deal a card. the values
# 	for score, wins, losses
#
# This program can be executed using Code Skulptor at the following link:
# http://www.codeskulptor.org/#user39_yXZCwjJPtSjoSRO_0.py
#######################################################
import simplegui
import random

# initialize some useful global variables
IN_PLAY = False
outcome = " "
score = 0
wins = 0
losses = 0
blackjack = 0
dealer_card = False

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    


# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# code for the card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        j.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        

# code for Hand class here
class Hand:
    def __init__(self, game_player):
        self.my_cards = []
        self.person = game_player
        self.card_value = 0
        
    def add_card(self, card):
        self.my_cards.append(card)
    
    def get_value(self): 
        number_of_aces = 0
        self.card_value = 0
        for card in self.my_cards:
            value_index = card.get_rank()
            if VALUES.get(value_index) == 1:
                number_of_aces += 1
            self.card_value += VALUES.get(value_index)
        if number_of_aces == 0:
            return self.card_value
        else:
            if self.card_value + 10 <= 21:
                return self.card_value + 10
            else:
                return self.card_value
        
    
    def draw(self, canvas, pos):
        x = 0
        for j in self.my_cards:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(j.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(j.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0]+ 15 * x + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            x += 5
            
    def __str__(self):
        ans = self.person + " Hand contains "
        for i in range(len(self.my_cards)):
            ans += str(self.my_cards[i])+" "
        return ans 
   
    
#code for Deck class here
class Deck:
    def __init__(self):
        self.my_deck = []
        for suit in SUITS:
            for rank in RANKS:
                my_card = Card(suit, rank)
                self.my_deck.append(my_card)
        return self.my_deck
    
    def shuffle(self):
        random.shuffle(self.my_deck)
        
    def deal_card(self):
        this_card = self.my_deck.pop(0)
        print "cards left in the deck >>> "+str(len(self.my_deck))
        return this_card
    
    def __str__(self):
        ans = "Deck contains "
        for i in range(len(self.my_deck)):
            ans += str(self.my_deck[i])+" "
        return ans 

    
# code for dealing a card
def deal():
    global IN_PLAY, player_hand, dealer_hand
    global my_deck, outcome, score, losses, dealer_card
    
    dealer_card = False
    outcome = "starting a new game..."
    print IN_PLAY
    if IN_PLAY:
        print "starting over the middle of a game...player loses"
        outcome = "starting over the middle of a game...player loses"
        score -= 1
        losses += 1
    
    IN_PLAY = True
    for a in range(5):
        print " "
    print "StArTiNg A nEw GaMe..."    
    player_hand = Hand("Player")
    dealer_hand = Hand("Dealer")
    my_deck = Deck()
    my_deck.shuffle()
    player_hand.add_card(my_deck.deal_card())
    print player_hand
    print "Player >>> the value of this hand >> ", player_hand.get_value()
    print " "
   
    dealer_hand.add_card(my_deck.deal_card())
    print dealer_hand
    print "Dealer >>> the value of this hand >> ", dealer_hand.get_value()
    print " "
    print " "
    print " "
 
    
# code for hitting a player
def player_hit():
    global IN_PLAY, player_hand, dealer_hand, outcome
    global score, wins, losses, blackjack
    
    if IN_PLAY == False:
        print "press the button 'deal a card'"
        outcome = "press the button 'deal a card'"
    else:
        player_hand.add_card(my_deck.deal_card())
        print player_hand
        print "the value of this hand >> ", player_hand.get_value()
        if player_hand.get_value() > 21:
            print "you're broke, busted, and disgusted!"
            outcome = "you're broke, busted, and disgusted!"
            score -= 1
            losses += 1
            IN_PLAY = False
        elif player_hand.get_value() == 21:
                print "BLACKJACK!!!! player wins!!!!"
                outcome = "BLACKJACK!!!! player wins!!!!"
                IN_PLAY = False
                score += 1
                wins += 1
                blackjack += 1
        else:    
            print "keep playing"
            outcome = "hit or stand?"
            print " "

            
# code for standing
def stand():
    global IN_PLAY, player_hand, dealer_hand, outcome
    global score, wins, losses, dealer_card
    
    
    if IN_PLAY == False:
        print "press the button 'deal a card'"
        outcome = "press the button 'deal a card'"
    else:
        print " "
        print "player stands..."
        dealer_card = True
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(my_deck.deal_card())
            print dealer_hand
            print "the value of this hand >> ", dealer_hand.get_value()
            print " "
        if dealer_hand.get_value() == 21:
            print "BLACKJACK!!! dealer wins!!!"
            outcome = "BLACKJACK!!! dealer wins!!!"
            score -= 1
            losses += 1
        elif dealer_hand.get_value() > 21:
            print "dealer is broke, busted, and disgusted! the player wins!"
            outcome = "dealer is broke, busted, and disgusted! the player wins!"
            score += 1
            wins += 1
        elif dealer_hand.get_value() < player_hand.get_value():
            print "player wins!"
            outcome = "player wins!"
            score += 1
            wins += 1
        elif dealer_hand.get_value() == player_hand.get_value():
            print "it's a tie but the dealer wins!"
            outcome = "it's a tie but the dealer wins!"
            score -= 1
            losses += 1
        else:
                print "dealer wins!"
                outcome = "dealer wins!"
                score -= 1
                losses += 1
        IN_PLAY = False
            

# draw the cards
def draw(canvas):
    global dealer_hand, player_hand
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('BLACKJACK', (170, 50), 20, 'White')
    canvas.draw_text('Dealer', (80, 230), 20, 'White')
    if not dealer_card:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0], 240 + CARD_BACK_CENTER[1]], CARD_SIZE)
    dealer_hand.draw(canvas, [20, 240])
    canvas.draw_text('Player', (80, 400), 20, 'White')
    player_hand.draw(canvas, [20, 410])
    canvas.draw_text(str(outcome), (130, 530), 20, 'White')
    canvas.draw_text('score: '+str(score), (400, 100), 20, 'White')
    canvas.draw_text('wins: '+str(wins), (400, 130), 20, 'White')
    canvas.draw_text('losses: '+str(losses), (400, 160), 20, 'White')
    canvas.draw_text('blackjack: '+str(blackjack), (400, 190), 20, 'White')
    
    
# code for the frame
frame = simplegui.create_frame("simple test", 600, 600)
frame.set_canvas_background('Black')
frame.add_button("Deal a card", deal)
frame.add_button("hit me!", player_hit)
frame.add_button("stand", stand)
frame.set_draw_handler(draw)

deal()
frame.start()

