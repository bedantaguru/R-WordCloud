import os
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np


class WC:
    def __init__(
            self,
            word_counts,
            transparent_logo="Resources/R_logo.png",
            out_folder="Out"):

        self.__wc = None
        self.__word_counts = word_counts
        if not isinstance(word_counts, Counter):
            raise Exception("word_counts must be a collections.Counter!")
        os.makedirs(out_folder, exist_ok=True)
        if os.path.exists(out_folder):
            self.__out_folder = out_folder
        else:
            raise Exception("Unable to set output folder.")
        if os.path.exists(transparent_logo):
            self.__transparent_logo = transparent_logo
        else:
            raise Exception("Unable to locate transparent logo.")
        try:
            self.__mask_image = Image.open(self.__transparent_logo).convert('RGBA')
        except Exception as e:
            print("Failed to load image!")
            raise e
        self.__mask_array = WC.create_mask(self.__mask_image)

    @staticmethod
    def create_mask(image):
        image_array = np.array(image)
        mask = np.where(image_array[:, :, 3] > 0, 0, 255).astype(np.uint8)
        return mask

    def create_wordcloud(self):
        wordcloud = WordCloud(
            width=self.__mask_image.width, height=self.__mask_image.height,
            # for SVG this is working:background_color='rgb(255, 255, 255,0)',
            background_color=None,
            mode='RGBA',
            mask=self.__mask_array,
            color_func=ImageColorGenerator(
                np.array(self.__mask_image))
        ).generate_from_frequencies(self.__word_counts)
        self.__wc = wordcloud
        self.save_wordcloud()

    def save_wordcloud(self):
        if self.__wc is not None:
            # Save as SVG
            wordcloud_svg = self.__wc.to_svg(embed_font=True)
            of = os.path.join(self.__out_folder, "wordcloud.svg")
            with open(of, "w") as f:
                f.write(wordcloud_svg)
            # Save as PNG
            png_path = os.path.join(self.__out_folder, "wordcloud.png")
            image = self.__wc.to_image()
            image.save(png_path, "PNG")
        else:
            print("Please generate wordcloud first using create_wordcloud.")
