class Polynomial:
    def __init__(self, coefficients, field):
        # Coefficients are stored from highest degree to lowest degree
        self.coefficients = coefficients
        self.field = field

        # Remove leading zeros for proper degree calculation
        while len(self.coefficients) > 1 and self.coefficients[0] == 0:
            self.coefficients.pop(0)

    def degree(self):
        # Returns the degree of the polynomial (index of the highest non-zero coefficient)
        return len(self.coefficients) - 1

    def add(self, other):
        # Polynomial addition in GF(2^8) (XOR operation)
        result_len = max(len(self.coefficients), len(other.coefficients))
        result = [0] * result_len

        # Adding coefficients starting from the end of the list to maintain degree alignment
        for i in range(result_len):
            a = self.coefficients[-(i + 1)] if i < len(self.coefficients) else 0
            b = other.coefficients[-(i + 1)] if i < len(other.coefficients) else 0
            result[-(i + 1)] = self.field.add(a, b)

        return Polynomial(result, self.field)

    def multiply(self, other):
        # Polynomial multiplication in GF(2^8)
        result = [0] * (len(self.coefficients) + len(other.coefficients) - 1)

        # Multiplying coefficients while maintaining degrees
        for i, a in enumerate(self.coefficients):
            for j, b in enumerate(other.coefficients):
                # Ensure multiplication is done in Galois Field
                result[i + j] = self.field.add(result[i + j], self.field.multiply(a, b))

        return Polynomial(result, self.field)

    def divide(self, other):
        # Inicjalizowanie ilorazu i reszty
        quotient = [0] * (self.degree() - other.degree() + 1)
        remainder = self.coefficients[:]  # Kopiowanie współczynników dzielnika

        while len(remainder) >= len(other.coefficients):
            # Obliczanie współczynnika prowadzącego
            lead_coeff = remainder[0]
            lead_degree = len(remainder) - 1
            divisor_lead_coeff = other.coefficients[0]

            # Obliczanie współczynnika ilorazu
            factor = self.field.divide(lead_coeff, divisor_lead_coeff)
            quotient[lead_degree - other.degree() - 1] = factor

            # Odejmowanie iloczynu od reszty
            for i in range(len(other.coefficients)):
                # Tylko jeśli wchodzimy w zakres reszty
                if i < len(remainder):
                    remainder[i] = self.field.subtract(remainder[i], self.field.multiply(factor, other.coefficients[i]))

            # Usuwanie prowadzącego współczynnika z reszty
            remainder.pop(0)

        # Czyszczenie prowadzących zer w reszcie
        while remainder and remainder[0] == 0:
            remainder.pop(0)

        return Polynomial(quotient, self.field), Polynomial(remainder, self.field)


