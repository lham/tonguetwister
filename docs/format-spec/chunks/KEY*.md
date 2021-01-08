# Resource Key Table

The resource key table is an array, each entry representing a parent-child [belongs-to relationship](#TODO)
for [resources](../readme.md#resource-relationships) within the file. Each entry has a primary key consisting of the
resource id of the parent and the [FourCC](#TODO) of the child. The other entry data is simply the resource id of the
child.

This means that there can be multiple child resources to each parent resource, but only a single child resource of each
chunk type.

``The [FourCC](#TODO) of the chunk is `KEY*`.

## Structure

The resource key table chunk is saved in **little-endian**.

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

## Array data

The array entries are simply stacked one after another. While `AAE` array elements are allocated, only `UAE` array
elements actually contains real entries, so we must not parse more than `UAE` entries.

### Array entries

The structure of a resource key table array entry is:

Ref.   | Bytes | Type(s) | Name                           | Description
---    | ---:  | ---     | ---                            | ---
`CHA`  | 4     | uint32  | child&#8209;resource&#8209;id  | The resource id of the child resource.
`CHA`  | 4     | uint32  | parent&#8209;resource&#8209;id | The resource id of the parent resource.
`FCC`  | 4     | char    | four&#8209;cc                  | The [FourCC](#TODO) identifying the of the child resource.
