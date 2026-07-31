import kpl.Object.Object as Object


def test_string_hash_key():

    hello1 = Object.String("Hello World")
    hello2 = Object.String("Hello World")

    diff1 = Object.String("My name is johnny")
    diff2 = Object.String("My name is johnny")

    assert hello1.hash_key() == hello2.hash_key()
    assert diff1.hash_key() == diff2.hash_key()
    assert hello1.hash_key() != diff1.hash_key()
