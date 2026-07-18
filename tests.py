import tokenizer
from parser import Parser, print_tree
from evaluator import Evaluator

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

    eval = Evaluator(definitions)
    reduced_tree = eval.run(program)

    print("Evaluated tree")
    print("=====")
    print_tree(reduced_tree)

def test_definitions():

    # tests = [
    #     ("identity", r"(\x.x) y"),                          # -> y
    #     ("identity application", r"(\x.x) (a b)"),         # -> (a b)
    #     ("constant", r"(\x.\y.x) a b"),                    # -> a
    #     ("second", r"(\x.\y.y) a b"),                      # -> b
    #     ("duplicate", r"(\x.x x) y"),                      # -> y y
    #     ("ignore arg", r"(\x.a) b"),                       # -> a
    #
    #     # Capture / alpha conversion
    #     ("capture avoidance", r"(\x.\y.x) y"),             # -> \y'.y
    #     ("capture avoidance 2", r"(\x.\y.y x) y"),         # -> \y'.y' y
    #
    #     # Shadowing
    #     ("shadow inner", r"(\x.\x.x) z"),                  # -> \x.x
    #     ("shadow outer", r"(\x.\x.x x) z"),                # -> \x.x x
    #     ("outer reference", r"(\x.\y.x y) z"),             # -> \y.z y
    #     ("inner application", r"(\x.(\x.x) x) z"),         # -> z
    #
    #     # Nested applications
    #     ("nested identity", r"(\x.x) ((\y.y) z)"),         # -> z
    #     ("apply twice", r"(\f.\x.f (f x)) (\y.y) a"),      # -> a
    #
    #     # Free variables
    #     ("free variable", r"(\x.x z) y"),                  # -> y z
    #     ("free application", r"(\x.z x) y"),              # -> z y
    #
    #     # More shadowing
    #     ("deep shadow", r"(\x.\x.\x.x) a"),                # -> \x.\x.x
    #     ("deep outer", r"(\x.\y.\z.x) a"),                 # -> \y.\z.a
    #
    #     # Combinations
    #     ("self application", r"(\x.x x) (\y.y)"),          # -> (\y.y) (\y.y)
    #     ("nested constant", r"(\a.(\b.a)) x"),             # -> \b.x
    # ]
    #

    tests = [
        # # Two independent definitions
        # ("two defs", r"{id = \x.x, const = \x.\y.x, } const"),
        #
        # # Definition application
        # ("identity call", r"{id = \x.x, } id z"),
        #
        # Multiple uses of same definition
        ("reuse", r"{id = \x.x, } id id"),

    #     # Nested definitions
    #     ("nested", r"{twice = \f.\x.f (f x), four = twice twice, } four"),
    #
    #     # Nested definition application
    #     ("nested application",
    #     r"{twice = \f.\x.f (f x), four = twice twice, id = \x.x, } four id"),
    #
        # Three-level expansion
        ("deep chain",
        r"{a = b, b = c, c = \x.x, } a"),

        #     # Application inside definition
    #     ("application rhs",
    #     r"{foo = (\x.x) (\y.y), } foo"),
    #
    #     # Definition referring to free variable
    #     ("free variable",
    #     r"{idz = \x.z, } idz"),
    #
    #     # Definition used inside lambda
    #     ("inside lambda",
    #     r"{id = \x.x, } \y.id y"),
    #
    #     # Definition used multiple places
    #     ("multiple expansion",
    #     r"{id = \x.x, } (id a) (id b)"),
    #
    #     # Definition shadows program variable
    #     ("free program variable",
    #     r"{id = \x.x, } (\id.id) y"),
    #
    #     # Definition expands to application
    #     ("application expansion",
    #     r"{foo = a b, } foo"),

         # Nested application expansion
         ("complex application",
         r"{foo = a b, bar = foo foo c, } bar"),


    #     # Large composed example
    #     ("compose",
    #     r"{id = \x.x, const = \x.\y.x, twice = \f.\x.f (f x), } twice id"),
    ]

    for name, source in tests:
        print(f"TESTING {name}")
        test_definition(name, source)
        print("-------")

def main():
    # test_expressions()
    test_definitions()

if __name__ == "__main__":
    main()
