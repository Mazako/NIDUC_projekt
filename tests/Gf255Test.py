import random

from reed_solomon_code.ReedSolomonCode import ReedSolomonCode
import pandas as pd

def rs_stat_test(solomon, poly_errors, parity_errors, is_decoding_success):
    """

    :type solomon: ReedSolomonCode
    """
    correct_probes = 0
    decoded_but_good = 0
    count = 250
    for i in range(count):
        rand_message = ReedSolomonCode.generate_random_message(solomon.k, solomon.m)
        message = ReedSolomonCode.array_to_binary(rand_message, solomon.m)
        encoded_message = solomon.encode_number(message)
        mesage_with_errors = solomon.add_errors_string(poly_errors, encoded_message, is_parity=False)
        mesage_with_errors = solomon.add_errors_string(parity_errors, mesage_with_errors, is_parity=True)
        try:
            decoded_message = solomon.decode_number(mesage_with_errors)
            if decoded_message == ReedSolomonCode.remove_leading_zeros(message):
                correct_probes += 1
            else:
                decoded_but_good += 1

        except:
            continue
    if is_decoding_success:
        return (correct_probes / count) * 100
    return (decoded_but_good / count) * 100


arr = []
solomon = ReedSolomonCode(8, 8)
solomon.print_general_info()
# for i in range(0, 9):
#     for j in range(0, 9):
#         if i + j > 8: continue
#         print(i, j)
#         arr.append([i, j, rs_stat_test(solomon, i, j, True), rs_stat_test(solomon, i, j, False)])
rand_combinations = []
i = 0
while i < 30:
    rand_message = random.randint(9, 239)
    rand_errors = random.randint(9, 16)
    combination = (rand_message, rand_errors)
    if combination in rand_combinations:
        continue
    arr.append([rand_message, rand_errors, rs_stat_test(solomon, rand_message, rand_errors, True), rs_stat_test(solomon, rand_message, rand_errors, False)])
    print(i)
    i += 1

frame = pd.DataFrame(data=arr, columns=['message', 'pairity', 'decoding', 'failure'])
frame.to_csv('results2.csv', sep=';', encoding='utf-8')