---
layout: draft
title: Discontinuities
summary: 'A bit of a think about discontinuities in structured data'
---

## Nested Data Structures

Computer programmers love collections, never more so than when those
collections can contain other collections.  If your collections
can contain other collections, you can build them up into a hierarchical
tree structure, and everyone loves those.

Some collections have keys, others have ordering, some have both,
for example in Python[^0]:

| | No Key | Key |
|---|---|---|
| No Order | `set` / `Counter`[^1] | `dict`[^2] |
| Order | `list` / `tuple` | `OrderedDict` / `namedtuple` |

... and while there's some other complexity there[^3] we can use this
to build arbitrary complex structures.

[^0]: Most languages have something similar.
[^1]: `set`s don't allow duplicates, `Counter`s do.
[^2]: Since Python 3.7 dict entries are also ordered by insertion.
[^3]: You can't put `list`s in a `set` because `list`s are mutable.
      On the other hand, since a list is mutable, you can add it to itself.
      Data structures are fun!

Most languages have broadly similar concepts ...
what they lack in formalism and efficiency they makes up for in
flexibility and universality.

## File System


## Structural Discontinuity

Problems which crop up when structures cross the discontinuity:

* LaTeX documents: for big ones it's traditional to split chapters
  into separate files.
* Java Class files with one class per file
* the whole `conf.d` mess that Linux gets into.
* HTML documents: what's in the path, what's in the fragment?



## Eliminating the Discontinuity

In the previous article [Boot Naked Linux](../art/boot-naked-linux/) I 
talk about building a system which has exactly one `init` program and
a heavily cut down kernel without even filesystem support.  

Thanks to the wonders of 64 bit CPUs, we can `mmap` the whole disk
partition into the process's address space.  The kernel will then take
care of paging data in and out of physical memory.

Normally in C code we'd use `malloc` to allocate memory on the heap.
If we want to allocate memory inside our new persistent space, we'll
need a new allocator.  Thankfully there's a few of these already:

* [A header-only C allocator library](https://github.com/abdimoallim/alloc/)
* [SHMALL: Simple Heap Memory Allocator](https://github.com/CCareaga/heap_allocator)

So, can we just `mmap` our drive, point our allocator library at that
memory space and go for it?   There's one fly in our ointment, which is that
`mmap` picks an arbitrary position for our memory-mapped storage to 
appear, so we can't store pointers and have them come back to where we left 
them.

Instead we'll have to store *references* which are the same thing but relative
to the start of the `mmap`ed file.  To use them, we then translate them
into pointers.  We do get one advantage from this though: if we choose to
we could expand a 32 bit reference to a 64 bit pointer aligned on a 8 byte 
boundary, and still address 32GB of storage.  If we're dealing with a lot
of small objects this could be worth it to more efficiently use the storage.

Other stuff the filesystem does that we don't:

* Permissions
* Locking
* 
