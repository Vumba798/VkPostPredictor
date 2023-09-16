import tensorflow as tf
from model import Predictor
if __name__ == "__main__":
    predictor = Predictor("weights", "vocabulary.txt")
    text = """Лазанья из макарон Ингредиенты: Макароны - 250-300 грамм;"""
    print(predictor.predict(text))