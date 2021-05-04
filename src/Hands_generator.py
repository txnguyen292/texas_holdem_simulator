import numpy as np 
import logging
import argparse
from typing import List, Dict, DefaultDict, Literal, Set
from card_simulator import Card_Deck
from Hands import Hands
from logzero import setup_logger 
from config import CONFIG

LOGLVL: Dict[str, int] = {"debug": logging.DEBUG, "info": logging.INFO, "warning": logging.WARNING}
logger = setup_logger(__file__, logfile=str(CONFIG.reports / "hands_generator.log"), level=logging.WARNING)

#==================================================== HELPER FUNCTION =============================================================
def get_args():
    parser = argparse.ArgumentParser(
        description="A poker hand generator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--loglvl", type=str, default=None,
                        help="Setting log level, defaults to debug")
    return parser.parse_known_args()

#=====================================================    END    ==================================================================

#==================================================== MAIN ========================================================================
class Hands_Generator:
    def __init__(self):
        pass
    def get_straight(self, straights: List[Card_Deck.Card], cards: Card_Deck, greater: bool=True) -> List[Card_Deck.Card]:
        """Get 7 cards that consist of 5 consecutive cards in a deck with a given card

        Args:
            straights (List[Card_Deck.Card]): first card
            cards: (List[Card_Deck.Card]): deck of card
            greater (bool, optional): whether to get bigger or lower consecutive numbers. Defaults to True.

        Returns:
            Card_Deck: a list of consecutive numbers
        """
        current_value = straights[0].value
        if 13 - current_value <= 4:
            max_val = 13
        else:
            max_val = current_value + 5
        if current_value - 4 <= 0:
            min_val = 0
        else:
            min_val = current_value - 4
        initial_value_to_pick = np.random.randint(min_val, max_val, 1)[0]
        if initial_value_to_pick > current_value:
            values_to_pick = list(range(initial_value_to_pick - 4, initial_value_to_pick + 1))
            logger.debug(f"Lower pick from: {values_to_pick}")
            straights = [cards.Card(x, np.random.choice(list(cards.SUITS.keys()))) for x in values_to_pick]
        else:
            values_to_pick = list(range(initial_value_to_pick, initial_value_to_pick + 5))
            logger.debug(f"Higher pick from: {values_to_pick}")
            straights = [cards.Card(x, np.random.choice(list(cards.SUITS.keys()))) for x in values_to_pick]
        while len(straights) < 7:
            potential_card = cards.deal()
            if potential_card.value not in values_to_pick:
                straights.append(potential_card)
                values_to_pick.append(potential_card.value)
        return straights

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
            same_suits.append(cards.deal(shuffle=True))
        return same_suits

    def get_same_value(self, first_card: List[Card_Deck.Card], cards: Card_Deck, type_of_pair: Literal["one", "two", "three", "four"]) -> List[Card_Deck.Card]:
        """Returns a list that contains fives which has number of type pairs

        Args:
            first_card (List[Card_Deck.Card]): list with first card
            cards (Card_Deck): card deck
            type_of_pair (Literal["one", "two", "three", "four"]): type of pair to produce. If "two", generate two pairs with different values.

        Returns:
            List[Card_Deck.Card]: List of number of type of pair cards with type of pair
        """
        first_card_copy = first_card.copy()
        valToInt: Dict[str, int] = {"one":2, "three": 3, "four": 4}
        first_value: int = first_card_copy[0].value
        idx: int = 0
        if type_of_pair != "two":
            no_cards_to_get = valToInt[type_of_pair]
            unique_suits = {first_card_copy[0].suit}
            logger.debug(f"Return {no_cards_to_get} cards.")
            while len(first_card_copy) < no_cards_to_get and idx < len(cards.cards):
                if cards.cards[idx].value == first_value and cards.cards[idx].suit not in unique_suits: 
                    first_card_copy.append(cards.cards[idx])
                    print(f"appending {cards.cards[idx]}")
                    unique_suits.add(cards.cards[idx].suit)
                    print(unique_suits)
                    logger.debug(f"Length of current list {len(first_card_copy)}")
                idx += 1
        else:
            unique_values: Set[int] = {first_value}
            first_card_copy: List[Card_Deck.Card] = self.get_same_value(first_card_copy, cards, "one")
            while len(unique_values) < 2:
                random_ind = np.random.randint(0, 52, 1)[0]
                random_card_1 = cards.cards[random_ind]
                if random_card_1.value not in unique_values:
                    unique_values.add(random_card_1.value)
            second_card: List[Card_Deck.Card] = self.get_same_value([random_card_1], cards, "one")
            first_card_copy = first_card_copy + second_card
        return first_card_copy

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
                pass
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
                    pass
            values.add(current_card.value)
            suits[current_card.suit] += 1
            first_card.append(current_card)
            idx += 1
            #TODO: Finish generating just high cards
        return first_card

#=======================================  END  =============================================================================

if __name__ == "__main__":
    args, _ = get_args()
    if args.loglvl is not None:
        logger.loglevel(LOGLVL[args.loglvl])
    hand_generator = Hands_Generator()
    card_deck = Card_Deck()
    for _ in range(1000):
        random_ind = np.random.randint(0, 52, 1)[0]
        random_card = card_deck.cards[random_ind]
        straights = hand_generator.get_straight([random_card], card_deck)
        assert len(straights) == 5