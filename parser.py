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
    def __init__(self, tokens):
        self.tokens = tokens
        self.curr = 0
        self.atom_indicators = {TokenType.IDENTIFIER, TokenType.LPAREN}

    def is_atom(self, token):
        return (
            token is not None and
            token.ttype in self.atom_indicators
        )

    # just a short function name/alias
    def parse(self):
        tree = self.parse_expression()
        if self.peek() is not None:
            raise Exception(f"Unexpected token {self.peek()}")
        return tree

    def parse_expression(self):
        token = self.peek()
        if token.ttype == TokenType.LAMBDA:
            return self.parse_lambda()
        elif self.is_atom(token):
            return self.parse_application()
        else:
            # nice error
            pass 

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

def print_tree(node, prefix="", is_last=True):
    if node is None:
        return

    connector = "└── " if is_last else "├── "

    if node.nodetype == NodeType.VARIABLE:
        label = f"Variable({node.value})"
    elif node.nodetype == NodeType.LAMBDA:
        label = f"Lambda({node.value})"
    elif node.nodetype == NodeType.APPLICATION:
        label = "Application"
    else:
        label = str(node.nodetype)

    print(prefix + connector + label)

    children = []
    if node.left is not None:
        children.append(node.left)
    if node.right is not None:
        children.append(node.right)

    next_prefix = prefix + ("    " if is_last else "│   ")

    for i, child in enumerate(children):
        print_tree(child, next_prefix, i == len(children) - 1)