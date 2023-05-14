from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

solomon = ReedSolomonCode(4, 3)
message = '101010010'
encoded = solomon.encode_number(message)
print(encoded)
encoded = solomon.add_errors_string(2, encoded, True)
encoded = solomon.add_missing_zeros(encoded, encoding=False)
decoded = solomon.simple_mochnacki_decoder(encoded)
print(decoded)