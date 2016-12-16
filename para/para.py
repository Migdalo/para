#!/usr/bin/python

from convert import *
import argparse
import logging
import cipher

logger = logging.getLogger(__name__)
printoffset = 19

""" Calls a function received as a parameter and logs its result. """
def log_event(my_function, convertable, printable_text):
    global printoffset
    formatstring = '{0: <' + str(printoffset) +'}'
    result = my_function(convertable)
    
    # Quiet mode: print only the result
    if logger.getEffectiveLevel() is 50:
        if result:
            logger.critical(str(result))
        else:
            logger.debug(str(result))
    
    # Otherwise print the table
    else:
        logevent = formatstring.format(printable_text) + ' | ' + str(result)
        if result:
            logger.critical(logevent)
        else:
            logger.debug(logevent)

""" Calls log_event for each dunction in the convert module. """
def print_results(convertable):
    global printoffset
    formatstring = '{0: <' + str(printoffset) +'}'
    logger.warn(formatstring.format('Action')+ ' | ' + 'Result')
    logger.warn('-' * printoffset * 3)
    logevent = formatstring.format('User input ') + ' | ' + convertable
    logger.debug(logevent)
    log_event(hex_to_ascii, (convertable), 'Hex to ascii')
    log_event(ascii_to_hex, (convertable), 'Ascii to hex')
    log_event(encode_base64, (convertable), 'Encode base64')
    log_event(decode_base64, (convertable), 'Decode base64')
    log_event(integer_to_hex, (convertable), 'Decimal to hex')
    log_event(hex_to_integer, (convertable), 'Hex to decimal')
    log_event(integer_to_ascii, (convertable), 'Decimal to ascii')
    log_event(ascii_to_integer, (convertable), 'Ascii to decimal')
    log_event(ascii_to_binary, (convertable), 'Ascii to binary')
    log_event(integer_to_binary, (convertable), 'Decimal to binary')
    log_event(binary_to_int, (convertable), 'Binary to decimal')
    log_event(binary_to_ascii, (convertable), 'Binary to ascii')
    log_event(cipher.rotate, (convertable), 'ROT13')

""" Initiate logging """
def set_logging(verbose, quiet):
    ch = logging.StreamHandler()
    logger.addHandler(ch)
    if verbose:
        logger.setLevel(logging.DEBUG)
    elif quiet:
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.WARN)

""" Creates command-line interface and processes arguments. """
def process_arguments():
    parser = argparse.ArgumentParser(description='Converts strings and numbers to other types.',\
        epilog='Author: Migdalo (https://github.com/Migdalo)')
    parser.add_argument('convertable', help='String or number you want to convert.')
    parser.add_argument('-r', '--rot', action='store_true', \
        help='Print more rotation cipher results.')
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument('-v', '--verbose', action='store_true', help='Use verbose mode.')
    verbosity_group.add_argument('-q', '--quiet', action='store_true', help='Use quiet mode.')
    args = parser.parse_args()
    
    set_logging(args.verbose, args.quiet)
    if args.rot:
        cipher.solve_rotation(args.convertable)
    else:
        print_results(args.convertable)
    logging.shutdown()

if __name__ == '__main__':
    process_arguments()
