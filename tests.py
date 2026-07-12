import tokenizer
from parser import Parser, print_tree


def test_expression(name, source):
    print("=" * 60)
    print(name)
    print("Source:")
    print(source)

    tokens = tokenizer.tokenize(source)

    print("\n=== Tokens ===")
    for token in tokens:
        print(token)

    print("\n=== AST ===")
    parser = Parser(tokens)
    tree = parser.parse()
    print_tree(tree)

    print()


def main():
    tests = [
        (
            "identity",
            r"\x.x"
        ),
        (
            "simple application",
            r"(\x.x) y"
        ),
        (
            "nested lambda",
            r"\x.\y.x"
        ),
        (
            "application chain",
            r"a b c"
        ),
        (
            "lambda body application",
            r"\x.x y"
        ),
        (
            "nested application",
            r"(\x.x) ((\y.y) z)"
        ),
        (
            "lambda as argument",
            r"(\x.x) (\y.y)"
        ),
        (
            "complex",
            r"(\f.\x.f (f x)) (\y.y) a"
        ),
        (
            "very complex",
            r"(\a.\b.a (\c.c b)) ((\x.x) (\y.y)) z"
        ),
        (
            "something ive seen",
            r"\m.\n.\f.\x.m f (n f x)"
        )
    ]

    for name, source in tests:
        test_expression(name, source)


if __name__ == "__main__":
    main()