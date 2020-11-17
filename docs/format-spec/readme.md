# The Director 6 file format
This structure aims to document the entire director 6 file format. It's a work in progress.

## Tidbits
A chunk can be either a
1. Normal chunk
1. Resource chunk

There exist "reserved blocks". Unknown what the purpose of these are. They might be reserved, some alignment-related
skips, or something else entirely.

Field prefixed with a question mark `?` refers to assumed/unconfirmed data.


## Table of contents
1. [Overview](#overview)
    1. [File types](#file-types)
    1. [Structure](#structure)


## Overview
A Director 6 file uses the file format [RIFX](#TODO) which is a variant of the [RIFF](#TODO) (Resource Interchange File
Format) file format used for different multimedia formats on earlier Windows versions. The format mainly uses
[big-endian byte order](#TODO), but it can vary within the file itself.


### File types
- `.dir`
- `.dcr`
- `.dxr`


### Structure
A file is divided into a number of **chunks**. Each chunk consists of an identifier, a chunk length and its chunk data
as described in the following table:

Ref.   | Bytes | Type   | Name    | Description
---    | ---:  | ---    | ---     | ---
&nbsp; | 4     | char   | four&#8209;cc | The chunk identifier. A chunk identifier is known as a [FourCC](#TODO) (four-character code).
`CL`   | 4     | uint32 | chunk&#8209;length | Length of the chunk data.
&nbsp; | `CL`  | &nbsp; | chunk&#8209;data | The data contained within the chunk.

It's worth noting that a chunk is evenly aligned, which means that if `CL` is uneven you need to read an extra padding
byte before reading the next chunk.

The first chunk is always the [RIFX](./chunks/RIFX.md) chunk and its chunk data contains all the other chunks. Then, the
first chunk within the RIFX chunk is the [initial map chunk (IMAP)](./chunks/imap.md). These two are the only "fixed"
chunks in the sense that they, and only they, always appear in at the same addresses within the file. The initial map
chunk serves as a bootloader for reading the remaining chunks in a structured way, although you could just read them
one-by-one as a long list. It points to a [memory map (mmap)](./chunks/mmap.md) which in turn maps all chunks and their
connections via various other helper chunks.


