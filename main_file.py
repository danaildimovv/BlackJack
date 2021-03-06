"""
This is the main py script for the Black Jack game
"""

import random
from getch1 import *
import os
import time


ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
         "Nine", "Ten", "Jack", "Queen", "King", "Ace")			

suits = ("Hearts", "Diamonds", "Spades", "Clubs")

values = {"Two":2, "Three":3, "Four":4, "Five":5, "Six":6, "Seven":7, "Eight":8,
        "Nine":9, "Ten":10, "Jack":10, "Queen":10, "King":10, "Ace":11}

playing = True


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.deck = []				# empty list for the cards to fill

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))

    def __str__(self):
        whole_deck = ""

        for card in self.deck:
            whole_deck = whole_deck + card + ", "

        return whole_deck

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        card = self.deck.pop()
        return card


class Hand:
    def __init__(self):
        self.cards_in_hand = []			# an empty list for the cards
        self.value = 0
        self.aces = 0

    def __str__(self):
        hand = ""

        for card in self.cards_in_hand:
            hand += str(card) + "\n"
        return hand

    def add_card(self, card):
        self.cards_in_hand.append(card)
        self.value += values[card.rank]
        
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1            
        


class Chips: 
    def __init__(self):
        self.total = 1000
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            player_bet = int(input("Place your bet: \n"))
            if player_bet > chips.total:
            	player_bet = int(input("Place a bet that you can afford:"))
            time.sleep(1)
        except:
            print("This should be a number.")
            continue
        else:	
            chips.bet = player_bet
            if chips.total <= 0:
                print("You have no chips")
            break    

def check_value(player_hand, dealer_hand, chips):
    global playing
    if player_hand.value > 21:
        show_full_hands(player_hand, dealer_hand)
        print("You busted over 21, You lost")
        chips.lose_bet()
        message(chips, "lost")
        playing = False
        
        

def show_hands(player_hand, dealer_hand):
    os.system("cls")
    print(f"Player cards:\n{player_hand}Value: {player_hand.value}\n")
    time.sleep(1)
    show_dealer_hand = str(dealer_hand.cards_in_hand[0]) + "\n" + "Second card: Hidden\nValue: Hidden"
    print(f"Dealer cards:\n{show_dealer_hand}")

def show_full_hands(player_hand, dealer_hand):
    print(f"{player_hand}Value: {player_hand.value}\n")
    print(f"{dealer_hand}Value: {dealer_hand.value}\n")

def hit_or_stay(deck, hand, chips):
    print("\nPress any key if you want to hit. Press Escape if you want to stay\n")
    player_respond = getch()
    global playing

    if ord(player_respond) == 27:
        playing = False
        os.system("cls")
    else:
        next_card = deck.deal()
        hand.add_card(next_card)
        hand.adjust_for_ace()
        playing = True
        os.system("cls")

def dealer_hit(deck, hand):
    next_card = deck.deal()
    hand.add_card(next_card)
    
def initial_fill(deck, hand):
    for card in range (0, 2):
        card = deck.deal()
        hand.add_card(card)

def message(chips, result):
    print(f"You {result} {chips.bet}")
    print(f"Chips available: {chips.total}")


if __name__ == "__main__":

    all_the_chips = Chips()
    
    while True:
        print("Welcome to your Black Jack game! ")

        main_deck = Deck()                          # creating the deck
        main_deck.shuffle()                         # shuffling the deck

        player_hand = Hand()                        # creating the player hand
        dealer_hand = Hand()                        # creating the dealer hand

        initial_fill(main_deck, player_hand)
        initial_fill(main_deck, dealer_hand)        

        take_bet(all_the_chips)

        while playing:
            show_hands(player_hand, dealer_hand)    # showing the hands 
            hit_or_stay(main_deck, player_hand, all_the_chips)     # asking for hit or bust
            check_value(player_hand, dealer_hand, all_the_chips)                # check if the player reached 21            

        if player_hand.value < 21:
            while dealer_hand.value < 17:
                dealer_hit(main_deck, dealer_hand)
                time.sleep(1)
                os.system("cls")
                time.sleep(1)
                show_full_hands(player_hand, dealer_hand)

            os.system("cls")     

            if dealer_hand.value > 21:
                show_full_hands(player_hand, dealer_hand)
                all_the_chips.win_bet()
                message(all_the_chips, "won")
            else:
                show_full_hands(player_hand, dealer_hand)
                if player_hand.value > dealer_hand.value:
                    print("You win")
                    all_the_chips.win_bet()
                    message(all_the_chips, "won")
                elif player_hand.value == dealer_hand.value:
                    print("It's a tie")
                else:
                    print("You lose")
                    all_the_chips.lose_bet()
                    message(all_the_chips, "lost")

            if all_the_chips.total <= 0:
                print("You ran out of money")
                break

            print("\nDo you want to play again? Press any key if yes, press Escape if you want to leave.\n")
            new_game = getch()
            if ord(new_game) == 27:
                break 
            else:
                playing = True

        else:
            break

                                        

        
            


   
   
