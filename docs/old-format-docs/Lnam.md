# Lingo namelist
The [L]ingo [nam]elist is saved in `big-endian`.

The structure is described by:

Ref.   | Length                   | Description
---    | ---:                     | ---
&nbsp; | `HL` bytes               | [Chunk header](#markdown-header-chunk-header)
&nbsp; | `NN` \* (4 + `NL`) bytes | [Name records](#markdown-header-name-records)

## Chunk header
The structure of the [chunk header](#markdown-header-chunk-header) is:

Ref.   | Length  | Type   | Name              | Description                                                  | Example
---    | ---:    | ---    | ---               | ---                                                          | ---
&nbsp; | 4 bytes | uint32 |                   | Unknown.                                                     | 0
&nbsp; | 4 bytes | uint32 |                   | Unknown.                                                     | 0
&nbsp; | 4 bytes | uint32 | `chunk-length`    | Total length of the chunk                                    | 61
&nbsp; | 4 bytes | uint32 | `chunk-length-2`  | Duplicate of above.                                          | 61
`HL`   | 2 bytes | uint16 | `header-length`   | Length of the [chunk header](#markdown-header-chunk-header). | 20
`NN`   | 2 bytes | uint16 | `number-of-names` | The number of [name records](#markdown-header-name-records). | 6

## Name records
The [name records](#markdown-header-name-records) consists of `NN` records, one for each [name](#markdown-header-name-records). The structure of a single [name](#markdown-header-name-records) is:

Ref.   | Length     | Type  | Name          | Description                                              | Example
---    | ---:       | ---   | ---           | ---                                                      | ---
`NL`   | 1 byte     | uint8 | `name-length` | The length of a [name](#markdown-header-name-records).   |
&nbsp; | `NL` bytes | uint8 | `name`        | The content of the [name](#markdown-header-name-records) |



