from dataclasses import dataclass
from typing import List, Optional, Union

from data_class.token import Token
from core.scanner import TokenType

@dataclass
class Attribute:
    scope_no: int
    mem_addr: str

@dataclass
class FuncAttribute(Attribute):
    args_addr: List[int]
    ret_val_addr: int
    jp_addr: int
    start_addr_in_PB: int
    have_returned_stmt: bool=False

@dataclass
class ItmtAttribute(Attribute):
    breaks_PB: List[int]
    continues_PB: List[int]
    SS_break: List[int]
    SS_cont: List[int]
    start_addr_in_PBs: List[int]

@dataclass
class Row:
    lexeme: Token
    type: TokenType  
    attribute: Union[Attribute, FuncAttribute, ItmtAttribute]      
