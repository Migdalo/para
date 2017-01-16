""" Test cases against convert functions. """
import unittest
import para.convert as convert
import para.cipher as cipher

class TestConvert(unittest.TestCase):
    def test_decimal_to_ascii(self):
        self.assertEqual(convert.decimal_to_ascii(123), '{')

    def test_decimal_to_ascii_fail(self):
        self.assertEqual(convert.decimal_to_ascii('asd'), '')

    def test_ascii_to_decimal(self):
        self.assertEqual(convert.ascii_to_decimal('{'), 123)

    def test_ascii_to_decimal_fail(self):
        self.assertEqual(convert.ascii_to_decimal(1), '')

    def test_decimal_to_hex(self):
        self.assertEqual(convert.decimal_to_hex(123), '7b')

    def test_decimal_to_hex_fail(self):
        self.assertEqual(convert.decimal_to_hex('asd'), '')

    def test_hex_to_decimal(self):
        self.assertEqual(convert.hex_to_decimal('7b'), 123)

    def test_hex_to_decimal_fail(self):
        self.assertEqual(convert.hex_to_decimal('sk'), '')

    def test_ascii_to_hex(self):
        self.assertEqual(convert.ascii_to_hex('123'), '313233')

    def test_ascii_to_hex_fail(self):
        self.assertEqual(convert.ascii_to_hex(123), '')

    def test_hex_to_ascii(self):
        self.assertEqual(convert.hex_to_ascii('7b'), '{')

    def test_hex_to_ascii_fail(self):
        self.assertEqual(convert.hex_to_ascii('sk'), '')

    def test_encode_base64(self):
        self.assertEqual(convert.encode_base64('123'), 'MTIz')

    def test_decode_base64(self):
        self.assertEqual(convert.decode_base64('MTIz'), '123')

    def test_decode_base64_fail(self):
        self.assertEqual(convert.decode_base64('92438y7'), '')

    def test_decimal_to_binary(self):
        self.assertEqual(convert.decimal_to_binary(123), '01111011')

    def test_decimal_to_binary_fail(self):
        self.assertEqual(convert.decimal_to_binary('asd'), '')

    def test_ascii_to_binary(self):
        self.assertEqual(convert.ascii_to_binary('123'), '001100010011001000110011')

    def test_ascii_to_binary_fail(self):
        self.assertEqual(convert.ascii_to_binary(123), '')

    def test_binary_to_decimal(self):
        self.assertEqual(convert.binary_to_decimal('01111011'), 123)

    def test_binary_to_decimal_fail(self):
        self.assertEqual(convert.binary_to_decimal('234'), '')

    def test_binary_to_ascii(self):
        self.assertEqual(convert.binary_to_ascii('001100010011001000110011'), '123')

    def test_binary_to_ascii_fail(self):
        self.assertEqual(convert.binary_to_ascii('2345'), '')

    def test_rotation_simple(self):
        self.assertEqual(cipher.rotate('T2st1ngR0tat10n'), '6fFGeAt4dGnGedA')

if __name__ == '__main__':
    unittest.main()
