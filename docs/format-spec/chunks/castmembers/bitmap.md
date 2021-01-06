# Bitmap cast member

A bitmap [cast member](../CASt.md) can either be an externally linked bitmap, a linked bitmap with the data duplicated
inside or an entirely internal bitmap. The bitmaps can have color depths of 2, 4, 8, 16 or 32-bit. However, it seems
like the alpha value in Director 6 is ignored, so the 32-bit images are in fact 24-bit. For 8-bit and lower the colors
are defined by a [palette](#TODO) rather than being inlined.

## Structure

The cast member itself contains only image metadata, consisting of `TSDL` bytes (see [cast member](../CASt.md)). The
actual image data is either externally located in an image file, or located in on of the following chunks:

- [Bitmap data](../BITD.md)
- [Editable media](../ediM.md)

## Type specific data

Ref.   | Bytes | Type   | Name                                          | Description
---    | ---:  | ---    | ---                                           | ---
`BPR`  | 2     | uint16 | bytes&#8209;per&#8209;image&#8209;row         | The number of bytes per row of the image. For a 32-bit image this would be the image width * 4 (alpha, red, green, blue). This value needs to be masked with `0x7fff` for some reason?
&nbsp; | 2     | int16  | top                                           | y-value of the top of the [**image bounding box rectangle**](#TODO).
&nbsp; | 2     | int16  | left                                          | x-value of the left side of the [**image bounding box rectangle**](#TODO).
&nbsp; | 2     | int16  | bottom                                        | y-value of the bottom side of the [**image bounding box rectangle**](#TODO).
&nbsp; | 2     | int16  | right                                         | x-value of the right side of the [**image bounding box rectangle**](#TODO).
&nbsp; | 1     | uint8  | &nbsp;                                        | Unknown. *global image alpha?*
&nbsp; | 1     | uint8  | &nbsp;                                        | Unknown. *global image alpha?*
&nbsp; | 2     | uint16 | ?number&#8209;of&#8209;image&#8209;operations | Probably the number of operations / edits that have been made to the image? Haven't been able to do a 1-to-1 mapping for this. Not affecting the rendering of the image.
&nbsp; | 2     | int16  | paint&#8209;window&#8209;offset&#8209;y       | y-offset inside the paint window of Director. Not affecting the rendering of the image.
&nbsp; | 2     | int16  | paint&#8209;window&#8209;offset&#8209;x       | x-offset inside the paint window of Director. Not affecting the rendering of the image.
&nbsp; | 2     | int16  | registration&#8209;point&#8209;y              | y-value of the [**image registration point**](#TODO).
&nbsp; | 2     | int16  | registration&#8209;point&#8209;x              | x-value of the [**image registration point**](#TODO).
&nbsp; | 1     | uint8  | ?import&#8209;options                         | Bit-flag field for [**import options**](#TODO)? If so, `0x08`: dither image. Not affecting the rendering of the image.
&nbsp; | 1     | uint8  | bit&#8209;depth                               | **Bit depth** (color depth) of the image.
&nbsp; | 2     | int16  | ?use&#8209;cast&#8209;palette                 | Probably whether or not to use a [predefined palette](./palette.md#TODO) or a [palette cast member](./palette.md). `-1` if predefined, `0` otherwise.
`P`    | 2     | int16  | palette                                       | A [predefined palette](./palette.md#TODO) if less than zero, otherwise it refers to a [palette cast member](./palette.md).

We can construct the width `W` as `right - left` and the height `H` as `bottom - top`.
