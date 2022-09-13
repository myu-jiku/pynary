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


class PYNEncoder:
    __slots__ = (
        "encoding_table",
        "magic",
    )

    encoding_table: dict
    magic: bytes

    def __init__(self) -> None:
        self.encoding_table = {}
        self.magic = b"PYN1"

        self.add_type(int, _pack_int)
        self.add_type(str, _pack_str)
        self.add_type(list, _pack_list)
        self.add_type(dict, _pack_dict)
        self.add_type(type(None), _pack_none)
        self.add_type(bool, _pack_bool)
        self.add_type(float, _pack_float)
        self.add_type(tuple, _pack_tuple)
        self.add_type(set, _pack_set)

    def dump(self, o: object) -> bytes:
        try:
            return self.magic + self.encoding_table[type(o)]["func"](
                self.encoding_table, o
            )
        except KeyError as E:
            t = E.args[0]

        raise TypeMissmatch(t)

    def add_type(self, t: type, function: callable) -> None:
        self.encoding_table[t] = {
            "func": function,
            "tag": struct.pack("<B", len(self.encoding_table)),
        }


class TypeMissmatch(Exception):
    def __init__(self, t: type) -> None:
        super().__init__(
            f"Type {t} is not supported. Consider using a custom PYNEncoder and PYNDecoder."
        )


def _pack_int(enc: dict, i: int) -> bytes:
    return enc[int]["tag"] + struct.pack("<I", i)


def _pack_str(enc: dict, s: str) -> bytes:
    bytestr: bytes = s.encode()
    return enc[str]["tag"] + struct.pack("<I", len(bytestr)) + bytestr


def _pack_list(enc: dict, l: list) -> bytes:
    content = b"".join(enc[type(item)]["func"](enc, item) for item in l)
    return enc[list]["tag"] + struct.pack("<I", len(content)) + content


def _pack_dict(enc: dict, d: dict) -> bytes:
    content = b"".join(
        enc[type(item)]["func"](enc, item) for items in d.items() for item in items
    )

    return enc[dict]["tag"] + struct.pack("<I", len(content)) + content


def _pack_none(enc: dict, _) -> bytes:
    return enc[type(None)]["tag"]


def _pack_bool(enc: dict, b: bool) -> bytes:
    return enc[bool]["tag"] + struct.pack("<?", b)


def _pack_float(enc: dict, f: float) -> bytes:
    return enc[float]["tag"] + struct.pack("<d", f)


def _pack_tuple(enc: dict, t: tuple) -> bytes:
    content = b"".join(enc[type(item)]["func"](enc, item) for item in t)
    return enc[tuple]["tag"] + struct.pack("<I", len(content)) + content


def _pack_set(enc: dict, s: set) -> bytes:
    content = b"".join(enc[type(item)]["func"](enc, item) for item in s)
    return enc[set]["tag"] + struct.pack("<I", len(content)) + content
