# Para

Para is a small command-line tool that converts user input to hex, ascii, integer, base64, binary and ROT13.

## Usage
```
usage: para [-h] [-r] [-v | -q] convertable

Converts user input to hex, ascii, integer, base64, binary and ROT13.

positional arguments:
  convertable    String or number you want to convert.

optional arguments:
  -h, --help     show this help message and exit
  -r, --rot      Print more rotation cipher results.
  -v, --verbose  Use verbose mode.
  -q, --quiet    Use quiet mode.
```

Example output:
```
example@example:~/$ para 123
Action              | Result
---------------------------------------------------------
Ascii to hex        | 313233
Encoding base64     | MTIz
Integer to hex      | 7b
Hex to integer      | 291
Integer to ascii    | {
Ascii to integer    | [49, 50, 51]
Ascii to binary     | 001100010011001000110011
Integer to binary   | 01111011
Binary to ascii     | {
ROT13               | 456
```

## License
Para is registered under [MIT license](/LICENSE).
