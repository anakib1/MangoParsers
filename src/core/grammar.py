from typing import Tuple, Set, TextIO, Union, List
from copy import copy, deepcopy

class BaseSymbol:
    """
    Basic token. Could be Terminal or NonTerminal.
    """

    __slots__ = ['symbol']

    def __init__(self, symbol : str) -> None:
        if len(symbol) > 1: 
            symbol = f'[{symbol}]'
        self.symbol = symbol
    
    def __repr__(self) -> str:
        return self.symbol

    def __eq__(self, other : object) -> bool:
        if not isinstance(other, BaseSymbol):
            return False
        return self.symbol == other.symbol

    def __hash__(self) -> int:
        return hash(self.symbol)

class NonTerminal(BaseSymbol):
    """
    Symbols that could produce rules
    """

    def __init__(self, symbol: str) -> None:
        assert symbol[0].isupper(), 'nonterminals should start from uppercase characters'
        super().__init__(symbol)

    def isEpsilon(self):
        return False

class Terminal(BaseSymbol):
    """
    Symbols that are terminal
    """

    def __init__(self, symbol : str) -> None:
        assert symbol.islower() or not symbol.isalpha(), 'terminals MUST be lowercase'
        super().__init__(symbol)
    
    def isEpsilon(self):
        return self.symbol == "[eps]"

class SymbolUtils:
    @staticmethod
    def getSymbol(s : str) -> BaseSymbol:
        if s[0].isupper():
            return NonTerminal(s)
        return Terminal(s)
    
    @staticmethod 
    def getSymbols(s : str) -> List[BaseSymbol]:
        """
        Returns tuple of symbols.
        """
        if s == 'eps':
            return tuple([SymbolUtils.getSymbol('eps')])
        return tuple(SymbolUtils.getSymbol(x) for x in s)


class Rule:
    """
    Rule of from A -> [Terminal|NonTerminal]*
    Flyweight pattern in use, we don't store references to provided arguments, and 
    you should not store references to returned values. 
    """

    __slots__ = ['st', 'en']

    def __init__(self, st : NonTerminal, en : Tuple[BaseSymbol, ...]) -> None:
        self.st = copy(st)
        self.en = deepcopy(en)

    def __contains__ (self, symbol : BaseSymbol) -> bool:
        return symbol in self.en 

    def __repr__(self) -> str :
        return f'{self.st} -> {[str(x) for x in self.en] if len(self.en) > 0 else "EPS"}'
        
    def __str__(self) -> str:
        return f"{self.st} -> {''.join([str(x) for x in self.en] if len(self.en) > 0 else '[eps]')}"

    def isEpsilon(self, bad_set : Set ) -> bool:
        return self.en[0].isEpsilon() or len(list(filter(lambda x : x not in bad_set, self.en))) == 0
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Rule): return False 
        if len(self.en) != len(other.en): return False
        for i, x in enumerate(self.en):
            if x != other.en[i]:
                return False 
        return self.st == other.st
    
    def __hash__(self):
        return hash(str(self.st) + '->' + ''.join(str(x) for x in self.en))
    


class Grammar:
    vocab : Set[BaseSymbol]
    non_terms : Set[NonTerminal]
    terms : Set[Terminal]
    start_symbol : NonTerminal
    rules : Set[Rule]

    """
    Basic class for grammar entity. 
    Flyweight pattern in use, we don't store references to provided arguments, and 
    you should not store references to returned values. 
    """

    def __init__ (self, nonterminals : Set[NonTerminal], terminals : Set[Terminal], rules : Set[Rule], start_symbol=NonTerminal("S")) -> None:
        self.terms = deepcopy(terminals)
        self.non_terms = deepcopy(nonterminals)
        self.vocab = self.terms | self.non_terms
        self.rules = deepcopy(rules)
        self.start_symbol = start_symbol

    @staticmethod
    def read(f : Union[TextIO, List[str]]):
        """
        Expects input of form
        A -> BcD | e | zz | EPS 
        EPS is defined constant for epsilon rule
        THIS INPUT SHOULD NOT CONTAIN MAYBE PRODUCED NonTerms LIKE [Abb1]
        """
        if not isinstance(f, List):
            f = [x.strip() for x in f.readlines()]

        vocab = set()
        rules = []
        for line in f: 
            line = line.replace(' ', '')
            st, end = line.split('->')
            vocab.add(SymbolUtils.getSymbol(st))

            end_list = end.split('|')
            for rule_part in end_list:
                rule_part_end = []
                if rule_part == "eps":
                    rule_part_end.append(Terminal("eps"))
                else:
                    for word in rule_part:
                        vocab.add(SymbolUtils.getSymbol(word))
                        rule_part_end.append(SymbolUtils.getSymbol(word))
                rules.append(Rule(NonTerminal(st), rule_part_end))
            
        return Grammar(
                set([x for x in vocab if isinstance(x, NonTerminal)]), 
                set([x for x in vocab if isinstance(x, Terminal)]),
                set(rules)
            )


    def find_creatures(self):
        bad_set = set()

        while True:
            start_size = len(bad_set)
            for rule in self.rules:
                if rule.isEpsilon(bad_set):
                    bad_set.add(rule.st)

            if start_size == len(bad_set):
                break
    

        return list(bad_set)

    def remove_eps_rules(self):
        creatures = self.find_creatures()
        ret = Grammar(set(), set(), [])
        for rule in self.rules:
            creatures_in_rule = [x for x in range(len(rule.en)) if rule.en[x] in creatures]
            ln = len(creatures_in_rule)
            for mask in range(1 << ln):
                nf = []
                for i in range(len(rule.en)):
                    if i in creatures_in_rule:
                        pos = creatures_in_rule.index(i)
                        if mask & 1 << pos:
                            nf.append(copy(rule.en[i]))
                    else:
                        nf.append(copy(rule.en[i]))
                rule_to_add = Rule(copy(rule.st), nf)
                if not rule_to_add.isEpsilon(set()):
                    ret.add_rule(rule_to_add)
        return ret

    def add_rule(self, rule:Rule):
        for other in self.rules:
            if other == rule:
                return
        for x in [rule.st] + rule.en:
            if not x in self.vocab:
                self.vocab.add(copy(x))
                if isinstance(x, Terminal):
                    self.terms.add(copy(x))
                else:
                    self.non_terms.add(copy(x))
        self.rules.append(rule)