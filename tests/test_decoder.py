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

from pynary import PYNDecoder, decoder

dec = PYNDecoder()


class TestDecoder(unittest.TestCase):
    def test_magic_missmatch(self):
        with self.assertRaises(decoder.MagicMissmatch):
            dec.load(b"\x04PYN0")

        with self.assertRaises(decoder.MagicMissmatch):
            dec.load((len(dec.magic) + 1).to_bytes(1, "big") + b"{dec.magic}0")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            dec.load(1)

    def test_tag_missmatch(self):
        with self.assertRaises(decoder.TagMissmatch):
            dec.load(len(dec.magic).to_bytes(1, "big") + dec.magic + b"\x00")
