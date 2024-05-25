
from Lib.FileOperation import UniqueLines
from Lib.Tokenizer import PlainLine
from Lib.WordCloudCustomized import WC

R_unique_lines = UniqueLines()

R_unique_lines.collect_unique_lines()

print(f'You have written {len(R_unique_lines.Lines)} - unique lines of R code')

tokens = PlainLine(R_unique_lines.Lines)

wc = WC(tokens.get_word_count())

wc.create_wordcloud()
