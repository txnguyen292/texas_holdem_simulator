from typing import List, Dict, DefaultDict
from card_simulator import Card_Deck
from Hands import Hands

class Hands_Generator:
    def __init__(self):
        pass
    # TODO: Move these helper functions into a seperate module and develop test cases for them
    def get_straight(self, straights: List[Card_Deck.Card], cards: Card_Deck, greater: bool=True) -> List[Card_Deck.Card]:
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

    def get_same_suits(self, same_suits: List[Card_Deck.Card], cards: Card_Deck)-> List[Card_Deck.Card]:
        """Return a list that contains five cards of the same suit

        Args:
            same_suits (List[Card_Deck.Card]): list that contain the first card
            cards (Card_Deck): deck of cards

        Returns:
            List[Card_Deck.Card]: list that contain at least 5 cards of the same suit
        """
        first_suit: str = same_suits[0].suit
        while len(same_suits) < 5:
            for idx, card in enumerate(cards.cards):
                if card.suit == first_suit:
                    same_suits.append(card)
        for _ in range(2):
            same_suits.append(cards.deal())
        return same_suits

    def get_same_value(self, first_card: List[Card_Deck.Card], cards: Card_Deck, type_of_pair: Literal["two", "three", "four"]) -> List[Card_Deck.Card]:
        """Returns a list that contains fives which has number of type pairs

        Args:
            first_card (List[Card_Deck.Card]): list with first card
            cards (Card_Deck): card deck
            type_of_pair (Literal[): type of pair to produce

        Returns:
            List[Card_Deck.Card]: List of 7 cards with type of pair
        """
        valToInt: Dict[str, int] = {"two": 2, "three": 3, "four": 4}
        first_value: int = first_card[0].value
        idx: int = 0
        while len(first_card) < valToInt[type_of_pair] and idx < len(cards.cards):
            if cards.cards[idx].value == first_value:
                first_card.append(cards.cards[idx])
            idx += 1
        return first_card

    def get_high_card(self, first_card: List[Card_Deck.Card], cards: Card_Deck) -> List[Card_Deck.Card]:
        """Return a list that contains only high cards

        Args:
            first_card (List[Card_Deck.Card]): list with first card
            cards (Card_Deck): card deck

        Returns:
            List[Card_Deck.Card]: high card hand
        """
        first_value: int = first_card[0].value
        first_suit: str = first_card[0].suit
        values: Set = set()
        suits: DefaultDict[str, int] = defaultdict(int)
        straight_upper = 1
        straight_lower = 1
        idx = 0
        while len(first_card) < 7 and idx < len(cards.cards):
            current_card = cards.cards[idx]
            if current_card.value in values: # if a pair, skip
                idx += 1
                continue
            if current_card.suit in suits and suits[current_card.suit] >= 4: # if a flush, skip
                idx += 1
                continue
            else: 
            # Check if hand contains a straight
            if first_value < 5:
                if straight_upper >= 4:
                    idx += 1
                    continue
                if current_card.value > first_card[-1].value: #TODO: should compare with the maximum value of first_card
                    straight_upper += 1
            else:
                if straight_lower >= 4:
                    idx += 1
                    continue
                if current_card.value < first_card[0].value: #TODO: Compare with the minimum value of first_card
                    straight_lower += 1
                if straight_upper >= 4:
                    idx += 1
                    continue
                if current_card.value > first_card[-1].value:
                
            values.add(current_card.value)
            suits[current_card.suit] += 1
            first_card.append(current_card)
            idx += 1
            #TODO: Finish generating just high cards
        return first_card

if __name__ == "__main__":
    pass