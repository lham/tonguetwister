# Memory Map

The memory map is basically an array containing metadata and the location of all
the [chunk resources](../readme.md#resources) in the Director file. The file format basically a memory dump, so the
memory map chunk serves as a lookup table for all the resources in the memory dump.

The array entry index represent the resource id of the chunk resource.

The [FourCC](#TODO) of the chunk is `mmap`.

## Structure

The memory map chunk is saved in **little-endian**.

The structure is described by:

Ref.   | Bytes              | Description
---    | ---:               | ---
&nbsp; | `HL`               | [Chunk header](#chunk-header)
&nbsp; | `DL` &times; `AAE` | [Array data](#array-data)

## Chunk header

The structure of the chunk header is:

Ref.   | Bytes | Type(s) | Name                                 | Description
---    | ---:  | ---     | ---                                  | ---
`HL`   | 2     | uint16  | header&#8209;length                  | Length of the header data.
`DL`   | 2     | uint16  | entry&#8209;length                   | The length of a single [entry](#array-entries).
`AAE`  | 4     | uint32  | allocated&#8209;array&#8209;elements | The number of allocated array slots.
`UAE`  | 4     | uint32  | used&#8209;array&#8209;elements      | The number of array slots filled by entries.
&nbsp; | 4     | int32   | ?junk&#8209;entry&#8209;position     | Probably something related to `junk` entries (position always seems to be pointing to a `junk` entry). Defaults to `-1`.
&nbsp; | 4     | &nbsp;  | &nbsp;                               | Unknown.
&nbsp; | 4     | uint32  | ?free&#8209;entry&#8209;position     | Probably something related to `free` entries (position always seems to be pointing to a `free` entry).

## Array data

The array entries are simply stacked one after another. While `AAE` array elements are allocated, only `UAE` array
elements actually contains real entries, so we must not parse more than `UAE` entries.

Each array entry represents a resource pointing to a chunk saved in the file.

### Array entries

The structure of a memory map array entry is:

Ref.   | Bytes | Type(s) | Name                | Description
---    | ---:  | ---     | ---                 | ---
`FCC`  | 4     | char    | four&#8209;cc       | The [FourCC](#TODO) identifying the chunk.
`CHL`  | 2     | uint16  | chunk&#8209;address | The address (from the beginning of the file) of the chunk.
`CHA`  | 4     | uint32  | chunk&#8209;length  | The length of the chunk.
&nbsp; | 8     | &nbsp;  | &nbsp;              | Unknown.

### Special FourCC's

There are two FourCCs that should not be parsed, namely

1. `free`
2. `junk`

The theory as to why this happens is the following.

When Director deletes a resource the pointer in the lookup table is simply unset, and the resource it pointed to may or
may not reside in the memory dump. This means that for (non-optimized) Director files some entries in the memory map
will be missing. Such unused memory map entries are represented by the FourCC's `free` and `junk`.

This will also be the case when Director replaces or updates the memory map for some reason (i.e. the memory map gets
too long), then entries will be shuffled around, generating more such "empty" entries. Note that this is also the reason
why the [initial map](./imap.md) exists, so that we can keep track of where the current memory map is located.

The reason to why you should not parse them at all is that their metadata (chunk address and chunk data length) might be
incorrect, and you will probably get errors if trying to read them. The `free` entries will have them both set to zero,
while the `junk` entries will not.

