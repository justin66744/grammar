from grammar import Grammar
from option_rules import Rules
from symbols import Terminal, Variable

#File isn't explicitly covered as I'm using a
#double that mimics the functionality for testing.
def parse_file(filename):
    grammar = Grammar()

    with open(filename, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]


    i = 0

    while i < len(lines):
        if lines[i] == '{':
            i += 1
            var = lines[i]
            i += 1
            rule = Rules(var)

            while i < len(lines) and lines[i] != '}':
                pieces = lines[i].split()
                weight = int(pieces[0])
                symbols = []

                for symbol in pieces[1:]:
                    if symbol[0] == '[' and symbol[len(symbol)-1] == ']' and len(symbol) > 2:
                        var_name = symbol[1:-1]
                        symbols.append(Variable(var_name))
                    else:
                        symbols.append(Terminal(symbol))
                rule.add_option(weight, symbols)
                i += 1
            grammar.add_rule(var, rule)
            i += 1
        else:
            i += 1

    return grammar