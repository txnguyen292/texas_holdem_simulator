from card_simulator import Card_Deck
from Hands import Hands

class Texas_Holdem(Card_Deck, Hands):
    """Implement a texas holdem simulator"""

    def __init__(self):
        super(Texas_Holdem, self).__init__()
        super(Hands, self).__init__()

if __name__ == "__main__":
    pass