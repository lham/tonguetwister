# Initial Map

The purpose of the initial map is to point us to the active [memory map chunk](./mmap.md). The initial map chunk
will always reside at the same address in a Director file, namely `0x0c`. 

The chunk abbreviation is `imap`.

## Structure

The initial map chunk is saved in **little-endian**.

The structure of the chunk data is:

Ref.   | Bytes | Type(s) | Name               | Description
---    | ---:  | ---     | ---                | ---
&nbsp; | 4     | uint32  | ?mmap&#8209;count  | *TODO: Can there be more than one memory map if we have >32k resources?*
&nbsp; | 4     | uint32  | mmap&#8209;address | The address of the active [memory map chunk](./mmap.md).
&nbsp; | 4     | uint32  | ?version           | &nbsp;
&nbsp; | 12    | &nbsp;  | &nbsp;             | Unknown.
