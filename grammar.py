import random

class Grammar:
    def __init__(self):
        self._rules = {}

    def get_rule(self, variable):
        return self._rules.get(variable, None)

    def add_rule(self, variable, options):
        self._rules[variable] = options



class Rules:
    def __init__(self, variable):
        self._var = variable
        self._options = []
        self._total_weight = 0

    def add_option(self, weight, symbols):
        self._options.append((weight, symbols))
        self._total_weight += weight

    def generate(self, grammar):
        if not self._options:
            return
        selected = random.randrange(self._total_weight)
        total = 0

        for weight, symbols in self._options:
            total += weight
            if selected <= total:
                for symbol in symbols:
                    yield from symbol.generate(grammar)
                break


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