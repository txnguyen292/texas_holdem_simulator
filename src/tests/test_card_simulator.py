import sys
import pytest
from config import CONFIG
sys.path.insert(0, str(CONFIG.src))
from card_simulator import Card_Deck

card_deck = Card_Deck()

@pytest.fixture
def card_deck():
    card_deck = Card_Deck()
    return card_deck

def test_cards(card_deck):
    assert len(card_deck.cards) == 52, "Reimplement your card_deck"

def test_shuffle(card_deck):
    test_cards = card_deck.cards.copy()
    assert test_cards != card_deck.shuffle().cards, "Reimplement your shuffle methods!"

def test_shuffle_seed(card_deck):
    test_cards1 = card_deck.cards.copy()
    card_deck1 = Card_Deck()
    assert test_cards1 != card_deck.shuffle(seed=124).cards, "Reimplement your seed in shuffle!"

def test_deal(card_deck):
    first_card = card_deck.cards[-1]
    first_dealt_card = card_deck.deal()
    assert first_card == first_dealt_card, f"You're comparing {first_card} vs. {first_dealt_card}"
    assert len(card_deck.cards) == 51, "Reimplement your deal method"

if __name__ == "__main__":
    print(card_deck.cards)
    print(card_deck.SUITS)
