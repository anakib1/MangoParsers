from core.iparser import IParser
from core.grammar import Terminal, NonTerminal, BaseSymbol, Grammar, SymbolUtils
from copy import deepcopy

class RecursiveParser(IParser):

    __slots__ = ['rules_by_symbol', 'grammar', 'read', 'unread']

    def __init__(self, grammar:Grammar):
        grammar = grammar.remove_eps_rules()
        self.rules_by_symbol = {}
        for rule in grammar.rules:
            self.rules_by_symbol[rule.st] = self.rules_by_symbol.setdefault(rule.st, []) + [rule]
        self.grammar = grammar

    def verify(self, s : str) -> bool:
        self.read = ''
        self.unread = s
        return self.try_rule(self.grammar.start_symbol)
        
    def expect_nonterminal(self, expected : Terminal) -> bool:

        if expected.isEpsilon():
            return True

        if len(self.unread) == 0:
            return False

        return expected == SymbolUtils.getSymbol(self.unread[0])

    def roll_forward(self):
        self.read = self.read + self.unread[0] if len (self.unread) > 0 else ''
        self.unread = self.unread[1:] if len (self.unread) > 0 else ''

    def try_rule(self, s:NonTerminal) -> bool:
        print(f'Trying rule with V = {s}, read = {self.read}, unread = {self.unread}')
        for current_rule in self.rules_by_symbol[s]:
            print(f'Trying to go through rule {current_rule}')
            suceeded = True 
            saved_state = (self.read, self.unread) 

            for currenct_character in current_rule.en:
                if isinstance(currenct_character, Terminal):
                    if not self.expect_nonterminal(currenct_character):
                        suceeded = False 
                        break
                    else:
                        self.roll_forward()
                else:
                    result = self.try_rule(currenct_character)
                    if not result:
                        suceeded = False
                        break

            if suceeded:
                return True
            else:
                self.read, self.unread = saved_state
        
        return False 




    


