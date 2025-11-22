# Dozenal

A comprehensive Python package for dozenal (base-12) mathematics, featuring an interactive REPL, conversion utilities, expression calculator, and NumPy-powered advanced operations.

## Features

### Interactive REPL Interface
When you run `dozenal` without arguments, you'll enter an interactive mode with:
- **Convert**: Bidirectional conversion between decimal and dozenal
- **Calc**: Evaluate dozenal expressions (e.g., `1+2*3`)
- **Table**: Display multiplication tables in dozenal
- **Sequence**: Generate number sequences (count, powers of 12, squares, cubes)
- **Compare**: Compare number representations across multiple bases
- **Matrix**: NumPy-powered matrix operations (addition, multiplication, determinant, inverse)
- **Stats**: Statistical operations (mean, median, std dev, min, max, sum)
- **Trig**: Trigonometric functions with dozenal output
- **Poly**: Polynomial evaluation
- **Regression**: Linear regression analysis

### Command-Line Tools
- **Converter**: Convert between decimal and dozenal
  ```bash
  dozenal --tool converter --to-doz 144    # Output: 100
  dozenal --tool converter --to-dec 100    # Output: 144
  ```
- **Calculator**: Evaluate dozenal expressions
  ```bash
  dozenal --tool calculator --calc-expr "T+2"  # Output: Decimal: 12, Dozenal: 10
  ```

### NumPy-Powered Features
- Matrix operations (addition, multiplication, determinant, inverse)
- Statistical analysis (mean, median, standard deviation)
- Polynomial evaluation
- Linear regression
- Trigonometric functions
- Eigenvalue computation

## Installation

```bash
pip install dozenal
```

**Note**: Requires Python 3.14+

## Usage

### Interactive Mode
Simply run:
```bash
dozenal
```
Or explicitly:
```bash
dozenal --interactive
```

### Command-Line Mode
```bash
# Convert decimal to dozenal
dozenal --tool converter --to-doz 3.5
# Output: 3.6

# Convert dozenal to decimal
dozenal --tool converter --to-dec T.6
# Output: 10.5

# Evaluate dozenal expression
dozenal --tool calculator --calc-expr "(1+2)*3"
# Output: Decimal result: 9, Dozenal result: 9

# List available tools
dozenal --list-tools
```

## Dozenal Number System

Dozenal uses base-12, with digits:
- `0-9`: Same as decimal
- `T`: Ten (10 in decimal)
- `E`: Eleven (11 in decimal)

### Examples
- `10` (dozenal) = `12` (decimal) - One dozen
- `100` (dozenal) = `144` (decimal) - One gross
- `T` (dozenal) = `10` (decimal)
- `E` (dozenal) = `11` (decimal)

## Development

### Running Tests
```bash
python -m pytest tests
```

### Project Structure
```
dozenal/
├── src/dozenal/
│   ├── __init__.py
│   ├── cli.py                        # Command-line interface
│   ├── dozenal_decimal_converter.py  # Conversion utilities
│   ├── dozenal_calc.py               # Expression calculator
│   ├── interactive.py                # Interactive REPL
│   └── advanced_math.py              # NumPy-powered operations
└── tests/
    ├── test_dozenal_decimal_converter.py
    ├── test_dozenal_calc.py
    ├── test_interactive.py
    └── test_advanced_math.py
```

## Examples

### Interactive Session
```
$ dozenal
============================================================
  Welcome to the Dozenal Interactive Calculator
  Base-12 Mathematics and Conversion Tools
============================================================

dozenal> table
Dozenal Multiplication Table (1-12)
----------------------------------------------------------------------
   |    1    2    3    4    5    6    7    8    9    T    E   10
----------------------------------------------------------------------
  1|    1    2    3    4    5    6    7    8    9    T    E   10
  2|    2    4    6    8    T   10   12   14   16   18   1T   20
  ...

dozenal> compare
Enter a decimal number: 144
Representations of 144:
  Binary (base-2):  0b10010000
  Octal (base-8):   0o220
  Decimal (base-10): 144
  Dozenal (base-12): 100
  Hex (base-16):    0x90

dozenal> quit
```

### Python API
```python
from dozenal import decimal_to_dozenal, dozenal_to_decimal
from dozenal.dozenal_calc import calculate
from dozenal.advanced_math import polynomial_eval, trigonometric_functions

# Conversion
print(decimal_to_dozenal(144))  # Output: 100
print(dozenal_to_decimal("100"))  # Output: 144

# Calculator
result = calculate("T+2")
print(f"{result.decimal} (decimal) = {result.dozenal} (dozenal)")

# Polynomial evaluation
result = polynomial_eval([1, 2, 3], 2)  # 1 + 2x + 3x² at x=2
print(result)  # {'decimal': '17.0', 'dozenal': '15'}

# Trigonometric functions
import math
result = trigonometric_functions(math.pi/4)
print(result['sin'])  # Both decimal and dozenal representations
```

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.
