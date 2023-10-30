from typing import Union, TextIO, List
from grammar import Grammar, Rule

class IParser:
    """
    Returns bool, indicating that current parser accepts the 
    given string
    """
    def verify(self, s : str) -> bool:
        pass 

    """
    Returns rules in order, that are required to build the given string. 
    """
    def parse(self, s : str) -> List[Rule]:
        pass

    """
    Initialises parser from the given file,
    or grammar as list of strings
    """
    def init(self, f : Grammar) -> None:
        pass 


    