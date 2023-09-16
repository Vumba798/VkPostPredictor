import numpy as np
import re
import pymorphy2
import nltk
import tensorflow as tf
from typing import List
from nltk.corpus import stopwords

class Predictor:
    def __init__(self, weights_path: str, vocabulary_path: str):
        self.stop_words = set(nltk.corpus.stopwords.words("russian"))
        self.morph = pymorphy2.MorphAnalyzer()
        self.vocabulary = []
        with open(vocabulary_path, "r", encoding="utf-8") as file:
            for word in file.readlines():
                self.vocabulary.append(word.rstrip())

        self.model = tf.keras.Sequential([
            tf.keras.layers.TextVectorization(vocabulary=self.vocabulary),
            tf.keras.layers.Embedding(
                input_dim=len((len(self.vocabulary),)),
                output_dim=64,
                mask_zero=True),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(3)
        ])
        self.model.load_weights(weights_path)

    def predict(self, text: str):
        preprocessed_text = " ".join(self.__preprocess_text(text))
        return self.model.predict((preprocessed_text, ))

    def __preprocess_text(self, text: str) -> List[str]:
        words = text.lower().split()
        words_of_letters = map(self.__filter_letters, words)
        nonempty_words = filter(None, words_of_letters)
        normalized_words = map(self.__normalize_word, nonempty_words)
        preprocessed_words = filter(lambda word: word not in self.stop_words, normalized_words)
        return list(preprocessed_words)

    def __filter_letters(self, word: str) -> str:
        return re.sub(r"[^а-я]", "", word)

    def __normalize_word(self, word: str) -> str:
        return self.morph.parse(word)[0].normal_form


