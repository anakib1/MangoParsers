import unittest

from core.grammar import Grammar, SymbolUtils
from typing import Set
from core import lookaheadUtils
from core.llk import LLKParserWrapped

class ParserTest(unittest.TestCase):
    def testParserLL1(self):
        grammar = Grammar.read(['S -> BA', 'A -> +BA | eps', 'B -> DC', 'C -> *DC | eps', 'D -> (S) | a'])
        parser = LLKParserWrapped(1)
        parser.init(grammar)

        self.assertTrue(parser.verify('(a+a)*a'))
        self.assertTrue(parser.verify('a+a'))
        self.assertTrue(parser.verify('a'))
        self.assertFalse(parser.verify('abc'))

    def testParserLL2(self):
        grammar = Grammar.read(['S -> aaA', 'A -> aAc | bBc', 'B -> bBc | bc'])
        parser = LLKParserWrapped(2)
        parser.init(grammar)

        # n = 2, m = 5
        self.assertTrue(parser.verify('aaaabbbbbccccccc'))
        self.assertFalse(parser.verify('aaaabbbbbcccccc'))

    def testParserLL3(self):
        grammar = Grammar.read(['S -> aSA', 'S -> eps', 'A -> aabS | c'])
        parser = LLKParserWrapped(3)
        parser.init(grammar)

        self.assertTrue(parser.verify('aaab'))
        self.assertTrue(parser.verify('aaabaaab'))
        self.assertTrue(parser.verify('aaabaaabac'))

    def testParserLL3Again(self):
        grammar = Grammar.read(['S -> aaB | aaC', 'B -> b', 'C -> c'])
        parser = LLKParserWrapped(3)
        parser.init(grammar)

        self.assertTrue(parser.verify('aab'))
        self.assertTrue(parser.verify('aac'))


if __name__ == '__main__':
    unittest.main()