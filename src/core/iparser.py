from typing import Union, TextIO, List

class IParser:
    """
    Returns bool, indicating that current parser accepts the 
    given string
    """
    def verify(s : str) -> bool:
        pass 

    """
    Initialises parser from the given file,
    or grammar as list of strings
    """
    def init(f : Union[List[str], TextIO]):
        pass 


    