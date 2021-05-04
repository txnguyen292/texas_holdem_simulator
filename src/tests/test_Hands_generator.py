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
        card_deck.shuffle()
        straight = hands_generator.get_straight(random_card_list, card_deck)
        assert len(straight) == 7, f"Must only generate 7 cards. Got {straight} of length {len(straight)}."
        count = 1
        sorted_straight = sorted(straight, key=lambda x: x.value)
        current_card = sorted_straight[0]
        for idx, card in enumerate(sorted_straight):
            if idx > 0 and card.value - 1 == current_card.value:
                current_card = card
                count += 1
        assert count >= 5, f"Cards: {sorted_straight}. Length of cards: {len(sorted_straight)}"

def test_get_same_value(hands_generator, random_card_list, card_deck):
    for _ in range(1000):
        card_deck = Card_Deck()
        card_deck.shuffle()
        one_pair = hands_generator.get_same_value(random_card_list, card_deck, type_of_pair="one")
        one_pair_unique = set([x.value for x in one_pair])
        one_pair_suit = set([x.suit for x in one_pair])
        assert len(one_pair) == 2, "One pair must contain two cards!"
        assert len(one_pair_unique) == 1, "One pair must contain only 1 unique value!"
        assert len(one_pair_suit) == 2, "One pair must contain 2 differnt suits!"
        two_pair = hands_generator.get_same_value(random_card_list, card_deck, type_of_pair="two")
        two_pair_unique = set([x.value for x in two_pair])
        two_pair_suits = set([x.suit for x in two_pair])
        assert len(two_pair) == 4, "Two pairs must contain 4 cards!"
        assert len(two_pair_unique) == 2, "Two pair must contain 2 unique values!"
        assert len(two_pair_suits) >= 2, "Two pair must contain at least 2 different suits!"
        three_of_a_kind = hands_generator.get_same_value(random_card_list, card_deck, "three")
        three_of_a_kind_unique = set([x.value for x in three_of_a_kind])
        three_of_a_kind_suits = set([x.suit for x in three_of_a_kind])
        assert len(three_of_a_kind) == 3, "Three of a kind must contain 3 cards!"
        print(three_of_a_kind)
        assert len(three_of_a_kind_unique) == 1, "Three of a kind must contain only 1 unique value!"
        assert len(three_of_a_kind_suits) == 3, "Three of a kind must contain 3 suits!"
        four_of_a_kind = hands_generator.get_same_value(random_card_list, card_deck, "four")
        four_of_a_kind_unique = set([x.value for x in four_of_a_kind])
        four_of_a_kind_suit = set([x.suit for x in four_of_a_kind])
        assert len(four_of_a_kind) == 4, "Four of a kind must contain 4 cards!"
        assert len(four_of_a_kind_unique) == 1, "Four of a kind must contain only 1 unique value"
        assert len(four_of_a_kind_suit) == 4, "Four of a kind must contain 4 suits!"


if __name__ == "__main__":
    pass




