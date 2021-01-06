# Lingo script (Lscr)
The [L]ingo [scr]ipt chunk is saved in `big-endian`. 

Somewhere in here the bodies of the [globals](#markdown-header-global-bodies) and the [properties](#markdown-header-property-bodies) should be found, where is yet unknown.

The structure is described by:

Ref.   | Length                                        | Description
---    | ---:                                          | ---
`H`    | `HL` bytes                                    | [Chunk header](#markdown-header-chunk-header)
&nbsp; | (`FL` + `NFA` + 2\*`NFL`+ `NX`) \* `NF` bytes | [Function bodies](#markdown-header-function-bodies)
&nbsp; | ?                                             | [Property headers](#markdown-header-property-headers)
&nbsp; | ?                                             | [Global headers](#markdown-header-global-headers)
&nbsp; | 42\*`NF` bytes                                | [Function headers](#markdown-header-function-headers)
&nbsp; | 8\*`NL` bytes                                 | [Literal headers](#markdown-header-literal-headers)
`LB`   | `LBL` bytes                                   | [Literal bodies](#markdown-header-literal-bodies)



## Chunk header
The structure of the [chunk header](#markdown-header-chunk-header) is:

Ref.   | Length   | Type   | Name                      | Description                                                                           | Example
---    | ---:     | ---    | ---                       | ---                                                                                   | ---
&nbsp; | 4 bytes  | uint32 |                           | Unknown.                                                                              | 0x006D 0x8ED8
&nbsp; | 4 bytes  | uint32 |                           | Unknown.                                                                              | 1
&nbsp; | 4 bytes  | uint32 | `length-of-chunk`         | Length of the entire chunk.                                                           | 324
&nbsp; | 4 bytes  | uint32 | `length-of-chunk-2`       | Duplicate of above.                                                                   | 324
`HL`   | 2 bytes  | uint16 | `header-length`           | Length of the [chunk header](#markdown-header-chunk-header).                          | 92
&nbsp; | 4 bytes  | uint32 |                           | Unknown. Script number?                                                               | 6
&nbsp; | 4 bytes  | uint32 |                           | Unknown.                                                                              | 0xFFFF 0xFFFF
&nbsp; | 12 bytes | ?      |                           | Unknown.                                                                              | 0x0000
&nbsp; | 4 bytes  | uint32 |                           | Unknown.                                                                              | 2
&nbsp; | 4 bytes  | uint32 |                           | Unknown.                                                                              | 3
&nbsp; | 2 bytes  | uint16 |                           | Unknown.                                                                              | 17
&nbsp; | 2 bytes  | uint16 |                           | Unknown.                                                                              | 0xFFFF
&nbsp; | 2 bytes  | uint16 |                           | Unknown. `handler-length`?                                                            | 0
&nbsp; | 4 bytes  | uint32 |                           | Unknown. `handler-offset`?                                                            | 0
&nbsp; | 4 bytes  | uint32 |                           | Unknown. Bitmask for `handler-flags`?                                                 | 0
`NP`   | 2 bytes  | uint16 | `number-of-properties`    | Number of [properties](#markdown-header-property-bodies).                             | 0
`PHO`  | 4 bytes  | uint32 | `property-headers-offset` | Offset to the [property headers](#markdown-header-property-headers), relative to `H`. | 178
`NG`   | 2 bytes  | uint16 | `number-of-globals`       | Number of [globals](#markdown-header-global-bodies).                                  | 0
`GHO`  | 4 bytes  | uint32 | `global-headers-offset`   | Offset to the [global headers](#markdown-header-global-headers), relative to `H`.     | 178
`NF`   | 2 bytes  | uint16 | `number-of-functions`     | Number of [functions](#markdown-header-function-bodies).                              | 1
`FHO`  | 4 bytes  | uint32 | `function-headers-offset` | Offset to the [function headers](#markdown-header-function-headers), relative to `H`. | 178
`NL`   | 2 bytes  | uint16 | `number-of-literals`      | Number of [literals](#markdown-header-literal-bodies).                                | 5
`LHO`  | 4 bytes  | uint32 | `literal-headers-offset`  | Offset to the [literal headers](#markdown-header-literal-headers), relative to `H`    | 220
`LBL`  | 4 bytes  | uint32 | `literals-length`         | Length of all the [literal bodies](#markdown-header-literal-bodies) combined.         | 64
`LBO`  | 4 bytes  | uint32 | `literals-offset`         | Offset to the [literal bodies](#markdown-header-literal-bodies), relative to `H`      | 260



## Function bodies
There are most likely missing parts in here as some headers are unknown.

The [function bodies](#markdown-header-function-bodies) consists of `NF` bodies, one for each [function](#markdown-header-function-bodies)  The structure of a single [function](#markdown-header-function-bodies) is:

Ref.   | Length         | Type   | Name        | Description                                                                                             | Example
---    | ---:           | ---    | ---         | ---                                                                                                     | ---
&nbsp; | `FL` bytes     | uint8  | `bytecode`  | Lingo byte-code instructions for the [function](#markdown-header-function-bodies)                       |
&nbsp; | `NFA` bytes    | uint8  | `arguments` | _Arguments_ to the [function](#markdown-header-function-bodies)  Exact size unknown. Likely byte-sized. |
&nbsp; | 2\*`NFL` bytes | uint16 | `locals`    | The _locals_ in the [function](#markdown-header-function-bodies)                                        |
&nbsp; | `NX` bytes     | uint8  |             | Unknown.                                                                                                |

## Property bodies
Unknown.

## Global bodies
Unknown.

## Property headers
Unknown.

## Global headers
Unknown.

## Function headers
The [function headers](#markdown-header-function-headers) consists of `NF` headers, one for each [function](#markdown-header-function-bodies)  The structure of a single [function header](#markdown-header-function-headers) is:

Ref.   | Length  | Type   | Name                  | Description                                                                                     | Example
---    | ---:    | ---    | ---                   | ---                                                                                             | ---
&nbsp; | 2 bytes | uint16 |                       | Unknown. Function-id?                                                                           | 0
&nbsp; | 2 bytes | uint16 |                       | Unknown. Handler?                                                                               | 0xFFFF
`FL`   | 4 bytes | uint32 | `function-length`     | Length the [function](#markdown-header-function-bodies)                                         | 76
`FO`   | 4 bytes | uint32 | `function-offset`     | Offset of the [function](#markdown-header-function-bodies)  relative to `H`.                    | 92
`NFA`  | 2 bytes | uint16 | `number-of-arguments` | Number of _arguments_ to the [function](#markdown-header-function-bodies)                       | 0
`FAO`  | 4 bytes | uint32 | `arguments-offset`    | Offset to the _arguments_ to the [function](#markdown-header-function-bodies)  relative to `H`. | 168
`NFL`  | 2 bytes | uint16 | `number-of-locals`    | Number of _locals_ in the [function](#markdown-header-function-bodies)                          | 1
`FLO`  | 4 bytes | uint32 | `locals-offset`       | Offset to the _locals_, relative to `H`.                                                        | 168
&nbsp; | 2 bytes | uint16 |                       | Unknown. `number-of-x`?                                                                         | 0
&nbsp; | 4 bytes | uint32 |                       | Unknown. `x-offset`, relative to `H`.                                                           | 170
&nbsp; | 2 bytes | uint16 |                       | Unknown.                                                                                        | 0
&nbsp; | 2 bytes | uint16 |                       | Unknown.                                                                                        | 11
&nbsp; | 2 bytes | uint16 |                       | Unknown.                                                                                        | 2
`NX`   | 2 bytes | uint16 |                       | Unknown. `line-count`?                                                                          | 8
`NXO`  | 4 bytes | uint32 |                       | Unknown. `line-count-offset`?, relative to `H`                                                  | 170



## Literal headers
The [literal headers](#markdown-header-literal-headers) consists of `NL` headers, one for each [literal](#markdown-header-literal-bodies)  The structure of a signle [literal header](#markdown-header-literal-headers) is:

Ref.   | Length  | Type   | Name             | Description                                                                 | Example
---    | ---:    | ---    | ---              | ---                                                                         | ---
&nbsp; | 4 bytes | uint32 | `literal-type`   | Type of the [literal](#markdown-header-literal-bodies)  0x01 = string?      | 1
&nbsp; | 4 bytes | uint32 | `literal-offset` | Offset to the [literal](#markdown-header-literal-bodies)  relative to `LB`. | 22


## Literal bodies
The [literal bodies](#markdown-header-literal-bodies) consists of `NL` bodies, one for each [literal](#markdown-header-literal-bodies)  A [literal](#markdown-header-literal-bodies) is 2-byte aligned. 

The structure of a single [literal](#markdown-header-literal-bodies) is:

Ref.   | Length         | Type   | Name             | Description                                                   | Example
---    | ---:           | ---    | ---              | ---                                                           | ---
`LL`   | 4 bytes        | uint32 | `literal-length` | Length of the [literal](#markdown-header-literal-bodies)      |
&nbsp; | `LL` bytes     | uint8  | `literal`        | The content of the [literal](#markdown-header-literal-bodies) |
&nbsp; | `LL` % 2 bytes | uint16 | `padding`        | If (`LL` % 2) == 0 then a padding byte `0x00`is added.        |
