import sys
import pytest
import numpy as np
from typing import List, Union, Literal, Set
from config import CONFIG

sys.path.insert(0, str(CONFIG.src))

from card_simulator import Card_Deck
from Hands_generator import Hands_Generator

@pytest.fixture
def hands_generator():
    hands_generator = Hands_Generator()
    return hands_generator

@pytest.fixture
def card_deck():
    card_deck = Card_Deck()
    return card_deck

@pytest.fixture
def random_card_list(card_deck):
    random_ind = np.random.randint(0, 52, 1)[0]
    random_card = card_deck.cards[random_ind]
    random_card_list = [random_card]
    return random_card_list

def test_get_straight(hands_generator, random_card_list):
    for _ in range(1000):
        card_deck = Card_Deck()
        straight = hands_generator.get_straight(random_card_list, card_deck)
        assert len(straight) == 7, f"Must only generate 7 cards. Got {straight} of length {len(straight)}."
        another_random_card = card_deck.cards[-1]
        #straight_lower = hands_generator.get_straight([another_random_card], card_deck, greater=False)
        #sorted_straight_lower = sorted(straight, key=lambda x: x.value)
        count = 1
        sorted_straight = sorted(straight, key=lambda x: x.value)
        current_card = sorted_straight[0]
        for idx, card in enumerate(sorted_straight):
            if idx > 0 and card.value - 1 == current_card.value:
                current_card = card
                count += 1
        assert count >= 5, f"Cards: {sorted_straight}. Length of cards: {len(sorted_straight)}"



if __name__ == "__main__":
    pass




