from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

solomon = ReedSolomonCode(4, 3)
message = solomon.encode_number('11011010101010001000')
print(message)