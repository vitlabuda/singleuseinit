# SPDX-License-Identifier: BSD-3-Clause
#
# Copyright (c) 2021 Vít Labuda. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#     disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#     following disclaimer in the documentation and/or other materials provided with the distribution.
#  3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#     products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


# Class diagram:
#     A         A
#    / \        |
#   /   \       |
#  B     C      B
#   \   /       |
#    \ /        |
#     D1        D2


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


# Output:
#   (<class '__main__.D1'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
#   D1 (x)
#   B (x)
#   C (x)
#   A
#
#   (<class '__main__.D2'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
#   D2 (x)
#   B (x)
#   Traceback (most recent call last):
#     File "/home/limited/PycharmProjects/singleuseinit/examples/problem1.py", line 51, in <module>
#       D2("x")
#     File "/home/limited/PycharmProjects/singleuseinit/examples/problem1.py", line 41, in __init__
#       super().__init__(x)
#     File "/home/limited/PycharmProjects/singleuseinit/examples/problem1.py", line 23, in __init__
#       super().__init__(x)
#   TypeError: __init__() takes 1 positional argument but 2 were given
