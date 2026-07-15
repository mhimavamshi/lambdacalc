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
        ("identity", r"(\x.x) y"),                    # -> y
        ("identity application", r"(\x.x) (a b)"),   # -> (a b)
        ("constant", r"(\x.\y.x) a b"),              # -> a
        ("second", r"(\x.\y.y) a b"),                # -> b
        ("duplicate", r"(\x.x x) y"),                # -> y y
        ("ignore arg", r"(\x.a) b"),                 # -> a
        ("nested lambda", r"(\x.\y.x) y"),                 # -> \y.y 
    ]

    for name, source in tests:
        test_expression(name, source)


def main():
    test_expressions()


if __name__ == "__main__":
    main()