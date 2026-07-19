import readline
from tokenizer import tokenize
from parser import Parser, print_tree
from evaluator import Evaluator
from utils import debug_print

parser = Parser()

COMMANDPREFIX = ":"

parsed_definitions = {}

evaluator = Evaluator(parsed_definitions)


def new_definition(source):
    global parsed_definitions
    tokens = tokenize(source)
    parsed_definition, _ = parser.process(tokens)
    parsed_definitions |= parsed_definition
    evaluator.add_definition(parsed_definition)


def remove_definition(name):
    if name in parsed_definitions:
        del parsed_definitions[name]
        evaluator.remove_definition(name)


def clear_definitions():
    global parsed_definitions
    parsed_definitions = {}
    evaluator.clear_definitions()


def evaluate_pipeline(program):
    tokens = tokenize(program)
    _, tree = parser.process(tokens)
    print()
    print("Immediately parsed tree:")
    print_tree(tree)
    print()
    final_tree = evaluator.run(tree)
    print()
    print("=====")
    print("reduced tree: ")
    print_tree(final_tree)
    print()


def define(args):
    r"""
    Define a function to be reused. for eg. ':def id = \x.x'
    """
    source = "{ " + " ".join(args) + " , " + "}"
    debug_print(source)
    new_definition(source)


def undefine(args):
    """
    Remove definition(s). for eg., ':undef id coolfun ...'
    """
    for arg in args:
        remove_definition(arg)


def cleardefines(args):
    """
    Clear all definitions.
    """
    clear_definitions()


# needs to serialize and deserialize AST nodes :)
# maybe later
def save(args):
    pass


def showdefines(args):
    """
    Prints all definitions that are currently defined.
    """
    for definition in parsed_definitions:
        print(definition)


def helpf(args=None):
    """
    Prints help for all commands if no arguments are given, else prints help for the commands mentioned in arguments.
    """
    if not args:
        args = commands.keys()

    for arg in args:
        if arg in commands:
            print(f":{arg}{commands[arg].__doc__}")
    print()


commands = {
    "def": define,
    "undef": undefine,
    "cleardefs": cleardefines,
    "showdefs": showdefines,
    "save": save,
    "help": helpf,
}


def execute_command(command):
    if command.startswith(COMMANDPREFIX):
        command = command[1:].split(" ")
        f = commands.get(command[0], None)
        if f is None:
            return
        f(command[1:])
    else:
        evaluate_pipeline(command)


def is_quit(command):
    return command == "q" or command.lower() == "quit"


def prompt():
    return input("λ> ")


def main():
    helpf()
    while True:
        command = prompt()
        if is_quit(command):
            break
        try:
            execute_command(command)
        except Exception as e:  # ideally we handle custom exceptions, like Cycle identified etc., but i am tired
            print(e)


if __name__ == "__main__":
    main()
