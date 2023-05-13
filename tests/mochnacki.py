from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

solomon = ReedSolomonCode(4, 3)
message = '001110011111001111111111111101111111'
encoded = solomon.encode_number(message)
print(encoded)
encoded = solomon.add_errors_string(6, encoded, True)
decoded = solomon.simple_mochnacki_decoder(encoded)
print(decoded)