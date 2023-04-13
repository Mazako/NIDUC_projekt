from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

solomon = ReedSolomonCode(4, 2)
solomon.print_general_info()
# message = solomon.encode_number('10100100100111')
message = solomon.encode_number('100101101111010101111010100101')
print('ENCODED MESSAGE: ', message)
decoded_message = solomon.decode_number(message)
print(decoded_message)
