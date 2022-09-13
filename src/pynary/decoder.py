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

import struct


class PYNDecoder:
    __slots__ = ("encoding_table", "magic",)

    encoding_table: dict
    magic: bytes

    def __init__(self) -> None:
        self.encoding_table = {}
        self.magic = b"PYN1"

        self.add_type(_unpack_int)
        self.add_type(_unpack_str)
        self.add_type(_unpack_list)
        self.add_type(_unpack_dict)
        self.add_type(_unpack_none)

    def load(self, b: bytes) -> object:
        if not b.startswith(self.magic):
            raise MagicMissmatch(magic, b[:len(self.magic)])

        b = b[len(self.magic) :]

        try:
            o, _ = self.encoding_table[b[:1]]["func"](self.encoding_table, b[1:])
            return o
        except KeyError as E:
            tag = E.args[0]

        raise TagMissmatch(tag)


    def add_type(self, function: callable) -> None:
        self.encoding_table[struct.pack("<B", len(self.encoding_table))] = {
            "func": function,
        }


class MagicMissmatch(Exception):
    def __init__(self, expected: bytes, recieved: bytes) -> None:
        super().__init__(f"Expected {expected.decode()} but got {recieved.decode()}.")


class TagMissmatch(Exception):
    def __init__(self, tag: bytes) -> None:
        super().__init__(f"Tag '{tag}' not supported. Are you using the right decoder?")


def _unpack_int(_, b: bytes) -> (int, int):
    return struct.unpack("<I", b[:4])[0], 4


def _unpack_str(_, b: bytes) -> (str, int):
    length: int = struct.unpack("<I", b[:4])[0]
    return b[4:4+length].decode(), 4 + length


def _unpack_list(enc: dict, b: bytes) -> (list, int):
    length: int = struct.unpack("<I", b[:4])[0]
    content: bytes = b[4:4+length]

    l: list = []

    while content:
        o, ol = enc[content[:1]]["func"](
            enc, content[1:]
        )

        content = content[ol+1:]
        l.append(o)

    return l, length + 4


def _unpack_dict(enc: dict, b: bytes) -> (dict, int):
    length: int = struct.unpack("<I", b[:4])[0]
    content: bytes = b[4:4+length]

    d: dict = {}
    key: str = None

    while content:
        o, ol = enc[content[:1]]["func"](
            enc, content[1:]
        )

        content = content[ol+1:]

        if key is None:
            key = o
        else:
            d[key] = o
            key = None

    return d, length + 4


def _unpack_none(_, __) -> (None, 0):
    return None, 0

