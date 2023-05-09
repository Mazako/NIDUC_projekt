def rs_stat_test(solomon, poly_errors, parity_errors):
    """

    :type solomon: ReedSolomonCode
    """
    correct_probes = 0
    for i in range(1):
        rand_message = ReedSolomonCode.generate_random_message(solomon.k, solomon.m)
        print('REAL_MESSAGE', rand_message)
        message = ReedSolomonCode.array_to_binary(rand_message, solomon.m)
        encoded_message = solomon.encode_number(message)
        mesage_with_errors = solomon.add_errors_string(poly_errors, encoded_message, is_parity=False)
        mesage_with_errors = solomon.add_errors_string(parity_errors, mesage_with_errors, is_parity=True)
        try:
            decoded_message = solomon.decode_number(mesage_with_errors)
            if decoded_message == ReedSolomonCode.remove_leading_zeros(message):
                correct_probes += 1
        except:
            continue
    return correct_probes / 1000


# solomon = ReedSolomonCode(4, 3)
# message = [1, 2, 3, 4, 6, 7, 8, 9]
# string = ReedSolomonCode.array_to_binary(message, 4)
# string = ReedSolomonCode.remove_leading_zeros(string)
# encoded_message = solomon.encode_number(string)
# encoded_message_array = ReedSolomonCode.binary_to_array(encoded_message, 4)
# encoded_message_array[0] = 4
# encoded_message_array[1] = 4
# encoded_message_array[2] = 4
# decoded = solomon.decode_number(ReedSolomonCode.array_to_binary(encoded_message_array, 4))
# print(string == decoded)

from reed_solomon_code.ReedSolomonCode import ReedSolomonCode


solomon = ReedSolomonCode(4, 3)
x = rs_stat_test(solomon, 0, 4)
print(x)