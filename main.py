from grammar import Terminal, NonTerminal, Rule, BaseSymbol, Grammar
from lookaheadUtils import firstK, followK
from llk import buildLLKTable, LLKParser
from grammarGenerator import generateString


grammar = Grammar.read(open("./gram.txt", "r"))
k = 2

first = firstK(grammar, k)
for key, val in first.items():
    print(key, val)

print("-----------------------")

follow = followK(grammar, k)
for key, val in follow.items():
    print(key, val)

print("--------------------")

out = buildLLKTable(grammar, k)
if out:
    table, ordering = out
    for key, val in table.items():
        print(key, val)
    for key, val in ordering.items():
        print(key, val)
    
    print("-----------------------")

    string = "(a+a)*a"
    sequence = LLKParser(string, grammar, table, ordering, k)
    print(sequence)

    print("-------------------------")

    string = generateString(grammar, ordering, sequence)
    print(string)
else:
    print(out)




