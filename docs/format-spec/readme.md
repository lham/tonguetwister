# The Director 6 file format
This structure aims to document the entire director 6 file format. It's a work in progress.

## Tidbits
A chunk can be either a
1. Normal chunk
1. Resource chunk

There exist "reserved blocks". Unknown what the purpose of these are. They might be reserved, some alignment-related
skips, or something else entirely.

Field prefixed with a question mark `?` refers to assumed/unconfirmed data.
