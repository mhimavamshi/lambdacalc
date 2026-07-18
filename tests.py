import tokenizer
from parser import Parser, print_tree
from evaluator import Evaluator


def test_expression(name, source):
    print("=" * 60)
    print(name)
    print("Source:")
    print(source)

    tokens = tokenizer.tokenize(source)

    print("\n=== Tokens ===")
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    tree = parser.parse()

    print("\n=== Parsed AST ===")
    print_tree(tree)

    evaluator = Evaluator(strategy="weak")
    reduced = evaluator.reduce(tree)

    print("\n=== Reduced AST ===")
    print_tree(reduced)

    print()

def test_expressions():

    tests = [
        ("identity", r"(\x.x) y"),                          # -> y
        ("identity application", r"(\x.x) (a b)"),         # -> (a b)
        ("constant", r"(\x.\y.x) a b"),                    # -> a
        ("second", r"(\x.\y.y) a b"),                      # -> b
        ("duplicate", r"(\x.x x) y"),                      # -> y y
        ("ignore arg", r"(\x.a) b"),                       # -> a

        # Capture / alpha conversion
        ("capture avoidance", r"(\x.\y.x) y"),             # -> \y'.y
        ("capture avoidance 2", r"(\x.\y.y x) y"),         # -> \y'.y' y

        # Shadowing
        ("shadow inner", r"(\x.\x.x) z"),                  # -> \x.x
        ("shadow outer", r"(\x.\x.x x) z"),                # -> \x.x x
        ("outer reference", r"(\x.\y.x y) z"),             # -> \y.z y
        ("inner application", r"(\x.(\x.x) x) z"),         # -> z

        # Nested applications
        ("nested identity", r"(\x.x) ((\y.y) z)"),         # -> z
        ("apply twice", r"(\f.\x.f (f x)) (\y.y) a"),      # -> a

        # Free variables
        ("free variable", r"(\x.x z) y"),                  # -> y z
        ("free application", r"(\x.z x) y"),              # -> z y

        # More shadowing
        ("deep shadow", r"(\x.\x.\x.x) a"),                # -> \x.\x.x
        ("deep outer", r"(\x.\y.\z.x) a"),                 # -> \y.\z.a

        # Combinations
        ("self application", r"(\x.x x) (\y.y)"),          # -> (\y.y) (\y.y)
        ("nested constant", r"(\a.(\b.a)) x"),             # -> \b.x
    ]


    for name, source in tests:
        test_expression(name, source)

def test_definition(name, source):
    tokens = tokenizer.tokenize(source)
    definitions, program = Parser().process(tokens)
    
    print(name, ":")
    print("Definitions")  
    for name, body in definitions.items():
        print("=====")
        print(name)
        print_tree(body)
   
    print("Program")
    print("=====")
    print_tree(program)

def test_definitions():
    tests = [
        ("simple program", r"{id = \x.x, misdirect = \x.y, } id misdirect")
    ]

    for name, source in tests:
        test_definition(name, source)

def main():
    # test_expressions()
    test_definitions()

if __name__ == "__main__":
    main()
