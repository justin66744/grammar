import random

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
            if selected < total:
                for symbol in symbols:
                    yield from symbol.generate(grammar)
                break