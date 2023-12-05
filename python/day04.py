from pathlib import Path
from dataclasses import dataclass

data = (Path(__file__).parent.parent / "data" / "day04.txt").read_text()


@dataclass
class Card:
    winning: set[int]
    hand: set[int]

    def count_matches(self):
        return len(self.hand & self.winning)

    def points(self):
        count = self.count_matches()
        if count == 0:
            return 0
        return 2 ** (count - 1)


def parse_cards(data):
    cards: dict[int, tuple[Card, int]] = {}
    for i, line in enumerate(data.splitlines(), 1):
        left, right = line.split(":")[1].split("|")
        winning = {int(x) for x in left.split()}
        hand = {int(x) for x in right.split()}
        cards[i] = (Card(winning=winning, hand=hand), 1)
    return cards


@dataclass
class ScratchCards:
    cards: dict[int, tuple[Card, int]]

    def __post_init__(self):
        self.count_cards()

    def count_cards(self):
        for key, (card, count) in self.cards.items():
            if not (card and count):
                return 0
            for i in range(key + 1, card.count_matches() + key + 1):
                item = self.cards.get(i)
                if item:
                    cards[i] = (item[0], count + item[1])


if __name__ == "__main__":
    cards = parse_cards(data)
    total = sum(card[0].points() for card in cards.values())
    print(total)

    scratch = ScratchCards(cards)
    print(sum(count for _, count in scratch.cards.values()))
