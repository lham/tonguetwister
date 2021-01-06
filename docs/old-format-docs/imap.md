# imap chunk


## Header
The imap chunk is saved in [little-endian]. 

24 bytes long?

Points to the valid mmap section? 

id  | Length        | Type    | Description             | Example
----|--------------:|---------|-------------------------|----------------
a   | 4 bytes       | uint32  | ?                       | 1
b   | 4 bytes       | uint32  | mmap-offset             | 44
c   | 4 bytes       | uint32  | ?                       | 1223
d   | 12 bytes      | ?       | 3x 0x0000               | [0x0000 0x0000 0x0000]


