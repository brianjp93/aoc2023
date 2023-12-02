from pathlib import Path
from dataclasses import dataclass, field

data = (Path(__file__).parent.parent / "data" / "day02.txt").read_text()

RED = 12
GREEN = 13
BLUE = 14

@dataclass
class Round:
    blue: int = 0
    red: int = 0
    green: int = 0


@dataclass
class Game:
    rounds: list[Round] = field(default_factory=list)


def parse_lines(data: str):
    games = []
    for row in data.splitlines():
        game = Game()
        a, b = row.split(":")
        a = int(a.lstrip("Game "))
        b = b.split(';')
        for round in b:
            roundmodel = Round()
            plays = round.strip().split(",")
            for colors in plays:
                count, color = colors.split()
                match color:
                    case 'blue':
                        roundmodel.blue = int(count)
                    case 'red':
                        roundmodel.red = int(count)
                    case 'green':
                        roundmodel.green = int(count)
                game.rounds.append(roundmodel)
        games.append(game)
    return games


def is_possible(game: Game):
    for round in game.rounds:
        if round.blue > BLUE:
            return False
        if round.green > GREEN:
            return False
        if round.red > RED:
            return False
    return True


def count_possible(games: list[Game]):
    return sum(i for i, game in enumerate(games, 1) if is_possible(game))


def power(game: Game):
    red = max(x.red for x in game.rounds)
    green = max(x.green for x in game.rounds)
    blue = max(x.blue for x in game.rounds)
    return red * green * blue


if __name__ == "__main__":
    games = parse_lines(data)
    count = count_possible(games)
    print(count)
    powers = sum(power(game) for game in games)
    print(powers)
