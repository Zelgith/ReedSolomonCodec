import random

class Transmitter:
    def __init__(self, error_probability):
        self.error_probability = error_probability

    def transmit(self, codeword):
        return [
            symbol ^ random.choice([0, 1]) if random.random() < self.error_probability else symbol
            for symbol in codeword
        ]
