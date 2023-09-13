"""
Extract scrabble scores from a legacy system.

The old system stored a list of letters per score:
    1 point: "A", "E", "I", "O", "U", "L", "N", "R", "S", "T",
    2 points: "D", "G",
    3 points: "B", "C", "M", "P",
    4 points: "F", "H", "V", "W", "Y",
    5 points: "K",
    8 points: "J", "X",
    10 points: "Q", "Z",

The new system instead stores the score per letter:
    "a" is worth 1 point.
    "b" is worth 3 points.
    "c" is worth 3 points.
    "d" is worth 2 points.
    Etc.
Transform the legacy data format to the new format.

Input: {1: ["A", "E"], 2: ["D", "G"]}
Output: {"a": 1, "d": 2, "e": 1, "g": 2}
"""
from typing import Dict, List


def transform(legacy_data: Dict[int, List[str]]) -> Dict[str, int]:
    output = {}
    for score, letters in legacy_data.items():
        for letter in letters:
            output[letter.lower()] = score
    return output
