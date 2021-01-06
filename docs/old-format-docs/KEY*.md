# KEY* chunk
The [KEY*] chunk is saved in `little-endian`.

The structure is described by:

Ref.   | Length             | Description
---    | ---:               | ---
&nbsp; | `HL` bytes         | [Chunk header](#markdown-header-chunk-header)
&nbsp; | `NK` \* `KL` bytes | [Key records](#markdown-header-name-records)


## Chunk header
The structure of the [chunk header](#markdown-header-chunk-header) is:

Ref.   | Length  | Type   | Name                       | Description                                                                                                     | Example
---    | ---:    | ---    | ---                        | ---                                                                                                             | ---
`HL`   | 2 bytes | uint16 | `header-length`            | Length of the [chunk header](#markdown-header-chunk-header).                                                    | 12
`KL`   | 2 bytes | uint16 | `key-length`               | Length of a **key** in the [key records](#markdown-header-key-records).                                         | 12
`NK`   | 4 bytes | uint32 | `number-of-keys`           | Number of **keys** in the [key records](#markdown-header-key-records).                                          | 67
&nbsp; | 4 bytes | uint32 | `number-of-used-key-slots` | Number of used **keys** in the [key records](#markdown-header-key-records) used in the [memory map](./mmap.md). | 23


## Key records
The [key records](#markdown-header-key-records) consists of `NK` records, one for each **key**. The structure of a single **key** is:

Ref.   | Length  | Type   | Name              | Description                                                                                   | Example
---    | ---:    | ---    | ---               | ---                                                                                           | ---
&nbsp; | 4 bytes | uint32 | `mmap-index`      | The index of the **key** in the [memory map](./mmap.md)                                       | 26
&nbsp; | 4 bytes | uint32 | `cast-mmap-index` | The index of the corresponding **cast member** to the **key** in the [memory map](./mmap.md). | 6
&nbsp; | 4 bytes | uint32 | `four-cc`         | The **member type** of the **cast member** of the **key**.                                    | STXT


