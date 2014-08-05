# Collection of classes and functions for the blackjack game
# Kahye Song 2014 April 20
# edit to try commit 8/4/2014
# my edit 1
# my edit 2

import random
class Card(object):
	""" Define standard 52 cards. """
	POINTS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]				# points for each rank
    	RANKS = ["A", "2", "3", "4", "5", "6", "7","8", "9", "10", "J", "Q", "K"]
    	SUITS = ["C", "D", "H", "S"]

    	def __init__(self, rank, suit, face_down = False):
        	self.rank = rank
        	self.suit = suit		
		self.points = self.POINTS[self.RANKS.index(rank)]
		self.face_down = face_down 		# for dealer's face down card

    	def __str__(self):
		if not self.face_down:
        		rep = "[" + self.rank + self.suit + "]"
		else:
			rep = "[ FACE DOWN CARD ]"	# do not show any info if face down
        	return rep
    	def flip(self):
        	self.face_down = not self.face_down
################################################
class CardHandler(object):
    	""" Define a basic card handling agent. """
    	def __init__(self):
        	self.cards = []
    	def __str__(self):
        	if self.cards:
           		rep = ""
           		for card in self.cards:
               			rep += str(card) + "  "
        	else:
            		rep = "No cards"
        	return rep
  	def clear(self):
        	self.cards = []
    	def add(self, card):
        	self.cards.append(card)
    	def remove(self, card):
        	self.cards.remove(card)	
################################################
class Hand(CardHandler):
    	""" Define a hand that has a name and other game relavant features. """
    	def __init__(self,name):
		self.name = name		# name for display purpose
        	self.cards = []			# cards in the hand
		self.status = "alive" 		# for determining final outcome ("alive","blackjack","busted","stand")
		self.points = 0 		# sum of the points of cards
		self.soft_ace = False 		# determine whether my ace is soft or not
		self.bet = 0 			# amount chips of bet the hand is betting
		self.split = False 		# whether this is a split hand
    	def __str__(self):
		""" Display cards and the total points if face up. """
        	if self.cards:
           		rep = ""
			any_face_down = False
           		for card in self.cards:
               			rep += str(card) + "  "
				if card.face_down:
					any_face_down = True
			if not any_face_down:				
				rep += " ( sum = "
				rep += str(self.points)
				rep += " )"
        	else:
            		rep = "No cards"
        	return rep
	def calculate_points(self):
		""" Calculate the total points in the hand. """
		points = 0
		num_ace = 0
		soft_ace = False
		for card in self.cards:
			points = points + card.points
			if card.rank == "A":
				num_ace += 1
		if num_ace > 0:
			# if the hand contains ace, check whether it is closer to 21 
			# and not exceeding 21 by counting it as 11.
			alt_points = points + 10
			if alt_points<=21:
				soft_ace = True
				points = alt_points
		self.points = points
		self.soft_ace = soft_ace
	def is_blackjack(self):
		""" Check whether my hand has blackjack. only called at the beginning of each round. """
		self.calculate_points()
		tf_blackjack = False	
		if (self.points == 21) & (not self.split):
			tf_blackjack = True
			self.status = "blackjack"
		return tf_blackjack
	def got_double(self):
		""" Check whether my hand has two card with same points for splitting. """
		tf_double = False
		card1 = self.cards[0]
		card2 = self.cards[1]
		if card1.points == card2.points:
			tf_double = True
		return tf_double
    	def add(self, card):
		""" Add a card to the hand and update the total points. """
        	self.cards.append(card)
		self.calculate_points()
################################################
class Deck(CardHandler):
	""" A deck of playing cards. """
    	def __init__(self,num_decks = 1):
		self.cards = []
		self.num_decks = num_decks
        	self.populate()
		self.shuffle()
	def populate(self):
		""" Populate a standard deck in order and by multiplicity. """
		for i in range(self.num_decks):
			for suit in Card.SUITS:
				for rank in Card.RANKS:
        				self.add(Card(rank, suit))
	def shuffle(self):      		
        	random.shuffle(self.cards)
	def deal(self, hands, num_cards = 1):
		""" Give out a card to hands in order until all hands have the number of card. """
		for i in range(num_cards):
            		for hand in hands:
                		if self.cards:
                   			top_card = self.cards[0]
                   			self.cards.remove(top_card)
					hand.add(top_card)
                		else:
                    			print("Deck is empty. Quit the game and increase the number of decks.")
################################################
def ask_yesno_question(phrase):
	""" Ask yes no question until getting a valid answer. """
	answer = "M"
	while not ( (answer == "Y") | (answer == "N") ):
		answer = raw_input(phrase + " (Y or N) :")
	return answer
################################################
def ask_int_range_question(phrase,min_value,max_value):
	""" Ask integer within a range until getting a valid answer. """
	answer = min_value-100
	while not (( answer >= min_value ) & ( answer <= max_value )):
		answer = input(phrase + " (between "+str(min_value)+" and "+str(max_value)+") :")
	return answer
