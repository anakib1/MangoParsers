from typing import Union, TextIO, List
from grammar import Grammar

class IParser:
    """
    Returns bool, indicating that current parser accepts the 
    given string
    """
    def verify(self, s : str) -> bool:
        pass 

    """
    Initialises parser from the given file,
    or grammar as list of strings
    """
    def init(self, f : Grammar) -> None:
        pass 


    