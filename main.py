from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

solomon = ReedSolomonCode(4, 2)
solomon.print_general_info()
message = solomon.encode_number('10100100100111')
print(message)
solomon.decode_number(message)
