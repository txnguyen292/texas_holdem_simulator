"""Test Hands methods"""
import sys
import numpy as np
import pytest

from typing import List
from config import CONFIG
sys.path.insert(0, str(CONFIG.src))
from Hands import Hands
from card_simulator import Card_Deck

#================================== HELPER FUNCTIONS ========================================
def get_straight(straights: List[Card_Deck.Card], cards: Card_Deck, greater: bool=True) -> List[Card_Deck.Card]:
    """Get 5 consecutive cards in a deck with a given card

    Args:
        straights (List[Card_Deck.Card]): first card
        cards: (List[Card_Deck.Card]): deck of card
        greater (bool, optional): whether to get bigger or lower consecutive numbers. Defaults to True.

    Returns:
        Card_Deck: a list of consecutive numbers
    """
    if greater:
        while len(straights) <= 5:
            current_count = straights[-1].value + 1
            for idx, card in enumerate(cards.cards):
                if card.value == current_count:
                    straights.append(card)
                    break
    else:
        while len(straights) <= 5:
            if straights[0].value == 1:
                current_count = 13
            else:
                current_count = straights[-1].value - 1
            for idx, card in enumerate(cards.cards):
                if card.value == current_count:
                    straights.append(card)
                    break
    for _ in range(2):
        straights.append(cards.deal())

def get_same_suits(same_suits: List[Card_Deck.Card], cards: Card_Deck)-> List[Card_Deck.Card]:
    """Return a list that contains five cards of the same suit

    Args:
        same_suits (List[Card_Deck.Card]): list that contain the first card
        cards (Card_Deck): deck of cards

    Returns:
        List[Card_Deck.Card]: list that contain at least 5 cards of the same suit
    """
    first_suit = same_suits[0].suit
    while len(same_suits) < 5:
        for idx, card in enumerate(cards.cards):
            if card.suit == first_suit:
                same_suits.append(card)
    for _ in range(2):
        same_suits.append(cards.deal())
    return same_suits

def get_three_of_a_kind(three_of_a_kinds: List[Card_Deck.Card], cards: Card_Deck) -> List[Card_Deck.Card]:
    """Return a a list that contains five cards of three of a kind

    Args:
        three_of_a_kinds (List[Card_Deck.Card]): [description]
        cards (Card_Deck): [description]

    Returns:
        List[Card_Deck.Card]: [description]
    """
    
#======================================== END ===============================================

@pytest.fixture
def card_deck():
    card_deck = Card_Deck()
    return card_deck

@pytest.fixture
def hand():
    hand = Hands()
    return hand

def test_is_flush(card_deck, hand):
    card_deck.shuffle()
    random_ind = np.random.randint(0, 52, 1)[0]
    random_card = card_deck.cards[random_ind]
    five_of_same_suits = get_same_suits([random_card], card_deck)
    five_different_suits = [card for card in card_deck.cards if card.suit != random_card.suit][0:7]
    assert hand._is_flush(five_of_same_suits), f"Checking suit of {five_of_same_suits}"
    assert not hand._is_flush(five_different_suits), f"Checking suit of {five_of_different_suits}"

def test_is_straight(card_deck, hand):
    card_deck.shuffle()
    random_ind = np.random.randint(0, 52, 1)[0]
    random_card = card_deck.cards[random_ind]
    straights1 = [random_card]
    straights2 = [random_card]
    not_straights = [random_card]
    if random_card.value < 5:
        # can only check straight greater than current value
        if random_card.value != 1:
            get_straight(straights1, card_deck)
            assert hand._is_straight(straights1), f"Checking straight of {straights1}"
        else:
            get_straight(straights1, card_deck)
            assert hand._is_straight(straights1), f"Checking straight of {straights1}"
            get_straight(straights2, card_deck)
            assert hand._is_straight(straights2), f"Checking straight of {straights2}"
    else:
        # check both bigger and smaller consecutive numbers
        get_straight(straights1, card_deck)
        assert hand._is_straight(straights1), f"Checking straight of {straights1}"
        get_straight(straights2, card_deck, False)
        assert hand._is_straight(straights2), f"Checking straight of {straights2}"

def test_is_highcard(card_deck, hand):
    card_deck.shuffle()
    random_ind = np.random.randint(0, 52, 1)[0]
    random_card = card_deck.cards[random_ind]
    five_of_same_suits = [card for card in card_deck.cards if card.suit == random_card.suit]
    straights = [random_card]
    get_straight(straights, card_deck)
    assert not hand._is_highcard(five_of_same_suits), "Flush is not high card!"
    assert not hand._is_highcard(straights), "Straight is not high cards!"
    # assert hand._is_highcard()

def test_is_pair(card_deck, hand):
    card_deck.shuffle()
    random_ind = np.random.randint(0, 52, 1)[0]
    random_card = card_deck.cards[random_ind]
    five_of_same_suits = [card for card in card_deck.cards if card.suit == random_card.suit]
    pass

    
if __name__ == "__main__":
    print(np.random.randint(0, 53, 1))