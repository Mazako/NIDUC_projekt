from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

solomon = ReedSolomonCode(8, 2)
# solomon.print_general_info()
# message = solomon.encode_number('1010010010011110101001010101001010101010011011010010101')
# print('ENCODED MESSAGE: ', message)
message = ReedSolomonCode.array_to_binary([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 210, 220, 190, 177], 8)
decoded_message = solomon.decode_number(message)
print(decoded_message)
