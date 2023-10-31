from core.grammar import Grammar, Terminal, NonTerminal, BaseSymbol, Rule
from typing import List, Tuple
from core.llk import LLKParserWrapped
import graphviz

class Visualiser:
    def __init__(self):
        pass 

    def add(self, val : BaseSymbol) -> int:

        name = str(val)
        clr = None
        if isinstance(val, Terminal):
            self.terminal_counter += 1
            name = "'" + name + "'" +  ' (' + str(self.terminal_counter) + ')'
            clr = 'Red'

        self.dot.node(str(self.counter), name, color = clr)
        self.counter += 1
        return val, self.counter - 1

    def build_tree(self, vertex : Tuple[BaseSymbol, int]) -> int:

        if isinstance(vertex[0], Terminal) :
            return vertex[1]

        if len(self.order) == 0:
            return 
        rule = self.order.pop(0)
        for x in rule.en:
            self.dot.edge(str(vertex[1]), str(self.build_tree(self.add(x))))

        return vertex[1]

    def draw(self, order : List[Rule]):
        self.counter = 0
        self.terminal_counter = 0
        self.order = order
        self.dot = graphviz.Digraph('parsing result')  
        self.build_tree(self.add(order[0].st))

        self.dot.render('dot', format='png', view=True)


