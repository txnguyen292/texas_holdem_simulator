"""Implement a Hand simulator"""

from typing import List
import sys
from config import CONFIG
sys.path.insert(0, str(CONFIG.src))
from card_simulator import Card_Deck


class Hands:
    """Implement a hands checker 
    """
    def __init__(self) -> None:
        self.highcard: int = 0 # five cards that do not interact with each other to make any hands
        self.pair: int = 0 # one pair consists of two cards of the same value and three extra cards
        self.two_pair: int = 0 # two pair consists of two cards of equal value, another two cards of equal value, and one extra card
        self.three_of_a_kind: int = 0 # three of a kind is 3 cards of the same value and 2 side cards of different values
        self.straight: int = 0 # straight has 5 cards of consecutive value that are not all the same suit
        self.flush: int = 0 # flush is a hand which has all cards of the same suit
        self.full_house: int = 0 # a full house consists of 1 trip and 1 pair
        self.four_of_a_kind: int = 0 # or 'quads' consists of 4 cards of equal value and two cards of another value 
        self.straight_flush: int = 0 # straight and flush
        self.royal_flush: int = 0 # royals, and straight_flush
    
    def _count_value_pair(self, cards: List[Card_Deck.Card]) -> bool:
        pass

    def _is_flush(self, cards: List[Card_Deck.Card]) -> bool:
        """Check if a hand is of the same suit

        Args:
            cards (List[Card_Deck.Card]): 5 cards of a player

        Returns:
            bool: [description]
        """
        suits = {}
        for card in cards:
            if card.suit not in suits:
                suits[card.suit] = 1
            else:
                suits[card.suit] += 1
        return max(list(suits.values())) >= 5
    
    def _is_straight(self, cards: List[Card_Deck.Card]) -> bool:
        """Check if a hand is 5 consecutive number

        Args:
            cards (List[Card_Deck.Card]): 5 cards of a player

        Returns:
            bool: [description]
        """
        def five_consecutive(cards: List[Card_Deck.Card]) -> bool:
            """Check if this is five consecutive number

            Args:
                cards (List[Card_Deck.Card]): [description]

            Returns:
                bool: [description]
            """
            count = 1
            idx = 0
            while count < 5 and idx < len(cards):
                current_card = cards[idx]
                previous_card = cards[idx - 1]
                if current_card == previous_card + 1:
                    count += 1
                    idx += 1
                else:
                    count = 1
                    idx += 1
            return count >= 5
        cards_value = [card.value for card in cards]
        cards_value.sort()
        return five_consecutive(cards_value)

    def _is_highcard(self, cards: List[Card_Deck.Card]) -> bool:
        """Check if a player's hand has high card or not

        Args:
            cards (List[Card_Deck.Card]): 5 cards of a player

        Returns:
            bool: true if hand is high
        """
        if not self._is_straight and not self._is_flush:
            return len(cards) == len(set(cards))
        return False

    def _is_pair(self, cards: List[Card_Deck.Card]) -> bool:
        """Check if a player's hand has a pair

        Args:
            cards (List[Card_Deck.Card]): 5 cards of a player

        Returns:
            bool: [description]
        """
        if not self._is_straight and not self._is_flush and not self._is_three_of_a_kind:
            return len(cards) - 1 == len(set(cards))
        return False

    def _is_three_of_a_kind(self, cards: List[Card_Deck.Card]) -> bool:
        """Check if a player's hand has a three of a kind

        Args:
            cards (List[Card_Deck.Card]): 5 cards of a player

        Returns:
            bool: true if hand is a three of a kind
        """
        unique_values = {}
        for card in cards:
            unique_values.update(card.value)
        return max(unique_values.values) == 3


if __name__ == "__main__":
    pass