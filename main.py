from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

solomon = ReedSolomonCode(4, 2)
solomon.print_general_info()
message = solomon.encode_number('1010010010011110101001010101001010101010011011010010101')
print('ENCODED MESSAGE: ', message)
decoded_message = solomon.decode_number(message)
print(decoded_message)
