from tokenizer import TokenType
from enum import Enum, auto
from utils import debug_print

class NodeType(Enum):
    LAMBDA = auto()
    APPLICATION = auto()
    VARIABLE = auto()

class Node:
    def __init__(self, nodetype, value, left, right):
        self.nodetype = nodetype
        self.value = value
        self.left = left
        self.right = right 

    def __repr__(self):
        return f"Node of type {self.nodetype}, value {self.value} with left: {self.left} and right: {self.right}"

class VariableNode(Node):
    def __init__(self, value):
        super().__init__(NodeType.VARIABLE, value, None, None)

class ApplicationNode(Node):
    def __init__(self, left, right):
        super().__init__(NodeType.APPLICATION, None, left, right)

class LambdaNode(Node):
    def __init__(self, value, right):
        super().__init__(NodeType.LAMBDA, value, None, right)

class Parser:
    def __init__(self):
        self.atom_indicators = {TokenType.IDENTIFIER, TokenType.LPAREN}

    def is_atom(self, token):
        return (
            token is not None and
            token.ttype in self.atom_indicators
        )

    # just a short function name/alias
    def parse(self):
        tree = self.parse_expression()
        return tree

    def parse_expression(self):
        token = self.peek()
        if token is None:
            return 
        if token.ttype == TokenType.LAMBDA:
            return self.parse_lambda()
        elif self.is_atom(token):
            return self.parse_application()
        else:
            # nice error
            raise Exception(f"Parse Expression recieved: {token}") 

    def parse_lambda(self):
        self.expect(TokenType.LAMBDA)
        identifier = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.PERIOD)
        expression = self.parse_expression()
        return LambdaNode(identifier.value, expression)

    def parse_atom(self):
        curr = self.peek()
        if curr.ttype == TokenType.LPAREN:
            self.expect(TokenType.LPAREN)
            expression = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expression 
        elif curr.ttype == TokenType.IDENTIFIER:
            val = self.expect(TokenType.IDENTIFIER)
            return VariableNode(val.value)
        

    def parse_application(self):
        left = self.parse_atom()
        application = None 
        # i know a single while loop can be enough
        # but for explicitness and readability
        # first time its new ApplicationNode
        # and then nested inside other ApplicationNodes
        if self.is_atom(self.peek()):
            right = self.parse_atom()
            application = ApplicationNode(left, right)
        while self.is_atom(self.peek()):
            right = self.parse_atom()
            application = ApplicationNode(application, right)
        if application is None:
            return left 
        else:
            return application 

    def advance(self):
        if self.curr >= len(self.tokens):
            return 
        val = self.tokens[self.curr]
        self.curr += 1
        return val 

    def peek(self):
        if self.curr >= len(self.tokens):
            return None 
        return self.tokens[self.curr]

    def expect(self, ttype):
        token = self.peek()
        if not token or token.ttype != ttype:
            raise Exception(f"Expected {ttype}, got {token}")
        token = self.advance()
        return token 

    def parse_definition(self):
        name = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.ASSIGNMENT)
        body = self.parse()
        self.expect(TokenType.COMMA)
        return name.value, body

    def parse_definitions(self):
        self.expect(TokenType.DEFINITION_BEGIN) 
        while True:
            if self.peek() is None or self.peek().ttype == TokenType.DEFINITION_END:
               break 
            name, body = self.parse_definition()
            self.definitions[name] = body 
        self.expect(TokenType.DEFINITION_END)

    def reset(self):
        self.tokens = []
        self.curr = 0
        self.definitions = {}

    def process(self, tokens):
        self.reset()

        if len(tokens) == 0:
            return {}, None 

        self.tokens = tokens 

        if self.peek().ttype == TokenType.DEFINITION_BEGIN:
            self.parse_definitions()
        tree = self.parse()
        return self.definitions, tree


RESET = "\033[0m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
GRAY = "\033[90m"


def print_tree(node, prefix="", is_last=True):
    if node is None:
        return

    connector = f"{GRAY}{'└── ' if is_last else '├── '}{RESET}"

    if node.nodetype == NodeType.VARIABLE:
        label = f"{GREEN}Variable{RESET}({YELLOW}{node.value}{RESET})"
    elif node.nodetype == NodeType.LAMBDA:
        label = f"{BLUE}Lambda{RESET}({YELLOW}{node.value}{RESET})"
    elif node.nodetype == NodeType.APPLICATION:
        label = f"{MAGENTA}Application{RESET}"   
    else:
        label = str(node.nodetype)

    print(prefix + connector + label)

    children = []
    if node.left is not None:
        children.append(node.left)
    if node.right is not None:
        children.append(node.right)

    prefix = prefix.replace("│", f"{GRAY}│{RESET}")   
    next_prefix = prefix + ("    " if is_last else f"{GRAY}│{RESET}   ")

    for i, child in enumerate(children):
        print_tree(child, next_prefix, i == len(children) - 1)
