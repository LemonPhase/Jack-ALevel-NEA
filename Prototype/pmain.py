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

    def shuffle_cards(self):
        for i in range(self.set_of_cards):
            for suit in SUITS:
                for rank in RANKS:
                    self.cards.append(Card(rank, suit))


Deck1 = Deck()
Deck1.shuffle_cards()

for card in Deck1.cards:
    print(card)
