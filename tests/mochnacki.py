from reed_solomon_code.ReedSolomonCode import ReedSolomonCode
import pandas as pd


def rs_stat_test(solomon, poly_errors, parity_errors):
    """

    :type solomon: ReedSolomonCode
    """
    correct_probes = 0
    decoded_but_good = 0
    count = 1000
    for i in range(count):
        rand_message = ReedSolomonCode.generate_random_message(solomon.k, solomon.m)
        message = ReedSolomonCode.array_to_binary(rand_message, solomon.m)
        encoded_message = solomon.encode_number(message)
        mesage_with_errors = solomon.add_errors_string(poly_errors, encoded_message, is_parity=False)
        mesage_with_errors = solomon.add_errors_string(parity_errors, mesage_with_errors, is_parity=True)
        try:
            decoded_message = solomon.simple_mochnacki_decoder(mesage_with_errors)
            if decoded_message == encoded_message:
                correct_probes += 1
        except:
            continue

    return round((correct_probes / count) * 100, 2)


solomon = ReedSolomonCode(4, 3)
arr = []
for i in range(4):
    for j in range(4):
        arr.append([i, j, rs_stat_test(solomon, i, j)])

frame = pd.DataFrame(data=arr, columns=['błędy w wiadomości', 'błędy w części kontrolnej', 'sukces dekodowania [%]'])
frame.to_csv('../csv/mochnacki.csv', sep=';')
