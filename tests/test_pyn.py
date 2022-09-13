import unittest

from pynary import pyn, decoder, encoder


class TestPyn(unittest.TestCase):
    def _compare_io(self, input_value):
        output_value = pyn.load(pyn.dump(input_value))
        self.assertEquals(input_value, output_value)

    def test_magic(self):
        self.assertEquals(
            None,
            pyn.load(pyn.encoder.magic + pyn.encoder.encoding_table[type(None)]["tag"]),
        )

        with self.assertRaises(decoder.MagicMissmatch):
            pyn.load(b"PYN0")

        with self.assertRaises(decoder.MagicMissmatch):
            pyn.load(pyn.encoder.magic + b"0\x00\x01\x00\x00\x00")

    def test_int(self):
        self._compare_io(2022)

    def test_str(self):
        self._compare_io("pynary")

    def test_list(self):
        self._compare_io([1, 2, ["python", 42]])
        self._compare_io([[i * x for x in range(100)] for i in range(100)])

    def test_dict(self):
        self._compare_io({"こんにちは": "世界"})
        self._compare_io({s: [{i: f"🍌banana{i}"} for i in range(100)] for s in "data"})

    def test_none(self):
        self._compare_io(None)
        self._compare_io([None, None, {"": None}, None])

    def test_bool(self):
        self._compare_io(True)
        self._compare_io(
            {
                "🍌": True,
                "🍍": False,
                "list": [1, True, "three", False, 5, 6, 7, 8, None, True],
            }
        )

    def test_float(self):
        self._compare_io(1.337)
        self._compare_io([3.14159265359, {8.9875517923: [42.0, "test"]}])

    def test_tuple(self):
        self._compare_io((1, 2, 3, 4))
        self._compare_io(((1, 2, 3, 4), [1, 2, 3, 4], {1: 2, 3: 4}, None))

    def test_set(self):
        self._compare_io({1, 3, 2})
        self._compare_io({tuple(range(10)), "pynary", True})


if __name__ == "__main__":
    unittest.main()
