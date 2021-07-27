# singleuseinit
**singleuseinit** is a tiny, single-function Python 3 library, making it easy for one to clearly and safely call (all) class initializers when using multiple inheritance and encountering [diamond problems](https://en.wikipedia.org/wiki/Multiple_inheritance#The_diamond_problem). 



## Why?
### Problem 1

Consider the following [code](examples/problem1.py):

```python3
class A:
    def __init__(self):
        print("A")


class B(A):
    def __init__(self, x):
        print("B ({})".format(x))

        # super().__init__ initializes (according to the MRO):
        #  - C in the case of D1 (argument must be given)
        #  - A in the case of D2 (argument mustn't be given)
        # -> What to do next?
        super().__init__(x)  # Even PyCharm is confused by this - it says "Unexpected argument", even though it is not always the case.


class C(A):
    def __init__(self, x):
        print("C ({})".format(x))
        super().__init__()


class D1(B, C):
    def __init__(self, x):
        print("D1 ({})".format(x))
        super().__init__(x)


class D2(B):
    def __init__(self, x):
        print("D2 ({})".format(x))
        super().__init__(x)


if __name__ == '__main__':
    print(D1.__mro__)
    D1("x")

    print()

    print(D2.__mro__)
    D2("x")
```

This code will inevitably crash. 
When initializing the ``D2`` class, the ``B`` class's initializer will pass an unexpected argument to the ``A`` class's initializer.
However, when initializing the ``D1`` class, the ``B`` class's initializer must pass the argument, because, according to the MRO (Method Resolution Order), it's initializing the ``C`` class. 

Even if the ``D2`` class wasn't present, this wouldn't be the best solution:
- We would have to know what classes are going to extend the ``B`` class and their constructors' arguments. This alone would be a poor object-oriented design.
- The programmer would have to reconstruct the whole MRO in their mind so that the ``B`` class's initializer wouldn't be confusing to them. *"Why is an argument passed to the ``A``'s initializer if it doesn't accept any arguments?"* 


### Problem 2
Consider the following [code](examples/problem2.py):

```python3
class A:
    def __init__(self):
        print("A")
        # In the case of the D1 class, this method gets called twice (because both B and C call A's __init__).


class B(A):
    def __init__(self, x):
        print("B ({})".format(x))
        A.__init__(self)


class C(A):
    def __init__(self, x):
        print("C ({})".format(x))
        A.__init__(self)


class D1(B, C):
    def __init__(self, x):
        print("D1 ({})".format(x))
        B.__init__(self, x)
        C.__init__(self, x)


class D2(B):
    def __init__(self, x):
        print("D2 ({})".format(x))
        B.__init__(self, x)


if __name__ == '__main__':
    print(D1.__mro__)
    D1("x")

    print()

    print(D2.__mro__)
    D2("x")
```

We switched from calling the superclasses' initializers via ``super()`` to calling them "statically".
The code is way cleaner and way more understandable now.
However, when initializing the ``D1`` class, the ``A`` constructor will get called twice, because both ``B`` and ``C`` call the ``A`` class's initializer. 


### Solution
Consider the following [code](examples/solution.py):

```python3
class A:
    @mark_init_as_single_use
    def __init__(self):
        print("A")


class B(A):
    @mark_init_as_single_use  # Not necessary in this (specific) case
    def __init__(self, x):
        print("B ({})".format(x))
        A.__init__(self)


class C(A):
    @mark_init_as_single_use  # Not necessary in this (specific) case
    def __init__(self, x):
        print("C ({})".format(x))
        A.__init__(self)


class D1(B, C):
    @mark_init_as_single_use  # Not necessary in this (specific) case
    def __init__(self, x):
        print("D1 ({})".format(x))
        B.__init__(self, x)
        C.__init__(self, x)


class D2(B):
    @mark_init_as_single_use  # Not necessary in this (specific) case
    def __init__(self, x):
        print("D2 ({})".format(x))
        B.__init__(self, x)


if __name__ == '__main__':
    print(D1.__mro__)
    D1("x")

    print()

    print(D2.__mro__)
    D2("x")
```

This is where this library comes in. 
It ensures that a class's initializer annotated with ``@mark_init_as_single_use`` will only get called once, when using the approach from [Problem 2](#problem-2).

When initializing the ``D1`` class, the initializers will be called in the following order: ``D1``, ``B``, ``A``, ``C``.
Granted, the MRO isn't followed, but the point is, that after a "static" call to a superclass's initializer finishes, it is ensured that the superclass is properly initialized and that it was initialized only once.



# Licensing 
This project is licensed under the **3-clause BSD license**. See the [LICENSE](LICENSE) file for details.

Written by **[Vít Labuda](https://vitlabuda.cz/)**.
