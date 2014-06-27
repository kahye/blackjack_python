from blackjack_util import * 
# Main blackjack game function
# Kahye Song 2014 April 20

# Welcome message
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")	
print(" Welcome to the BlackJack Casino ")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")	
print("   Rules: ")
print(" - This is a single player game. However, when you decide to split, you can have multiple hands.")
print(" - You start with 100 chips and you have to bet at least one chip each hand.")
print(" - When you split, you are doubling the initial bet. (or by the multiplicity of the hands)")
print(" - The payout ratio is 1:1, meaning when you win, you earn twice of your bet and when you push you earn exactly as you bet.")
print(" - You can choose the number of decks.")
print(" - You can choose whether the dealer can have soft or hard ace.")


num_decks = ask_int_range_question("How many decks do you want?",1,6)
hit_soft_ace = ask_yesno_question("Does the dealer hit the soft ace?")

budget = 100

while True:

	# define a deck
	deck = Deck(num_decks)

	# define a dealer
	dealer = Hand("Dealer")

	# define a single hand
	hand1 = Hand("Hand1")

	# ask for the bet
	bet = ask_bet(hand1.name,budget)

	# deal out two cards to the hand and the dealer
	deck.deal([hand1,dealer],2)

	# face down the first card of the dealer and face down.
	dealer.cards[0].face_down = True

	# check whether the hand got double and add as many doubles as possible
	hands = split_hand(hand1,deck)

	# update the bet for each hand and adjust budget accordingly
	[hands,budget] = update_bet_budget(hands,bet,budget)

	# ennumerate hands for naming
	fix_hand_names(hands)	

	#------------------#
	# PLAYERS PLAYS
	#------------------#
	i=0 # ennumerate on hands
	for hand in hands:
		print("==============================================")
		print(hand.name + ", Let's start!")
		print("Dealer's cards are: ")
		print(dealer)

		# Play a single round of game for a hand and update the hand status after playing
		hands[i] = hands_game(hand,deck)

		i += 1
	print("==============================================")
	#------------------#
	# DEALERS TURN
	#------------------#
	# face up the dealer's top card
	dealer.cards[0].face_down = False

	# Play a single round of dealer's game
	dealers_game(dealer,deck,hit_soft_ace)

	#------------------#
	# ANNOUNCE OUTCOME
	#------------------#
	# check who won and what is the total winning
	hands_winning = declare_winner(hands,dealer)
	# adjust the budget by the winning
	budget +=hands_winning
	# announce the new budget
	print("==============================================")
	print("You won " + str(hands_winning) + " chips, and your total budget including this winning is " + str(budget) +" chips.")
	print("==============================================")
	# if any budget is remaining, ask the player whether to play again
	if budget>0:		
		replay_answer = ask_yesno_question("Do you play again?")
		if replay_answer == "N":
			print("Thank you for playing at BlackJack Casino. Good bye!")
			break
	# if out of the budget, quit
	else:
		print("You are out of budget. Thank you for playing at BlackJack Casino. Good bye!")
		break
