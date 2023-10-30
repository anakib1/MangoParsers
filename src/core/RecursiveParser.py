from core.iparser import IParser
from core.grammar import Terminal, NonTerminal, BaseSymbol, Grammar, SymbolUtils, Rule
from copy import deepcopy

class RecursiveParser(IParser):

    __slots__ = ['rules_by_symbol', 'grammar', 'read', 'unread']

    def __init__(self, grammar = None):
        if grammar is not None:
            self.init(grammar) 

    def init(self, grammar : Grammar):
        self.grammar = grammar.remove_eps_rules()
        self.rules_by_symbol = {}
        for rule in self.grammar.rules:
            self.rules_by_symbol[rule.st] = self.rules_by_symbol.setdefault(rule.st, []) + [rule]


    def is_compatible(self, rule : Rule):
        if len(rule.en) > len(self.parse_stack):
            return False
        for i,x in enumerate(rule.en[::-1]):
            if self.parse_stack[-1-i] != x:
                return False
        return True
    
    def reduce(self, rule:Rule):
        self.parse_stack = self.parse_stack[:-len(rule.en)]
        self.parse_stack.append(rule.st)


    def try_parse(self) -> bool:
        if len(self.input) == 0 and len(self.parse_stack) == 1 and self.parse_stack[0] == self.grammar.start_symbol:
            return True
        
        moves = []
        for rule in self.grammar.rules:
            if self.is_compatible(rule):
                moves.append((1, rule))
        if len(self.input) > 0:
            moves.append((2, 'reduce'))

        for move in moves:
            saved_moment = deepcopy((self.parse_stack, self.input))
            if move[0] == 2:
                self.parse_stack.append(SymbolUtils.getSymbol(self.input[0]))
                self.input = self.input[1:]
                if (self.try_parse()):
                    return True
            else:
                self.reduce(move[1])
                if (self.try_parse()):
                    return True
            
            self.parse_stack, self.input = saved_moment
        
        return False
                    




    def verify(self, s : str) -> bool:
        self.parse_stack = []
        self.input = s
        return self.try_parse()



    


