# Bitmap cast member
A bitmap [cast member](../CASt.md) can either be an externally linked bitmap, a linked bitmap with the data duplicated
inside or an entirely internal bitmap. The bitmaps can have color depths of 2, 4, 8, 16 or 32-bit. However it seems like
the alpha value in Director 6 is ignored, so the 32-bit images are in fact 24-bit. For 8-bit or lower the colors are
defined by a [palette](#TODO) rather than being inlined.


## Structure
The bitmap cast member chunk is saved in **big-endian**.

The cast member itself contains only header data, consisting of `TSDL` bytes (see [cast member](../CASt.md)). The actual
image data is either externally located in an image file, or located in on of the following resource chunks:

* [Bitmap data](../BITD.md)
* [Editable media](../ediM.md)


## Type specific data
Ref.   | Length  | Type   | Name                          | Description
---    | ---:    | ---    | ---                           | ---
&nbsp; | 2 bytes | uint16 | `bytes-per-image-row`         | The number of bytes per row of the image. For a 32-bit image this would be the image width * 4 (alpha, red, green, blue). This value needs to be masked with `0x7fff` for some reason?
&nbsp; | 2 bytes | int16  | `top`                         | y-value of the top of the [image bounding box rectangle](#TODO).
&nbsp; | 2 bytes | int16  | `left`                        | x-value of the left side of the [image bounding box rectangle](#TODO).
&nbsp; | 2 bytes | int16  | `bottom`                      | y-value of the bottom side of the [image bounding box rectangle](#TODO).
&nbsp; | 2 bytes | int16  | `right`                       | x-value of the right side of the [image bounding box rectangle](#TODO).
&nbsp; | 1 bytes | uint8  | &nbsp;                        | Unknown. *global image alpha?*
&nbsp; | 1 bytes | uint8  | &nbsp;                        | Unknown. *global image alpha?*
&nbsp; | 2 bytes | uint16 | `?number-of-image-operations` | Probably the number of operations / edits that have been made to the image? Haven't been able to do a 1-to-1 mapping for this. Not affecting the rendering of the image.
&nbsp; | 2 bytes | int16  | `paint-window-offset-y`       | y-offset inside the paint window of Director. Not affecting the rendering of the image.
&nbsp; | 2 bytes | int16  | `paint-window-offset-x`       | x-offset inside the paint window of Director. Not affecting the rendering of the image.
&nbsp; | 2 bytes | int16  | `registration-point-y`        | y-value of the [image registration point](#TODO).
&nbsp; | 2 bytes | int16  | `registration-point-x`        | x-value of the [image registration point](#TODO).
&nbsp; | 1 bytes | uint8  | `?import-options`             | Bit-flag field for import options? If so, `0x08`: dither image. Not affecting the rendering of the image.
&nbsp; | 1 bytes | uint8  | `bit-depth`                   | Bit depth (color depth) of the image.
&nbsp; | 2 bytes | int16  | `?use_cast_palette`           | Probably whether or not to use a predefined palette or a palette cast member. `-1` if predefined, `0` otherwise.
&nbsp; | 2 bytes | int16  | `palette`                     | A [predefined palette](./palette.md#TODO) if less than zero, otherwise it refers to a [palette cast member](./palette.md).
