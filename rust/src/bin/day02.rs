use std::fs;

type Num = i32;

const RED: Num = 12;
const GREEN: Num = 13;
const BLUE: Num = 14;

#[derive(Debug)]
struct Round {
    red: Num,
    green: Num,
    blue: Num,
}

#[derive(Debug)]
struct Game {
    rounds: Vec<Round>,
}

fn main() {
    let raw = fs::read_to_string("../data/day02.txt").unwrap();
    let games = parse(&raw);

    let p1 = count_possible(&games);
    dbg!(p1);
    let p2: Num = games.iter().map(|game| power(game)).sum();
    dbg!(p2);
}

fn is_possible(game: &Game) -> bool {
    for round in game.rounds.iter() {
        if round.blue > BLUE {
            return false;
        }
        if round.green > GREEN {
            return false;
        }
        if round.red > RED {
            return false;
        }
    }
    return true;
}

fn power(game: &Game) -> Num {
    let red: Num = game.rounds.iter().map(|x| x.red).max().unwrap();
    let green: Num = game.rounds.iter().map(|x| x.green).max().unwrap();
    let blue: Num = game.rounds.iter().map(|x| x.blue).max().unwrap();
    return red * green * blue;
}

fn count_possible(games: &Vec<Game>) -> Num {
    return games
        .iter()
        .enumerate()
        .filter_map(|(i, game)| {
            if is_possible(game) {
                return Some(i as Num);
            }
            return None;
        })
        .sum();
}

fn parse(data: &str) -> Vec<Game> {
    return data
        .trim()
        .lines()
        .map(|line| {
            let mut split = line.split(":");
            split.next();
            let b = split.next().unwrap();
            let rounds = b
                .split(";")
                .map(|part| {
                    let mut round = Round {
                        red: 0,
                        green: 0,
                        blue: 0,
                    };
                    for colors in part.trim().split(",") {
                        let mut colorsplit = colors.trim().split(" ");
                        let count: Num = colorsplit.next().unwrap().parse().unwrap();
                        let color = colorsplit.next().unwrap();
                        match color {
                            "blue" => round.blue = count,
                            "red" => round.red = count,
                            "green" => round.green = count,
                            _ => {
                                unreachable!("Uh oh");
                            }
                        }
                    }
                    return round;
                })
                .collect::<Vec<Round>>();
            return Game { rounds };
        })
        .collect();
}
