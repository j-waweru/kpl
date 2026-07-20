import getpass
import kpl.Repl.Repl as Repl


def main():
    username = getpass.getuser()

    print(f"Hello {username}! This is the Kikuyu programming language!")
    print("Feel free to type in commands")

    Repl.start()


if __name__ == "__main__":
    main()
