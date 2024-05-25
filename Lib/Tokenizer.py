from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
import nltk


class PlainLine:
    def __init__(self, lines, count_immediately=True):
        self.lines = lines
        if count_immediately:
            self.count_words()
        else:
            self.__word_counts = None

    @staticmethod
    def check_and_download_punkt():
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

    @staticmethod
    def tokenize_line(line_st):
        return nltk.word_tokenize(line_st)

    def count_words(self):
        PlainLine.check_and_download_punkt()
        word_counts = Counter()
        with ThreadPoolExecutor() as exe:
            futures = [exe.submit(PlainLine.tokenize_line, line)
                       for line in self.lines]
            for future in tqdm(as_completed(futures),
                               desc="Processing lines",
                               unit="lines", total=len(self.lines)):
                words = future.result()
                word_counts.update(words)

        self.__word_counts = word_counts
        return self.__word_counts

    def get_word_count(self):
        """
        Returns the word count. If ran already it will not run again.
        :return: The plain word count of lines
        """
        if self.__word_counts is None:
            self.count_words()
        return self.__word_counts
