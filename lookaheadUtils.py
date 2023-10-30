from grammar import Grammar, NonTerminal, Terminal, Rule, SymbolUtils, BaseSymbol
from typing import List, Set, Tuple, Dict
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
    if not str1 or str1[0].isEpsilon():
        str1 = tuple()
    if not str2 or str2[0].isEpsilon():
        str2 = tuple()
    ans =  tuple(list(str1) + list(str2[0:max(0, min(k - len(str1), len(str2)))]))
    if not ans:
        return tuple([Terminal("eps")])
    else:
        return ans


def KconcatenateTwoSets(set1: Set[Tuple[Terminal]], set2: Set[Tuple[Terminal]], k: int) -> Set[Tuple[Terminal]]:
    """
    this function k-concatenates two sets of terminal k-strings
    """
    if not set1 or not set2:
        return {tuple([Terminal("eps")])}
    set3 = set()
    for str1 in set1:
        for str2 in set2:
            set3.add(KconcatenateTwostrings(str1, str2, k))
    return set3


def KconcatenateListOfSets(lst: List[Set[Tuple[Terminal]]], k: int) -> Set[Tuple[Terminal]]:
    """
    this function k-concatenates sets of terminal k-strings
    """
    if not lst:
        return {tuple([Terminal("eps")])}
    ans = lst[0]
    for i in range(1, len(lst)):
        ans = KconcatenateTwoSets(ans, lst[i], k)
    return ans


def firstK(grammar: Grammar, k: int) -> Dict[NonTerminal, Set[Tuple[Terminal]]]:
    """
    for every terminal in grammmar returns the set of all 
    possible firstk tuples that the NonTerminal can produce
    """
    ans = {
        nterm : "-" 
        for nterm in grammar.non_terms
    }
    for rule in grammar.rules:
        if checkNonTerminalRule(rule):
            if ans[rule.st] == "-":
                ans[rule.st] = set()
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
            if "-" in lst:
                continue
            new_set = KconcatenateListOfSets(lst, k)
            if ans[rule.st] == "-":
                ans[rule.st] = set()
            if not new_set.issubset(ans[rule.st]):
                stop = False
                ans[rule.st].update(new_set)
        if stop:
            break
    return ans


def sequenceFirstK(seq: Tuple[BaseSymbol], dct: Dict[NonTerminal, Set[Tuple[Terminal]]], k: int) -> Set[Tuple[Terminal]]:
    """
    return every possible firstK tuples for sequence of termainl and 
    non-terminal symbols
    """
    sets = []
    for elem in seq:
        if isinstance(elem, Terminal):
            sets.append({tuple([elem])})
        else:
            sets.append(dct[elem])
    return KconcatenateListOfSets(sets, k)


def followK(grammar: Grammar, k: int):
    """
    for every terminal in grammmar returns the set of all 
    possible firstk tuples that the NonTerminal can produce
    """
    ans = {
        nterm: "-"
        for nterm in grammar.non_terms
    }
    ans[grammar.start_symbol] = {tuple([Terminal("eps")])}
    while True:
        stop = True
        for rule in grammar.rules:
            for i, sym in enumerate(rule.en):
                if isinstance(sym, NonTerminal):
                    if ans[rule.st] == "-":
                        continue
                    set1 = sequenceFirstK(tuple(rule.en[i+1:]), firstK(grammar, k), k)
                    set2 = ans[rule.st]
                    new_set = KconcatenateTwoSets(set1, set2, k)
                    if ans[sym] == "-":
                        ans[sym] = set()
                    if not new_set.issubset(ans[sym]):
                        stop = False
                        ans[sym].update(new_set)
        if stop:
            break
    return ans
