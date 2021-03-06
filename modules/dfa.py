
from utils.constants import UNKNOWN, ASCII_LOWERCASE, ASCII_UPPERCASE, DIGIT, FINAL_STATE


class DFA:
    """a general DFA class to define its policy"""
    
    state: int = 0
    """ current state of the DFA"""

    lookahead: bool = False
    """whether lookahead occured or not"""

    def reset(cls):
        """reset DFA to initial state"""
        cls.state = 0
        cls.lookahead = False
    
    def move(cls, action: str) -> int:
        """move within DFA and return next state"""


class CommentDFA(DFA):
    chars = ["#", "/"]

    def move(cls, action: str): # what about lookahead and unknown and these stuff?
        state = cls.state
        next_state: int = UNKNOWN

        if state == 0:
            if action == "#":
                next_state = 5
            elif action == "/":
                next_state = 1
        elif state == 1:
            if action == "*":
                next_state = 2
            else:
                next_state = UNKNOWN
        elif state == 2:
            if action != "*":
                next_state = 2
            elif action == "*":
                next_state = 3
        elif state == 3:
            if action != "/":
                next_state = 2
            elif action == "/":
                next_state = FINAL_STATE # ?
        elif state == 5:
            if action == '\n' or action == None: # == None is EOF?
                next_state = FINAL_STATE
            else:
                next_state = 5
        cls.state = next_state
        return next_state

class WhitespaceDFA(DFA):
    whitespace_chars = [" ", "\r", "\t", "\n", "\v", "\f"]

    def move(cls, action: str):
        state = cls.state
        next_state: int = UNKNOWN

        if state == 0 and action in cls.whitespace_chars:
            next_state = FINAL_STATE
        
        cls.state = next_state
        return next_state

class SymbolDFA(DFA):
    chars = ["=", "*", ";", ":", ",", "[", "]", "(", ")", "+", "-", "<"]
    gen_others = list(ASCII_LOWERCASE + ASCII_UPPERCASE + DIGIT)
    others = gen_others + CommentDFA.chars + WhitespaceDFA.whitespace_chars

    def move(cls, action: str):
        state = cls.state
        next_state: int = UNKNOWN

        if state == 0:
            if action in "".join(cls.chars[2:]):
                next_state = FINAL_STATE
            elif action == cls.chars[0]:
                next_state = 1
            elif action == cls.chars[1]:
                next_state = 2
            else:
                next_state = UNKNOWN

        elif state == 1:
            if action == cls.chars[0]:
                next_state = FINAL_STATE
            elif action in cls.others:
                next_state = FINAL_STATE
                cls.lookahead = True
            else:
                next_state = UNKNOWN
                    
        elif state == 2:
            if action == cls.chars[1]:
                next_state = FINAL_STATE
            elif action in cls.others and action != "/":
                next_state = FINAL_STATE
                cls.lookahead = True
            else:
                next_state = UNKNOWN

        cls.state = next_state
        return next_state

class NumberDFA(DFA):

    others = WhitespaceDFA.whitespace_chars + CommentDFA.chars + SymbolDFA.chars
    
    def move(cls, action: str):
        state = cls.state
        next_state: int = UNKNOWN

        if state == 0 and action.isdigit():
            next_state = 1

        elif state == 1:
            if action.isdigit():
                next_state = 1
            elif action == ".":
                next_state = 2
            elif action not in cls.others: 
                next_state = UNKNOWN
            else: # if not action.isalpha() and not action in ["!", "$"]:
                next_state = FINAL_STATE

        elif state == 2 and action.isdigit():
            next_state = 3
        
        elif state == 3:
            if action.isdigit():
                next_state = 3
            elif action not in cls.others:  ## DUPP
                next_state = UNKNOWN
            else: # if not action.isalpha() and not action in ["!", "$"]:
                next_state = FINAL_STATE
        
        else:
            next_state = UNKNOWN

        if next_state == FINAL_STATE:
            cls.lookahead = True

        cls.state = next_state
        return next_state


class IDDFA(DFA):
    others = SymbolDFA.chars + WhitespaceDFA.whitespace_chars + CommentDFA.chars
    def move(cls, action: str):
        state = cls.state
        next_state: int = UNKNOWN
        
        if state == 0:
            if action.isalpha():
                next_state = 1
        elif state == 1:
            if action.isalpha() or action.isdigit():
                next_state = 1
            elif action not in cls.others:
                next_state = UNKNOWN
            else:
                next_state = FINAL_STATE
                cls.lookahead = True
                
        cls.state = next_state
        return next_state