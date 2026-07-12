from parser import NodeType
from utils import debug_print

class Evaluator:
    def __init__(self, strategy):
        self.strategy = strategy
        self.reductions = 0

    def evaluate(self, tree):
        if tree.nodetype == NodeType.APPLICATION:
            if tree.left.nodetype == NodeType.LAMBDA:
                self.reductions += 1
                return self.substitute(tree.left, tree.right)
            
            tree.left = self.evaluate(tree.left)
            tree.right =self.evaluate(tree.right)

            return tree

        elif tree.nodetype == NodeType.LAMBDA:
            if self.strategy == "strong":
                tree.right = self.evaluate(tree.right)
            return tree

        elif tree.nodetype == NodeType.VARIABLE:
            return tree

        else:
            return tree

    def reduce(self, tree):
        i = 0
        while True:
            self.reductions = 0
            tree = self.evaluate(tree)
            if self.reductions == 0:
                return tree  
            i += 1
            debug_print(f"at {i} pass: performed {self.reductions}")