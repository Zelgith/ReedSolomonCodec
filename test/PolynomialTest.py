import unittest
from src.GaloisField import GaloisField
from src.Polynomial import Polynomial

class TestPolynomial(unittest.TestCase):
    def setUp(self):
        # GF(2^8) with primitive polynomial x^8 + x^4 + x^3 + x^2 + 1 (0x11d)
        primitive_polynomial = 0x11d
        field_size = 256
        self.gf = GaloisField(primitive_polynomial, field_size)

    def test_add(self):
        p1 = Polynomial([2, 3, 1], self.gf)  # Represents 2x^2 + 3x + 1
        p2 = Polynomial([1, 1], self.gf)      # Represents x + 1
        result = p1.add(p2)
        expected = Polynomial([2, 2, 0], self.gf)  # Represents 2x^2 + 2x (coefficients may need validation)
        self.assertEqual(result.coefficients, expected.coefficients)

    def test_multiply(self):
        p1 = Polynomial([2, 3, 1], self.gf)  # 2x^2 + 3x + 1
        p2 = Polynomial([1, 1], self.gf)      # x + 1
        result = p1.multiply(p2)
        expected = Polynomial([2, 1, 2, 1], self.gf)  # Represents 2x^3 + 1x^2 + 2x + 1
        self.assertEqual(result.coefficients, expected.coefficients)

    def test_divide(self):
        p1 = Polynomial([2, 3, 1], self.gf)  # 2x^2 + 3x + 1 (dividend)
        p2 = Polynomial([1, 1], self.gf)      # x + 1 (divisor)
        quotient, remainder = p1.divide(p2)

        expected_quotient = Polynomial([2, 1], self.gf)  # Expected quotient: 2x + 1
        expected_remainder = Polynomial([], self.gf)  # Expected remainder: 0

        self.assertEqual(quotient.coefficients, expected_quotient.coefficients)
        self.assertEqual(remainder.coefficients, expected_remainder.coefficients)

    def test_divide_with_remainder(self):
        p1 = Polynomial([1, 2, 2], self.gf)  # x^2 + 2x + 2
        p2 = Polynomial([1, 1], self.gf)  # x + 1
        quotient, remainder = p1.divide(p2)

        expected_quotient = Polynomial([1, 3], self.gf)  # Expected quotient: x + 3
        expected_remainder = Polynomial([1], self.gf)  # Expected remainder: 1

        self.assertEqual(quotient.coefficients, expected_quotient.coefficients)
        self.assertEqual(remainder.coefficients, expected_remainder.coefficients)

    def test_add_zero_polynomial(self):
        p1 = Polynomial([2, 3, 1], self.gf)  # 2x^2 + 3x + 1
        p2 = Polynomial([0], self.gf)         # Represents the zero polynomial
        result = p1.add(p2)
        self.assertEqual(result.coefficients, p1.coefficients)  # Should be equal to p1

    def test_multiply_by_zero_polynomial(self):
        p1 = Polynomial([2, 3, 1], self.gf)  # 2x^2 + 3x + 1
        p2 = Polynomial([0], self.gf)         # Represents the zero polynomial
        result = p1.multiply(p2)
        expected = Polynomial([0], self.gf)    # Expected: 0
        self.assertEqual(result.coefficients, expected.coefficients)

if __name__ == '__main__':
    unittest.main()
