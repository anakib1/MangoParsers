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

class Terminal(BaseSymbol):
    """
    Symbols that are terminal
    """

    def __init__(self, symbol : str) -> None:
        assert symbol.islower(), 'terminals MUST be lowercase'
        super().__init__(symbol)

class SymbolUtils:
    @staticmethod
    def getSymbol(s : str) -> BaseSymbol:
        if s[0].isupper():
            return NonTerminal(s)
        return Terminal(s)


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

    def __init__ (self, nonterminals : Set[NonTerminal], terminals : Set[Terminal], rules : Set[Rule]) -> None:
        self.terms = deepcopy(terminals)
        self.non_terms = deepcopy(nonterminals)
        self.vocab = self.terms | self.non_terms
        self.rules = deepcopy(rules)

    @staticmethod
    def read(f : Union[TextIO, List[str]]) -> Grammar:
        """
        Expects input of form
        A -> BcD | e | zz | EPS 
        EPS is defined constant for epsilon rule
        THIS INPUT SHOULD NOT CONTAIN MAYBE PRODUCED NonTerms LIKE [Abb1]
        """
        if not isinstance(f, List):
            f = f.readlines()

        vocab = set()
        rules = []
        terms = []
        nonterms = []
        for line in f: 
            line = line.replace(' ', '')
            st, end = line.split('->')
            vocab.add(SymbolUtils.getSymbol(st))

            end_list = end.split('|')
            for rule_part in end_list:
                rule_part_end = []
                for word in rule_part:
                    vocab.add(SymbolUtils.getSymbol(word))
                    rule_part_end.add(SymbolUtils.getSymbol(word))
                rules.append(Rule(st, rule_part_end))
            
        return Grammar(
                [x for x in vocab if isinstance(x, NonTerminal)], 
                [x for x in vocab if isinstance(x, Terminal)],
                rules
            )

