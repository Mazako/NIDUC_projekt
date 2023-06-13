from reed_solomon_code.ReedSolomonCode import ReedSolomonCode


def encode(encoder):
    """

    :type encoder: ReedSolomonCode
    """
    message = input('Wprowadzaj kolejne symbole oddzielone spacją: ')
    symbol_message = list(map(int, message.split(' ')))
    result = encoder.encode_symbol_array_message(symbol_message)
    print('Zakodowana wiadomość:', result)


def decode(decoder):
    """

    :type decoder: ReedSolomonCode
    """
    message = input('Wprowadzaj kolejne symbole oddzielone spacją: ')
    symbol_message = list(map(int, message.split(' ')))
    result = decoder.decode_message_array(symbol_message)
    print('Odkodowania wiadomość:', result)


def createCoder():
    mode = input('Wybierz tryb kodownaia: 4 / 8: ')
    if mode != '4' and mode != '8':
        print('Wybrano niewlaściwy tryb kodowania')
        quit(-1)
    t = input('Wybierz zdolnosc korekcyjną (t): ')
    return ReedSolomonCode(int(mode), int(t))


def main():
    print('Dekoder Reed-Solomon')
    solomon = createCoder()
    program = True
    while program:
        print('================================')
        solomon.print_general_info()
        print('1) Zakoduj wiadomosc')
        print('2) Odkoduj wiadomosc')
        print('3) Zmien parametry kodu')
        print('4) Wyjdz')
        option = input('Wybierz: ')
        if option == '1':
            encode(solomon)
        elif option == '2':
            decode(solomon)
        elif option == '3':
            solomon = createCoder()
        elif option == '4':
            program = False
        else:
            print('Nie ma takiej opcji')


main()
