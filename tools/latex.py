filename = None

def set_filename(name: str):
    global filename 
    filename = name

_numbers = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
    6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
    11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
    16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen",
    20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
    60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety",
    100: "onehundred"
}
def _define_numbers():
    for number in range(21, 100):
        if number % 10 != 0:
            tens = number // 10 * 10
            ones = number % 10
            _numbers[number] = _numbers[tens] + _numbers[ones]
_define_numbers()

_prefixes = {
    "p": "\\pico",
    "n": "\\nano",
    "µ": "\\micro",
    "u": "\\micro",
    "m": "\\milli",
    "": "",
    "k": "\\kilo",
    "Meg": "\\mega",
}
_symbols = {
    "R": "\\ohm",
    "L": "\\henry",
    "C": "\\farad",
    "V": "\\volt",
    "s": "\\second",
}

def generate_variables(variables: dict):
    with open(f"{filename}-variables.tex", "w") as latexfile:
        for name, value in variables.items():
            identifier = name[1:]
            symbol = name[0]

            if identifier.isdigit():
                latex_name = f"{symbol}{_numbers[int(identifier)]}"
            elif identifier.isalpha():
                latex_name = f"{symbol}{identifier}"
            else: 
                raise ValueError(f"Invalid reference designator: {name}")

            if identifier.endswith(("Tdelay", "Trise", "Tfall", "Ton", "Tperiod")):
                symbol = "s"

            numeric = ""
            prefix = ""
            if symbol in _symbols:
                for char in value:
                    if char.isdigit() or char == "." or char == "-":
                        numeric += char
                    else:
                        prefix += char
                unit = _symbols[symbol]
                latex_value = f"{numeric}\\ {_prefixes[prefix]}{unit}"
            else: 
                latex_value = value

            latexfile.write(f"\\newcommand{{\\{latex_name}}}{{{latex_value}}}\n")