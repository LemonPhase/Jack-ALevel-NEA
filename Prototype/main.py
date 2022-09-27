import random

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["Spades", "Hearts", "Clubs", "Diamonds"]
RANK_VALUES = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
               "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}



class Card:
    def __init__(self, rank, suit, value, dealed=False) -> None:
        self.rank = rank
        self.suit = suit
        self.value = value
        self.dealed = False

    def __repr__(self) -> str:
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self, player_count=2) -> None:
        self.player_count = player_count
        self.set_of_cards = player_count + 1
        self.cards = []
        self.dealt_cards = []

    def __repr__(self) -> str:
        deck_comp = ""
        for card in self.cards:
            deck_comp += "\n" + card.__str__()
        return f"The deck has: {deck_comp}"

    # No. of player +1 new set of cards
    def create_deck(self):
        for i in range(self.set_of_cards):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append(Card(rank, suit, RANK_VALUES[rank]))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        card = self.cards.pop(0)
        self.dealt_cards.append(card)
        return card


class Player:
    def __init__(self, name, id, token) -> None:
        self.name = name
        self.id = id
        self.__token = int(token)
        self.hand = []
        self.ranks = []
        self.value = 0
        self.aces = 0
    
    def __repr__(self) -> str:
        return f"{self.name} has {len(self.hand)} cards."
    
    def add(self, card):
        self.hand.append(card)
        self.value += card.value
    
    def cal_value(self):
        self.value = 0
        for card in self.hand:
            self.value += card.value
        return self.value
    
    def rank(self):
        ranks = [card.rank for card in self.hand]
        self.ranks = ranks
        return ranks

    def ace(self):
        for card in self.hand:
            if card.rank == 'A':
                card.value = 1
            break
        value = self.cal_value()
    
    def is_bj(self):
        if "A" in self.rank() and ("K" in self.rank() or "Q" in self.rank() or "J" in self.rank() or "10" in self.rank()):
            return True




deck1 = Deck()
deck1.create_deck()
deck1.shuffle()


def round():

    # Initial deal
    dealer = Player("Dealer", "000000", 100)
    player1 = Player("P1", "000001", 100)
    for i in range(2):
        player1.add(deck1.deal())
        dealer.add(deck1.deal())
    

    # Player's turn
    print(player1.hand)

    
    choice = ""
    print(f"Dealer's first card: {dealer.hand[0]}")
    if player1.is_bj():
        print("Blackjack!")

    while choice != "S" and player1.value <= 21:
        choice = input("Hit or stand? (H/S): ").upper()
        if choice == "H":
            card = deck1.deal()
            print(card)
            player1.add(card)
            print(f"{player1.hand} Value: {player1.value}")

        elif choice == "S":
            break

    if player1.value > 21:
        print("Player bust, dealer won.")
        return


    # Dealer's turn
    print(dealer.hand)
    while dealer.value < 17:
        dealer.add(deck1.deal())
        print(f"{dealer.hand} Value: {dealer.value}")
    
    if dealer.value > 21:
        print("Dealer bust, player won.")
        return
    
    if player1.value > dealer.value:
        print("Player won")
    elif player1.value < dealer.value:
        print("Dealer won")
    else:
        print("Draw")
    
    print("End of game")






# # Test deck, shuffle, player and deal
# test_deck = Deck()
# test_deck.create_deck()
# test_deck.shuffle()
# test_player1 = Player("Bob", "123", 500)
# test_player2 = Player("Amy", "456", 100)
# for i in range(2):
#     test_player1.add(test_deck.deal())
#     test_player2.add(test_deck.deal())

# # print(test_player1)
# # print(test_player2)
# print(test_player1.hand)
# print(test_player1.value)
# print(test_player2.hand)
# print(test_player2.value)

# # Test ace value adaptation
# for card in test_player1.hand:
#     if card.rank == "A":
#         test_player1.add(test_deck.deal())
#     if test_player1.cal_value() > 21:
#         print(test_player1.cal_value())
#         test_player1.ace()

# print(test_player1.hand)
# print(test_player1.value)

round()