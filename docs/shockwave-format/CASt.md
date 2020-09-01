# CASt chunk


## Header
The CASt chunk is saved in [big-endian]. 

id  | Length        | Type    | Description           | Example
----|--------------:|---------|-----------------------|----------------
a   | 4 bytes       | uint32  | type                  | 3
b   | 4 bytes       | uint32  | data-length = D       | 75
c   | 4 bytes       | uint32  | offset-length = O     | 28
d   | X bytes       | ?       | Unknown. Block that starts with an uint32 size_b, and the have size_b-4 bytes. | [32, 28 bytes ?]
e   | 2 bytes       | uint16  | skip-size = S         | 8
f   | S bytes       | ?       | Unknown.              | [0...]
g   | O bytes       | ?       | Unkonwn. Block with repeating number | [0x000, 0x005, 0x000 0x005, ...]
h   | 1 bytes       | uint8   | text-length = T       | 3
i   | T bytes       | uint8   | text                  | API
j   | 1 bytes       | uint8   | 0x00 terminator       | 0x00
k   | 6 bytes       | uint16  | 3 [0x00]              | [0x00, 0x00, 0x00]
l   | 6 bytes       | uint16  | 3 [0xFF]              | [0xFF, 0xFF, 0xFF]
m   | 6 bytes       | uint16  | 3 [0x00]              | [0x00, 0x00, 0x00]
n   | 10 bytes      | ?       | Unknonwn.             |
o   | (pad) 2 bytes | uint16  | Padding bytes         | 116

Note that D = length of [f - j].


