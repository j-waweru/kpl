import getpass
import kpl.Repl.Repl as Repl
import tests.evaluator_test as evaluator_test


def main():
    username = getpass.getuser()

    print(f"Hello {username}! Welcome to the Kikuyu Programming Language!")
    print("Feel free to type in commands")
    Repl.start()


if __name__ == "__main__":
    main()
