---
layout: draft
title: Discontinuities
summary: 'A bit of a think about discontinuities in structured data'
---

## Hierarchical Data Structures

Computer programmers love collections, never more so than when those
collections can contain other collections.  If your collections
can contain other collections, you can build them up into a hierarchical
tree structure, and everyone loves those.

### Collections

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

So we end up with JSON and XML and ASN-1 and TOML and so on, 
all strucured data formats which serialze this kind of data so
you can put it in a file.

### File System

There's another hierarchical data structure on (most) computers, which
is the file system.  Directories can contain files, and also other directories.
Directories are really just another kind of collection:

* We normally thing of files as "having a name" but actually the name
  is just a key in the directory which contains the file.
* We don't think of files in a directory as having an ordering other
  than what we apply when we make a list of files: by name, by date, by size, etc.
* Depending on the filesystem, things like symbolic and hard links can
  make the filesystem less of a tree and more of a ball of hair, but 
  let's ignore that for now.

Some but not all files are "text files" which are kind of an ordered 
collection of "lines", if you choose to treat them that way.  Other files
contain hierarchical trees of data as above, or collections of binary 
symbols in a library, etc.

### Discontinuity

The problem is there's a *discontinuity* between the hierarchy of files
and the hierarchy inside each file.  

Problems which crop up when structures cross the discontinuity:

* LaTeX documents: for big documents it's common to split chapters
  into separate files.
* Java Class files with one class per file
* the whole `conf.d` mess that Linux gets into.
* HTML documents: what's in the path, what's in the fragment?

## Eliminating the Discontinuity

In the previous article [Boot Naked Linux](../art/boot-naked-linux/) I 
talk about building a system which has exactly one `init` program and
a heavily cut down kernel without even filesystem support.  

If we don't have any filesystem how are we meant to save state?
Well, we still have a disk partition.  This appears as a "block device",
something like `/dev/sda`, which we can read and write as if it was
one giant file.

### mmap

We could do this by `lseek` the block device and `write`ing 
serialized data, but thanks to the wonders of the 64 bit OS,
we can `mmap` the whole disk partition into the process's address space.

Now instead of one big file our disk looks like one big array:

    int fd = open("/dev/sda", O_RDWR);
    uint8_t *one_big_array = mmap(NULL, fd,
        PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);

... [add your own error handling] and as we read and write to that array
the kernel will take care of paging data in and out of physical memory.

But manually copying our state in and out of the One Big Array would
still be annoying. How about we just create our state right in there?

### Allocators

Normally in C code we'd use `malloc` to allocate memory on the heap.
We ask for some space, it marks a little bit of the heap as used and
lets us know where that is.

But if we want to allocate memory inside our new persistent space, we'll
need a new allocator.  Thankfully there's a few of these already:

* [A header-only C allocator library](https://github.com/abdimoallim/alloc/)
* [SHMALL: Simple Heap Memory Allocator](https://github.com/CCareaga/heap_allocator)

There's one fly in our ointment, which is that
`mmap` picks an arbitrary position for our memory-mapped storage to 
appear.
We can *ask* for a specific location, but because of the way Linux process
memory maps work, we're not always going to get it.

This is annoying because we'd like one piece of data to point to another,
C programmers love pointers, but we can't store pointers as the next time
we run our program the mmaped memory could be somewhere else, rendering our
pointers invalid.

Instead we'll have to store *references* which are the same thing but relative
to the start of the `mmap`ed file.  To use them, we then translate them
into pointers.  We do get one advantage from this though: if we choose to
we could expand a 32 bit reference to a 64 bit pointer aligned on a 8 byte 
boundary, and still address 32GB of storage.  If we're dealing with a lot
of small objects this could be worth it to more efficiently use the storage.

    typedef uint32_t ref_t;
    typedef struct storage_s {
        void *ptr;
        size_t size;
        unsigned int mult;
    } storage_t;

    void *ref_to_ptr(storage_t *storage, ref_t ref) { 
        if (ref == 0) return NULL;
        assert(ref*storage->mult < storage->size);
        void *ptr = storage->ptr + (ref*storage->mult);
        return ptr;
    }
    ref_t ptr_to_ref(storage_t *storage, void *ptr) {
        if (ptr == NULL) return 0;
        assert(ptr % storage->size == 0);
        return (ptr / storage->mult) - storage->ptr;
    }

### Other stuff the filesystem does that we don't

* Permissions
* Locking
* Portability 
