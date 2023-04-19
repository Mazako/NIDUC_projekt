import math

from reed_solomon_code.GaloisFields import *


# FIELDS:
# __m - size of symbol in bits
# __t - number of correctable symbols
# __n - word size in symbols
# __k - message size in symbols
# __table - table of galois field (16 or 256)
# __generator - generator of code message


class ReedSolomonCode:
    @staticmethod
    def add_galois(x, y):
        return x ^ y

    @staticmethod
    def remove_leading_zeros(message):
        i = 0
        while i < len(message) and message[i] == '0':
            i += 1
        if i == len(message):
            return '0'
        return message[i:]

    @staticmethod
    def array_to_binary(array, offset):
        result = ''
        for element in array:
            if offset == 4:
                result += '{0:04b}'.format(element)
            else:
                result += '{0:08b}'.format(element)
        return result

    def __init__(self, bits_mode, correctable_symbols):
        self.__m = bits_mode
        self.__t = correctable_symbols
        self.__n = pow(2, self.__m) - 1
        self.__k = self.__n - 2 * self.__t
        self.__generate_table()
        self.__reed_solomon_generator()

    def print_general_info(self):
        print('RS(', self.__n, ',', self.__k, ')')
        print('generator:', self.__generator)

    def get_generator(self):
        return self.__generator.copy()

    def encode_number(self, message):
        max_bits_per_word = self.__m * self.__k
        if len(message) == max_bits_per_word:
            return self.remove_leading_zeros(self.__encode_message(message))
        elif len(message) < max_bits_per_word:
            return self.remove_leading_zeros(self.__encode_message(self.__add_missing_zeros(message, True)))
        else:
            words = math.ceil(len(message) / max_bits_per_word)
            total_word = ''
            words -= 1
            missing_message_end_len = len(message) - (words * max_bits_per_word)
            total_word += self.__encode_message(self.__add_missing_zeros(message[0:missing_message_end_len], True))
            k = missing_message_end_len
            for i in range(words):
                total_word += self.__encode_message(message[k:k + max_bits_per_word])
                k += max_bits_per_word
            return self.remove_leading_zeros(total_word)

    def decode_number(self, message):
        max_bits_per_word = (self.__m * self.__k) + (self.__t * 2 * self.__m)
        if len(message) < max_bits_per_word:
            message = '0' * (max_bits_per_word - len(message)) + message
            return self.remove_leading_zeros(self.__decode_message(message))
        elif len(message) == max_bits_per_word:
            return self.remove_leading_zeros(self.__decode_message(message))
        else:
            words = math.ceil(len(message) / max_bits_per_word)
            total_word = ''
            words -= 1
            missing_message_end_len = len(message) - (words * max_bits_per_word)
            total_word += self.__decode_message(self.__add_missing_zeros(message[0:missing_message_end_len], False))
            k = missing_message_end_len
            for i in range(words):
                total_word += self.__decode_message(message[k:k + max_bits_per_word])
                k += max_bits_per_word
            return self.remove_leading_zeros(total_word)

    def __generate_table(self):
        if self.__m == 4:
            self.__table = get_gf_16()
        elif self.__m == 8:
            self.__table = get_gf_256()
        else:
            raise Exception('Unsupported bits mode - {}'.format(self.__m))

    def __reed_solomon_generator(self):
        sub_polynomial_numbers = 2 * self.__t
        generator = [1]
        for i in range(1, sub_polynomial_numbers + 1):
            generator = self.__multiply_poly_galois(generator, [1, self.__table[i]])
        self.__generator = generator

    def __multiply_galois(self, x, y):
        x = int(x)
        y = int(y)
        if x == 0 or y == 0:
            return 0
        gf_x = self.__table.index(x)
        gf_y = self.__table.index(y)
        return self.__table[(gf_x + gf_y) % (2 ** self.__m - 1)]

    def __multiply_poly_galois(self, a, b):
        a_len = len(a)
        b_len = len(b)
        solution = [0] * (a_len + b_len - 1)
        for i in range(a_len):
            for j in range(b_len):
                solution[i + j] = ReedSolomonCode.add_galois(solution[i + j], self.__multiply_galois(a[i], b[j]))
        return solution

    def __encode_message(self, message):
        print('message:', message)
        message_polynomial = self.__get_message_polynomial(message, True)
        print('message in polynomial', message_polynomial)
        parity_check = self.__calculate_pairity_check(message_polynomial)
        print('parity: ', parity_check)
        poly_encoded = message_polynomial + parity_check
        print('polynomial mesage:', poly_encoded)
        return message + ReedSolomonCode.array_to_binary(parity_check, self.__m)

    def __decode_message(self, message):
        polynomial = self.__get_message_polynomial(message, False)
        syndromes = self.__calculate_syndrome_components(polynomial)
        print('Polynomial: ', polynomial)
        print('Syndromes: ', syndromes)
        error_locator_polynomial = self.__berlekamps_massey(syndromes)
        print('delta: ', error_locator_polynomial)
        magnitude = self.__calculate_error_magnitude(syndromes, error_locator_polynomial)
        print('magnitude ', magnitude)
        error_locations = self.__chein_search(error_locator_polynomial)
        print('roots: ', error_locations)
        error_values = self.__forney_algorithm(magnitude, error_locator_polynomial, error_locations)
        print('error values: ', error_values)
        error_indexes = list(map(lambda x: self.__table.index(self.__inverse_galois(x)), error_locations))
        print('error indexes: ', error_indexes)
        self.__repair_message(polynomial, error_values, error_indexes)
        print('repaired message: ', polynomial)
        message_length = len(polynomial) - 2 * self.__t
        return self.array_to_binary(polynomial[:message_length], self.__m)

    def __get_message_polynomial(self, message, encoding):
        galois_polynomial = []
        offset = self.__m
        if encoding:
            limit = self.__k
        else:
            limit = self.__n
        k = 0
        for i in range(limit):
            galois_polynomial.append(int(''.join(message[k: k + offset]), 2))
            k += self.__m
        i = 0
        while i < len(galois_polynomial) and galois_polynomial[i] == 0:
            i += 1
        return galois_polynomial[i:]

    def __add_missing_zeros(self, message, encoding):
        if encoding:
            return '0' * ((self.__k * self.__m) - len(message)) + message
        else:
            return '0' * ((self.__k * self.__m) + (self.__t * 2 * self.__m) - len(message)) + message

    def __calculate_pairity_check(self, message):
        x_2_t = [0] * (self.__t * 2 + 1)
        x_2_t[0] = 1
        multiplied_message = self.__multiply_poly_galois(message, x_2_t)
        q, r = self.__galois_division(multiplied_message, self.__generator)
        return r

    def __galois_division(self, dividend, divisor):
        result = list(dividend)
        for i in range(0, len(dividend) - (len(divisor) - 1)):
            coef = result[i]
            if coef != 0:
                for j in range(1, len(divisor)):
                    if divisor[j] != 0:
                        result[i + j] = ReedSolomonCode.add_galois(result[i + j],
                                                                   self.__multiply_galois(divisor[j], coef))

        separator = -(len(divisor) - 1)
        return result[:separator], result[separator:]

    def __calculate_polynomial(self, polynomial, value):
        total = polynomial[len(polynomial) - 1]
        for i in range(1, len(polynomial)):
            poly_index = len(polynomial) - i - 1
            total = self.add_galois(total, self.__multiply_galois(polynomial[poly_index], self.__galois_pow(value, i)))
        return total

    def __galois_pow(self, value, i):
        if i == 0:
            return 1
        value = (self.__table.index(value) * i) % (2 ** self.__m - 1)
        return self.__table[value]

    def __calculate_syndrome_components(self, polynomial):
        syndromes = []
        for i in range(1, 2 * self.__t + 1):
            syndromes.append(self.__calculate_polynomial(polynomial, self.__table[i]))
        return syndromes

    def __berlekamps_massey(self, syndromes):
        k = 1
        l = 0
        c_x = [1, 0]
        delta_x = [1]
        while k <= 2 * self.__t:
            e = syndromes[k - 1]
            for j in range(1, l + 1):
                e = self.add_galois(e, self.__multiply_galois(delta_x[len(delta_x) - j - 1], syndromes[k - 1 - j]))
            if e != 0:
                delta_star = self.__add_two_polynomials(delta_x, self.__poly_multiply_by_scalar(c_x, e))
                if 2 * l < k:
                    l = k - l
                    c_x = self.__poly_multiply_by_scalar(delta_x, self.__inverse_galois(e))
                delta_x = delta_star
            k += 1
            c_x.append(0)
        return delta_x

    def __poly_multiply_by_scalar(self, polynomial, scalar):
        multiplied = [0] * len(polynomial)
        for i in range(0, len(polynomial)):
            multiplied[i] = self.__multiply_galois(polynomial[i], scalar)
        return multiplied

    def __add_two_polynomials(self, p1, p2):
        if len(p1) > len(p2):
            greater = p1
            lesser = [0] * (len(p1) - len(p2)) + p2
        else:
            greater = p2
            lesser = [0] * (len(p2) - len(p1)) + p1
        total = [0] * len(greater)
        for i in range(0, len(greater)):
            if i < len(lesser):
                total[i] = self.add_galois(greater[i], lesser[i])
            else:
                total[i] = greater[i]
        return total

    def __inverse_galois(self, x):
        if x == 1:
            return 1
        alpha = self.__table.index(x)
        return self.__table[((2 ** self.__m - 1) - alpha)]

    def __calculate_error_magnitude(self, syndromes, locator):
        reversed_syndromes = syndromes.copy()
        reversed_syndromes.reverse()
        s_times_delta = self.__multiply_poly_galois(reversed_syndromes, locator)
        divisor = [1] + [0] * (self.__t * 2 - 1)
        q, r = self.__galois_division(s_times_delta, divisor)
        return r

    def __chein_search(self, error_locator_polynomial):
        roots = []
        for x in self.__table:
            if self.__calculate_polynomial(error_locator_polynomial, x) == 0:
                roots.append(x)
        return roots

    def __forney_algorithm(self, error_magnitude, error_locator, roots):
        Y = []
        for x in roots:
            magnitude = self.__calculate_polynomial(error_magnitude, x)
            d_x_locator = self.__delta_derivative(error_locator, x)
            y = self.__multiply_galois(magnitude, self.__inverse_galois(d_x_locator))
            Y.append(y)
        return Y

    def __delta_derivative(self, error_locator, x):
        """
        Brand new kurwa model ---> delta[1] + delta[3] x x^-2 + delta[5] x x^-4 + ...
        """
        error_locator_reversed = error_locator.copy()
        error_locator_reversed.reverse()
        total = error_locator_reversed[1]
        power = -2
        for i in range(3, len(error_locator_reversed)):
            if i % 2 != 0:
                new_power = (2 ** self.__m - 1) + power
                total = self.add_galois(total, self.__multiply_galois(error_locator_reversed[i],
                                                                      self.__galois_pow(x, new_power)))
                power -= 2
        return total

    def __repair_message(self, polynomial, error_values, error_indexes):
        #TODO: to nie dziala jak indeks jest wiekszy niz wielomian
        for i in range(len(error_values)):
            index = len(polynomial) - error_indexes[i] - 1
            polynomial[index] = self.add_galois(polynomial[index], error_values[i])
