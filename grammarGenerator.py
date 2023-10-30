from grammar import Grammar, Rule, Terminal, NonTerminal
from typing import Dict, List


def generateString(grammar: Grammar, ordering: Dict[int, Rule], sequence: List[int]) -> List[Terminal]:
    mas = [grammar.start_symbol]
    for pos, rule_num in enumerate(sequence):
        pos = -1
        for i, sym in enumerate(mas):
            if isinstance(sym, NonTerminal):
                pos = i
                break
        if pos == -1:
            print(f"Error near {pos}, there has no nonterminals")
        rule = ordering[rule_num]
        nterm = mas[pos]
        if rule.st != nterm:
            print(f"Error near {pos}, not correct nonterminal, {nterm} != {rule.st}")
        if rule.en[0] == Terminal("eps"):
            mas = mas[:pos] + mas[pos+1:]
        else:
            mas = mas[:pos] + list(rule.en) + mas[pos+1:]
    return mas