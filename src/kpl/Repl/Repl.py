import sys
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


def print_parser_errors(errors):
    print("\nParser errors:\n")
    for error in errors:
        print(f"  • {error}")
    print()


def run_source(source, env):
    lexer = Lexer.New(source)
    parser = Parser.New(lexer)

    program = parser.parse_program()

    if parser.errors:
        print_parser_errors(parser.errors)
        return

    evaluated = Evaluator.evals(program, env)

    if evaluated is not None and evaluated != Evaluator.GUTIRI:
        print(evaluated.Inspect())


def start():
    print(LOGO)

    env = Object.Environment()

    # kpl myprogram.kpl
    if len(sys.argv) > 1:
        filename = sys.argv[1]

        with open(filename, "r", encoding="utf-8") as f:
            source = f.read()

        run_source(source, env)
        return

    # Interactive REPL
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

        run_source(line, env)
