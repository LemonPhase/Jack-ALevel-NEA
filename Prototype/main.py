import random

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["Spades", "Hearts", "Clubs", "Diamonds"]
RANK_VALUES = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
               "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}
print(RANKS)


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

    def create_deck(self):
        for i in range(self.set_of_cards):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append(Card(rank, suit, RANK_VALUES[rank]))

    def shuffle(self):
        cards = self.cards.copy()
        self.cards = random.choices(cards, k=len(cards))

    def deal_card(self):
        card = self.cards.pop(0)
        self.dealt_cards.append(card)
        return card


class Player:
    def __init__(self, user_name, id, token) -> None:
        self.user_name = user_name
        self.id = id
        self.__token = token
        self.hand = []

    def count(self):
        count = 0
        for card in self.hand:
            if type(card) == int:
                count += card


# Test
Deck1 = Deck()
Deck1.create_deck()
Deck1.shuffle()

for card in Deck1.cards:
    print(card)
print("--------------------------------------------------------------------------")
print(Deck1.deal_card())
print(Deck1.deal_card())
print(Deck1.dealt_cards)
