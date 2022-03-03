from collections import Counter
from dataclasses import dataclass
import re
from typing import List


@dataclass
class WordAnalysis:
    word_count: int
    unique_word_count: int
    top_words: List[str]


def word_count(text: str):
    """
    Perform a naive word count analysis on given text
    """
    text = text.lower()
    text = re.sub("[^\w ]", "", text)
    words = [word for word in text.split(" ") if word != ""]
    counter = Counter(words)
    top_words = list([word for word, _count in counter.most_common(10)])
    return WordAnalysis(
        word_count=len(words),
        unique_word_count=len(counter),
        top_words=top_words,
    )
