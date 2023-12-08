from functools import cached_property
from pathlib import Path
from dataclasses import dataclass, field
from collections import Counter
from typing import Self

data = (Path(__file__).parent.parent / "data" / "day07.txt").read_text()


@dataclass
class Hand:
    cards: str
    bid: int
    jokers_on: bool = False
    RANKS: list[str] = field(default_factory=lambda: ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])

    @cached_property
    def groups(self):
        cards = [(x[1], self.RANKS.index(x[0])) for x in Counter(self.cards).items()]
        cards.sort(reverse=True)
        return cards

    @cached_property
    def best_hand(self):
        hands = []
        if "J" not in self.cards:
            return self
        for rank in self.RANKS:
            if rank == 'J':
                continue
            cards = self.cards
            cards = cards.replace('J', rank)
            hands.append(Hand(cards=cards, bid=self.bid))
        return max(hands)

    @cached_property
    def card_ranks(self):
        return [self.RANKS.index(x) for x in self.cards]

    @cached_property
    def rank(self):
        match [x[0] for x in self.groups]:
            case [1, 1, 1, 1, 1]:
                return 1
            case [2, 1, 1, 1]:
                return 2
            case [2, 2, 1]:
                return 3
            case [3, 1, 1]:
                return 4
            case [3, 2]:
                return 5
            case [4, 1]:
                return 6
            case [5]:
                return 7
            case _:
                raise Exception("???")

    def __lt__(self, other: Self):
        if self.jokers_on:
            this_card = self.best_hand
            other_card = other.best_hand
        else:
            this_card = self
            other_card = other
        if this_card.rank < other_card.rank:
            return True
        elif this_card.rank > other_card.rank:
            return False
        return self.card_ranks < other.card_ranks

    def __gt__(self, other: Self):
        if self.jokers_on:
            this_card = self.best_hand
            other_card = other.best_hand
        else:
            this_card = self
            other_card = other
        if this_card.rank > other_card.rank:
            return True
        elif this_card.rank < other_card.rank:
            return False
        return self.card_ranks > other.card_ranks

    def __eq__(self, other: Self):
        if self.jokers_on:
            this_card = self.best_hand
            other_card = other.best_hand
        else:
            this_card = self
            other_card = other
        if this_card.rank != other_card.rank:
            return False
        return self.card_ranks == other.card_ranks


def parse(data):
    hands: list[Hand] = []
    for line in data.splitlines():
        hand, bid = line.split()
        hands.append(Hand(cards=hand, bid=int(bid)))
    return hands

def parse2(data):
    hands: list[Hand] = []
    for line in data.splitlines():
        hand, bid = line.split()
        hands.append(
            Hand(
                cards=hand,
                bid=int(bid),
                RANKS=['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'],
                jokers_on=True,
            )
        )
    return hands

def find_winnings(hands: list[Hand]):
    total = 0
    hands.sort()
    for i, hand in enumerate(hands, 1):
        total += hand.bid * i
    return total

if __name__ == '__main__':
    hands = parse(data)
    winnings = find_winnings(hands)
    print(winnings)

    hands = parse2(data)
    winnings = find_winnings(hands)
    print(winnings)
