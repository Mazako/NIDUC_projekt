from reed_solomon_code.ReedSolomonCode import  ReedSolomonCode

solomon = ReedSolomonCode(4, 3)


def while_mochnacki_bad():
    global encoded, decoded
    try:
        while True:
            messsage = ReedSolomonCode.generate_random_message(9, 4)
            print(messsage)
            messsage = ReedSolomonCode.array_to_binary(messsage, 4)
            encoded = solomon.encode_number(messsage)
            errors = solomon.add_errors_string(1, encoded, is_parity=False)
            errors = solomon.add_errors_string(2, errors, is_parity=True)
            decoded = solomon.simple_mochnacki_decoder(errors)
            if solomon.add_missing_zeros(decoded, encoding=False) != solomon.add_missing_zeros(encoded, encoding=False):
                raise Exception
    except:
        print('ERRRRROR')
        print('ENCODED= ', ReedSolomonCode.binary_to_array(encoded, 4))
        print('WITH_ERRORS', ReedSolomonCode.binary_to_array(errors, 4))

def while_normal_bad():
    global encoded, decoded
    try:
        while True:
            messsage = ReedSolomonCode.generate_random_message(9, 4)
            print(messsage)
            messsage = ReedSolomonCode.array_to_binary(messsage, 4)
            encoded = solomon.encode_number(messsage)
            errors = solomon.add_errors_string(4, encoded, is_parity=False)
            errors = solomon.add_errors_string(2, errors, is_parity=True)
            try:
                decoded = solomon.decode_number(errors)
            except:
                continue
            if solomon.add_missing_zeros(decoded, encoding=False) != solomon.add_missing_zeros(messsage, encoding=False):
                raise Exception
    except:
        print('ERRRRROR')
        print('ENCODED= ', ReedSolomonCode.binary_to_array(encoded, 4))
        print('WITH_ERRORS', ReedSolomonCode.binary_to_array(errors, 4))
        print('DECODED', ReedSolomonCode.binary_to_array(decoded, 4))


# while_normal_bad()


tested =   [13, 9, 3, 11, 1, 2, 9, 6, 12, 4, 3, 0, 10, 14, 11]
original = [6, 15, 7, 11, 1, 2, 9, 6, 14, 9, 3, 0, 10, 14, 0]
encoded = ReedSolomonCode.array_to_binary(tested,  4)
decoded = solomon.decode_number(encoded)
print(original)
print(tested)
print(solomon.get_message_polynomial(solomon.add_missing_zeros(decoded, encoding=True), encoding=True))
synd_decoded = [15, 11, 13, 13, 14, 13, 1, 8, 13, 6, 6, 1, 3, 2, 14]
print(solomon.hamming_distance(original, tested))
print(solomon.hamming_distance(tested, synd_decoded))
print(solomon.hamming_distance(original, synd_decoded))

