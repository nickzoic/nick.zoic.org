# PyConAU talk outline

## welcome

You, by which I mean all the Eukaryotes in the audience, are running on an operating system a couple of billion years old which is full of primordial libraries, monkey patches, self-modifying code, viral hacks and even containers running a different operating system.

This talk is all about the freakish parallels between cell biology and computer architecture.

## introduction

My name's Nick Moore, I'm a consultant, software developer, notorious tinkerer.
And recently, a Bioinformatician.

Thanks to my colleagues at Walter and Eliza Hall Institute of Medical Research and at the University of Washington Genome Sciences for their patience while I've found my feet in this field.

Mistakes and oversimplifications are all mine.  The one true rule of biology is
that all rules have exceptions, and those exceptions have exceptions, and it's 
exceptions all the way down.
So some of this talk will oversimplify complex issues but hopefully it'll be enough to give you a general idea.

## humans timeline

Bioinformatics is the study of biological systems using numerical analysis.  Biological systems are pretty complex: the human genome is about 3 billion base-pairs long.
So typically this analysis requires computers.
 
It's not entirely surprising that cellular biology and computing are a bit intertwined given their overlapping history of discovery:

**TIMELINE GOES HERE**

We've learned a lot about cellular biology while we've been working out computing, but evolution has billions of years of head-start on us.

## this is a computer / this is a cell

OK, so this is a computer conference, so let's start with a computer:

There's a box to keep outside stuff from getting in.

There's a bunch of ports in the box which let power and signals in and out.

There's a central processing unit which runs the programs, and a bunch of
peripherals which support those operations.
Some of those have their own little processors.

There's brackets and wires and stuff to keep the parts together
and connect them up.

Wait, I think I've got my slides muddled up.

This is a cell.

There's a *cell membrane*, which keeps the inside and outside separated.

It has a many *channels* which allow specific molecules in or out.

The *nucleus* holds the cell's DNA, and executes the cell's programming.
There's a bunch of *organelles* which support these programs, and a 
structure caled the *cytoskeleton* which connects it all together.

This is a *eukaryotic* cell.  We like to think of Eukaryota as being the
pinnacle of evolution because animals, including us, are Eukaryotes but
let's not get too ahead of ourselves here because Eukaryota also includes 
plants, fungi, yeasts and slime molds.

## evolution timeline

How did we get here?

About 4.5gya the Earth formed, initially it was just a big ball of molten
rock but eventually it'd cool down enough to have oceans and continents and
weather.  No life, just yet.

About 4gya, the first cellular life arose.  How we got there is a whole
'nother question, but these primitive cells are our common ancestor.
We don't know much about these cells, except for what we can derive from
the common features of their descendants.
But at some point some molecules just happened to work out how to organize themselves into cells and reproduce themselves, and while there's no trace left of these "Univeral Common Ancestors", we can tell a little bit about them from the common features of their descendants, the anaerobic Archaea, aerobic Proteobacteria and photosyntheic Cyanobacteria.

These early organisms are *unicellular*, each organism is a single cell.
A cell is a little bundle of molecular parts, bounded by a cell membrane which keeps the insides in and the outsides out.

The working parts of the cell are *proteins* and these are like little machines which fit within or on the surface of the cell membrane or poke through it to make little *channels* to move stuff in or out of the cell.

## Genes & Evolution

*Genes* are the instructions for how to make these proteins and are encoded as
*chromosomes*, very long *DNA* molecules not unlike a tape.
Cells reproduce by making copies of their innards, then splitting in two.

Errors can arise during copying, sometimes leading to novel features in the cells.
Good features thrive, bad features dwindle, and that's evolution.
Bacteria can also exchange genes with other bacteria, even with different kinds of bacteria.
This is called *horizontal gene transfer*.
It may seem counter-intuitive to give away your code to your competitors, but consider: the thing evolution is optimizing is not the organism, but the gene.

Yep, Free Software is billions of years old, and there's been a whole lot of cutting and pasting from the primordial script archive.

## transcription and translation

The "source code" of the genome is DNA, but DNA is just a stable storage for the genome, it doesn't actually **do** anything.
Instead, DNA is *transcribed* into RNA, and then RNA is *translated* into
proteins.
This is often called the "central dogma" of cellular biology.

**diagram with arrows**

There's also replication and reverse transcription and ncRNA to consider.

**draws extra arrows**

Transcription from DNA to RNA is done by a protein complex called "RNA polymerase".  This little machine unzips the DNA and assembles an RNA molecule, but RNAP is itself made of proteins.

**more arrows**

Proteins are produced from genes, so to build the transcription mechanism we first have to run the transcription mechanism ... 

Oh no.

Before we can compile the compiler, we need to compile the compiler.
In computing, we call this *bootstrapping*.
You start off by using very primitive tools, possibly even a pencil, to create a very simple compiler, and then using that compiler you can build a more sophisticated compiler, and so on.

