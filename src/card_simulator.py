"""Implement a card simulator"""
from typing import Tuple, Union, List, Dict, NamedTuple
from collections import namedtuple
import numpy as np
import random
from config import CONFIG



class Card_Deck:
    """Implement a card deck with shuffle, 
    deal methods"""
    SUITS: Dict[str, str] = {"heart": "\u2665", "diamonds": "\u2666", "spades": "\u2660", "clubs": "\u2663"}
    Card = namedtuple("Card", ["value", "suit"])

    def __init__(self) -> None:
        _royals = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
        self.cards: List[Card] = [Card_Deck.Card(value, suit) for value in range(1, 14) for suit in Card_Deck.SUITS]

    def shuffle(self, seed: int=123) -> None:
        """shuffle the cards with seed""
        Args:
            seed (int, optional): seed to shuffle. Defaults to 123.
        """
        np.random.seed(seed)
        np.random.shuffle(self.cards)
        self.cards = self.cards[::-1]
        return self

    def deal(self, shuffle: bool=False) -> Card:
        """Deal the card on top of the deck

        Args:
            shuffle (bool, optional): Whether to shuffle before dealing or not. Defaults to False.

        Returns:
            [Card]: a card
        """
        if shuffle:
            self.shuffle()
        return self.cards.pop()


if __name__ == "__main__":
    pass
