from parser import NodeType, ApplicationNode, LambdaNode
from utils import debug_print

class Evaluator:
    def __init__(self, strategy):
        self.strategy = strategy
        self.reductions = 0

    def alpha_convert(self, tree):
        # it goes through the tree
        # keeps track of variables in outer scope
        # or scopes
        # if its newly defined again
        # we can have metadata saying they're new ones bound to new lambda, don't substitute
        # or just encode that information in the re-naming
        pass

    def substitute(self, node, replacement, variable):
        # lambda is simply a variable: \x.x 
        if node.nodetype == NodeType.VARIABLE: 
            return replacement if node.value == variable else node 

        # of course, alpha_convert is necessary
        # ignore, for now
        if node.nodetype == NodeType.LAMBDA:       
            body = node.right
            return LambdaNode(node.value, self.substitute(body, replacement, variable))
            
        if node.nodetype == NodeType.APPLICATION:
            return ApplicationNode(self.substitute(node.left, replacement, variable), self.substitute(node.right, replacement, variable))
        

    def evaluate(self, tree):
        if tree.nodetype == NodeType.APPLICATION:
            if tree.left.nodetype == NodeType.LAMBDA:
                self.reductions += 1
                body = tree.left.right
                return self.substitute(body, tree.right, tree.left.value)
            
            tree.left = self.evaluate(tree.left)
            tree.right = self.evaluate(tree.right)

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
