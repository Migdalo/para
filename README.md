# Para

Para is a small command-line tool that converts user input to hex, ascii, decimal, base64, binary and ROT13.

## Usage
```
usage: para.py [-h] [-s SOURCE] [-t TARGET] [-v | -q] [convertable]

Converts strings and numbers to other types.

positional arguments:
  convertable           String or number you want to convert.

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Input value type.
  -t TARGET, --target TARGET
                        Output value type.
  -v, --verbose         Use verbose mode.
  -q, --quiet           Use quiet mode.

  Source and target type values:
                        1 = string
                        2 = decimal
                        3 = hex
                        4 = binary

Author: Migdalo (https://github.com/Migdalo)

```

Example output:
```
example@example:~/$ para 123
Action              | Result
---------------------------------------------------------
Ascii to binary     | 001100010011001000110011
Ascii to decimal    | [49, 50, 51]
Ascii to hex        | 313233
Encode base64       | MTIz
Decimal to ascii    | {
Decimal to binary   | 01111011
Decimal to hex      | 7b
Hex to ascii        | ģ
Hex to binary       | 100100011
Hex to decimal      | 291

```
Example of quiet output when converting from decimal to ascii (note: there is no new line after the result):

```
via@kali:~/Documents/para2$ python para/para.py -q -s 2 -t 1 123
{
```


## License
Para is registered under [MIT license](/LICENSE).
