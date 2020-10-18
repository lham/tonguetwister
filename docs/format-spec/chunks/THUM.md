# Thumbnail (THUM)
A thumbnail can belong to a [bitmap cast member](./castmembers/bitmap.md) and is a downscaled version of the image used
in the [cast](#TODO) windows and property explorer in Director. A thumbnail for a bitmap seems to be created once the
size of the bitmap is larger than 2500 pixels.

The chunk abbreviation is `THUM`.


## Structure
The thumbnail chunk is saved in **big-endian**.

The structure is described by:

Ref.   | Bytes | Type   | Description
---    | ---:  | ---    | ---
`HL`   | 4     | uint32 | Header length
&nbsp; | `HL`  | &nbsp; | [Chunk header](#chunk-header)
`DL`   | 4     | uint32 | Image data length
&nbsp; | `DL`  | &nbsp; | Raw [image data](#unpacking-the-image-data) for the thumbnail.


## Chunk header
The structure of the thumbnail header is:

Ref.   | Bytes | Type   | Name    | Description
---    | ---:  | ---    | ---     | ---
&nbsp; | 2     | int16  | top     | y-value of the top of the [image bounding box rectangle](#TODO).
&nbsp; | 2     | int16  | left    | x-value of the left side of the [image bounding box rectangle](#TODO).
&nbsp; | 2     | int16  | bottom  | y-value of the bottom side of the [image bounding box rectangle](#TODO).
&nbsp; | 2     | int16  | right   | x-value of the right side of the [image bounding box rectangle](#TODO).

We can construct the width `W` as `right - left` and the height `H` as `bottom - top`.


## Unpacking the image data
The image data in a thumbnail is basically just the same data as in a [bitmap data chunk](./BITD.md). We can parse it
exactly the same as a [bitmap cast member](./castmembers/bitmap.md) if we set

* `bit-depth` = 8
* `palette` = [predefined palette "System - Mac"](./castmembers/palette.md#TODO)
* `bytes-per-image-row` = `W` (add 1 if `W` is odd, so that every row is an even number of bytes)

and use the width `W` and height `H` given by the header data.
