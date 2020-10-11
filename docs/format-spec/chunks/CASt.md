# Cast member (CASt)
The cast members are the basic building blocks of a Director [movie](#TODO). Each cast member has a type which in turn gives
it specific properties. All types are listed [below](#cast-member-types).

The chunk abbreviation is `CASt`.


## Structure
The cast member chunk is saved in **big-endian**.

The structure is described by:

Ref.   | Length       | Description
---    | ---:         | ---
&nbsp; | 12 bytes     | [Chunk header](#chunk-header)
&nbsp; | `CDL` bytes  | [Common data](#common-data)
&nbsp; | `TSDL` bytes | [Type specific data](#type-specific-data)


## Chunk header
The structure of the cast member chunk header is:

Ref.   | Length  | Type   | Name                        | Description
---    | ---:    | ---    | ---                         | ---
`T`    | 4 bytes | uint32 | `cast-member-type`          | [Cast member type](#cast-member-types).
`CDL`  | 4 bytes | uint32 | `common-data-length`        | Length of the [common data](#common-data).
`TSDL` | 4 bytes | uint32 | `type-specific-data-length` | Length of the [type specific data](#type-specific-data).


## Common data
The common data consists of `CDL` bytes. The structure is defined as follows:

Ref.   | Length                | Type(s)  | Name                                | Description
---    | ---:                  | ---      | ---                                 | ---
`RL`   | `4` bytes             | uint32   | `reserved-length`                   | The length of the **reserved block** (including self).
&nbsp; | `(RL - 1) * 4` bytes  | uint32   | &nbsp;                              | **Reserved block**. Unknown purpose.
`NPD`  | `2` bytes             | uint16   | `number-of-data-properties-defined` | The number of **data properties** defined for this chunk.
`PL`   | `(NDP + 1) * 4` bytes | uint32   | `data-property-lengths`             | Array of data property lengths.
&nbsp; | `sum(PL)` bytes       | *varies* | `data-properties`                   | Array of data properties.

This is a bit tricky to parse. First you need to know that each common data property has a fixed index. The properties
with their indices and types are given by the following table:

Index | Type               | Name                      | Description
---:  | ---                | ---                       | ---
0     | Unknown            | &nbsp;                    | &nbsp;
1     | string<sup>1</sup> | `cast-member-name`        | Name of the cast member.
2     | string<sup>1</sup> | `external-path`           | The relative path/directory of an imported cast member.
3     | string<sup>1</sup> | `external-filename`       | The filename (excluding extension) of an imported cast member.
4     | Unknown            | &nbsp;                    | &nbsp;
5     | Unknown            | &nbsp;                    | &nbsp;
6     | Unknown            | &nbsp;                    | &nbsp;
7     | Unknown            | &nbsp;                    | &nbsp;
8     | Unknown            | &nbsp;                    | &nbsp;
9     | Unknown            | &nbsp;                    | &nbsp;
10    | Unknown            | &nbsp;                    | &nbsp;
11    | Unknown            | &nbsp;                    | &nbsp;
12    | Unknown            | &nbsp;                    | &nbsp;
13    | Unknown            | &nbsp;                    | &nbsp;
14    | Unknown            | &nbsp;                    | &nbsp;
15    | Unknown            | &nbsp;                    | &nbsp;
16    | string<sup>1</sup> | `external-file-extension` | The file extension of an imported cast member.

<sup>1</sup> A string here consists of an uint8 length `L`, followed by `L` characters and a terminating `NULL` byte.

A cast member does not need to define all of these properties, but since the properties are always ordered/indexed in
the same way, all "undefined" properties before the property with the highest index will also need to be defined. They
will simply be defined as zero-length entries.

Now we know that we have `NDP` properties that can be parsed. The lengths can be gleaned from the offset values from the
`NDP` byte. So first we read `NDP + 1` values into an array `a`, where each value is an offset. The array of data
property lengths `PL` are then defined as `PL[i] = a[i + 1] - a[i]`.

Finally each data property can be read using the lengths `PL`. They are just stacked one after another.

The parsing can probably be done differently / more efficiently as this seems like a convoluted way of saving the data.


## Type specific data
The type specific data consists of `TSDL` bytes. The layout and data depends on the cast member type `T`. See each type
under the section [Cast member types](#cast-member-types) below for specifics on each cast member type.


## Cast member types
The predefined cast member types in Director are listed below, indexed by their cast member type `T`:

Type `T` | Type name
---:     | ---
0        | Unknown
1        | [Bitmap](./castmembers/bitmap.md)
2        | Unknown
3        | [Field](./castmembers/field.md)
4        | Unknown
5        | Unknown
6        | Unknown
7        | Unknown
8        | [Shape](./castmembers/shape.md)
9        | Unknown
10       | Unknown
11       | [Script](./castmembers/script.md)
12       | Unknown
13       | Unknown
14       | Unknown
15       | Unknown
16       | Unknown
17       | Unknown
18       | Unknown
