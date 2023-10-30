import unittest

from grammar import Grammar, SymbolUtils
from typing import Set
import lookaheadUtils

class LookaheadUtilsTest(unittest.TestCase):
    def checkSets(self, a : Set, b : Set):
        self.assertEqual(len(a), len(b))
        for x in a:
            self.assertTrue(x in b, f'set b does not contain element {x}')

    def testFirstKTable(self) :

        grammar = Grammar.read(['S -> BA', 'A -> +BA | eps', 'B -> DC', 'C -> *DC | eps', 'D -> (S) | a'])
        
        result = lookaheadUtils.firstK(grammar, 2)
        self.checkSets(
            result[SymbolUtils.getSymbol('A')], 
            set([
                SymbolUtils.getSymbols('eps'), 
                SymbolUtils.getSymbols('+a'), 
                SymbolUtils.getSymbols('+(')
            ])
        )
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()