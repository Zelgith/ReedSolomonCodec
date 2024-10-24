class GaloisField:
    def __init__(self, primitive_polynomial, field_size):
        # Inicjalizacja tabel logarytmów i wykładników
        self.field_size = field_size
        self.exp_table = [0] * (2 * field_size)
        self.log_table = [0] * field_size
        self._build_tables(primitive_polynomial)

    def _build_tables(self, primitive_polynomial):
        x = 1
        for i in range(self.field_size - 1):
            self.exp_table[i] = x
            self.log_table[x] = i
            x <<= 1
            if x & self.field_size:
                x ^= primitive_polynomial
        for i in range(self.field_size - 1, 2 * self.field_size - 1):
            self.exp_table[i] = self.exp_table[i - (self.field_size - 1)]

        # Set log_table[0] to -1 to signify that log(0) is undefined
        self.log_table[0] = -1

    def add(self, a, b):
        return a ^ b  # Dodawanie w GF(2^8) to operacja XOR

    def subtract(self, a, b):
        return a ^ b  # Odejmowanie w GF(2^8) to też XOR

    def multiply(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.exp_table[(self.log_table[a] + self.log_table[b]) % (self.field_size - 1)]

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero in Galois Field.")
        if a == 0:
            return 0
        return self.exp_table[(self.log_table[a] - self.log_table[b]) % (self.field_size - 1)]
