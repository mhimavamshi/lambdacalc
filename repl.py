import readline
from tokenizer import tokenize
from parser import Parser, print_tree 
from evaluator import Evaluator

parser = Parser()

COMMANDPREFIX = ":"

commands = {

}

definitions = {

}

def evaluate_pipeline(program):
    tokens = tokenize(program) 
    parsed_definitions, tree = parser.process(tokens)
    print()
    print("Immediately parsed tree:")
    print_tree(tree)
    print()
    final_tree = Evaluator(parsed_definitions).run(tree)
    print()
    print("=====") 
    print("reduced tree: ")
    print_tree(final_tree)
    print()

def execute_command(command):
    if command.startswith(COMMANDPREFIX):
        f = commands.get(command[1:], None) 
        if f is None:
            return
        f()
    else:       
        evaluate_pipeline(command)

def is_quit(command):
    return command == "q" or command.lower() == "quit"

def prompt():
    return input("λ> ")

def main():
    while True:
        command = prompt()
        if is_quit(command):
            break 
        execute_command(command)
        
if __name__ == "__main__":
    main()
