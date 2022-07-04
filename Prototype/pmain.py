import random

RANKS = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
SUITS = ["Spades", "Hearts", "Clubs", "Diamonds"]

print(RANKS)


class Card:
    def __init__(self, rank, suit, dealed=False) -> None:
        self.rank = rank
        self.suit = suit
        self.dealed = False

    def __repr__(self) -> str:
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self, player_count=2) -> None:
        self.player_count = player_count
        self.set_of_cards = player_count + 1
        self.cards = []

    def create_deck(self):
        for i in range(self.set_of_cards):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append(Card(rank, suit))

    def shuffle(self):
        cards = self.cards.copy()
        self.cards = random.choices(cards, k=len(cards))

    def deal_card(self):
        card = self.cards.pop()
        return card


Deck1 = Deck()
Deck1.create_deck()
Deck1.shuffle()

for card in Deck1.cards:
    print(card)
print("--------------------------------------------------------------------------")
print(Deck1.deal_card())
print(Deck1.deal_card())
