# -*- coding: UTF-8 -*-
# !/usr/bin/env python
"""
Para is a conversion tool that converts user input to hex, ascii,
decimal, base64, binary.
"""
from __future__ import print_function
import argparse
import logging
import sys
import ast
import inspect
import string

try:
    from conversion import *
    import conversion
except ImportError:
    from para.conversion import *
    import para.conversion as conversion


PRINT_OFFSET = 19
FORMATSTRING = '{0: <' + str(PRINT_OFFSET) + '}'


class Para(object):
    """ Convert variable of some type to another type. """
    def __init__(self, value, logger, source='1 2 3 4 5',
                 target='1 2 3 4 5', out=sys.stdout):
        self.value = self.parse(value)
        self.logger = logger
        self.source = source.split()
        self.target = target.split()
        self.output_stream = out

    if sys.version_info < (3, 0):
        def parse(self, result):
            try:
                return result.encode('utf-8')
            except UnicodeDecodeError:
                return result.decode('utf-8')
    else:
        def parse(self, result):
            return result

    def is_subclass(self, sub_cls, cls):
        '''
        Returns True if the class received as the first parameter is a
        subclass of the class received as the second parameter and
        they are not the same class. Otherwise, returns False.
        '''
        return issubclass(sub_cls, cls) and sub_cls is not cls

    def iterate_conversions(self):
        """ Get list of functions in the convert module and call them. """
        self.logger.warning(FORMATSTRING.format('Action') + ' | ' + 'Result')
        self.logger.warning('-' * PRINT_OFFSET * 3)
        logevent = FORMATSTRING.format('User input ') + ' | ' +\
            ''.join(self.value)
        self.logger.info(logevent)
        convert_classes = inspect.getmembers(conversion, inspect.isclass)
        for title, conv in convert_classes:
            if not (self.is_subclass(conv, Conversion) and
                    conv.source_type_id in self.source):
                continue
            # For each class in conversion file,
            # run the related get_value function.
            for sub_title, conversion_method in convert_classes:
                if not (self.is_subclass(conversion_method, conv) and
                        conversion_method.target_type_id in self.target):
                    continue
                # Run these functions
                conversion_method.target_type_id
                c = conversion_method(self.value)
                self.log_event(c)

    def log_event(self, convertable):
        """ Call a function received as a parameter and log the result. """
        printable_text = convertable.title
        try:
            result = convertable.get_value()
        except Exception as e:  # pragma: no cover
            self.logger.debug(
                'DEBUG (Unhandeled exception). ' +
                'Failed to convert user input:', e)
            pass
        if type(result) is not str:
            try:
                result = str(result)
            except UnicodeEncodeError:
                pass
            except Exception as e:  # pragma: no cover
                self.logger.debug(
                    'DEBUG (Unhandeled exception). ' +
                    'Failed to convert the result to a string:', e)
                pass
        if self.logger.getEffectiveLevel() is not 50:
            # If not Quiet mode: print the table
            logevent = FORMATSTRING.format(printable_text) + ' | ' + result
        else:
            logevent = result
        if result:
            if self.logger.getEffectiveLevel() is 50\
                    and (len(self.source) == 1 and len(self.target) == 1):
                # In quiet mode, if there is only one result,
                # emit the last new line.
                print(logevent, end='', file=self.output_stream)
            else:
                self.logger.critical(logevent)
        else:
            self.logger.info(logevent)


def set_logging(verbose, quiet, out, debug):
    """ Initiate logging """
    logger = logging.getLogger(__name__)
    stream_handler = logging.StreamHandler(out)
    logger.addHandler(stream_handler)
    if verbose:
        logger.setLevel(logging.INFO)
    elif quiet:
        logger.setLevel(logging.CRITICAL)
    elif debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    return logger

def get_argument_parser():
    parser = argparse.ArgumentParser(
        description='Converts strings and numbers to other types.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''\
  Source and target type values:
                        1 = string
                        2 = decimal
                        3 = hex
                        4 = binary

Author: Migdalo (https://github.com/Migdalo)''')
    parser.add_argument(
        'convertable', nargs='?', default='',
        help='String or number you want to convert.')
    parser.add_argument(
        '-s', '--source', metavar='type', default='1 2 3 4',
        help='Input value type.')
    parser.add_argument(
        '-t', '--target', metavar='type', default='1 2 3 4 5',
        help='Output value type.')
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument(
        '-v', '--verbose', action='store_true', help='Use verbose mode.')
    verbosity_group.add_argument(
        '-q', '--quiet', action='store_true', help='Use quiet mode.')
    parser.add_argument(
        '-d', '--debug', action='store_true', help='Use debug mode.')
    return parser

def process_arguments(
        out=sys.stdout, instream=sys.__stdin__, args_list=[], debug=False):
    """ Create command-line interface and process arguments. """
    parser = get_argument_parser()

    if not args_list:
        if not instream.isatty():
            try:
                input_line = '"' + instream.readline().strip() + '"'
                args_list.append(ast.literal_eval(input_line))
            except UnicodeDecodeError:
                # Raised when piping compiled code to Para if Para
                # is installed using Python 3.
                raise parser.error('bad input')
            except (TypeError, ValueError) as te:
                # Capture null byte exceptions.
                # TypeError in Python2 and ValueError in Python3
                #print(sys.exc_info()[2].print_stack())
                raise parser.error(str(te))
            except Exception as e:  # pragma: no cover
                logger.debug(
                    'DEBUG (Unhandeled exception). ' +
                    'Failed to process user input:', e)
                raise parser.error('Unknown input')
        if sys.argv[0] != 'setup.py':  # pragma: no cover
            args_list.extend(sys.argv[1:])
    args = parser.parse_args(args_list)
    if not args.convertable:
        raise parser.error('too few arguments')
    if args.debug:
        debug = args.debug
    logger = set_logging(args.verbose, args.quiet, out, debug)
    try:
        convertable = Para(args.convertable, logger, args.source, args.target, out)
    except UnicodeDecodeError:  # pragma: no cover
        raise parser.error('UnicodeDecodeError')
    convertable.iterate_conversions()
    logging.shutdown()


if __name__ == '__main__':  # pragma: no cover
    process_arguments()
