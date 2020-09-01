# STXT chunk


## Header
The STXT chunk is saved in [big-endian]. 

id  | Length        | Type    | Description           | Example
----|--------------:|---------|-----------------------|----------------
a   | 4 bytes       | uint32  | Local offset (d)      | 12
b   | 4 bytes       | uint32  | data-length = D       | 26
c   | 4 bytes       | uint32  | Unkonwn? footer-length = F? | 22
e   | D bytes       | uint16  | data: Text string separated by 0x0D | [hello world0x0Dhere is0x0Dan exp]   | F bytes       | ?       | Unknown.              | [0...]


