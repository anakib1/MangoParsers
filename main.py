from grammar import Terminal, NonTerminal, Rule, BaseSymbol, Grammar
from lookaheadUtils import firstK, followK


grammar = Grammar.read(open("./gram.txt", "r"))

first = firstK(grammar, 1)
for key, val in first.items():
    print(key, val)

print("-----------------------")

follow = followK(grammar, 1)
for key, val in follow.items():
    print(key, val)

print("llk")