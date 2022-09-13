# Pynary – binary representation of python objects

**Pynary** is a simple library that allows you to represent python objects as binary data. The only module it uses is [struct](https://docs.python.org/3/library/struct.html) from the standard library.

Unlike the [pickle](https://docs.python.org/3/library/pickle.html) module, Pynary doesn't allow arbitraty code execution (by default). This though means that only
a small subset of python objects is supported (by default). Currently this
includes:
- 16 bit unsigned integers
- strings of any length
- lists of any size containing any other type
- dictionaries of any size
- NoneType

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
import struct  # for the sake of this example

from pynary import PYNDecoder, PYNEncoder


class MyClass:
    x: int
```

The pack function (which doesn't need to be named like this) always takes two
arguments and has to return a `bytes` object. The first one is the encoding
table provided by the `PYNEncoder` and the second one is the object that is to
be encoded. If you don't need the encoding table you can also specify _ as
the argument name.
```python
def pack_my_object(enc: dict, my_object: MyClass) -> bytes:
    return (
        enc[MyClass]["tag"]  # tag used to identify the object's type
```

Here we convert the value 'x' to a 16 bit integer in the little endian format,
but you can do practically everything as long as you are consistent (and the
result is of type bytes).
```python
        + struct.pack("<I", my_object.x)
    )
```

The unpack function works similarly. It also takes the encoding table (from the
PYNDecoder though) as it's first argument. We only need that if we need to
identify other types that are contained in our object, so we can omit it here.
The second argument is the `bytes` object which contains the data we that
corresponds to our object. Instead of only returning one thing here, we have to
return two: the decoded python object and how much space it took in the encoded
data in bytes. Since a 16 bit integer always has a size of 4 bytes we can just return that.
```python
def unpack_my_object(_, b: bytes) -> (MyClass, int):
    my_object = MyClass()

    # unpack returns a tuple, so we need to access the element at position 0
    my_object.x = struct.unpack("<I", b[:4])[0]

    return my_object, 4
```

Finally we create our encoder and decoder and give them our functions. The
encoder's `add_type` function additionally needs the type of our object.
When adding multiple types the order matters. Add the functions `pack_a`, `pack_b` and `pack_c` to the encoder in the same order as `unpack_a`, `unpack_b` and `unpack_c` to the decoder.
```python
encoder = PYNEncoder()
encoder.add_type(MyClass, pack_my_object)

decoder = PYNDecoder()
decoder.add_type(unpack_my_object)
```

It might also be a good idea to define a custom magic byte sequence to ensure
that data that is valid for our new format. This can be any sequence of bytes.
```python
magic: bytes = b"MyMagic"
encoder.magic = magic
decoder.magic = magic
```

To load or dump data use `decoder.load()` or `encoder.dump()`.

### Change the default behaviour
Detailed guide soon. If you want to know how now, just take a look at the source code. I might also add another default parser that can handle 32 bit signed
integers.
