""" Test the Para module. """
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import unittest
import para.para as para

class TestPara(unittest.TestCase):
    """ Test process_arguments() function. """
    def test_decimal_input(self):
        """ Test para with a basic input. """
        result = 'Action              | Result\n' + \
                 '---------------------------------------------------------\n' + \
                 'Ascii to binary     | 001100010011001000110011\n' + \
                 'Ascii to decimal    | [49, 50, 51]\n' + \
                 'Ascii to hex        | 313233\n' + \
                 'Decimal to ascii    | {\n' + \
                 'Decimal to binary   | 01111011\n' + \
                 'Decimal to hex      | 7b\n' + \
                 'Encode base64       | MTIz\n' + \
                 'Hex to decimal      | 291\n' + \
                 'ROT13               | 456'
        out = StringIO()
        para.process_arguments(out, ['123'])
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)

    def test_verbosity(self):
        """ Test para with a basic input using verbose mode. """
        result = 'Action              | Result\n' + \
                 '---------------------------------------------------------\n' + \
                 'User input          | 123\n' + \
                 'Ascii to binary     | 001100010011001000110011\n' + \
                 'Ascii to decimal    | [49, 50, 51]\n' + \
                 'Ascii to hex        | 313233\n' + \
                 'Binary to ascii     | \n' + \
                 'Binary to decimal   | \n' + \
                 'Decimal to ascii    | {\n' + \
                 'Decimal to binary   | 01111011\n' + \
                 'Decimal to hex      | 7b\n' + \
                 'Decode base64       | \n' + \
                 'Encode base64       | MTIz\n' + \
                 'Hex to ascii        | \n' + \
                 'Hex to decimal      | 291\n' + \
                 'ROT13               | 456'
        out = StringIO()
        para.process_arguments(out, ['-v', '123'])
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)

    def test_quiet(self):
        """ Test para with a basic input using quiet mode. """
        result = '001100010011001000110011\n[49, 50, 51]\n' + \
                 '313233\n{\n01111011\n7b\nMTIz\n291\n456'
        out = StringIO()
        para.process_arguments(out, ['-q', '123'])
        my_result = out.getvalue().strip()
        self.assertMultiLineEqual(my_result, result)

if __name__ == '__main__':
    unittest.main()

