# KPL language features

## Variables

```text
Reka a = 10$
a$

Reka b = a + 5$
b$

Reka name = 'Joe'$
name$
```

---

## Integer arithmetic

```text
5 + 5$
10 - 3$
8 * 7$
20 / 5$
17 % 5$

2 * (5 + 10)$
(5 + 10 * 2 + 15 / 3) * 2 + -10$
```

---

## Prefix operators

```text
-5$
--5$

!Ma$
!Maheni$
!!5$
```

---

## Comparisons

```text
1 < 2$
1 > 2$

1 == 2$
1 == 1$

1 === 1$
1 === 2$

1 ==== 1$
1 ==== 2$

1 ===== 1$
1 ===== 2$

1 ====== 1$
1 ====== 2$

1 != 2$
```

---

## Booleans

```text
Ma$
Maheni$

Ma == Maheni$
Ma != Maheni$

(1 < 2) == Ma$
(1 > 2) == Maheni$
```

---

## If / Else

```text
Akorwo (Ma)
Anjiriria
    10$
Rikia
```

```text
Akorwo (1 > 2)
Anjiriria
    10$
Rikia
Tiguo
Anjiriria
    20$
Rikia
```

---

## Return

```text
Chokia 5$
```

Nested

```text
Akorwo (10 > 1)
Anjiriria
    Akorwo (1 < 2)
    Anjiriria
        Chokia 99$
    Rikia

    Chokia 0$
Rikia
```

---

## Strings

```text
'Hello'$
'World'$

'Hello' + ' World'$

'Hello' - 'World!'$
'Programming' - 'Python'$
'AABBCC' - 'BBCCDD'$
```

---

## Functions

```text
Reka identity = fn(x)
Anjiriria
    x$
Rikia$

identity(5)$
```

```text
Reka add = fn(x, y)
Anjiriria
    x + y$
Rikia$

add(10, 20)$
```

Anonymous

```text
fn(x)
Anjiriria
    x * x$
Rikia(9)$
```

---

## Closures

```text
Reka makeAdder = fn(x)
Anjiriria
    Chokia fn(y)
    Anjiriria
        x + y$
    Rikia$
Rikia$

Reka addFive = makeAdder(5)$
addFive(10)$
```

---

## Arrays

```text
[]$

[1,2,3]$

['one','two','three']$

[1,2*2,3+3]$
```

---

## Array indexing

```text
[1,2,3][0]$

[1,2,3][2]$

Reka arr = [10,20,30]$

arr[1]$

arr[0] + arr[2]$
```

---

## Hashes

```text
{}$

{'name':'Joe'}$

{
'name':'Joe',
'age':25,
'admin':Ma
}$
```

Expression keys

```text
Reka key = 'name'$

{
key:'Joe'
}$
```

Expression values

```text
{
'one':1,
'two':2+2,
'three':3*3
}$
```

---

## Hash indexing

```text
{'name':'Joe'}['name']$

{'name':'Joe'}['missing']$
```

```text
Reka person = {
'name':'Joe',
'age':25
}$

person['name']$

person['age']$
```

Nested

```text
Reka people = [
{
'name':'Alice',
'age':24
},
{
'name':'Anna',
'age':28
}
]$

people[0]['name']$

people[1]['age']$

people[0]['age'] + people[1]['age']$
```

---

## Built-ins

### _Uraihu

```text
_Uraihu('')$

_Uraihu('Hello')$

_Uraihu([1,2,3,4])$
```

---

### _Mbere

```text
_Mbere([1,2,3])$

_Mbere(['A','B','C'])$
```

---

### _Muico

```text
_Muico([1,2,3])$

_Muico(['A','B','C'])$
```

---

### _HauHangi

```text
_HauHangi([1,2,3,4])$

_HauHangi(_HauHangi([1,2,3,4]))$
```

---

### _Ikia

```text
_Ikia([1,2,3],4)$

_Ikia([],1)$
```

---

### _Nyonia

```text
_Nyonia('Hello')$

_Nyonia(123)$

_Nyonia([1,2,3])$

_Nyonia({'name':'Joe'})$

_Nyonia('One','Two','Three')$
```

---

## Combined example

```text
Reka people = [
{
'name':'Alice',
'age':24
},
{
'name':'Bob',
'age':30
}
]$

Reka getName = fn(person)
Anjiriria
    person['name']$
Rikia$

Reka getAge = fn(person)
Anjiriria
    person['age']$
Rikia$

_Nyonia(getName(people[0]))$
_Nyonia(getAge(people[1]))$

Reka nums = [1,2,3,4]$

_Nyonia(_Uraihu(nums))$
_Nyonia(_Mbere(nums))$
_Nyonia(_Muico(nums))$
_Nyonia(_HauHangi(nums))$
_Nyonia(_Ikia(nums,5))$

Reka greeting = 'Hello' + ' World'$

_Nyonia(greeting)$

_Nyonia('Programming' - 'Python')$
```

