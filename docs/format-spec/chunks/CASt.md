# Cast member (CASt)

The cast members are the basic building blocks of a Director [movie](../readme.md#director-overview). Each cast member
has a type which in turn gives it specific properties. All types are listed [below](#cast-member-types).

The chunk abbreviation is `CASt`.

## Structure

The cast member chunk is saved in **big-endian**.

The structure is described by:

Ref.   | Bytes  | Description
---    | ---:   | ---
&nbsp; | 12     | [Chunk header](#chunk-header)
&nbsp; | `CDL`  | [Common data](#common-data)
&nbsp; | `TSDL` | [Type specific data](#type-specific-data)

## Chunk header

The structure of chunk header is:

Ref.   | Bytes | Type   | Name                                        | Description
---    | ---:  | ---    | ---                                         | ---
`T`    | 4     | uint32 | cast&#8209;member&#8209;type                | The [type](#cast-member-types) of this cast member.
`CDL`  | 4     | uint32 | common&#8209;data&#8209;length              | Length of the [common data](#common-data).
`TSDL` | 4     | uint32 | type&#8209;specific&#8209;data&#8209;length | Length of the [type specific data](#type-specific-data).

## Common data

The common data consists of `CDL` bytes. The structure is:

Ref.   | Bytes                                     | Type(s)  | Name                                                      | Description
---    | ---:                                      | ---      | ---                                                       | ---
`RL`   | 4                                         | uint32   | reserved&#8209;length                                     | The length of the **reserved block** (including self).
&nbsp; | (`RL`&nbsp;-&nbsp;1)&nbsp;&times;&nbsp;4  | uint32   | &nbsp;                                                    | **Reserved block**. Unknown purpose.
`NPD`  | 2                                         | uint16   | number&#8209;of&#8209;data&#8209;properties&#8209;defined | The number of **data properties** defined for this chunk.
`PL`   | (`NDP`&nbsp;+&nbsp;1)&nbsp;&times;&nbsp;4 | uint32   | data&#8209;property&#8209;lengths                         | Array of **data property** lengths (the raw uint32 values are offsets, see explanation below).
&nbsp; | &Sigma;(`PL`)                             | *varies* | data&#8209;properties                                     | Array of **data properties**.

This is a bit tricky to parse. First you need to know that each common **data property** has a fixed index. The
properties with their indices and types are given by the following table:

Index | Type               | Name                         | Description
---:  | ---                | ---                          | ---
0     | &nbsp;             | &nbsp;                       | Unknown.
1     | string<sup>1</sup> | cast&#8209;member&#8209;name | Name of the cast member.
2     | string<sup>1</sup> | external&#8209;path          | The relative path/directory of an [imported](#TODO) cast member.
3     | string<sup>1</sup> | external&#8209;filename      | The filename (excluding extension) of an [imported](#TODO) cast member.
4     | &nbsp;             | &nbsp;                       | Unknown.
5     | &nbsp;             | &nbsp;                       | Unknown.
6     | &nbsp;             | &nbsp;                       | Unknown.
7     | &nbsp;             | &nbsp;                       | Unknown.
8     | &nbsp;             | &nbsp;                       | Unknown.
9     | &nbsp;             | &nbsp;                       | Unknown.
10    | &nbsp;             | &nbsp;                       | Unknown.
11    | &nbsp;             | &nbsp;                       | Unknown.
12    | &nbsp;             | &nbsp;                       | Unknown.
13    | &nbsp;             | &nbsp;                       | Unknown.
14    | &nbsp;             | &nbsp;                       | Unknown.
15    | &nbsp;             | &nbsp;                       | Unknown.
16    | string<sup>1</sup> | file&#8209;format&#8209;name | The [format](#TODO) name an [imported](#TODO) cast member.

<sup>1</sup> A string here consists of an uint8 length `L`, followed by `L` characters and a terminating `NULL` byte.

A cast member does not need to define all of these properties, but since the properties are always ordered/indexed in
the same way, all "undefined" properties before the property with the highest index will also need to be defined. They
will simply be defined as zero-length entries.

Now we know that we have `NDP` properties that can be parsed. The lengths can be gleaned from the offset values from the
`NDP` byte. So first we read `NDP + 1` values into an array `a`, where each value is an offset. The array of data
property lengths `PL` are then defined as `PL[i] = a[i + 1] - a[i]`.

Finally each data property can be read using the lengths `PL`. They are just stacked one after another.

The parsing can probably be done differently/more efficiently as this seems like a convoluted way of saving the data.

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
