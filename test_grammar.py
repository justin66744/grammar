import unittest
from grammar import Grammar
from option_rules import Rules
from symbols import *


class TestGrammar(unittest.TestCase):
   def test_grammar_initialization(self):
       grammar = Grammar()
       self.assertEqual(grammar._rules, {})


   def test_add_and_get_rule(self):
       grammar = Grammar()
       rule = Rules('TestRule')
       grammar.add_rule('TestRule', rule)


       retrieved_rule = grammar.get_rule('TestRule')
       self.assertEqual(retrieved_rule, rule)


   def test_get_nonexistent_rule(self):
       grammar = Grammar()
       result = grammar.get_rule('NonExistent')
       self.assertIsNone(result)


   def test_has_rule(self):
       grammar = Grammar()
       rule = Rules('ExistingRule')
       grammar.add_rule('ExistingRule', rule)


       self.assertTrue(grammar.has_rule('ExistingRule'))


       self.assertFalse(grammar.has_rule('NonExistentRule'))


       empty_grammar = Grammar()
       self.assertFalse(empty_grammar.has_rule('AnyRule'))


   def test_generate_with_existing_rule(self):
       grammar = Grammar()
       rule = Rules('TestVar')
       rule.add_option(1, [Terminal('hello')])
       grammar.add_rule('TestVar', rule)


       result = list(grammar.generate('TestVar'))
       self.assertEqual(result, ['hello'])


   def test_generate_with_nonexistent_rule(self):
       grammar = Grammar()
       result = list(grammar.generate('NonExistent'))
       self.assertEqual(result, [])




if __name__ == '__main__':
   unittest.main()




