class Polynomial:
    def __init__(self, coefficients, field):
        self.coefficients = coefficients
        self.field = field

    def add(self, other):
        result_len = max(len(self.coefficients), len(other.coefficients))
        result = [0] * result_len
        for i in range(result_len):
            a = self.coefficients[i] if i < len(self.coefficients) else 0
            b = other.coefficients[i] if i < len(other.coefficients) else 0
            result[i] = self.field.add(a, b)
        return Polynomial([r % self.field.field_size for r in result], self.field)

    def multiply(self, other):
        result = [0] * (len(self.coefficients) + len(other.coefficients) - 1)
        for i, a in enumerate(self.coefficients):
            for j, b in enumerate(other.coefficients):
                result[i + j] = self.field.add(result[i + j], self.field.multiply(a, b))
        return Polynomial([r % self.field.field_size for r in result], self.field)

    def divide(self, other):
        quotient = [0] * len(self.coefficients)
        remainder = self.coefficients[:]
        while len(remainder) >= len(other.coefficients):
            factor = self.field.divide(remainder[0], other.coefficients[0])
            quotient[len(remainder) - len(other.coefficients)] = factor
            for i in range(len(other.coefficients)):
                remainder[i] = self.field.subtract(remainder[i], self.field.multiply(factor, other.coefficients[i]))
            remainder.pop(0)
        return Polynomial([q % self.field.field_size for q in quotient], self.field), Polynomial([r % self.field.field_size for r in remainder], self.field)
