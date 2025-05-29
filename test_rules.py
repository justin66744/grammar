import unittest
from option_rules import Rules
from symbols import Terminal
from grammar import Grammar




class TestRules(unittest.TestCase):
   def test_rules_initialization(self):
       rule = Rules('TestVar')
       self.assertEqual(rule._var, 'TestVar')
       self.assertEqual(rule._options, [])
       self.assertEqual(rule._total_weight, 0)


   def test_add_option(self):
       rule = Rules('TestVar')
       symbols = [Terminal('hello'), Terminal('world')]
       rule.add_option(5, symbols)


       self.assertEqual(len(rule._options), 1)
       self.assertEqual(rule._total_weight, 5)
       self.assertEqual(rule._options[0][0], 5)
       self.assertEqual(rule._options[0][1], symbols)


   def test_add_multiple_options(self):
       rule = Rules('TestVar')
       symbols1 = [Terminal('option1')]
       symbols2 = [Terminal('option2')]


       rule.add_option(3, symbols1)
       rule.add_option(7, symbols2)


       self.assertEqual(len(rule._options), 2)
       self.assertEqual(rule._total_weight, 10)


   def test_generate_single_option(self):
       grammar = Grammar()
       rule = Rules('TestVar')
       rule.add_option(1, [Terminal('only'), Terminal('option')])


       result = list(rule.generate(grammar))
       self.assertEqual(result, ['only', 'option'])


   def test_generate_empty_options(self):
       grammar = Grammar()
       rule = Rules('TestVar')


       result = list(rule.generate(grammar))
       self.assertEqual(result, [])




if __name__ == '__main__':
   unittest.main()