There's also some RNA which acts directly.

**add extra arrows for ncRNA, tRNA**
 
Translation from RNA to Protein is done by a whole heap of molecules 
called Transfer RNA, or tRNA for short.  Each tRNA binds to an amino acid
and to the RNA codons, assembling the protein like a zipper and then
releasing.

These tRNAs are also transcribed out of our genes.
Not all organisms have exactly the same "translation table", because some organisms have have different sets of tRNA.

Transcription isn't quite as straightforward as I've made it sound, either.
Chromosomes hold not just genes, but also "untranslated regions" which include *promoters* which control how much a gene should be expressed, and *introns* which get trimmed out.
Guess what does the promoting and the trimming?
Proteins and RNA.

**more arrows**

All of this only works because the *oocyte*, the egg you grew from, contained enough of these mechanisms to get the whole process started.
You can think of these genes, as an "operating system" which the rest of a
cell's biology is implemented on top of.

There are a few major operating
systems which have a lot in common and a few differences.  Organisms as 
different as humans and yeasts have a lot in common though, enough that we
can actually insert human genes into a yeast and have them produce proteins.

## Eukaryotes & Mitochondria & mtDNA

Most (not all) Eukaryotes are multicellular, an organism is made up of many,
many cells. Every cell ...
**METADISCLAIMER: BIOLOGY IS JUST LIKE THIS**

okay, mostly every cell most of the time. I'm going to stop adding in 
all these disclaimers now, it's biology, it's just like this

*Mostly* every cell in an organism has the same DNA, the same programming, and what role it ends up performing
depends on how it is specialized.  You can think of a the DNA as a docker container
image which gets specialized at runtime.

The cells in your kidneys contain
all the instructions needed to be a brain cell, they just don't use them.

In addition to the nucleus, which contains the nuclear DNA, Eukaryotic cells
contain *mitochondria*, self contained little coprocessors which are thought
to have originated when a host Archaea absorbed Proteobacteria.

Interestingly, mitochondria have their own separate genome, including their
own RNAP and tRNA, and the mitochondrial tRNA translation table is a little bit
different to the eukaryotic nucleus: they've been absorbed but they're still separate and running their own OS.

In addition, mitochondria have been observed to move between cells.
Try not think about it.

## Promoter Regions

## RNA interactions / monkey patching

## Deep Mutational Scanning / Fuzzing

## mRNA Vaccines

Messenger RNA, or *mRNA* has been in the news a lot recently,
for all the wrong reasons.  A very large proportion of us here today 
will have benefited from mRNA vaccine technology and a lot of us will
get to benefit further as research continues into mRNA therapies.
 
Your immune system is very effective, but also kind of slow to anger.
If you can give it a hint about what things to look for it can respond
much more rapidly and effectively.

That's called vaccination.
Historically it's been done using similar but less
deadly infections, such as cowpox inoculations for smallpox, or by 
introducing an attenuated, inactivated or dead organism for our 
immune system to learn from without risk of infection.

Ideally we'd like to be able to target vaccination more accurately and develop new vaccines more effectively. This can be a tricky thing to manage.

Cells don't just read any old mRNA they find laying around.
Instead, stray mRNA will induce an immune response and get cleaned up by
your immune system — get caught your body's spam filter, in other words.

Instead, mRNA has to get smuggled into the cell with a bit of a
bait-and-switch ... just like spam:

```
Ηο𝚝 Ꮮսхս𝚛у ꓪа𝚝сℎ℮ꜱ
ıո γοᴜⲅ ⍺𝖗ҽа
```

None of those letters are what they seem, instead they're a smattering of letters from Armenian, Cyrillic, Greek, Turkish and other alphabets and some other symbols and smallcaps thrown in [^1].  This can help sneak messages past your spam filters while still remaining human readable

[^1] thanks to https://util.unicode.org/UnicodeJsps/confusables.jsp

Similarly, substituting naturally occurring alternate "characters" such as pseudouridine for uridine in RNA can prevent an immune response to the mRNA, allowing it to be taken up by cells.

| nucleoside | modified nucleoside | 
|---|---|
| uridine (U) | pseudouridine (Ψ)<br>5-methyluridine (m5U)<br>2-thiouridine (s2U)|
|adenosine (A) | N6-methyladenosine (m6A) |
| cytidine (C) | 5-methylcytidine (m5C) |

Like the unicode characters, the modified nucleosides are different enough to evade spam filtering but similar enough to be "read" by RNA polymerases and used to make proteins, and those proteins go on to produce the desired immune response.

The technique of using pseudouridine to smuggle mRNA vaccines into cells[^2] was pioneered by Katalin Karikó in 2005, used in the Pfizer and Moderna COVID vaccines in 2020 and won Karikó a Nobel prize in 2023.

[^2] https://pmc.ncbi.nlm.nih.gov/articles/PMC2775451/ 

## Horizontal Gene Transfer

## 
