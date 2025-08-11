# PyConAU talk outline

## welcome

 You, by which I mean all the Eukaryotes in the audience, are running on an operating system a couple of billion years old which is full of primordial libraries, monkey patches, self-modifying code, viral hacks and even containers running a different operating system.

This talk is all about the freakish parallels between cell biology and computer architecture.

## introduction

G'day my name's Nick, I'm a consultant, software developer, notorious tinkerer.
And recently, a Bioinformatician.

Thanks to my colleagues at Walter and Eliza Hall Institute of Medical Research and at
the University of Washington Genome Sciences for their patience while I've found my feet
in this field.

Mistakes and oversimplifications are all mine.  The one true rule of biology is
that all rules have exceptions, and those exceptions have exceptions, and it's 
exceptions all the way down.

## humans timeline

Bioinformatics is the study of biological systems using numerical analysis, thus, 
generally, using computers.

It's not entirely surprising that cellular biology and
computing are a bit intertwined given their history:

**TIMELINE GOES HERE**

## this is a computer / this is a cell

OK, so this is a computer conference, so here's a computer:

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
the common features of their descendants, the anaerobic Archaea, aerobic
Proteobacteria and photosyntheic Cyanobacteria.

About 2gya, somehow, an Archaea absorbed a Proteobacteria to form the first
Eukaryotic organisms.  We'll come back to those soon.

**diagram**

## DNA, RNA, Proteins

Most (not all) Eukaryotes are multicellular, an organism is made up of many,
many cells. Every cell
(okay, mostly every cell most of the time. I'm going to stop adding in 
all these disclaimers now, it's biology, it's just like this)
has the same DNA, the same programming, and what role it ends up performing
depends on how it is specialized.  You can think of a the DNA as a container
image which gets specialized at runtime.  The cells in your kidneys contain
all the instructions needed to be a brain cell, they just don't use them.

## transcription and translation

Our genome is encoded as DNA stored in *chromosomes*, but DNA is just a
stable storage for the genome, it doesn't actually **do** anything.
Instead, DNA is *transcribed* into RNA, and then RNA is *translated* into
proteins.

This is often called the "central dogma" of cellular biology, although
there's also replication and reverse transcription and ncRNA to consider ...
 
## bootstrapping tRNA

Okay,t: DNA becomes RNA becomes Proteins, according to
some great and perfect law of nature.

No.

Transcription from DNA to RNA is done by a protein complex called
"RNA polymerase" or RNAP.  This little machine unzips the DNA and assembles 
an RNA molecule, but RNAP is itself made of proteins,
which come from genes, so to build the transcription mechanism we first
have to run the transcription mechanism ... oh no.

Also, translation from RNA to Protein is done by a whole heap of molecules 
called Transfer RNA, or tRNA for short.  Each tRNA binds to an amino acid
and to the RNA codons, assembling the protein like a zipper and then
releasing. These tRNAs are also transcribed out of our genes.  Not all
organisms have exactly the same "translation table", because some organisms
have have different tRNA.

All of this only works because the *oocyte* you grew from contained enough
RNA polymerase and enough tRNA to bootstrap the whole process, and from then
on your cells keep producing their own RNAP and tRNA.

You can think of these genes, as an "operating system" which the rest of a
cell's biology is implemented on top of.  There are a few major operating
systems which have a lot in common and a few differences.  Organisms as 
different as humans and yeasts have a lot in common though, enough that we
can actually insert human genes into a yeast and have them produce proteins.

## Eukaryotes & Mitochondria & mtDNA

In addition to the nucleus, which contains the nuclear DNA, Eukaryotic cells
contain *mitochondria*, self contained little coprocessors which are thought
to have originated when a host Archaea absorbed Proteobacteria.

Interestingly, mitochondria have their own separate genome, including their
own RNAP and tRNA, and the mitochondrial DNA translation table is a little bit
different to the host cell: they've been absorbed but they're still running
their own OS.

In addition, mitochondria have been observed to move between cells.
Try not think about it.

## Promoter Regions

## RNA interactions / monkey patching

## Deep Mutational Scanning / Fuzzing

## mRNA & papa1

Messenger RNA, or *mRNA* has been in the news a lot recently,
for all the wrong reasons.  A very large proportion of us here today 
will have benefited from mRNA vaccine technology and a lot of us will
get to benefit further as research continues into mRNA therapies.
 
Your immune system is very effective, but also kind of slow to anger.
If you can give it a hint about what things to look for it can respond
much more rapidly. Historically that's been done using similar but less
deadly infections, such as cowpox inoculations for smallpox, or by 
introducing an attenuated, inactivated or dead organism for your 
immune system to learn from without risk of infection.

The immune system "learns" about the proteins on the outside of the 
pathogens.  Ideally we'd like to be able to target vaccination more accuratelyThis can be a tricky thing to manage.

But cells don't just read any old mRNA they find laying around. 
Instead, mRNA has to get smuggled into the cell with a bit of a
bait-and-switch.

You might remember this exciting URL:

    paypa1.com
    
but you probably wanted:
    
    paypal.com
    
In the same way, 

Replacing *uridine* with *pseudouridine*

## Horizontal Gene Transfer

## 
