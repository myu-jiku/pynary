# Copyright 2022 Myu/Jiku
#
# This python module file is part of the Pynary package.
# Pynary is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# Pynary is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Pynary. If
# not, see <https://www.gnu.org/licenses/>

import unittest

from pynary import pyn, PYNBlank


class TestDecoder(unittest.TestCase):
    def _compare_io(self, input_value):
        output_value = pyn.load(pyn.dump(input_value))
        self.assertEqual(input_value, output_value)

    def test_none(self):
        self._compare_io(None)
        self._compare_io([None] * 4)

    def test_bool(self):
        self._compare_io(True)
        self._compare_io([True, False, True, False, False])

    def test_int(self):
        self._compare_io(45)

        _pyn = PYNBlank()

        _pyn.add_int(signed=True)
        input_value = -1
        output_value = _pyn.load(_pyn.dump(input_value))
        self.assertEqual(input_value, output_value)

        _pyn.add_int(6)
        input_value = 10000000000
        output_value = _pyn.load(_pyn.dump(input_value))
        self.assertEqual(input_value, output_value)

    def test_float(self):
        self._compare_io(0.0)
        self._compare_io(-1.03)
        self._compare_io(3.1415926535)

    def test_str(self):
        self._compare_io("test")
        self._compare_io(list("pynary"))

    def test_tuple(self):
        self._compare_io((1, 2, 3))
        self._compare_io(tuple((l,) for l in "tuple"))

    def test_list(self):
        self._compare_io(list(range(100)))
        self._compare_io([i + j for i in range(10) for j in range(10)])

    def test_set(self):
        self._compare_io({1, 2, 3})
        self._compare_io({(1, 2, 3), ("four", "five", "six"), (True, False, None)})

    def test_dict(self):
        self._compare_io({})
        self._compare_io({"key": "value"})
        self._compare_io({"test": {"test": {"test": list(range(50))}}})
