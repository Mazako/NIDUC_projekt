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

    def test_solomon_4_2(self):
        for i in range(1000):
            solomon = ReedSolomonCode(4, 2)
            message = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]
            message_string = ReedSolomonCode.remove_leading_zeros(ReedSolomonCode.array_to_binary(message, 4))
            encoded_message = solomon.encode_number(message_string)
            encoded_message_with_errors = solomon.add_errors_string(2, encoded_message, is_parity=False)
            decoded_number = solomon.decode_number(encoded_message_with_errors)
            self.assertEqual(message_string, decoded_number)


if __name__ == '__main__':
    unittest.main()
