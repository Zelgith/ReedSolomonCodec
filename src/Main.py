from GaloisField import GaloisField
from ReedSolomonDecoder import ReedSolomonDecoder
from ReedSolomonEncoder import ReedSolomonEncoder
from Transmitter import Transmitter

# Ustawienia pola Galois
primitive_polynomial = 0x11d  # Prymitywny wielomian dla GF(2^8)
field_size = 256  # Rozmiar ciała Galois dla GF(2^8)

n = 15  # Długość słowa kodowego
k = 9   # Długość wiadomości
t = 3   # Możliwość poprawienia do 3 błędów

# Inicjalizacja ciała Galois
gf = GaloisField(primitive_polynomial, field_size)

# Wiadomość do zakodowania (9 symboli)
message = [32, 91, 4, 55, 89, 100, 13, 42, 200]

# Koder Reeda-Salomona
encoder = ReedSolomonEncoder(gf, n, k)
encoded_message = encoder.encode(message)

# Symulacja zakłóceń w kanale
transmitter = Transmitter(error_probability=0.3)
received_message = transmitter.transmit(encoded_message)

# Dekoder Reeda-Salomona
decoder = ReedSolomonDecoder(gf, n, k, t)
decoded_message = decoder.decode(received_message)

print(encoded_message)
print(received_message)
print(decoded_message)