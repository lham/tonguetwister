# Bitmap data (BITD)
This is a [resource chunk](#TODO). It contains image data for a [bitmap cast member](./castmembers/bitmap.md). The
bitmap data can not be decoded and rendered without data from its bitmap cast member chunk.

The chunk abbreviation is `BITD`.


## Structure
The bitmap data chunk contains raw image data. Depending on its bit depth and size the data may or may not be encoded
using run length encoding.


## Decoding the data into 32-bit aRGB bitmaps
Generally speaking the decoding process follow the same steps for each bit depth, but that partially depends on your
implementation. So this explanation follows the steps this library uses for decoding.

To unpack the bitmap data we need access to the following variables from the
[bitmap cast member](./castmembers/bitmap.md):

- bytes-per-image-row `BDP`
- width `W`
- height `H`
- palette `P`

The steps to unpack the bitmaps data are roughly the following:

1. Convert the bitmap data into a stream.
1. For each row in the image:
    1. Read the number of bytes specified by the bytes-per-image-row `BDP` from the data stream.
        - If size of the stream is equal to `H` &times; `BDP`, then the data is not encoded. Just read the bytes into a
          long stream.
        - Otherwise the data is encoded using the [PackBits algorithm](https://en.wikipedia.org/wiki/PackBits). Decode
          using the steps of the algorithm. Before returning the bytes they need to be reordered if the depth depth is
          16-bit or 32-bit; the bytes for each 16-bit word and 32-bit word, respectively, are encoded so that every
          first byte for each word in the row comes first, then every second byte for each word in the row, etc.
    1. Convert the byte list into 32, 16, 8, 4, 2, or 1-bit words depending on the bit depth. For bit depths 8 and below
       there might be left-over bits in the byte list, so the list of words need to be trimmed to `W` elements.
1. Convert each word into a color.
    - For a 32-bit word, there are 4 color channels: alpha, red, green, blue. They are packed into the word in that
      order with 8 bits per channel. The alpha channel does not seem to be used in Director 6, hence it can be replaced
      with the maximum alpha value, usually 255.
    - For a 16-bit word, there are 3 color channels: red, green, blue. They are packed into the word in that order with
      5 bits per channel. The left-most bit is unused. To obtain an 8-bit channel from the 5-bit channel, the 5-bit
      value is concatenated from the right with the middle 3 bits of the value in question.
    - For words with 8 bits or fewer, the word is used as an index inside the palette `P` to get the RGB color value.
1. Flip the rows of the image so that the first row becomes the last row, the second row becomes the second-to-last row
   and so on. This is done because bitmaps are read upside down, see this
   [link](https://medium.com/sysf/bits-to-bitmaps-a-simple-walkthrough-of-bmp-image-format-765dc6857393) for more
   information.
   
For more information on exact steps see the [implementation](../../../tonguetwister/chunks/bitmap_data.py).
