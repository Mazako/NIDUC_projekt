from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

solomon = ReedSolomonCode(4, 3)
message = [1, 2, 3, 4, 6, 7, 8, 9]
string = ReedSolomonCode.array_to_binary(message, 4)
string = ReedSolomonCode.remove_leading_zeros(string)
encoded_message = solomon.encode_number(string)
encoded_message_array = ReedSolomonCode.binary_to_array(encoded_message, 4)
encoded_message_array[0] = 4
encoded_message_array[1] = 4
encoded_message_array[2] = 4
decoded = solomon.decode_number(ReedSolomonCode.array_to_binary(encoded_message_array, 4))
print(string == decoded)



"""
RS(4, 1)
RS(4, 2)
RS(4, 3)
RS(4, 4)
RS(4, 5)

RS(8, 2)
RS(8, 8)
RS(8, 12)
RS(8, 22)
"""
