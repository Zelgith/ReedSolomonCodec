class ReedSolomonDecoder:
    def __init__(self, field, n, k, t):
        self.field = field
        self.n = n
        self.k = k
        self.t = t

    def decode(self, received):
        # Step 1: Calculate syndromes
        syndromes = [self._evaluate(received, self.field.exp_table[i]) for i in range(1, 2 * self.t + 1)]

        # Check if syndromes are all zero, meaning no errors
        if max(syndromes) == 0:
            return received[:self.k]  # No errors detected

        # Step 2: Find error locator polynomial using Berlekamp-Massey algorithm
        error_locator = self._berlekamp_massey(syndromes)

        # Step 3: Find error positions using Chien search
        error_positions = self._chien_search(error_locator)

        # Step 4: Calculate error magnitudes using Forney's algorithm
        error_magnitudes = self._forney_algorithm(syndromes, error_locator, error_positions)

        # Step 5: Correct errors in received message
        corrected_message = received[:]
        for i, pos in enumerate(error_positions):
            corrected_message[pos] = self.field.subtract(corrected_message[pos], error_magnitudes[i])

        return corrected_message[:self.k]  # Return corrected message

    def _evaluate(self, poly, x):
        result = 0
        for coeff in poly:
            result = self.field.add(self.field.multiply(result, x), coeff)
        return result

    def _berlekamp_massey(self, syndromes):
        # Berlekamp-Massey algorithm to find the error locator polynomial
        error_locator = [1]  # Start with 1 as the error locator polynomial
        b = [1]  # Auxiliary polynomial
        l = 0  # Length of current error locator polynomial
        m = 1
        for i in range(len(syndromes)):
            # Calculate discrepancy
            discrepancy = syndromes[i]
            for j in range(1, l + 1):
                discrepancy ^= self.field.multiply(error_locator[j], syndromes[i - j])

            if discrepancy != 0:
                t = error_locator[:]  # Copy current error locator polynomial
                # Ensure error_locator is long enough
                while len(error_locator) < len(b) + m:
                    error_locator.append(0)

                for j in range(len(b)):
                    error_locator[j + m] ^= self.field.multiply(discrepancy, b[j])

                if 2 * l <= i:
                    l = i + 1 - l
                    b = t[:]
                    m = 0
            m += 1
        return error_locator

    def _chien_search(self, error_locator):
        # Chien search to find the positions of errors
        error_positions = []
        for i in range(self.n):
            eval_result = self._evaluate(error_locator, self.field.exp_table[self.n - 1 - i])
            if eval_result == 0:
                error_positions.append(self.n - 1 - i)
        return error_positions

    def _forney_algorithm(self, syndromes, error_locator, error_positions):
        # Forney's algorithm to compute error magnitudes
        error_magnitudes = []
        # First, calculate the error evaluator polynomial (Ω)
        error_evaluator = [0] * (2 * self.t)
        for i in range(self.t):
            error_evaluator[i] = syndromes[i]
            for j in range(1, i + 1):
                error_evaluator[i] ^= self.field.multiply(syndromes[i - j], error_locator[j])
        # Compute error magnitudes
        for pos in error_positions:
            xi_inverse = self.field.exp_table[self.n - 1 - pos]
            numerator = self._evaluate(error_evaluator, xi_inverse)
            denominator = self._evaluate(self._derivative(error_locator), xi_inverse)
            error_magnitudes.append(self.field.divide(numerator, denominator))
        return error_magnitudes

    def _derivative(self, poly):
        # Compute the formal derivative of the polynomial
        derivative = []
        for i in range(1, len(poly), 2):  # Only take odd-degree terms
            derivative.append(poly[i])
        return derivative
