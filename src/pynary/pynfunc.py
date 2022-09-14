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


def build_none() -> (callable, callable):
    encode = lambda enc, _: enc[type(None)]["tag"]
    decode = lambda _, __: (None, 0)

    return encode, decode


def build_bool() -> (callable, callable):
    def encode(enc: dict, b: bool) -> bytes:
        return enc[bool]["tag"] + b.to_bytes(1, "big")

    def decode(_, b: bytes) -> (bool, 1):
        return bool.from_bytes(b[:1], "big"), 1

    return encode, decode


def build_int(size: int = 4, signed: bool = False) -> (callable, callable):
    def encode(enc: dict, i: int) -> bytes:
        return enc[int]["tag"] + i.to_bytes(size, "big", signed=signed)

    def decode(_, b: bytes) -> int:
        return int.from_bytes(b[:size], "big", signed=signed), size

    return encode, decode


def build_float(_64bit: bool = True) -> (callable, callable):
    def encode(enc: dict, f: float) -> bytes:
        return enc[float]["tag"] + struct.pack(f">{('f', 'd')[_64bit]}", f)

    def decode(_, b: bytes) -> (float, int):
        return struct.unpack(f">{('f', 'd')[_64bit]}", b[: 4 * (1 + _64bit)])[0], 4 * (
            1 + _64bit
        )

    return encode, decode


def build_str(size: int = 4) -> (callable, callable):
    def encode(enc: dict, s: str) -> bytes:
        bytestr: bytes = s.encode()
        return enc[str]["tag"] + len(bytestr).to_bytes(size, "big") + bytestr

    def decode(_, b: bytes) -> (callable, callable):
        length: int = int.from_bytes(b[:size], "big")
        return b[size : size + length].decode(), size + length

    return encode, decode


def build_tuple(size: int = 4) -> (callable, callable):
    def encode(enc: dict, t: tuple) -> bytes:
        content = b"".join(enc[type(item)]["func"](enc, item) for item in t)
        return enc[tuple]["tag"] + len(content).to_bytes(size, "big") + content

    def decode(enc: dict, b: bytes) -> tuple:
        length: int = int.from_bytes(b[:size], "big")
        end: int = size + length
        content: bytes = b[size:end]

        t: tuple = ()

        while content:
            o, ol = enc[content[:1]]["func"](enc, content[1:])

            content = content[ol + 1 :]
            t = t + (o,)

        return t, end

    return encode, decode


def build_list(size: int = 4) -> (callable, callable):
    def encode(enc: dict, l: list) -> bytes:
        content = b"".join(enc[type(item)]["func"](enc, item) for item in l)
        return enc[list]["tag"] + len(content).to_bytes(size, "big") + content

    def decode(enc: dict, b: bytes) -> list:
        length: int = int.from_bytes(b[:size], "big")
        end: int = size + length
        content: bytes = b[size:end]

        l: list = []

        while content:
            o, ol = enc[content[:1]]["func"](enc, content[1:])

            content = content[ol + 1 :]
            l.append(o)

        return l, end

    return encode, decode


def build_set(size: int) -> (callable, callable):
    def encode(enc: dict, s: set) -> bytes:
        content = b"".join(enc[type(item)]["func"](enc, item) for item in s)
        return enc[set]["tag"] + len(content).to_bytes(size, "big") + content

    def decode(enc: dict, b: bytes) -> set:
        length: int = int.from_bytes(b[:size], "big")
        end: int = size + length
        content: bytes = b[size:end]

        s: set = set()

        while content:
            o, ol = enc[content[:1]]["func"](enc, content[1:])

            content = content[ol + 1 :]
            s = s | {o}

        return s, end

    return encode, decode


def build_dict(size: int = 4) -> (callable, callable):
    def encode(enc: dict, d: dict) -> bytes:
        keys: bytes = b"".join(enc[type(key)]["func"](enc, key) for key in d.keys())
        values: bytes = b"".join(
            enc[type(value)]["func"](enc, value) for value in d.values()
        )

        return (
            enc[dict]["tag"]
            + len(keys).to_bytes(size, "big")
            + len(values).to_bytes(size, "big")
            + keys
            + values
        )

    def decode(enc: dict, b: bytes) -> dict:
        length_keys: int = int.from_bytes(b[:size], "big")
        length_vals: int = int.from_bytes(b[size : 2 * size], "big")

        end: int = 2 * size + length_keys + length_vals
        key_bytes: bytes = b[2 * size : 2 * size + length_keys]
        val_bytes: bytes = b[2 * size + length_keys : end]

        d: dict = {}

        while key_bytes:
            k, kl = enc[key_bytes[:1]]["func"](enc, key_bytes[1:])
            v, vl = enc[val_bytes[:1]]["func"](enc, val_bytes[1:])

            key_bytes = key_bytes[kl + 1 :]
            val_bytes = val_bytes[vl + 1 :]

            d[k] = v

        return d, end

    return encode, decode
