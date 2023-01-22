use std::fs;
use std::str::FromStr;

use fraction::BigFraction;

pub fn read(file_path: String) -> Vec<Vec<BigFraction>> {
    let contents = fs::read_to_string(file_path).unwrap();
    let mut data: Vec<Vec<BigFraction>> = Vec::new();
    let mut current: Vec<BigFraction> = Vec::new();
    let mut last_index = 0;
    for (index, c) in contents.chars().enumerate() {
        if c == '[' && index > 0 {
            last_index = index + 1;
        } else if c == ']' && index < contents.len() - 1 {
            current.push(BigFraction::from_str(&contents[last_index..index]).unwrap());
            data.push(current);
            current = Vec::new();
            last_index = index + 1;
        } else if c == ',' {
            if index > last_index {
                current.push(BigFraction::from_str(&contents[last_index..index]).unwrap());
            }
            last_index = index + 1;
        }
    }
    data
}