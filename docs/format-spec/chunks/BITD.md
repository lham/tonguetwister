# Bitmap data (BITD)
This is a [resource chunk](#TODO). It contains image data for a [bitmap cast member](./castmembers/bitmap.md). The data
can not be rendered without data from its bitmap cast member chunk.

The chunk abbreviation is `BITD`.


## Structure
The bitmap data chunk contains raw image data. It's usually run length encoded.


## Decoding bitmap data
The decoding process depends on the bit depth of the bitmap.


### 8-bit
It's easiest to describe the 8-bit decoding first. 8-bit bitmaps use a palette to defined it's colors. This means that
each byte (8 bits) represents in the image data represents an index inside a palette. Thus we can have 256 different
RGB colors inside a single image.

The data is encoded using run length encoding, (probably) using the [PackBits](https://en.wikipedia.org/wiki/PackBits)
algorithm. It basically goes like this:

    while data.notEmpty():
        header_byte = data.pop(uint8)

        if header_byte < 0x80:
            length = header_byte + 1
            indices = [data.pop(uint8) for i in 0..length]
        else:
            length = twos_complement(header_byte) + 1
            index = data.pop(uint8)
            indices = [index for i in 0..length]

        image_data.extend([palette[i] for i in indices])

Now we got all the image data in a long list and can use the image width and height to reshape the data into a 2D image.
Note that bitmaps are saved in reversed row-order. So `n` color constituting the first image row pixel data is actually
bottom row of the image. To solve this we simply swap the order of the pixel rows. See this
[link](https://medium.com/sysf/bits-to-bitmaps-a-simple-walkthrough-of-bmp-image-format-765dc6857393) for more
information.


### 32-bit
For 32-bit bitmaps we extend the 8-bit model. Now we don't use a palette anymore and the aRGB values are encoded
directly into the data stream. To decode this we need the image width and height before we start algorithm.

First, do a simple check to see if the data is run length encoded in the first place. If the image is small enough the
image data is not encoded, and the aRGB data is simply laid out byte-by-byte. So if the size of the data is
`width * height * 4` (4 channels: alpha, red, green, blue), then it's not encoded.

If the data is in fact encoded we decode it row by row. Initialize a row by using the image width. Then fill up each
color channel (in the order: a, r, g, b) until the row is "filled". Iterate for until the data stream is empty / all
rows are complete. Pseudo-code gives us:

    row = ImageRow(width)

    while data.notEmpty():
        header_byte = data.pop(uint8)

        if header_byte < 0x80:
            length = header_byte + 1
            bytes = [data.pop(uint8) for i in 0..length]
        else:
            length = twos_complement(header_byte) + 1
            byte = data.pop(uint8)
            bytes = [byte for i in 0..length]

        row.push_bytes_in_first_available_channel(bytes)

        if row.all_channels_filled():
            image_data.append(row)
            row.reset()

Note that for Director 6 the alpha channel doesn't seem to be used, so we might need to replace the alpha value with
ones depending on how we choose to render our image.

Again the bitmap is saved in reversed row-order. See [decoding 8-bit](#8-bit).
