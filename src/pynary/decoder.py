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


class PYNDecoder:
    __slots__ = (
        "encoding_table",
        "magic",
    )

    encoding_table: dict
    magic: bytes

    def __init__(self) -> None:
        self.encoding_table = {}
        self.magic = b"PYN1"

    def load(self, b: bytes) -> object:
        if not isinstance(b, bytes):
            raise TypeError(f"Expected {bytes}, but got {type(b)}.")

        if not b[1 : 1 + int.from_bytes(b[:1], "big")] == self.magic:
            raise MagicMissmatch(self.magic, b[: len(self.magic)])

        b = b[1 + len(self.magic) :]

        try:
            o = self.encoding_table[b[:1]]["func"](self.encoding_table, b[1:])
            return o
        except KeyError as E:
            tag = E.args[0]

        raise TagMissmatch(tag)

    def add_type(self, function: callable, len_f: callable = lambda: None) -> None:
        self.encoding_table[len(self.encoding_table).to_bytes(1, "big")] = {
            "func": function,
            "leng": len_f,
        }


class MagicMissmatch(Exception):
    def __init__(self, expected: bytes, recieved: bytes) -> None:
        super().__init__(f"Expected {expected.decode()} but got {recieved.decode()}.")


class TagMissmatch(Exception):
    def __init__(self, tag: bytes) -> None:
        super().__init__(f"Tag '{tag}' not supported. Are you using the right decoder?")
