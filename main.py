from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

solomon = ReedSolomonCode(4, 5)
solomon.print_general_info()
message = solomon.encode_number(ReedSolomonCode.array_to_binary([1], 8))
print(message)
message = solomon.add_missing_zeros(message, False)
poly = solomon.get_message_polynomial(message, False)
print(poly)
print(solomon.add_errors(4, poly, is_parity=True))
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