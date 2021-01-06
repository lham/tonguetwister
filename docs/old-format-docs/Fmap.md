# Fmap chunk
The Fmap chunk is saved in [big-endian]. The structure is described by

id  | Length        |  Description
----|--------------:|-----------------------------
a   | 36 bytes      | Header
b   | 8*B bytes     | Description of font entries
c   | A bytes       | Body


## Header

id  | Length        | Type    | Description             | Example
----|--------------:|---------|-------------------------|----------------
d   | 4 bytes       | uint32  | Unkonwn. Some length?   | 52
e   | 4 bytes       | uint32  | body-length = A         | 91
f   | 4 bytes       | uint32  | Unknown. Always zero?   | 0
g   | 4 bytes       | uint32  | Unknown. Always zero?   | 0
h   | 4 bytes       | uint32  | number-of-font-entries = B | 3
i   | 4 bytes       | uint32  | Unknown. Above again?   | 3
j   | 12 bytes      | ?       | Unkonwn. ?              | [28 2 186 73 16 1 206 86 96 0]


## Description of Font entries

id  | Length        | Type    | Description             | Example
----|--------------:|---------|-------------------------|----------------
k   | 4 bytes       | uint32  | body-offset (from c)    | 30
l   | 2 bytes       | uint16  | Unknown. Constant 2?    | 2
m   | 2 bytes       | uint16  | Unknown. ID?            | 1


## Body
The structure is described by

id  | Length        |  Description
----|--------------:|-----------------------------
n   | 36 bytes      | Header
o   | 8*B bytes     | Font entries
p   | 91 - ? bytes  | Footer


### Header

id  | Length        | Type    | Description             | Example
----|--------------:|---------|-------------------------|----------------
q   | 4 bytes       | uint32  | Unkonwn. Always zero?   | 0
r   | 4 bytes       | uint32  | Unkonwn. Always zero?   | 0
s   | 4 bytes       | uint32  | Unkonwn. ?              | 62
t   | 4 bytes       | uint32  | Body length = same as A | 91
u   | 2 bytes       | uint16  | Unknown. ?              | 18


### Font entry
The font entires are 4-byte aligned.

id  | Length              | Type    | Description               | Example
----|--------------------:|---------|---------------------------|----------------
v   | 4 bytes             | uint32  | text-length = A           | 5
w   | A bytes             | uint8   | text                      | Arial
x   | 4 - ((4+A)%4) bytes | uint8   | padding (can be non-zero) | 0x00 0x6C 0x69
