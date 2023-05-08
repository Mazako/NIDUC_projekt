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
