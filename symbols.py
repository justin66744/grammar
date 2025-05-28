class Terminal:
    def __init__(self, value):
        self._value = value

    def generate(self, grammar):
        yield self._value


class Variable:
    def __init__(self, name):
        self._name = name

    def generate(self, grammar):
        rule = grammar.get_rule(self._name)
        if rule:
            yield from rule.generate(grammar)