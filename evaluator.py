from parser import NodeType, ApplicationNode, LambdaNode, print_tree
from copy import deepcopy
from utils import debug_print


class Evaluator:
    def __init__(self, definitions, strategy="strong"):
        self.strategy = strategy
        self.definitions = definitions
        self.init_definitions()
        self.reductions = 0
        self._active_lambda_scopes = {}
        self._mono_id = -1

    def init_definitions(self):
        self.generate_metadata()
        self.detect_cycles()
        self.definition_cache = {}

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
            stack.pop()
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
            return ApplicationNode(
                self.substitute(node.left, replacement, variable),
                self.substitute(node.right, replacement, variable),
            )

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
        print("=====")
        print("alpha converted tree:")
        print_tree(tree)
        i = 0
        while True:
            self.reductions = 0
            tree = self.evaluate(tree)
            if self.reductions == 0:
                return tree
            i += 1
            print("=====")
            print(f"at #{i} pass: performed {self.reductions}")
            print_tree(tree)

    def find_references(self, node, references):
        if node.nodetype == NodeType.VARIABLE:
            if node.value in self.definitions:
                references[node.value] = references.get(node.value, 0) + 1

        if node.nodetype == NodeType.LAMBDA:
            self.find_references(node.right, references)

        if node.nodetype == NodeType.APPLICATION:
            self.find_references(node.left, references)
            self.find_references(node.right, references)

    def generate_metadata(self):
        self.metadata = {}

        for definition, body in self.definitions.items():
            references = {}
            self.find_references(body, references)
            self.metadata[definition] = references

        debug_print(f"metadata generated: {self.metadata}")

    def _detect_cycles_backend(self, start, visited=None):
        if visited is None:
            visited = set()

        if start in visited:
            raise Exception(f"Cycle detected in definitions: {' -> '.join(visited)}")

        visited.add(start)
        references = self.metadata[start]
        for reference in references.keys():
            self._detect_cycles_backend(reference, visited)
        visited.remove(start)

    def detect_cycles(self):
        self.metadata = dict(
            sorted(self.metadata.items(), key=lambda item: len(item[1]))
        )
        self._detect_cycles_backend(next(iter(self.metadata)))

    def fetch_definition(self, definition):

        references = self.metadata[definition]
        if len(references) == 0:
            debug_print(f"no references for {definition} found, skipping cache")
            return self.definitions[definition]

        if definition in self.definition_cache:
            debug_print(f"cache hit: {definition}")
            return self.definition_cache[definition]

        body = self.definitions[definition]
        self.definition_cache[definition], _ = self.expansion_pass(body)
        debug_print(f"cache miss: cached definition {definition} after expansion_pass")
        return self.definition_cache[definition]

    def expansion_pass(self, program):

        if program is None:
            return None, False

        if program.nodetype == NodeType.VARIABLE:
            if program.value in self.definitions:
                body = self.fetch_definition(
                    program.value
                )  # guaranteed that there won't be cycles
                return deepcopy(body), True

            return program, False

        if program.nodetype == NodeType.LAMBDA:
            body, changed = self.expansion_pass(program.right)
            return LambdaNode(program.value, body), changed

        if program.nodetype == NodeType.APPLICATION:
            left, left_changed = self.expansion_pass(program.left)
            right, right_changed = self.expansion_pass(program.right)
            return ApplicationNode(left, right), (left_changed or right_changed)

        return program, False

    # Idea:
    # Derive metadata from definitions: each definition mapped to its unique references
    # sort it by the number of references
    # you have a graph
    # in the graph check for cycles: have a nice error message showing the cycle
    # if not, you have a graph of definitions
    # during expansion, you can decide to go deeper or not if the number of references is not 0
    # you can cache after first expansion for re-use
    #
    # WOULD BE VERY COOL IF IT IS MADE INCREMENTAL!!!
    #
    # but for now, expose add_definition, remove_definition, clear_all that all do reset()
    # which involves clearing out the metadata, cache, rebuilding graph, and detecting new cycles

    def run(self, program):
        changed = True
        while changed:
            program, changed = self.expansion_pass(program)

        print("=====")
        print("after definition expansion")
        print_tree(program)

        return self.reduce(program)
