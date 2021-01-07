# RIFX

The RIFX is the container chunk for the Director file format. All other chunks are contained within it. It helps us
determine if we're looking at a Director file, and if so, which version of the program the file was created with. The
RIFX chunk will always reside at the same address in a Director file, namely `0x00`.

The chunk abbreviation is `RIFX`.

## Structure

The RIFX chunk is saved in **little-endian**.

The structure of the chunk data is:

Ref.   | Bytes       | Type(s)  | Name    | Description
---    | ---:        | ---      | ---     | ---
`V`    | 4           | char     | version | The four character code denoting the [Director version](#director-version-codes) this file was saved with.
&nbsp; | *remaining* | *varies* | data    | The data containing all other chunks.

## Director version codes

Version code `V` | Version
---              | ---
`MV93`           | Director 6, Director 6.5

*TODO: Fill this table with different versions*
