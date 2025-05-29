class Grammar:
    def __init__(self):
        self._rules = {}

    def get_rule(self, variable):
        return self._rules.get(variable, None)

    def add_rule(self, variable, options):
        self._rules[variable] = options

    def has_rule(self, variable):
        return variable in self._rules

    def generate(self, variable):
        rule = self.get_rule(variable)
        if rule:
            yield from rule.generate(self)