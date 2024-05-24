
from Lib.FileOperation import UniqueLines
from Lib.Tokenizer import PlainLine
from Lib.WordCloudCustomized import WC

R_unique_lines = UniqueLines("C:/Users/Nil/Downloads/R")

tokens = PlainLine(R_unique_lines.Lines)

wc = WC(tokens.get_word_count())

wc.create_wordcloud()
