# -*- coding: UTF-8 -*-
# !/usr/bin/env python
"""
Para is a conversion tool that converts user input to hex, ascii,
decimal, base64, binary and ROT13.
"""
from __future__ import print_function
import argparse
import logging
import sys
import ast
import inspect
import string

# For python 2 + python 3 compatibility
try:
    from conversion import *
    import conversion
except ImportError:
    from para.conversion import *
    import para.conversion as conversion
try:
    import cipher
except ImportError:
    import para.cipher as cipher


PRINT_OFFSET = 19
FORMATSTRING = '{0: <' + str(PRINT_OFFSET) + '}'


class Para(object):
    """ Convert variable of some type to another type. """
    def __init__(self, value, source='1 2 3 4 5',
                 target='1 2 3 4 5', out=sys.stdout):
        self.value = value
        self.source = source.split()
        self.target = target.split()
        self.convertable_list = self.value.split()
        self.output_stream = out

    def log_event(self, convertable, logger):
        """ Call a function received as a parameter and log the result. """
        try:
            printable_text = convertable.title
            result = convertable.get_value()
        except TypeError:
            # Capture error if function requires wrong number of parameters
            logger.debug('Failed to run function: ' + printable_text)
            return
        except (UnicodeDecodeError, AttributeError):
            logger.debug('Recieved non unicode characters.')
            return
        if type(result) in [int, list]:
            result = str(result)
        if logger.getEffectiveLevel() is not 50:
            # If not Quiet mode: print the table
            logevent = FORMATSTRING.format(printable_text) + ' | ' + result
        else:
            logevent = result
        if result:
            if logger.getEffectiveLevel() is 50\
            and (len(self.source) == 1 and len(self.target) == 1):
                # In quiet mode emit the last new line.
                print(logevent, end='', file=self.output_stream)
            else:
                logger.critical(logevent)
        else:
            logger.info(logevent)

    def print_results(self, logger):
        """Call log_event for each function in the convert module."""
        logger.warning(FORMATSTRING.format('Action') + ' | ' + 'Result')
        logger.warning('-' * PRINT_OFFSET * 3)
        logevent = FORMATSTRING.format('User input ') + ' | ' + str(self.value)
        logger.info(logevent)
        convertable_list = self.value.split()
        if len(convertable_list) == 1:
            self.iterate_options(logger)

    def iterate_options(self, logger):
        """ Get list of functions in the convert module and call them. """
        convert_classes = inspect.getmembers(conversion, inspect.isclass)
        for conv in convert_classes:
            if issubclass(conv[1], Conversion) and conv[1] is not Conversion \
                    and conv[1].source_type_id in self.source:
                # For each class in conversion file, run the related get_value function.
                for sub_conv in convert_classes:
                    if issubclass(sub_conv[1], conv[1]) and sub_conv[1] is not\
                            conv[1] and sub_conv[1].target_type_id in self.target:
                        try:
                            # Run these functions
                            sub_conv[1].target_type_id
                            c = sub_conv[1](self.value)
                            self.log_event(c, logger)
                        except AttributeError:
                            continue


def set_logging(verbose, quiet, out):
    """ Initiate logging """
    logger = logging.getLogger(__name__)
    stream_handler = logging.StreamHandler(out)
    if verbose:
        logger.setLevel(logging.INFO)
    elif quiet:
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.WARNING)
    logger.addHandler(stream_handler)
    return logger


def process_arguments(out=sys.stdout, test_args=None):
    """ Create command-line interface and process arguments. """
    parser = argparse.ArgumentParser(
        description='Converts strings and numbers to other types.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''\
  Source and target type values:
                        1 = bytestring
                        2 = decimal
                        3 = hex
                        4 = binary

Author: Migdalo (https://github.com/Migdalo)''')
    parser.add_argument(
        'convertable', nargs='?', default='',
        help='String or number you want to convert.')
    parser.add_argument(
        '-s', '--source', default='1 2 3 4',
        help='Specify the variable type you want your input ' +
        'to be considered by Para.')
    parser.add_argument(
        '-t', '--target', default='1 2 3 4 5',
        help='Specify the target type you want your input ' +
        'to be converted to.')
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument(
        '-v', '--verbose', action='store_true', help='Use verbose mode.')
    verbosity_group.add_argument(
        '-q', '--quiet', action='store_true', help='Use quiet mode.')

    if test_args: 
        args = parser.parse_args(test_args)
        if not args.convertable:
            raise parser.error("too few arguments")
        convertable = Para(args.convertable, args.source, args.target)
    else:
        if not sys.__stdin__.isatty():
            try:
                line = sys.__stdin__.readline().strip().split()
                line.extend(sys.argv[1:])
            except UnicodeDecodeError:
                raise parser.error("received non unicode characters")
        else:
            line = sys.argv[1:]
        args = parser.parse_args(line)
    convertable = Para(args.convertable, args.source, args.target, out)
    logger = set_logging(args.verbose, args.quiet, out)
    convertable.print_results(logger)
    logging.shutdown()


if __name__ == '__main__':
    process_arguments()
