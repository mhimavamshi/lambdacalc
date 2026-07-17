from parser import NodeType, ApplicationNode, LambdaNode, print_tree
from utils import debug_print

class Evaluator:
    def __init__(self, strategy):
        self.strategy = strategy
        self.reductions = 0
        self._active_lambda_scopes = {}
        self._mono_id = -1

    def alpha_convert(self, node):
        if node.nodetype == NodeType.APPLICATION:
            self.alpha_convert(node.left)
            self.alpha_convert(node.right)

        if node.nodetype == NodeType.LAMBDA:
           scope_id = self.push_scope(node)
           self.alpha_convert(node.right)
           self.pop_scope(node)
           self.rename_node(node, scope_id)

        if node.nodetype == NodeType.VARIABLE:
            scope_id = self.get_scope_id(node.value)
            if scope_id is None:
                return 
            self.rename_node(node, scope_id)

    def rename_node(self, node, scope_id):
        node.value = f"{node.value}#{scope_id}"

    def mono(self):
        self._mono_id += 1
        return self._mono_id

    def push_scope(self, node):
        key = node.value 
        new_id = self.mono()
        if key in self._active_lambda_scopes:
            stack = self._active_lambda_scopes[key] 
            stack.append(new_id) 
        else:
            self._active_lambda_scopes[key] = [new_id]
        return new_id 
           

    def pop_scope(self, node):
        key = node.value
        if key in self._active_lambda_scopes:
            stack = self._active_lambda_scopes[key]
            last_id = stack.pop()
            if not stack:
                del self._active_lambda_scopes[key]
            return

    def get_scope_id(self, value):
        if value in self._active_lambda_scopes:
            stack = self._active_lambda_scopes[value]
            return stack[-1] 
        return None

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
        self.alpha_convert(tree)
        print_tree(tree) 
        i = 0
        while True:
            self.reductions = 0
            tree = self.evaluate(tree)
            if self.reductions == 0:
                return tree  
            i += 1
            debug_print(f"at {i} pass: performed {self.reductions}")
