import pandas as pd

from reed_solomon_code.ReedSolomonCode import ReedSolomonCode


def rs_stat_test(solomon, poly_errors, parity_errors):
    arr = []
    """

    :type solomon: ReedSolomonCode
    """
    correct_probes = 0
    decoded_but_good = 0
    count = 1000
    i = 0
    while i < count:
        rand_message = ReedSolomonCode.generate_random_message(solomon.k, solomon.m)
        if rand_message in arr:
            continue
        arr.append(rand_message)
        message = ReedSolomonCode.array_to_binary(rand_message, solomon.m)
        encoded_message = solomon.encode_number(message)
        mesage_with_errors = solomon.add_errors_string(poly_errors, encoded_message, is_parity=False)
        mesage_with_errors = solomon.add_errors_string(parity_errors, mesage_with_errors, is_parity=True)
        try:
            decoded_message = solomon.simple_mochnacki_decoder(mesage_with_errors)
            if solomon.add_missing_zeros(decoded_message, encoding=False) == solomon.add_missing_zeros(encoded_message,
                                                                                                       encoding=False):
                correct_probes += 1
            i += 1
        except:
            i += 1
            continue

    return round((correct_probes / count) * 100, 2)


solomon = ReedSolomonCode(4, 3)
arr = []
for i in range(5):
    for j in range(5):
        arr.append([i, j, rs_stat_test(solomon, i, j), round((((i + j) / 15) * 100), 2)])

frame = pd.DataFrame(data=arr, columns=['błędy w wiadomości', 'błędy w części kontrolnej', 'sukces dekodowania [%]',
                                        'stopień zepsucia wiadomości [%]'])
frame.to_csv('../csv/mochnacki.csv', sep=';')
