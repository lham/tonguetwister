# The Director 6 file format

This is an attempt to document the entire director 6 file format. It draws on previous research found in various
[sources](#sources); research conducted by myself, and research conducted by our contributors.

It's a work in progress and not (yet) a complete source of truth.

# Table of contents

1. [Director overview](#director-overview)
1. [File types](#file-types)
1. [File structure](#file-structure)
    1. [Loading the file](#loading-the-file)
    1. [Resources](#resources)
        1. [The memory map](#the-memory-map)
        1. [Resource relationships](#resource-relationships)
        1. [Movie resources](#movie-resources)
    1. [Chunk reference](#chunk-reference)

       [`BITD`](./chunks/BITD.md),
       [`CAS*`](./chunks/CAS*.md),
       [`CASt`](./chunks/CASt.md),
       [<code>ccl </code>](./chunks/ccl.md),
       [`Cinf`](./chunks/Cinf.md),
       [`CLUT`](./chunks/CLUT.md),
       [`DCRF`](./chunks/DRCF.md),
       [`ediM`](./chunks/ediM.md),
       [`Fmap`](./chunks/Fmap.md),
       [`free`](./chunks/mmap.md#special-fourccs),
       [`FXmp`](./chunks/FXmp.md),
       [`imap`](./chunks/imap.md),
       [`junk`](./chunks/mmap.md#special-fourccs),
       [`KEY*`](./chunks/KEY*.md),
       [`Lctx`](./chunks/Lctx.md),
       [`Lnam`](./chunks/Lnam.md),
       [`Lscr`](./chunks/Lscr.md),
       [`MCsL`](./chunks/MCsL.md),
       [`mmap`](./chunks/mmap.md),
       [`RIFX`](./chunks/RIFX.md),
       [`RTE0`](./chunks/RTE0.md),
       [`RTE1`](./chunks/RTE1.md),
       [`RTE2`](./chunks/RTE2.md),
       [`Sord`](./chunks/Sord.md),
       [`STXT`](./chunks/STXT.md),
       [`THUM`](./chunks/THUM.md),
       [`VWFI`](./chunks/VWFI.md),
       [`VWSC`](./chunks/VWSC.md),
       [`XTRl`](./chunks/XTRl.md)
1. [Sources](#sources)

# Director overview

*TODO: Describe the theater analogy.*

# File types

- `.dir`
- `.dcr`
- `.dxr`

# File structure

A Director 6 file is structured using the file format [RIFX](#TODO), which is a variant of
the [RIFF (Resource Interchange File Format)](#TODO) file format used for different multimedia formats on earlier
Windows versions. The format mainly uses [big-endian byte order](#TODO), but it can vary within the file itself.

A file is divided into a number of **chunks**. Each chunk consists of an identifier, a chunk length and its chunk data
as described in the following table:

Ref.   | Bytes | Type     | Name               | Description
---    | ---:  | ---      | ---                | ---
&nbsp; | 4     | char     | four&#8209;cc      | A four-character code identifying the chunk, a [FourCC](#TODO).
`CL`   | 4     | uint32   | chunk&#8209;length | Length of the chunk data.
&nbsp; | `CL`  | *varies* | chunk&#8209;data   | The data contained within the chunk.

It's worth noting that the chunks are evenly aligned within the file, i.e., if `CL` is odd there will be an unused byte
before the next chunk.

## Loading the file

The first chunk is always the [RIFX chunk](./chunks/RIFX.md), which identifies the file. Its chunk data contains the
file version and all the other chunks contained within the file. Address references are always indexed from the
beginning of the file however.

The first chunk within the RIFX chunk is the [initial map chunk](./chunks/imap.md), located at address `0x0c`. The
initial map and the RIFX chunk are the only two chunks with "fixed" addresses. The initial map chunk serves as a
bootloader for reading the remaining chunks. It points to a [memory map chunk](./chunks/mmap.md) that is basically an
array listing all chunks, which in turn enables us to read them.

The reason the file is structured and read this way, is because the Director file format is basically a memory dump of
what happens inside the program. For example, when a resource is deleted it remains in memory and its pointer is just
dereferenced. The memory map is a list of pointers (active as well as inactive) to all resources within the memory.
Sometimes Director shuffles things around and creates a new memory map, for example when it reaches its max limit, hence
we need the initial map so that we can find the location of the currently active memory map.

This also means that an unoptimized Director file data can contain a lot of data segments that looks like chunks but in
reality are not. They are just dereferenced chunks that are relics in the dumped memory that is the file. Thus, we can
not simply loop through the file looking for chunks since we might get false positives.

Finally, we continue loading the file by looking up and loading resource assoc table chunk, and then loading all
resources belonging to the Director movie itself. These steps are described further [below](#resources).

## Resources

The next thing to talk about is **resources**. If a **chunk** contains all Director movie data, then the file format
uses a **resource** to link the chunks together. Each resource is identified by its resource id, which can be negative.

There are two types of resources.

1. **Chunk resources**. A chunk resource has a pointer to a chunk as well as some metadata. They are listed in the
   [memory map chunk](./chunks/mmap.md).
2. **Abstract resources**. An abstract resource can represent pretty much anything, from abstract concepts to builtin
   data that is not saved with in the file, such as predefined palettes.

### The memory map

The [memory map chunk](./chunks/mmap.md) is actually an array of aforementioned chunk resources, each entry representing
a single chunk resource. The index of that entry is the resource's resource id (obviously not negative in this case).

The first four resources of the memory map are always the same, pointing to the following chunks:

1. The [RIFX](./chunks/RIFX.md) chunk.
2. The [initial map](./chunks/imap.md) chunk.
3. The [memory map](./chunks/mmap.md) chunk (i.e. a self reference).
4. The [resource assoc table](./chunks/KEY*.md) chunk.

### Resource relationships

Resources can have linked resources in a `1..*` parent-child relation. In fact, most resources have a parent resource,
though in some cases the parent resource will be an abstract resource. However, it's easier to think of the majority of
the resources as "standalone" resources, i.e. that they don't have an actual parent. That way we can describe the child
resources in more tightly coupled relationships as **data resources**.

For example, a [cast](./chunks/CAS*.md) will have multiple [cast members](./chunks/CASt.md), but each cast member is a
pretty much standalone entity and would in theory need to be assigned to a cast. An example of a much stronger
relationship would be that between a [bitmap cast member chunk](./chunks/castmembers/bitmap.md) (which only contains
metadata) and a [bitmap data chunk](./chunks/BITD.md) (which only contains raw encoded image data). So in order for us
to read the image in the chunk correctly we need to connect it with its image data chunk, hence the tight coupling.

This is done using the [resource assoc table chunk](./chunks/KEY*.md), given by the fourth resource in the memory map.
This is a relationship mapping table, where each entry represents a [belongs-to relationship](#TODO). Such an entry
consists of a resource id, a FourCC and the resource id of parent resource to which it belongs.

The resource id and the FourCC forms the [primary key](#TODO) for the relationship mapping table. The reason for having
such a combined primary key is to represent resources that can own multiple data resources. In our example above the
image would only have a single data resource, namely the image data, but other chunks might need more.

### Movie resources

Inside the resource assoc table there are a couple of resources belonging to the movie itself. They all have a fixed
parent resource id, namely the `INTERNAL_RESOURCE_ID = 1024`. All saved Director movie data in the loaded file can be
traced back to these resources through nested belongs-to relationships. Hence, once the memory map chunk and the
resource assoc table chunk are identified and parsed, the rest of the data follows by loading the resources having this
parent resource id.

The movie resources listed below can be present in a Director file and are loaded in the following order:

1. The [director config](./chunks/CDRF.md).
1. The [director file info](./chunks/VWFI.md).
1. The [font mapping](./chunks/FXmp.md).
1. The [cast libraries](./chunks/MCsL.md).
1. The [cast sorting order](./chunks/Sord.md).
1. The [score and frame data](./chunks/VWSC.md).

Note that there will only be a single chunk resource of each type listed above.

*TODO: This list is probably incomplete.*

## Chunk reference

The following chunks have been identified. For detailed information about each one of them see their linked
specification.

- [`BITD` Bitmap Data](./chunks/BITD.md)
- [`CAS*` Cast Association Map](./chunks/CAS*.md)
- [`CASt` Cast Member](./chunks/CASt.md)
- [<code>ccl </code>&nbsp;Unknown](./chunks/ccl.md)
- [`Cinf` Cast Libraries Info](./chunks/Cinf.md)
- [`CLUT` Color Lookup Table](./chunks/CLUT.md)
- [`DCRF` Director Config](./chunks/DRCF.md)
- [`ediM` Editable Media](./chunks/ediM.md)
- [`Fmap` Font Map](./chunks/Fmap.md)
- [`free` Dummy](./chunks/mmap.md#special-fourccs)
- [`FXmp` Font Xtra Map](./chunks/FXmp.md)
- [`imap` Initial Map](./chunks/imap.md)
- [`junk` Dummy](./chunks/mmap.md#special-fourccs)
- [`KEY*` Resource Assoc Table](./chunks/KEY*.md)
- [`Lctx` Lingo Context](./chunks/Lctx.md)
- [`Lnam` Lingo Name List](./chunks/Lnam.md)
- [`Lscr` Lingo Script](./chunks/Lscr.md)
- [`MCsL` Movie Cast Libraries](./chunks/MCsL.md)
- [`mmap` Memory Map](./chunks/mmap.md)
- [`RIFX` RIFX](./chunks/RIFX.md)
- [`RTE0` Unknown](./chunks/RTE0.md)
- [`RTE1` Unknown](./chunks/RTE1.md)
- [`RTE2` Unknown](./chunks/RTE2.md)
- [`Sord` Sort Order](./chunks/Sord.md)
- [`STXT` Styled Text](./chunks/STXT.md)
- [`THUM` Thumbnail](./chunks/THUM.md)
- [`VWFI` VideoWorks File Info](./chunks/VWFI.md)
- [`VWSC` VideoWorks Score](./chunks/VWSC.md)
- [`XTRl` Unknown](./chunks/XTRl.md)

# Sources

Printed material:

- Bruce A. Epstein. **Director in a Nutshell**. O'Reilly. 1999. *A bit of everything about everything. Not necessarily
  describing the exact file format but filling in a lot of gaps on how stuff works behind the scenes. Targets Director
  6, 6.5 and 7.0.1.*
- Macromedia. **Director 6: Using Director**. 1997. Macromedia. *The written instruction manual included with the
  program.*
- Macromedia. **Director 6: Learning Lingo**. 1997. Macromedia. *The written Lingo tutorial included with the program.*
- Macromedia. **Director 6: Lingo Dictionary**. 1997. Macromedia. *The written Lingo reference included with the
  program.*

Digitally published material:

- [**A Tour of the Adobe Director
  Format**](https://medium.com/@nosamu/a-tour-of-the-adobe-director-file-format-e375d1e063c0). *A detailed description
  of how large parts of the director format works. The basis for the article is the Director 8.5. It doesn't go into
  detail over how each chunk is structured.*
- [**The Story Of Shockwave And 3D
  Webgames**](https://medium.com/bluemaximas-flashpoint/the-story-of-shockwave-and-3d-webgames-8f3647865a7). *A fairly
  detailed history of the Macromedia Director (later Adobe) program and related file formats and techniques.*
- [**More Director Movie File Unofficial
  Documentation**](https://docs.google.com/document/d/1jDBXE4Wv1AEga-o1Wi8xtlNZY4K2fHxW2Xs8RgARrqk). *Another attempt to
  document the Director file formats. By [Team Earthquake](#TODO). Targets Director 8.5.*
- [**Shockwave (Director)**](http://fileformats.archiveteam.org/wiki/Shockwave_(Director)). *An overview of the
  Shockwave platform and file formats. Has links to a couple of other projects.*
- [**Lingo bytecode**](http://fileformats.archiveteam.org/wiki/Lingo_bytecode). *A partial, work-in-progress examination
  of Lingo code. Targets Director 4.0.*

Code repositories

- [**System25/drxtract**](https://github.com/System25/drxtract/). *A file disassembler for Director 5 DRI and DRX
  files.*
- [**denaldobf/D4Player**](https://github.com/renaldobf/D4Player). *A player for Director 4 movie files. Not capable of
  running Lingo scripts and missing some functionality.*
- [**scrummvm/scrummvm**](https://github.com/scummvm/scummvm). Specifically
  its [director engine](https://github.com/scummvm/scummvm/tree/master/engines/director). *An emulator targeting games
  made with early versions of Director.*
- [**Earthquake-Project/ProjectorRays**](https://github.com/Earthquake-Project/ProjectorRays). *An experimental Lingo
  decompiler.*
- [**Earthquake-Project/Shockky**](https://github.com/Earthquake-Project/Shockky). *A Shockwave file disassembler.*

## Tidbits (This is a section just containing some small notes)

There exist "reserved blocks". Unknown what the purpose of these are. They might be reserved, some alignment-related
skips, or something else entirely.

Field prefixed with a question mark `?` refers to assumed/unconfirmed data.
