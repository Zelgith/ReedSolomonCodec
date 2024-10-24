import unittest
from src.GaloisField import GaloisField

class TestGaloisFieldExtended(unittest.TestCase):

    def setUp(self):
        # Initialize Galois field for GF(2^8) with a standard primitive polynomial
        self.gf = GaloisField(0x11d, 256)  # 0x11d is the primitive polynomial for GF(2^8)

    def test_add(self):
        # Add operation in GF should be XOR
        self.assertEqual(self.gf.add(6, 9), 6 ^ 9)
        self.assertEqual(self.gf.add(128, 128), 0)  # 128 ^ 128 = 0
        self.assertEqual(self.gf.add(255, 0), 255)  # 255 ^ 0 = 255

    def test_subtract(self):
        # Subtraction in GF should also be XOR (same as addition)
        self.assertEqual(self.gf.subtract(15, 10), 15 ^ 10)
        self.assertEqual(self.gf.subtract(100, 100), 0)
        self.assertEqual(self.gf.subtract(50, 0), 50)

    def test_multiply(self):
        # Test some known multiplication values in GF(2^8)
        self.assertEqual(self.gf.multiply(4, 7), self.gf.exp_table[(self.gf.log_table[4] + self.gf.log_table[7]) % 255])
        self.assertEqual(self.gf.multiply(45, 78), self.gf.exp_table[(self.gf.log_table[45] + self.gf.log_table[78]) % 255])
        self.assertEqual(self.gf.multiply(1, 123), 123)  # 1 * anything should be the same value
        self.assertEqual(self.gf.multiply(123, 1), 123)

    def test_divide(self):
        # Test division in GF(2^8)
        self.assertEqual(self.gf.divide(18, 6), self.gf.exp_table[(self.gf.log_table[18] - self.gf.log_table[6]) % 255])
        self.assertEqual(self.gf.divide(200, 10), self.gf.exp_table[(self.gf.log_table[200] - self.gf.log_table[10]) % 255])
        self.assertEqual(self.gf.divide(255, 255), 1)  # Any non-zero number divided by itself should be 1
        self.assertEqual(self.gf.divide(0, 1), 0)  # 0 divided by any number is 0
        with self.assertRaises(ZeroDivisionError):
            self.gf.divide(25, 0)  # Dividing by zero should raise an error

    def test_log_table(self):
        # Test that log(1) = 0 in the logarithm table
        self.assertEqual(self.gf.log_table[1], 0)

        # Test that log(0) should be undefined or handled in a special way (like returning -1 or a placeholder)
        self.assertEqual(self.gf.log_table[0], -1)  # Check that the log of 0 is set to -1 or another placeholder.

    def test_exp_table(self):
        # Test that exp_table[log_table[x]] = x
        for i in range(1, 256):
            self.assertEqual(self.gf.exp_table[self.gf.log_table[i]], i)
        # Test some known values
        self.assertEqual(self.gf.exp_table[1], 2)  # 2^1 = 2 in GF(2^8)
        self.assertEqual(self.gf.exp_table[0], 1)  # 2^0 = 1 in GF(2^8)

    def test_identity_properties(self):
        # Identity properties for multiplication and addition
        self.assertEqual(self.gf.add(0, 123), 123)  # 0 + x = x
        self.assertEqual(self.gf.add(123, 0), 123)
        self.assertEqual(self.gf.multiply(1, 234), 234)  # 1 * x = x
        self.assertEqual(self.gf.multiply(234, 1), 234)
        self.assertEqual(self.gf.multiply(0, 234), 0)  # 0 * x = 0
        self.assertEqual(self.gf.multiply(234, 0), 0)

    def test_multiplication_with_inverses(self):
        # Multiplying a number with its inverse should return 1
        for i in range(1, 256):
            inverse = self.gf.divide(1, i)  # Find the multiplicative inverse of i
            self.assertEqual(self.gf.multiply(i, inverse), 1)

if __name__ == '__main__':
    unittest.main()
