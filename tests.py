import tokenizer
from parser import Parser, print_tree


def test_parser(file):
    tokens = tokenizer.tokenize(file)

    print("=== Tokens ===")
    for token in tokens:
        print(token)

    print("\n=== AST ===")
    parser = Parser(tokens)
    tree = parser.parse()
    print_tree(tree)

def main():
    test_parser("file.lc")

if __name__ == "__main__":
    main()