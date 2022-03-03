from dataclasses import dataclass
from collections import Counter
from pathlib import Path
from typing import List
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import RegexpTokenizer

tokenizer = RegexpTokenizer(r"\w+")
stop_words_en = set(stopwords.words("english"))
wordnet_lemmatizer = WordNetLemmatizer()


@dataclass
class WordAnalysis:
    word_count: int
    unique_word_count: int
    top_words: List[str]


def word_count(filepath: Path):
    """
    Perform a naive word count analysis on given text

    Improvements:
    - use lemms for unique_word_count
    - use stopwords to eliminate common words from top_words
    """

    content = filepath.read_text("utf-8")

    word_tokens = tokenizer.tokenize(content)
    lemms = [wordnet_lemmatizer.lemmatize(word) for word in word_tokens]
    counter = Counter([lem for lem in lemms if lem.lower() not in stop_words_en])
    top_words = list([word for word, _count in counter.most_common(10)])
    return WordAnalysis(
        word_count=len(word_tokens),
        unique_word_count=len(counter),
        top_words=top_words,
    )
