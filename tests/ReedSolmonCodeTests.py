import unittest
from reed_solomon_code.ReedSolomonCode import ReedSolomonCode

class ReedSolomonCodeTests(unittest.TestCase):

    def test_generator_function_16(self):
        solomon_15_13 = ReedSolomonCode(4, 1).get_generator()
        solomon_15_11 = ReedSolomonCode(4, 2).get_generator()
        solomon_15_9 = ReedSolomonCode(4, 3).get_generator()
        solomon_15_7 = ReedSolomonCode(4, 4).get_generator()
        self.assertEqual(solomon_15_13, [1, 6, 8])
        self.assertEqual(solomon_15_11, [1, 13, 12, 8, 7])
        self.assertEqual(solomon_15_9, [1, 7, 9, 3, 12, 10, 12])
        self.assertEqual(solomon_15_7, [1, 9, 4, 3, 4, 13, 6, 14, 12])

    def test_generator_function_256(self):
        solomon_255_253 = ReedSolomonCode(8, 1).get_generator()
        solomon_255_251 = ReedSolomonCode(8, 2).get_generator()
        solomon_255_249 = ReedSolomonCode(8, 3).get_generator()
        solomon_255_247 = ReedSolomonCode(8, 4).get_generator()
        solomon_255_215 = ReedSolomonCode(8, 20).get_generator()
        self.assertEqual(solomon_255_253, [1, 6, 8])
        self.assertEqual(solomon_255_251, [1, 30, 216, 231, 116])
        self.assertEqual(solomon_255_249, [1, 126, 4, 158, 58, 49, 117])
        self.assertEqual(solomon_255_247, [1, 227, 44, 178, 71, 172, 8, 224, 37])
        self.assertEqual(solomon_255_215, [
            1, 185, 199, 211, 145, 4, 13, 169, 242, 158, 179, 8, 47, 227, 94, 108,
            236, 94, 238, 83, 50, 131, 102, 25, 192, 28, 111, 81, 42, 237, 188, 120,
            100, 183, 252, 104, 93, 19, 163, 137, 160]
        )

    def test_solomon_4_1_False(self):
        for i in range(1000):
            solomon = ReedSolomonCode(4, 1)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 23, 3, 5, 2]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 4))
            encoded_message = solomon.encode_number(message_string)
            print(encoded_message)
            encoded_message_with_errors = solomon.add_errors_string(1, encoded_message, is_parity=False)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)

    def test_solomon_4_1_True(self):
        for i in range(1000):
            solomon = ReedSolomonCode(4, 1)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 23, 3, 5, 6, 2, 6, 2, 4]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 4))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(1, encoded_message, is_parity=True)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_4_2_False(self):
        for i in range(1000):
            solomon = ReedSolomonCode(4, 2)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 4))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(2, encoded_message, is_parity=False)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_4_2_True(self):
        for i in range(1000):
            solomon = ReedSolomonCode(4, 2)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 4))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(2, encoded_message, is_parity=True)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_4_3_False(self):
        for i in range(1000):
            solomon = ReedSolomonCode(4, 3)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 23, 3, 5, 6, 2, 6, 2, 4]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 4))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(3, encoded_message, is_parity=False)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_4_3_True(self):
        for i in range(1000):
            solomon = ReedSolomonCode(4, 3)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 23, 3, 5, 6, 2, 6, 2, 4]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 4))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(3, encoded_message, is_parity=True)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_4_4_False(self):
        for i in range(1000):
            solomon = ReedSolomonCode(4, 4)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 23, 3, 5, 6, 2, 6, 2, 4]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 4))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(4, encoded_message, is_parity=False)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_4_4_True(self):
        for i in range(1000):
            solomon = ReedSolomonCode(4, 4)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 23, 3, 5, 6, 2, 6, 2, 4]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 4))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(4, encoded_message, is_parity=True)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_4_5_False(self):
        for i in range(1000):
            solomon = ReedSolomonCode(4, 3)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 23, 3, 5, 6, 2, 6, 2, 4]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 4))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(5, encoded_message, is_parity=False)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_4_5_True(self):
        for i in range(1000):
            solomon = ReedSolomonCode(4, 3)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 23, 3, 5, 6, 2, 6, 2, 4]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 4))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(5, encoded_message, is_parity=True)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_8_2_False(self):
        for i in range(1000):
            solomon = ReedSolomonCode(8, 2)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5, 8, 5, 2, 35, 6, 7, 1, 8, 0, 56, 2, 34, 6, 4, 26,
             7, 3, 4, 7, 5, 2, 1, 6, 5, 5, 3, 6]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 8))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(2, encoded_message, is_parity=False)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_8_2_True(self):
        for i in range(1000):
            solomon = ReedSolomonCode(8, 2)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5, 8, 5, 2, 35, 6, 7, 1, 8, 0, 56, 2, 34, 6, 4, 26,
             7, 3, 4, 7, 5, 2, 1, 6, 5, 5, 3, 6]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 8))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(2, encoded_message, is_parity=True)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_8_8_False(self):
        for i in range(1000):
            solomon = ReedSolomonCode(8, 2)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5, 8, 5, 2, 35, 6, 7, 1, 8, 0, 56, 2, 34, 6, 4, 26,
             7, 3, 4, 7, 5, 2, 1, 6, 5, 5, 3, 6, 7, 7, 3, 7, 1, 3, 4, 8, 2, 4, 2, 76, 3]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 8))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(8, encoded_message, is_parity=False)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_8_8_True(self):
        for i in range(1000):
            solomon = ReedSolomonCode(8, 2)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5, 8, 5, 2, 35, 6, 7, 1, 8, 0, 56, 2, 34, 6, 4, 26,
             7, 3, 4, 7, 5, 2, 1, 6, 5, 5, 3, 6, 7, 7, 3, 7, 1, 3, 4, 8, 2, 4, 2, 76, 3]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 8))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(8, encoded_message, is_parity=True)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_8_12_False(self):
        for i in range(1000):
            solomon = ReedSolomonCode(8, 2)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5, 8, 5, 2, 35, 6, 7, 1, 8, 0, 56, 2, 34, 6, 4, 26,
             7, 3, 4, 7, 5, 2, 1, 6, 5, 5, 3, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 8))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(12, encoded_message, is_parity=False)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_8_12_True(self):
        for i in range(1000):
            solomon = ReedSolomonCode(8, 2)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5, 8, 5, 2, 35, 6, 7, 1, 8, 0, 56, 2, 34, 6, 4, 26,
             7, 3, 4, 7, 5, 2, 1, 6, 5, 5, 3, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 8))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(12, encoded_message, is_parity=True)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_8_22_False(self):
        for i in range(1000):
            solomon = ReedSolomonCode(8, 2)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5, 8, 5, 2, 35, 6, 7, 1, 8, 0, 56, 2, 34, 6, 4, 26,
             7, 3, 4, 7, 5, 2, 1, 6, 5, 5, 3, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 8))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(22, encoded_message, is_parity=False)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)
    def test_solomon_8_22_True(self):
        for i in range(1000):
            solomon = ReedSolomonCode(8, 2)
            message = [7, 4, 0, 5, 15, 9, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5, 8, 5, 2, 35, 6, 7, 1, 8, 0, 56, 2, 34, 6, 4, 26,
             7, 3, 4, 7, 5, 2, 1, 6, 5, 5, 3, 6, 15, 5, 10, 5, 24, 6, 7, 12, 8, 3, 5]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 8))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(22, encoded_message, is_parity=True)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)

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

if __name__ == '__main__':
    unittest.main()