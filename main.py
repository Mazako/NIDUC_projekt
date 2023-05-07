from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

solomon = ReedSolomonCode(4, 2)
message = solomon.encode_number(ReedSolomonCode.array_to_binary([1, 2, 3, 4], 4))
print(message)
message = solomon.add_missing_zeros(message, False)
poly = solomon.get_message_polynomial(message, False)
print(poly)
print(solomon.add_errors(message, 2, True))