from reed_solomon_code.ReedSolomonCode import  ReedSolomonCode

solomon = ReedSolomonCode(4, 3)
# try:
#     while True:
#         messsage = ReedSolomonCode.generate_random_message(9, 4)
#         print(messsage)
#         messsage = ReedSolomonCode.array_to_binary(messsage, 4)
#         encoded = solomon.encode_number(messsage)
#         errors = solomon.add_errors_string(1, encoded, is_parity=False)
#         errors = solomon.add_errors_string(1, errors, is_parity=True)
#         decoded = solomon.simple_mochnacki_decoder(errors)
#         if solomon.add_missing_zeros(decoded, encoding=False) != solomon.add_missing_zeros(encoded, encoding=False):
#             raise Exception
# except:
#         print('ERRRRROR')
#         print('ENCODED= ', ReedSolomonCode.binary_to_array(encoded, 4))
#         print('WITH_ERRORS', ReedSolomonCode.binary_to_array(errors, 4))


tested =   [1, 6, 7, 10, 6, 10, 3, 6, 11, 6, 6, 5, 0, 8, 1]
original = [7, 6, 7, 10, 6, 10, 3, 6, 11, 6, 6, 5, 0, 8, 11]
encoded = ReedSolomonCode.array_to_binary(tested,  4)
decoded = solomon.simple_mochnacki_decoder(encoded)
print(original)
print(solomon.binary_to_array(decoded, 4))
