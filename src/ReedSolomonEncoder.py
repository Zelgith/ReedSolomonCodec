from Polynomial import Polynomial


class ReedSolomonEncoder:
    def __init__(self, field, n, k):
        self.field = field
        self.n = n
        self.k = k
        self.generator_polynomial = self._generate_polynomial()

    def _generate_polynomial(self):
        poly = Polynomial([1], self.field)
        for i in range(self.n - self.k):
            poly = poly.multiply(Polynomial([1, self.field.exp_table[i]], self.field))
        return poly

    def encode(self, message):
        message_poly = Polynomial(message + [0] * (self.n - self.k), self.field)
        remainder = message_poly.divide(self.generator_polynomial)[1]
        return message + remainder.coefficients
