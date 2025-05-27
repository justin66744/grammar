class Grammar:
    def __init__(self):
        self._rules = {}

    def get_rule(self, variable):
        return self._rules.get(variable, None)

    def add_rule(self, variable, options):
        self._rules[variable] = options

class Rules:
    def __init__(self, weight, symbols):
        self._weight = weight
        self._symbols = symbols

class Symbol:
    def generate(self, grammar):
        pass

class Terminal(Symbol):
    def __init__(self, value):
        self._value = value

    def generate(self, grammar):
        yield self._value


class Variable(Symbol):
    def __init__(self, name):
        self._name = name

    def generate(self, grammar):
        rule = grammar.get_rule(self._name)
        if rule:
            yield from rule.generate(grammar)