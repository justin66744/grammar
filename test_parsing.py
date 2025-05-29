import unittest
from grammar import Grammar
from option_rules import Rules
from symbols import Terminal, Variable


class FakeGrammarReader:
    def __init__(self, content_lines):
        self.content_lines = content_lines

    def read_lines(self, filename):
        return [line.strip() for line in self.content_lines if line.strip()]


class FileGrammarReader:
    def read_lines(self, filename):
        try:
            with open(filename, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"File doesn't exist")
            return []
        except IOError:
            print(f"Couldn't open file")
            return []


def parse_grammar(reader, filename = None):
    grammar = Grammar()
    lines = reader.read_lines(filename)

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
                    if symbol[0] == '[' and symbol[len(symbol) - 1] == ']':
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


class TestParseGrammar(unittest.TestCase):
    def test_simple_grammar_parsing(self):
        grammar_content = [
            "{", "IsGerald", "1 Gerald is [Adjective] today", "}",
            "{", "Adjective", "3 happy", "2 excited", "}"
        ]
        reader = FakeGrammarReader(grammar_content)
        grammar = parse_grammar(reader)

        self.assertIsInstance(grammar, Grammar)
        self.assertTrue(grammar.has_rule('IsGerald'))
        self.assertTrue(grammar.has_rule('Adjective'))

        gerald_rule = grammar.get_rule('IsGerald')
        self.assertEqual(gerald_rule._var, 'IsGerald')
        self.assertEqual(len(gerald_rule._options), 1)

        adjective_rule = grammar.get_rule('Adjective')
        self.assertEqual(adjective_rule._var, 'Adjective')
        self.assertEqual(len(adjective_rule._options), 2)

    def test_complex_grammar_with_multiple_options(self):
        grammar_content = [
            "{", "Sentence", "2 [Subject] [Verb] [Object]", "1 [Subject] [Verb]", "}",
            "{", "Subject", "5 I", "3 You", "1 They", "}",
            "{", "Verb", "2 run", "2 walk", "1 jump", "}",
            "{", "Object", "1 quickly", "1 slowly", "}"
        ]
        reader = FakeGrammarReader(grammar_content)
        grammar = parse_grammar(reader)

        sentence_rule = grammar.get_rule('Sentence')
        self.assertEqual(len(sentence_rule._options), 2)

        subject_rule = grammar.get_rule('Subject')
        self.assertEqual(len(subject_rule._options), 3)

        weights = [option[0] for option in subject_rule._options]
        self.assertIn(5, weights)
        self.assertIn(3, weights)
        self.assertIn(1, weights)

    def test_terminal_and_variable_symbol_parsing(self):
        grammar_content = [
            "{", "TestRule", "1 simple terminal", "1 [Variable] mixed with terminals",
            "1 [Var1] [Var2] multiple variables", "}"
        ]
        reader = FakeGrammarReader(grammar_content)
        grammar = parse_grammar(reader)

        rule = grammar.get_rule('TestRule')
        options = rule._options

        first_option_symbols = options[0][1]
        self.assertEqual(len(first_option_symbols), 2)
        self.assertIsInstance(first_option_symbols[0], Terminal)
        self.assertIsInstance(first_option_symbols[1], Terminal)
        self.assertEqual(first_option_symbols[0]._value, 'simple')
        self.assertEqual(first_option_symbols[1]._value, 'terminal')

        second_option_symbols = options[1][1]
        self.assertEqual(len(second_option_symbols), 4)
        self.assertIsInstance(second_option_symbols[0], Variable)
        self.assertEqual(second_option_symbols[0]._name, 'Variable')

        third_option_symbols = options[2][1]
        self.assertEqual(len(third_option_symbols), 4)
        self.assertIsInstance(third_option_symbols[0], Variable)
        self.assertIsInstance(third_option_symbols[1], Variable)
        self.assertEqual(third_option_symbols[0]._name, 'Var1')
        self.assertEqual(third_option_symbols[1]._name, 'Var2')

    def test_empty_option_symbols(self):
        grammar_content = ["{", "EmptyRule", "1", "}"]
        reader = FakeGrammarReader(grammar_content)
        grammar = parse_grammar(reader)

        rule = grammar.get_rule('EmptyRule')
        self.assertEqual(len(rule._options), 1)
        option = rule._options[0]
        self.assertEqual(option[0], 1)
        self.assertEqual(len(option[1]), 0)

    def test_comments_are_ignored(self):
        grammar_content = [
            "This is a comment line", "Another comment",
            "{", "RuleAfterComments", "1 test rule", "}",
            "Comment between rules",
            "{", "AnotherRule", "2 another test", "}",
            "Final comment at end"
        ]
        reader = FakeGrammarReader(grammar_content)
        grammar = parse_grammar(reader)

        self.assertTrue(grammar.has_rule('RuleAfterComments'))
        self.assertTrue(grammar.has_rule('AnotherRule'))
        self.assertEqual(len(grammar._rules), 2)

    def test_whitespace_handling(self):
        grammar_content = [
            "{", "  SpacedRule  ", "  1   spaced   symbols   ",
            "  2 [Variable]   terminal   [AnotherVar]  ", "}"
        ]
        reader = FakeGrammarReader(grammar_content)
        grammar = parse_grammar(reader)

        rule = grammar.get_rule('SpacedRule')
        self.assertEqual(len(rule._options), 2)

        first_option = rule._options[0]
        self.assertEqual(len(first_option[1]), 2)
        self.assertEqual(first_option[1][0]._value, 'spaced')
        self.assertEqual(first_option[1][1]._value, 'symbols')

    def test_single_character_symbols(self):
        grammar_content = [
            "{", "SingleChar", "1 a b c", "1 [X] [Y] [Z]", "1 ! @ #", "}"
        ]
        reader = FakeGrammarReader(grammar_content)
        grammar = parse_grammar(reader)

        rule = grammar.get_rule('SingleChar')
        self.assertEqual(len(rule._options), 3)

        first_option = rule._options[0]
        self.assertEqual(len(first_option[1]), 3)
        for i, char in enumerate(['a', 'b', 'c']):
            self.assertIsInstance(first_option[1][i], Terminal)
            self.assertEqual(first_option[1][i]._value, char)

    def test_large_weights(self):
        grammar_content = [
            "{", "LargeWeights", "100 high weight option", "1000 very high weight", "1 low weight",
            "}"
        ]
        reader = FakeGrammarReader(grammar_content)
        grammar = parse_grammar(reader)

        rule = grammar.get_rule('LargeWeights')
        weights = [option[0] for option in rule._options]
        self.assertIn(100, weights)
        self.assertIn(1000, weights)
        self.assertIn(1, weights)

    def test_empty_grammar(self):
        grammar_content = []
        reader = FakeGrammarReader(grammar_content)
        grammar = parse_grammar(reader)

        self.assertIsInstance(grammar, Grammar)
        self.assertEqual(len(grammar._rules), 0)

    def test_grammar_with_only_comments(self):
        grammar_content = [
            "This is just a comment", "Another comment line", "# Yet another comment"
        ]
        reader = FakeGrammarReader(grammar_content)
        grammar = parse_grammar(reader)

        self.assertIsInstance(grammar, Grammar)
        self.assertEqual(len(grammar._rules), 0)


if __name__ == '__main__':
    unittest.main()