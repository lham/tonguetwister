# Sort order

The sort order chunk container a quick reference for Director to look up different cast members. In many places the cast
members are referenced by a number, called a **cast member reference id**. Each entry in this chunk represent such a
cast member reference, when the entry's index is the cast member reference id.

Each entry consists of a cast number `CN` (1-indexed), referencing a [cast](#TODO) defined inside
the [cast assoc table](./CAS*.md) (0-indexed). It also contains a cast member slot number, referencing in which slot
number the cast member is located. To use this cast member number, it needs to be used by the first needs to be offset
by the first occupied slot `FOS` inside the [cast assoc table](./CAS*.md) referenced by the cast number `CN`.

The [FourCC](#TODO) of the chunk is `Sord`.

## Structure

The sort order chunk is saved in **big-endian**.

The structure is described by:

Ref.   | Bytes              | Description
---    | ---:               | ---
&nbsp; | `HL`               | [Chunk header](#chunk-header)
&nbsp; | `EL` &times; `AAE` | [Array data](#array-data)

## Chunk header

The structure of the chunk header is:

Ref.   | Bytes | Type(s) | Name                                 | Description
---    | ---:  | ---     | ---                                  | ---
&nbsp; | 4     | uint32  | &nbsp;                               | Unknown.
&nbsp; | 4     | uint32  | &nbsp;                               | Unknown.
`AAE`  | 4     | uint32  | allocated&#8209;array&#8209;elements | The number of allocated array slots.
`UAE`  | 4     | uint32  | used&#8209;array&#8209;elements      | The number of array slots filled by entries.
`HL`   | 2     | uint16  | header&#8209;length                  | Length of the header data.
`EL`   | 2     | uint16  | entry&#8209;length                   | The length of a single [entry](#array-entries).

## Array data

The array entries are simply stacked one after another. While `AAE` array elements are allocated, only `UAE` array
elements actually contains real entries, so we must not parse more than `UAE` entries. However, it looks like this
particular table is always kept up to date so that `AAE` = `UAE`.

### Array entries

The structure of a sort order array entry is:

Ref.   | Bytes | Type(s) | Name                                      | Description
---    | ---:  | ---     | ---                                       | ---
`CN`   | 2     | uint16  | cast&#8209;number                         | The number of the [cast](#TODO).
&nbsp; | 2     | uint16  | cast&#8209;member&#8209;slot&#8209;number | The number of the slot inside the cast `CN` where the referenced cast member is located.
