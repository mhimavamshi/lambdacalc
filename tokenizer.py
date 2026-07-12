from enum import Enum, auto
from utils import debug_print

class TokenType(Enum):
    LPAREN = auto()
    RPAREN = auto()
    LAMBDA = auto()
    PERIOD = auto()
    IDENTIFIER = auto()

class Token:
    def __init__(self, ttype, value, pos):
        self.ttype = ttype
        self.value = value 
        self.pos = pos 

    def __repr__(self):
        return f"Token at {self.pos}: {self.ttype} type, '{self.value}' value"

def read_file(file):
    try:
        with open(file) as fl:
            data = fl.read()
        return data 
    except:
        return 


def tokenize(data):
    tokens = []
    i = 0

    while i < len(data):
        ch = data[i]
        debug_print(f"at {i}: {data[i]}")

        if ch.isspace():
            i += 1
            continue 
        
        match ch:
            case "(":
                tokens.append(Token(TokenType.LPAREN, ch, i))
            case ")":
                tokens.append(Token(TokenType.RPAREN, ch, i))
            case "\\":
                tokens.append(Token(TokenType.LAMBDA, ch, i))
            case ".":
                tokens.append(Token(TokenType.PERIOD, ch, i))
            case _:
                if not ch.isalpha():
                    raise RuntimeError(f"Invalid character at position {i}: {ch}")
                string = [ch]
                start = i
                i += 1
                while i < len(data) and (data[i].isalpha() or data[i] == "_"):
                    string.append(data[i])
                    i += 1
                tokens.append(Token(TokenType.IDENTIFIER, "".join(string), start))
                continue

        i += 1 
                
    return tokens 
