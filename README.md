# Pynary – binary representation of python objects

**Pynary** is a simple library that allows you to represent python objects as binary data. The only module it uses is [struct](https://docs.python.org/3/library/struct.html) from the standard library.

Unlike the [pickle](https://docs.python.org/3/library/pickle.html) module, Pynary doesn't allow arbitraty code execution (by default). This though means that only
a small subset of python objects is supported (by default). Currently this
includes:
- `NoneType`
- `bool`
- `int` – u32 by default
- `float` – 64 bit (default) and 32 bit 
- `str`
- `tuple`
- `list`
- `set`
- `dict`

Additional types can be supported with a [custom decoder and encoder](#modifying-the-decoder-and-encoder).

## Basic usage

```python
# Import the default decoder and encoder set:
from pynary import pyn

# Prepare the object you want to encode
your_object: object = ...

# Encode the object
encoded_object: bytes = pyn.dump(your_object)

# Decode the object
decoded_object: object = pyn.load(encoded_object)
```

If your input data cannot be parsed, a `pynary.PYNEncoder.TypeMissmatch` is
raised.

## Modifying the Decoder and Encoder

**WARNING:** Modifying the decoder and the encoder can introduce security risks.
Just be aware of that and act accordingly.

### Adding types to the default parser

If you don't want to change the behaviour of existing types you can simply
use the `add_type` method of the `PYNEncoder` and `PYNDecoder`.

Here is an example for adding a custom class:

```python
from pynary.pyn import _pyn

class MyClass:
    x: int

def _encode_my_object(enc: dict, my_object: MyClass) -> bytes:
    return enc[MyClass]["tag"] + int.to_bytes(my_object.x, 4, "big")

def _decode_my_object(_, b: bytes) -> (MyClass, int):
    my_object = MyClass()
    my_object.x = int.from_bytes(b[:4], "big")
    return my_object, 4

_pyn.encoder.add_type(MyClass, _encode_my_object)
_pyn.decoder.add_type(_decode_my_object)
```

The encode function (which doesn't have to be named like this) always takes two
arguments and has to return a `bytes` object. The first one is the encoding
table provided by the `PYNEncoder (_pyn.encoder)` and the second one is the object
that is to be encoded. 


The decode function works similarly. It needs an encoding table from the `PYNDecoder (_pyn.decoder)` as it's first argument. We only need that if we need 
to identify other types that are contained in our object (e.g. like in a list), so
we can omit it here. The second argument is the `bytes` object which contains the
data we that corresponds to our object. Instead of only returning one thing here,
we have to return two: the decoded python object and how much space it took in the
encoded data in bytes. Since we gave our x a size of 4 bytes in the encoding function we can just return that.

After that we add out encoding function to `_pyn.encoder` and our decoding function to `_pyn.decoder` with the `add_type` method. Note that the encoder's
method also requires us to add the type of the objects we want to encode, which in
this case is `MyClass`. For an object to be able to be parsed, `type(object)` must
return `MyClass`. Objects of classes that inherit from `MyClass` will raise an
error if not handled seperately.

It might also be a good idea to define a custom magic byte sequence to ensure
that data that is valid for our new format. This can be any sequence of bytes.
```python
magic: bytes = b"MyMagic"
_pyn.encoder.magic = magic
_pyn.decoder.magic = magic
```

To load or dump data use `_pyn.encoder.dump()` or `_pyn.decoder.load()`. If you
think that's a bit complicated you can create a `dump` and a `load` variable and
make them equal to their respective `_pyn` function.

```python
dump: callable = _pyn.encoder.dump
load: callable = _pyn.decoder.load
```

Now you can use your custom parser just like you would use the default.

```python
import my_pyn

my_object = MyClass()
my_object.x = 12

my_pyn.dump(my_object)
>>> b'\x07MyMagic\t\x00\x00\x00\x0c'

my_pyn.load(my_pyn.dump(my_object))
>>> <__main__.MyClass object at 0x...>
```

### Change the default behaviour
Detailed guide soon. If you want to know how now, just take a look at the source code. It's not well documented though...
