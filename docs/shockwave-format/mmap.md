# mmap chunk


## Header
The mmap chunk is saved in [little-endian]. 

id  | Length        | Type    | Description             | Example
----|--------------:|---------|-------------------------|----------------
a   | 2 bytes       | uint16  | header-length           | 24
b   | 2 bytes       | uint16  | length-of-record        | 20
c   | 4 bytes       | uint32  | number-of-commands      | 150
d   | 4 bytes       | uint32  | number-of-commands-used | 148
e   | 4 bytes       | uint32  | ?                   | [0xFFFF 0xFFFF]
e   | 4 bytes       | uint32  | ?                   | [0xFFFF 0xFFFF]
f   | 4 bytes       | uint32  | Index of the first empty mapping.                       | 33


## Body
Repeating entries with the structure in the table below. Each entry represents a command found in the FIRX file.

id  | Length        | Type    | Description               | Example
----|--------------:|---------|---------------------------|----------------
a   | 4 bytes       | uint32  | command-name              | CASt
b   | 4 bytes       | uint32  | command-block-length      | 117 B
c   | 4 bytes       | uint32  | table-offset              | 5246 B
d   | 4 bytes       | uint32  | Unkonwn. Protected flag?  | 0
e   | 4 bytes       | uint32  | Unkonwn. Incrementing(-ish) for the free command  | 0


## Footer / unused entries
2x 20 Byte chunks?
