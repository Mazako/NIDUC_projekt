from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

solomon = ReedSolomonCode(8, 2)
solomon.print_general_info()
message = solomon.encode_number('11011010101010001000')
print(message)