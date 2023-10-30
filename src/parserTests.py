import unittest

from core.grammar import Grammar, SymbolUtils
from core.RecursiveParser import RecursiveParser
from typing import Set
from core import lookaheadUtils

class ParserTest(unittest.TestCase):
    def testParser(self):
        grammar = Grammar.read(['S -> BA', 'A -> +BA | eps', 'B -> DC', 'C -> *DC | eps', 'D -> (S) | a'])
        parser = RecursiveParser(grammar)
        self.assertTrue(parser.verify('(a+a)*a'))
        self.assertTrue(parser.verify('a+a'))
        self.assertTrue(parser.verify('a'))
        self.assertFalse(parser.verify('abc'))


if __name__ == '__main__':
    unittest.main()