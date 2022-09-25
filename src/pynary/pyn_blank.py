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

from pynary import PYNDecoder, PYNEncoder
from pynary import pynfunc


class PYNBlank:
    __slots__ = (
        "encoder",
        "decoder",
        "dump",
        "load",
        "signed",
        "int_size",
    )

    encoder: PYNEncoder
    decoder: PYNDecoder

    dump: callable
    load: callable

    signed: bool
    int_size: int

    def __init__(self) -> None:
        self.encoder = PYNEncoder()
        self.decoder = PYNDecoder()

        self.dump = self.encoder.dump
        self.load = self.decoder.load

        self.signed = False
        self.int_size = 4

    def add_none(self) -> None:
        encode, decode, length = pynfunc.build_none()

        self.encoder.add_type(type(None), encode)
        self.decoder.add_type(decode, length)

    def add_bool(self) -> None:
        encode, decode, length = pynfunc.build_bool()

        self.encoder.add_type(bool, encode)
        self.decoder.add_type(decode, length)

    def add_int(self, size: int = None, signed: bool = None) -> None:
        if signed is None:
            signed = self.signed

        if size is None:
            size = self.int_size

        encode, decode, length = pynfunc.build_int(size, signed)

        self.encoder.add_type(int, encode)
        self.decoder.add_type(decode, length)

    def add_float(self, _64bit: bool = True) -> None:
        encode, decode, length = pynfunc.build_float(_64bit)

        self.encoder.add_type(float, encode)
        self.decoder.add_type(decode, length)

    def add_str(self, size: int = None) -> None:
        if size is None:
            size = self.int_size

        encode, decode, length = pynfunc.build_str(size)

        self.encoder.add_type(str, encode)
        self.decoder.add_type(decode, length)

    def add_list(self, size: int = None) -> None:
        if size is None:
            size = self.int_size

        encode, decode, length = pynfunc.build_list(size)

        self.encoder.add_type(list, encode)
        self.decoder.add_type(decode, length)

    def add_tuple(self, size: int = None) -> None:
        if size is None:
            size = self.int_size

        encode, decode, length = pynfunc.build_tuple(size)

        self.encoder.add_type(tuple, encode)
        self.decoder.add_type(decode, length)

    def add_set(self, size: int = None) -> None:
        if size is None:
            size = self.int_size

        encode, decode, length = pynfunc.build_set(size)

        self.encoder.add_type(set, encode)
        self.decoder.add_type(decode, length)

    def add_dict(self, size: int = None) -> None:
        if size is None:
            size = self.int_size

        encode, decode, length = pynfunc.build_dict(size)

        self.encoder.add_type(dict, encode)
        self.decoder.add_type(decode, length)
