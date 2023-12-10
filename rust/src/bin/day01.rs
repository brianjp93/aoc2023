use fancy_regex::Regex;
use std::fs;

const NUMS: [&str; 9] = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
];

fn main() {
    let data = fs::read_to_string("../data/day01.txt").unwrap();
    let pat = Regex::new(r"(\d)").unwrap();
    let p1 = get_sum(&data, &pat, false);
    dbg!(p1);
    let p2 = get_sum(&data, &pat, true);
    dbg!(p2);
}

fn convert(n: &str) -> &str {
    match n {
        "one" => "one1one",
        "two" => "two2two",
        "three" => "three3three",
        "four" => "four4four",
        "five" => "five5five",
        "six" => "six6six",
        "seven" => "seven7seven",
        "eight" => "eight8eight",
        "nine" => "nine9nine",
        _ => n,
    }
}

fn get_sum(data: &String, pattern: &Regex, is_replace: bool) -> i32 {
    return data
        .trim()
        .lines()
        .map(|line| {
            let mut line = line.to_string();
            if is_replace {
                for num in NUMS.iter() {
                    line = line.replace(num, convert(num));
                }
            }
            let matches: Vec<&str> = pattern
                .find_iter(line.as_str())
                .map(|x| convert(x.unwrap().as_str()))
                .collect();
            let a = matches.first().unwrap();
            let b = matches.last().unwrap();
            let n: i32 = format!("{}{}", a, b).parse().unwrap();
            n
        })
        .sum();
}
