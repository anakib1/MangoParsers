from grammar import Grammar, NonTerminal, Terminal, Rule, SymbolUtils, BaseSymbol
from typing import List, Set, Tuple
from copy import deepcopy


def checkNonTerminalRule(rule: Rule) -> bool:
    """
    checks whether the end of the rule has only terminals
    in other words checks whethere the rule is terminal
    """
    for sym in rule.en:
        if isinstance(sym, NonTerminal):
            return False
    return True


def KconcatenateTwostrings(str1: Tuple[Terminal], str2: Tuple[Terminal], k: int) -> Tuple[Terminal]:
    """
    this function k-concatenates two k-terminal strings
    """
    if str1[0].isEpsilon():
        str1 = tuple()
    if str2[0].isEpsilon():
        str2 = tuple()
    return tuple(list(str1) + list(str2[0:max(0, min(k - len(str1), len(str2)))]))


def KconcatenateTwoSets(set1: Set[Tuple[Terminal]], set2: Set[Tuple[Terminal]], k: int) -> Set[Tuple[Terminal]]:
    """
    this function k-concatenates two sets of terminal k-strings
    """
    set3 = set()
    for str1 in set1:
        for str2 in set2:
            set3.add(KconcatenateTwostrings(str1, str2, k))
    return set3


def KconcatenateListOfSets(lst: List[Set[Tuple[Terminal]]], k) -> Set[Tuple[Terminal]]:
    """
    this function k-concatenates sets of terminal k-strings
    """
    if not lst:
        return set()
    ans = lst[0]
    for i in range(1, len(lst)):
        ans = KconcatenateTwoSets(ans, lst[i], k)
    return ans


def firstK(grammar: Grammar, k: int) -> dict[NonTerminal, Set[Tuple[Terminal]]]:
    """
    for every terminal in grammmar returns the set of all 
    possible firstk tuples that the NonTerminal can produce
    """
    ans = {
        nterm : set() 
        for nterm in grammar.non_terms
    }
    for rule in grammar.rules:
        if checkNonTerminalRule(rule):
            ans[rule.st].add(tuple(rule.en[:min(len(rule.en), k)]))
    while True:
        stop = True
        for rule in grammar.rules:
            lst = []
            for sym in rule.en:
                if isinstance(sym, Terminal):
                    lst.append({tuple([sym])})
                else:
                    lst.append(ans[sym])
            new_set = KconcatenateListOfSets(lst, k)
            if not new_set.issubset(ans[rule.st]):
                stop = False
                ans[rule.st].update(new_set)
        if stop:
            break
    return ans

