from grammar import Terminal, NonTerminal, Rule, BaseSymbol, Grammar
from lookaheadUtils import KconcatenateTwostrings, KconcatenateTwoSets, firstK


grammar = Grammar.read(open("./gram.txt", "r"))

s = firstK(grammar, 2)
for key, val in s.items():
    print(key, val)