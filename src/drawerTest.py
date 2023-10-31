from core.grammar import Grammar
from core.llk import LLKParserWrapped
from core.drawer import Visualiser

grammar = Grammar.read(['S -> BA', 'A -> +BA | eps', 'B -> DC', 'C -> *DC | eps', 'D -> (S) | a'])
parser = LLKParserWrapped(1)
parser.init(grammar)

order = parser.parse('(a+a)*a')

drawer = Visualiser()
drawer.draw(order)