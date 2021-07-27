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


import os.path
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))

from singleuseinit import mark_init_as_single_use


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


# Output:
#   (<class '__main__.D1'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
#   D1 (x)
#   B (x)
#   A
#   C (x)
#
#   (<class '__main__.D2'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
#   D2 (x)
#   B (x)
#   A
