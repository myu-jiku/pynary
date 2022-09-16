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

    def dump(self, o: object) -> bytes:
        try:
            return (
                len(self.magic).to_bytes(1, "big")
                + self.magic
                + self.encoding_table[type(o)]["func"](self.encoding_table, o)
            )
        except KeyError as E:
            t = E.args[0]

        raise TypeMissmatch(t)

    def add_type(self, t: type, function: callable) -> None:
        self.encoding_table[t] = {
            "func": function,
            "tag": len(self.encoding_table).to_bytes(1, "big"),
        }


class TypeMissmatch(Exception):
    def __init__(self, t: type) -> None:
        super().__init__(
            f"Type {t} is not supported. Consider using a custom PYNEncoder and PYNDecoder."
        )
