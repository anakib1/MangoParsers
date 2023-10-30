from lookaheadUtils import followK, firstK, sequenceFirstK, KconcatenateTwoSets
from grammar import Grammar, Terminal, NonTerminal, Rule
from typing import Tuple, List, Dict
from iparser import IParser

def buildLLKTable(grammar: Grammar, k: int):
    """
    builds a table of rules for stack automata to parse strings
    this function returns table, reverse_ordering
    table : dict[NonTerminal, dict[Tuple[Terminal], int]]
    reverse_ordering : dict[int, Rule]
    where table is the table for transitions and reverse_ordering is the 
    labeling of rules for the table
    
    The function returns None if the grammar is not strong LL(k)
    """
    first = firstK(grammar, k)
    follow = followK(grammar, k)
    ordering = dict()
    reverse_ordering = dict()
    for i, rule in enumerate(grammar.rules):
        ordering[rule] = i
        reverse_ordering[i] = rule
    sets = dict()
    for rule in grammar.rules:
        set1 = sequenceFirstK(rule.en, first, k)
        set2 = follow[rule.st]
        sets[rule] = KconcatenateTwoSets(set1, set2, k)
    ans = {
        nterm: dict()
        for nterm in grammar.non_terms
    }
    for rule in grammar.rules:
        for tup in sets[rule]:
            if tup in ans[rule.st]:
                return None
            ans[rule.st][tup] = ordering[rule]
    return ans, reverse_ordering


def LLKParser(string: str, grammar: Grammar, table: Dict[NonTerminal, Dict[Tuple[Terminal], int]], ordering: Dict[int, Rule], k: int) -> List[int]:
    """
    Parse the given string using LL(k) parser
    if the string can not be parsed prints the error and return None
    otherwise returns the sequence of rules to produce the string
    """
    stack = [grammar.start_symbol]
    sequence = []
    pos = 0
    while stack:
        nterm = stack.pop()
        if isinstance(nterm, Terminal):
            if pos >= len(string):
                print(f"Synthax error near end, the string ends, but the stack doesn't")
                return None
            if nterm.symbol != string[pos]:
                print(f"Synthax error near {pos} symbol, {string[pos]} != {nterm}")
                return None
            pos += 1
            continue
        tup = tuple(Terminal(term) for term in string[pos: min(pos + k, len(string))])
        if not tup:
            tup = tuple([Terminal("eps")])
        if not (tup in table[nterm]):
            print(f"Synthax error near {pos} symbol, can not parse {nterm} -> {tup}")
            return None
        rule_num = table[nterm][tup]
        sequence.append(rule_num)
        rule = ordering[rule_num]
        if rule.en[0] == Terminal("eps"):
            continue
        for sym in reversed(rule.en):
            stack.append(sym)
    if pos < len(string):
        print(f"Synthax error near {pos} symbol")
        return None
    return sequence

class LLKParserWrapped(IParser):

    def __init__(self, k = 5):
        self.k = k 

    def init(self, grammar:Grammar) -> None:
        self.grammar = grammar 
        self.table, self.order = buildLLKTable(grammar, self.k)

    def verify(self, s: str) -> bool:
        ret = LLKParser(s, self.grammar, self.table, self.order, self.k)
        if ret is None:
            return False
        return True
        
    def parse(self, s : str) -> List[Rule]:
        ret = LLKParser(s, self.grammar, self.table, self.order, self.k)
        if ret is None:
            return []
        return [self.order[x] for x in ret]
