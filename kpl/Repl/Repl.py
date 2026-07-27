import kpl.Lexer.Lexer as Lexer
import kpl.Evaluator.Evaluator as Evaluator
import kpl.Parser.Parser as Parser

PROMPT = ">> "

LOGO = r"""
██╗  ██╗██████╗ ██╗
██║ ██╔╝██╔══██╗██║
█████╔╝ ██████╔╝██║
██╔═██╗ ██╔═══╝ ██║
██║  ██╗██║     ███████╗
╚═╝  ╚═╝╚═╝     ╚══════╝

      Kikuyu Programming Language
"""


def print_parser_errors(errors: list[str]):
    print("\nParser errors:")

    for error in errors:
        print(f"  • {error}")

    print()


def start():

    print(LOGO)

    # while True:
    #     try:
    #         line = input(PROMPT)
    #     except EOFError:
    #         print()
    #         return

    line = "Reka x = 5 + 10 * 3$"
    line = "5"
    line = "Maheni"
    line = "!Maheni"
    l = Lexer.New(line)
    p = Parser.New(l)

    program = p.parse_program()

    if p.errors:
        print_parser_errors(p.errors)
        # continue

    print("The program is :")
    print(program)

    print()

    evaluated = Evaluator.evals(program)
    if evaluated is not None:
        print("Evaluated program is : ")
        print(evaluated.Inspect())
