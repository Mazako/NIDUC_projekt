import math
import random

from reed_solomon_code.GaloisFields import *

N = 4
# FIELDS:
# __m - size of symbol in bits
# __t - number of correctable symbols
# __n - word size in symbols
# __k - message size in symbols
# __table - table of galois field (16 or 256)
# __generator - generator of code message


def calculate_weight(param):
    weight = 0
    for i in param:
        if i == '1':
            weight += 1
    return weight


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
    def remove_leading_zeros_array(message):
        i = 0
        while i < len(message) and message[i] == 0:
            i += 1
        if i == len(message):
            return 0
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

    @staticmethod
    def binary_to_array(string, offset):
        result = []
        i = 0
        while i < len(string):
            result.append(int(string[i:i + offset], 2))
            i += 4
        return ReedSolomonCode.remove_leading_zeros_array(result)

    @staticmethod
    def generate_random_message(length, m):
        array = []
        for i in range(length):
            if m == 4:
                array.append(random.randint(1, 15))
            else:
                array.append(random.randint(1, 255))
        return array

    def __init__(self, bits_mode, correctable_symbols):
        self.m = bits_mode
        self.t = correctable_symbols
        self.n = pow(2, self.m) - 1
        self.k = self.n - (2 * self.t)
        self.__generate_table()
        self.__reed_solomon_generator()

    def print_general_info(self):
        print('RS(', self.n, ',', self.k, ')')
        print('generator:', self.__generator)

    def get_generator(self):
        return self.__generator.copy()

    def encode_number(self, message):
        max_bits_per_word = self.m * self.k
        if len(message) == max_bits_per_word:
            return self.__encode_message(message)
        elif len(message) < max_bits_per_word:
            return self.__encode_message(self.add_missing_zeros(message, True))
        else:
            words = math.ceil(len(message) / max_bits_per_word)
            total_word = ''
            words -= 1
            missing_message_end_len = len(message) - (words * max_bits_per_word)
            total_word += self.__encode_message(self.add_missing_zeros(message[0:missing_message_end_len], True))
            k = missing_message_end_len
            for i in range(words):
                total_word += self.__encode_message(message[k:k + max_bits_per_word])
                k += max_bits_per_word
            return total_word

    def decode_number(self, message):
        max_bits_per_word = (self.m * self.k) + (self.t * 2 * self.m)
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
            total_word += self.__decode_message(self.add_missing_zeros(message[0:missing_message_end_len], False))
            k = missing_message_end_len
            for i in range(words):
                total_word += self.__decode_message(message[k:k + max_bits_per_word])
                k += max_bits_per_word
            return self.remove_leading_zeros(total_word)

    def __generate_table(self):
        if self.m == 4:
            self.__table = get_gf_16()
        elif self.m == 8:
            self.__table = get_gf_256()
        else:
            raise Exception('Unsupported bits mode - {}'.format(self.m))

    def __reed_solomon_generator(self):
        sub_polynomial_numbers = 2 * self.t
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
        return self.__table[(gf_x + gf_y) % (2 ** self.m - 1)]

    def __multiply_poly_galois(self, a, b):
        a_len = len(a)
        b_len = len(b)
        solution = [0] * (a_len + b_len - 1)
        for i in range(a_len):
            for j in range(b_len):
                solution[i + j] = ReedSolomonCode.add_galois(solution[i + j], self.__multiply_galois(a[i], b[j]))
        return solution

    def __encode_message(self, message):
        # print('message:', message)
        message_polynomial = self.get_message_polynomial(message, True)
        # print('message in polynomial', message_polynomial)
        parity_check = self.__calculate_pairity_check(message_polynomial)
        # print('parity: ', parity_check)
        poly_encoded = message_polynomial + parity_check
        # print('polynomial mesage:', poly_encoded)
        return message + ReedSolomonCode.array_to_binary(parity_check, self.m)

    def __decode_message(self, message):
        polynomial = self.get_message_polynomial(message, False)
        syndromes = self.__calculate_syndrome_components(polynomial)
        # print('Polynomial: ', polynomial)
        # print('Syndromes: ', syndromes)
        if sum(syndromes) == 0:
            return self.array_to_binary(polynomial[:len(polynomial) - 2 * self.t], self.m)
        error_locator_polynomial = self.__berlekamps_massey(syndromes)
        # print('delta: ', error_locator_polynomial)
        magnitude = self.__calculate_error_magnitude(syndromes, error_locator_polynomial)
        magnitude = ReedSolomonCode.remove_leading_zeros_array(magnitude)
        # print('magnitude ', magnitude)

        error_locations = self.__chein_search(error_locator_polynomial)
        # print('roots: ', error_locations)
        if len(error_locations) != len(error_locator_polynomial) - 1:
            raise Exception
        if len(error_locations) > self.t:
            raise Exception

        error_values = self.__forney_algorithm(magnitude, error_locator_polynomial, error_locations)
        # print('error values: ', error_values)
        error_indexes = list(map(lambda x: self.__table.index(self.__inverse_galois(x)), error_locations))
        # print('error indexes: ', error_indexes)
        self.__repair_message(polynomial, error_values, error_indexes)
        # print('repaired message: ', polynomial)
        # print(self.__calculate_syndrome_components(polynomial))
        if sum(self.__calculate_syndrome_components(polynomial)) > 0:
            raise Exception
        message_length = len(polynomial) - 2 * self.t
        # print('SUCCESS')
        return self.array_to_binary(polynomial[:message_length], self.m)

    def get_message_polynomial(self, message, encoding):
        galois_polynomial = []
        offset = self.m
        if encoding:
            limit = self.k
        else:
            limit = self.n
        k = 0
        for i in range(limit):
            galois_polynomial.append(int(''.join(message[k: k + offset]), 2))
            k += self.m
        i = 0
        while i < len(galois_polynomial) and galois_polynomial[i] == 0:
            i += 1
        return galois_polynomial[i:]

    def add_missing_zeros(self, message, encoding):
        if encoding:
            return '0' * ((self.k * self.m) - len(message)) + message
        else:
            return '0' * ((self.k * self.m) + (self.t * 2 * self.m) - len(message)) + message

    def __calculate_pairity_check(self, message):
        x_2_t = [0] * (self.t * 2 + 1)
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
        value = (self.__table.index(value) * i) % (2 ** self.m - 1)
        return self.__table[value]

    def __calculate_syndrome_components(self, polynomial):
        syndromes = []
        for i in range(1, 2 * self.t + 1):
            syndromes.append(self.__calculate_polynomial(polynomial, self.__table[i]))
        return syndromes

    def __berlekamps_massey(self, syndromes):
        k = 1
        l = 0
        c_x = [1, 0]
        delta_x = [1]
        while k <= 2 * self.t:
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
        delta_x = self.remove_leading_zeros_array(delta_x)
        if len(delta_x) - 1 > self.t:
            raise Exception
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
        if x == 0:
            return 0
        if x == 1:
            return 1
        alpha = self.__table.index(x)
        return self.__table[((2 ** self.m - 1) - alpha)]

    def __calculate_error_magnitude(self, syndromes, locator):
        reversed_syndromes = syndromes.copy()
        reversed_syndromes.reverse()
        s_times_delta = self.__multiply_poly_galois(reversed_syndromes, locator)
        divisor = [1] + [0] * (self.t * 2 - 1)
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
        power = 2
        for i in range(3, len(error_locator_reversed)):
            if i % 2 != 0:
                total = self.add_galois(total, self.__multiply_galois(error_locator_reversed[i],
                                                                      self.__galois_pow(x, power)))
                power += 2
        if total == 0:
            raise Exception()
        return total

    def __repair_message(self, polynomial, error_values, error_indexes):
        if max(error_indexes) < len(polynomial):
            for i in range(len(error_values)):
                index = len(polynomial) - error_indexes[i] - 1
                polynomial[index] = self.add_galois(polynomial[index], error_values[i])
        else:
            raise Exception('chuj')

    def add_errors(self, error_number, message, is_parity):
        """
            przyjmuje ze message jest tablicą juz zamienioną na bity
            przyjmuje ze od lewej patrzac najpierw jest n-k=2t bajtow pairity i potem k bajtow data.
            bajty mnoze przez 8 i lece po tablicy to samo dla add_parity_errors
        """
        pairity_count = 2 * self.t
        message_count = len(message) - 2 * self.t
        if (is_parity and pairity_count < error_number) or (not is_parity and message_count < error_number):
            raise Exception('Too much error number to correct')
        error_indexes = []
        error_counter = 0
        while error_counter < error_number:
            if is_parity:
                index = random.randint(len(message) - (2 * self.t), len(message) - 1)
            else:
                index = random.randint(0, len(message) - (2 * self.t) - 1)
            if index not in error_indexes:
                symbol = random.randint(1, 2 ** self.m - 1)
                if symbol == message[index]:
                    continue
                message[index] = symbol
                error_indexes.append(index)
                error_counter += 1
        return message

    def add_errors_string(self, error_number, message, is_parity):
        if error_number == 0:
            return message
        max_bits_per_word = (self.m * self.k) + (self.t * 2 * self.m)
        if len(message) > max_bits_per_word:
            words = math.ceil(len(message) / max_bits_per_word)
            total_word = ''
            words -= 1
            missing_message_end_len = len(message) - (words * max_bits_per_word)
            word = self.add_errors(error_number,
                                   self.get_message_polynomial(
                                       self.add_missing_zeros(message[0:missing_message_end_len], False),
                                       encoding=False),
                                   is_parity)
            total_word += self.array_to_binary(word, self.m)
            k = missing_message_end_len
            for i in range(words):
                word = self.add_errors(error_number, self.get_message_polynomial(
                    self.add_missing_zeros(message[k:k + max_bits_per_word], False), encoding=False), is_parity)
                total_word += self.array_to_binary(word, self.m)
                k += max_bits_per_word
            return self.remove_leading_zeros(total_word)
        message = self.add_missing_zeros(message, encoding=False)
        array = self.get_message_polynomial(message, encoding=False)
        array = self.add_errors(error_number, array, is_parity)
        return self.array_to_binary(array, self.m)

    def simple_mochnacki_decoder(self, message):
        i = 0
        weight = 0
        while True:
            message_poly = self.get_message_polynomial(message, encoding=False)
            syndrome_poly = self.__galois_division(message_poly, self.__generator)[1]
            weight = calculate_weight(self.array_to_binary(syndrome_poly, self.m))
            if weight <= self.t:
                break
            if i == self.k:
                raise Exception
            message = self.__shift_right(message)
            message = self.add_missing_zeros(message, encoding=False)
            i += 1
        message_poly = self.__add_two_polynomials(message_poly, syndrome_poly)
        message = self.array_to_binary(message_poly, self.m)
        for j in range(i):
            message = self.__shift_left(message)
        return message

    def __shift_right(self, message):
        shifted = message[-N:] + message[:-N]
        return shifted

    def __shift_left(self, message):
        shifted = message[N:] + message[:N]
        return shifted