################################################
def declare_winner(hands,dealer):
	""" Given the status of all hands and the dealer declare the winner and calculate player's winning. """
	blackjack_winning = 0
	blackjack_hands = ""
	all_standing_hands = "" # both standing and blackjack

	# check any hand has blackjack or standing position
	for hand in hands:
		if hand.status == "blackjack":
			blackjack_hands += (hand.name + " ")			
			blackjack_winning += hand.bet
			all_standing_hands += (hand.name + " ")
		elif hand.status == "stand":
			all_standing_hands += (hand.name + " ")		
	# initilize the total winning
	hands_winning = 0		
	if dealer.status == "blackjack":
		# if the dealer has blackjack, only the hands with blackjack has push and receiving the original bet. 		
		if len(blackjack_hands)>0:		
			print("push between Dealer and "+blackjack_hands)			
			hands_winning += blackjack_winning
		else:
			# Otherwise all lose the bet.
			print("Dealer wins!")		
			# no winning				
	elif dealer.status == "stand":
		# those who have blackjack or those are standing and higher points than the dealer wins double bet.
		if len(blackjack_hands)>0:
			winning_hands = blackjack_hands + " "
		else:
			winning_hands = ""
		hands_winning += blackjack_winning
		push_hands = ""
		for hand in hands:
			if hand.status == "stand":
				# if the hand is standing and has the higher points
				if hand.points>dealer.points:		
					winning_hands += (hand.name + " ")
					hands_winning += hand.bet*2		
				# if tie between the dealer, only gets the bet back. no winning
				elif hand.points == dealer.points:
					push_hands += (hand.name  + " ")					
					hands_winning += hand.bet		
		if len(winning_hands)>0:
			print(winning_hands+ " won by points!")
		if len(push_hands)>0:
			print("push between Dealer and "+push_hands)
		# if nobody has higher points than the dealer
		if (len(winning_hands)==0) & (len(push_hands)==0):			
			print("Dealer wins!")	
	else:
		# if the dealer busts all standing and blackjack hands win
		if len(all_standing_hands)>0:
			print(all_standing_hands + " won!")
		else:
			# if nobody is standing, the dealer wins 
			print("Dealer wins!")
		# when the dealer busts, everyone wins except those busted
		for hand in hands:
			if all_standing_hands.find(hand.name)>-1:
				hands_winning += hand.bet*2		
	return hands_winning
################################################
def split_hand(myhand,deck):
	""" Handle splitting hands. Recursively split hands until no hands with same points are found. """
	# default: return the original hand
	updated_hands = [myhand]	
	# check whether I have two cards with same points
	if myhand.got_double():
		print(myhand.name+", YOU GOT DOUBLE!!!!! Your cards are:")
		print(myhand)		
		split_answer = ask_yesno_question("Do you want to split????")
		if split_answer == "Y":
			# remove a card from the original hand and add it to the other hand
			top_card = myhand.cards[0]
			myhand.remove(top_card)
			myhand.split = True 		# check split true for handling blackjacks
			deck.deal([myhand])			

			newhand = Hand("new")
			newhand.add(top_card)
			newhand.split = True		
			deck.deal([newhand])		

			# announce new hands			
			print("Your first split hand is ")
			print myhand
			print("Your second split hand is ")
			print newhand

			# check whether the new hands can be split
			myhand_update = split_hand(myhand,deck)
			newhand_update = split_hand(newhand,deck)

			# return the updated hands
			updated_hands = newhand_update
			# copy over the other hands to the final return variable
			for single_hand in myhand_update:
				updated_hands.append(single_hand)
	return updated_hands
################################################
def fix_hand_names(hands):
	""" Enumerate hands for naming them. """
	for i in range(len(hands)):
		hands[i].name = "Hand"+str(i)
################################################
def update_bet_budget(hands,bet,budget):
	""" Assign the same bet to all hands. """
	# update the bet of each hand
	for i in range(len(hands)):
		hands[i].bet = bet
	# adjust budget after betting
	budget -= bet*len(hands)
	return hands, budget

################################################
def ask_bet(hand_name,budget):
	""" Ask the player to bet. """
	bet = ask_int_range_question(hand_name +", How many chips do you want to bet?",1,budget)
	return bet
################################################
def hands_game(hand,deck):
	""" Main game function for a single hand play """
	# if blackjack, announce and quit
	if hand.is_blackjack():
		print("Your cards are: ")
		print(hand)
		print("You got blackjack!")
	else:	
		# while the player is not busted nor stop hitting
		while hand.status == "alive":
			# show the current cards
			print("Your cards are: ")
			print(hand)
			# check whether the hand is busted
			if hand.points>21:
				hand.status = "busted"
				print("You are busted!")
			# stand automatically if the hand has 21 points
			elif hand.points == 21:
				hand.status = "stand"
			# otherwise ask for hitting
			else:
				hit_answer = ask_yesno_question("Do you want to hit?")
				# if the hand stops hitting, update status
				if hit_answer == "N":
					hand.status = "stand"
				# if hitting, get a card from the deck.
				else:
					deck.deal([hand])
	return hand
################################################
def dealers_game(dealer,deck,hit_soft_ace):
	""" Main game function for the dealer """
	# check whether the dealer has blackjack
	if dealer.is_blackjack():
		print("Dealer's cards are: ")
		print(dealer)
		print("Dealer got blackjack!")
	else:
		# as long as the dealer is not busted nor standing
		while dealer.status == "alive":			
			print("Dealer's cards are: ")
			print(dealer)
			# check whether the hand is busted
			if dealer.points>21:
				dealer.status = "busted"
				print("Dealer is busted!")
			# if the dealer reches 17 not exceeding 21
			elif dealer.points>=17:
				# check whether it is exactly 17 with soft ace and whether it is getting hit 
				if (dealer.points==17) & dealer.soft_ace & (hit_soft_ace == "Y"):
					# if true, get hit
					deck.deal([dealer])
				else:
					dealer.status = "stand"
					print("Dealer stands.")				 		
			# if the dealer has points less than 17, it should get hit
			else:
				deck.deal([dealer])

