import kpl.Lexer.Lexer as Lexer
import kpl.Parser.Parser as Parser
import kpl.Evaluator.Evaluator as Evaluator
import kpl.Object.Object as Object

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
    print("\nParser errors:\n")

    for error in errors:
        print(f"  • {error}")

    print()


def start():
    print(LOGO)

    # Persist between commands
    env = Object.Environment()

    while True:
        try:
            line = input(PROMPT)
        except EOFError:
            print()
            break

        if line.strip() == "":
            continue

        if line.lower() in ("exit", "quit"):
            break

        lexer = Lexer.New(line)
        parser = Parser.New(lexer)

        program = parser.parse_program()

        if parser.errors:
            print_parser_errors(parser.errors)
            continue

        evaluated = Evaluator.evals(program, env)

        if evaluated is not None and evaluated != Evaluator.GUTIRI:
            print(evaluated.Inspect())
