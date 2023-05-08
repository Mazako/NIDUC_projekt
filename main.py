from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

tab4 = [1, 2, 3, 4, 5]
tab8 = [2, 8, 13, 22]

for i in tab4:
    for j in range(1, i):
        solomon = ReedSolomonCode(4, i-1)
        solomon.print_general_info()
        message = solomon.encode_number(ReedSolomonCode.array_to_binary([7, 4, 0, 5, 15, 9, 6, 15, 5, 10], 4))
        print(message)
        message = solomon.add_missing_zeros(message, False)
        poly = solomon.get_message_polynomial(message, False)
        print(poly)
        print(solomon.add_errors(2, poly, is_parity=True))
        print()

for i in tab8:
    for j in range(1, i-1):
        solomon = ReedSolomonCode(8, i)
        solomon.print_general_info()
        message = solomon.encode_number(ReedSolomonCode.array_to_binary(
            [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5, 8, 5, 2, 35, 6, 7, 1, 8, 0, 56, 2, 34, 6, 4, 26,
             7, 3, 4, 7, 5, 2, 1, 6, 5, 5, 3, 6], 8))
        print(message)
        message = solomon.add_missing_zeros(message, False)
        poly = solomon.get_message_polynomial(message, False)
        print(poly)
        print(solomon.add_errors(7, poly, is_parity=True))
        print()

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
