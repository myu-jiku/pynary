# Copyright 2022 Myu/Jiku
#
# This file is part of the Pynary package.
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

from pynary import PYNEncoder, encoder

enc = PYNEncoder()


class TestDecoder(unittest.TestCase):
    def test_type_missmatch(self):
        with self.assertRaises(encoder.TypeMissmatch):
            enc.dump(1)
