# The Kikuyu Programming language

[KplLogo](/resources/kpl.png)

Inspired by [DreamBerd](https://github.com/TodePond/GulfOfMexico) and based on the [Monkey language](https://interpreterbook.com/).

Welcome to the Kikuyu Programming language (abbr kpl), a not blazingly fast language written in python.

Here are its features. Syntax is made to resemble the Kikuyu language as much as possible though sometimes I could not find equivalent translations.

Once you are done reading through you can check out the [examples](./resources/Examples.md)

---

## Features

Be fancy.
In kpl every line ends with a dollar sign.

### Declarations

Declarations are made using the Reka keyword. To see all the types make sure to read the examples.

> [!NOTE]
> All keywords are written in Title Case

```python
Reka a = 10$

Reka b = a + 5$

Reka name = 'John'$

Reka arr = [10,20,30]$

Reka foobar = fn(x, y)

```

### Strings

You can declare strings using either single or double quotes.

```python
'Hello'$
"World"$

```

Strings support the following operations:

Concatenation using the + operator.

```python
'Hello' + ' ' + 'World!' # Hello World!

```

You can also perform deconcatenation using minus operator.

```python
'Hello' - 'World!$ # "HeWrd!"
'abcdef' - 'bd'$ # "acef"
'abc' - 'xyz'$ # "abcxyz"

```

### Integers

Integers support 5 equals comparison operators.

```python
"1 == 1"$ # True : always true
"1 === 1"$ # True : type of a is same as that of b
"1 ==== 1"$ # True : value of a equal that of b
"1 ===== 1"$ # True : a is b
"1 ====== 1"$ # False : always false

# And that means

"1 == 2"$ # True 
"1 === 2"$ # True
"1 ==== 2"$ # False
"1 ===== 2"$ # False
"1 ====== 2"$ # False

```

### Floats

Floats are a relic of an archaic programming past and don't even apply to real world objects. After all have you ever seen half a ng'ombe.
Therefore Kpl has no support for them.

### Booleans

Kpl supports two boolean operators: Ma and Maheni used as follows:

```python
!5$               # False
!Maheni$            # True
(1 < 2) == Ma$      # True
(1 < 2) == Maheni$  # False

```

### If else return statements

Kpl has a very verbose syntax on purpose to make it easier to understand linguistically.

If else statements can be declared as follows:

```python
Akorwo (10 > 1)     # if 
Anjiriria           # other languages use start or {
    Akorwo (1 < 2)  # nested if
    Anjiriri a
        Chokia 99$
    Rikia           # other languages use end or }

    Chokia 0$       # return
Rikia

```

> [!NOTE]
> To improve programming experience the shortened forms can be used instead.

```python
# Anj: Anjiriria,
# Rik: Rikia,

# This should be fine
Akorwo (Ma)
Anj
    10$
Rik

```

### Functions

In kpl functions are first class citizens and declared using Fn keyword.

```python
Reka makeAdder = Fn(x)
Anjiriria
    Chokia Fn(y)
    Anjiriria
        x + y$
    Rikia$
Rikia$

Reka addFive = makeAdder(5)$
addFive(10)$

```

### Arrays

Some languages begin indexing at 0 which is unintuitive for humans while others begin at 1 which is not how computers really work.
Kpl makes the worst out of both worlds.
Indexing starts at -1 and only negative values are supported.

```python
Reka array =[1, 2, 3]$

array[-1]    # first
array[-2]    # second
array[-3]    # third

```

Doing the following will result in an error.

```python
array[0]    # Error
array[1]    # Error
array[-5]   # GUTIRI 

```

### Builtins

Kpl has the following built-in functions.

* `_Nyonia` - similar to print functions in other languages
```python
_Nyonia('Hello')$ # prints hello

```


* `_Uraihu` - returns the length of strings or elements in an array.
```python
_Uraihu('Hello')$    # 5 
_Uraihu([1,2,3,4])$    # 4 

```


* `_Mbere` - returns the first element of an array
```python
_Mbere([1,2,3])$    # 1

```


* `_Muico` - returns the last element of an array
```python
_Muico(['A','B','C'])$  # C

```


* `_HauHangi` - returns all but first element
```python
_HauHangi([1,2,3,4])$  # 2 , 3 , 4

```


* `_Ikia` - pushes values into an array
```python
_Ikia([1,2,3],4)$  # [1,2,3,4]

```



### Errors

To build the programmers morale, all runtime errors are prefixed with unicode character `U+1F595 U+1F3FF`.
Error messages try to adhere as close as possible to the Kikuyu language.
Here are some examples:

```python
[1, 2, 3][0]$     # Array indices chithiaga oo -1,-2,-3. Ndona 0. Gutiri 0,1,2
_Uraihu('one', 'two') # Namba ndĩkinyanĩte. Ndona=2, ngwendaga=1.

```

---

## Installation

To get started with the Kikuyu Programming Language you can copy-paste this readme file into your favourite AI eg ChatGPT and ask it to create an interpreter for you.

> [!NOTE]
> The kpl interpreter is now finished.

You can clone the repo and run:

```bash
pip install -e .

```

Then you can run:

```bash
kpl # Open the REPL 

# or alternatively

kpl myfile.kpl # to read the code from a file

```

---

## FAQ

* **What is Kpl written in:** It's written in python.
* **Where can I see code examples:** If you can already program in another language, you can check out the [examples](https://www.google.com/search?q=./resources/Examples.md).
* **Where can I get more documentation:** This Readme file is the documentation. After checking out the examples you can consider yourself an expert in the Kikuyu Programming Language. Feel free to add it to your resume and bring it up in your next interview.
* **What are the advantages of kpl:** For once no AI models have been trained on kpl so by using it you can be guaranteed that all code is human generated and not vibecoded hence its of higher quality.

---

## Ownership

Using the name kpl, Kikuyu Programming language or any term that matches the regex:

```regex
\bK(?:i(?:k(?:u(?:y(?:u)?)?)?)?)?\s*P(?:r(?:o(?:g(?:r(?:a(?:m(?:m(?:i(?:n(?:g)?)?)?)?)?)?)?)?)?\s*L(?:a(?:n(?:g(?:u(?:a(?:g(?:e)?)?)?)?)?)?\b

```

in your project implies Kpl Foundation **does not** own your project.
However not using them implies the Kpl Foundation **does** own your project. If you would like to keep ownership of your work, please always use the appropriate terms as indicated.

### Examples:

* ✅ `KikProLanScript` implies that Kpl foundation does not own your project. You are free to use this name.
* ❌ `PythonFoundation` owned by the Kpl foundation please consider renaming.
* ❌ `SafaricomKenyaFoundation` owned by the Kpl foundation please consider renaming.
