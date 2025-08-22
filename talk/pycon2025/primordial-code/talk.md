# PyConAU talk outline

## welcome

You, by which I mean all the mammals in the audience, are running on an operating system a couple of billion years old which is full of primordial libraries, monkey patches, self-modifying code, viral hacks and even containers running a different operating system.

This talk is all about the freakish parallels between cell biology and computer architecture.

### introduction

My name's Nick Moore, I'm a consultant, software developer, notorious tinkerer.
And recently, a Bioinformatician.

Thanks to my colleagues at Walter and Eliza Hall Institute of Medical Research and at the University of Washington Genome Sciences for their patience while I've found my feet in this field.

Mistakes and oversimplifications are all mine.
The one true rule of biology is that all rules have exceptions, and those exceptions have exceptions, and it's exceptions all the way down.
So some of this talk will oversimplify complex issues but hopefully it'll be enough to give you a general idea.

## humans timeline

Bioinformatics is the study of biological systems using numerical analysis.  Biological systems are pretty complex, so typically this analysis requires computers.
 
It's not entirely surprising that cellular biology and computing are a bit intertwined given their overlapping history of discovery:

**TIMELINE GOES HERE**

We've learned a lot about cellular biology while we've been working out computing, but evolution has billions of years of head-start on us.

## 4 Billion Years of Biology in 8 Minutes

The basic unit of life is the cell.
Primitive organisms like bacteria are *unicellular*, each organism is one cell and each cell is one organism, and they reproduce by copying their innards and splitting in two.

A cell is a little bit like a computer.
There's an outer cell membrane which keeps the insides in and the outsides out.
Inside there's a bunch of programs called *genes* which tell the cell how to make *proteins*, which are the working machinery of the cell.
Proteins can stay within the cell or they can make little *channels* through the cell membrane, kind of like ports which selectively let specific molecules in and out of the cell.
Unicellular organisms reproduce by making copies of their innards, then splitting in two so that each cell now is a full copy of the original.

**Picture of DNA**

Genes, the programs of the cell, are encoded as *chromosomes*, very long *DNA* molecules not unlike a tape.
DNA is built up out of four "bases", Adenine, Cytosine, Guanine and Thymine, generally just abbreviated as A C G and T.  
They zip together in pairs, A complements T and C complements G, so we generally refer to this smallest piece of genetic information as a "base pair".
This is the unit we'll use to compare genome sizes, because there's four
possible pairs each "base pair" is equivalent to 2 binary bits of information.

**Cells picture**

Bacteria have relatively small genomes, typically a single circular chromosome of hundreds of thousands through to a million base pairs.
The human genome by constrast has about 3 billion base pairs, and we have two copies spread over multiple chromosomes.
We're a lot more complicated than a bacteria, but there's a species of lungfish with 130 billion base pairs and an amoeba with 670 billion base pairs[^lsgitw]. 

Also, we make do with each cell having two copies of our genome but there's a frog whose every cell keeps 12 copies[^ucf] so who's counting?
 
[^lsgitw] `https://www.researchgate.net/publication/235907922_Largest_and_Smallest_Genome_in_the_World`

[^ucf] `https://en.wikipedia.org/wiki/Uganda_clawed_frog`

### Genes and evolution

Unicellular organisms reproduce by copying, and errors can arise during the copying process, sometimes leading to novel features in the cells.
Good features thrive, bad features dwindle, and that's natural selection, leading to evolution.

Bacteria can also exchange genes with other bacteria, even with differnt kinds of bacteria, by passing *plasmids*, which are like mini chromosomes.
This is called *horizontal gene transfer*. 
It may seem counter-intuitive to give away your code to your competitors, but consider: the thing evolution is optimizing here is not the organism, but the gene.
If a gene which confers, say, antibiotic resistance gets copied into a new organism and that organism thrives, then the gene is successful even if the old organism is out-competed, and the gene will get passed on to more organisms.

Yep, Free Software is billions of years old, and there's been a whole lot of cutting and pasting from the primordial script archive.

At some point some molecules just happened to work out how to organize themselves into cells and reproduce themselves.
There's no documentation or source control, but by looking at the common features of all cellular life we can hypothesize a "univeral common ancestor" which arose about 4 billion years ago, and from which all life is descended.

### Transcription and Translation

**central dogma slide**

The "source code" of the genome is DNA, but DNA is just a stable storage for the genome, it doesn't actually **do** anything.
Instead, DNA is *transcribed* into RNA, and then RNA is *translated* into
proteins.
This is often called the "central dogma" of cellular biology.

**add some arrows for replication, retrotranscription, ncRNA**

There's also cell replication to consider, and retroviruses can translate RNA back into DNA so we'd better include that, and there's also *non-coding RNA* which functions directly rather than being translated into a protein first.

**add RNAP arrow back from proteins to DNA->RNA edge**

Transcription from DNA to RNA is done by a protein complex called *RNA polymerase (RNAP)*.  This little machine unzips the DNA and assembles an RNA molecule, but RNAP is itself made of proteins.

Proteins are produced from genes, so to build the transcription mechanism we first have to run the transcription mechanism ... 

**add arrows for splicing**

There's also *splicing* to consider. 
DNA is translated into RNA but that RNA isn't in it's final form, first it needs to be *spliced*.
This is done by, yep, more ncRNA and more proteins.

**add arrows for ribosomes and tRNA**

Translation isn't simple either. 
A protein is a long chain of amino acids, which is built up by a complex molecular machine called a *ribosome*, built from ncRNA and proteins ...

So, this is pretty simple, right?
Before we can compile the compiler, we need to compile the compiler.

### bootstrapping

In computing, we call this *bootstrapping*.
You start off by using very primitive tools, possibly even a pencil, to create a very simple first compiler, and then using that compiler you can build a more sophisticated compiler, and so on.

All of this only works because the *oocyte*, the egg you grew from, contained enough of these mechanisms to get the whole process started.
You can think of these genes, as an "operating system" which the rest of a
cell's biology is implemented on top of.

### Expression

The mapping from RNA to protein is done by *transfer RNA (tRNA)*.
Groups of three bases called *codons* correspond to different 
tRNAs which each bring an amino acid molecule to add onto the protein.

This table shows the "standard code" which maps codons to amino acids.
Not all organisms have the exact same code: this table isn't a law of nature, it's a result of what tRNA happen to be around, and tRNA is produced from the genome, so this translation is happening "in software".

It somewhat resembles the instruction decoding tables used in microprocessors — there's some redundancy where 64 codons translate to 20 amino acids, translation starts at a "start" codon and finishes when it reaches a "stop" codon.

But there's no looping or branching or similar, so how is this like a program?

Well, the details of how that gene is expressed can depend on the expression of other genes.
If each gene is a statement, the cell's "program" is found in the interaction between those statements.

### Eukaryotes

At some point about 3 billion years ago, a particularly entrepreneurial branch of the Archaea developed a more sophisticated internal cell structure.
These are the *Eukaryotes*.

Animals (including humans), plants, fungi, algae and slime molds are all Eukaryotes.
 
The Eukaryotic genome is protected inside a *nucleus*, and specialist *organelles* perform specific functions within the cell.
They're linked together by the *cytoskeleton*, a network of filaments and tubes which spans the inside of the cell.

You can think of these as peripheral controllers or coprocessors supporting the main processor, linked by buses.
DNA to RNA transcription occurs in the nucleus, and then RNA to protein translation occurs outside the nucleus, in the *endoplasmic reticulum* which surrounds the nucleus.

Some of these organelles, the *mitochondria*, appear to once have been independent Proteobacteria, which were engulfed by the proto-Eukaryotes and instead of being destroyed they were put to work.

Mitochondria are like little containers with their own separate genome.
The cell benefits from their ability to produce ATP, and the mitochondria benefit from the cell's protection.

But they're effectively running their operating system, like little containers within the host cell, and they have their own replication and protein synthesis.
They even have their own tRNA, and as a result use a slightly different translation code to the host cell.
They've been engulfed but they're still separate and running their own OS.

We like to think of vertebrates as the pinnacle of evolution but plants have done this twice!
In addition to harnessing proteobacteria as mitochondria, plants have harnessed photosynthetic cyanobacteria as *chloroplasts*.
Also a species of algae has been discovered to have harnessed another cyanobacteria to let it fix nitrogen[^nitroplast].

[^nitroplast] `https://en.wikipedia.org/wiki/Nitroplast`

You're probably familiar with the phrase "Embrance, Extend, Extinguish"
referring to the way proprietary systems can use and then destroy open ones.
This may be happening here too: there's evidence that the functions in mitochondria are slowly migrating into the nuclear DNA and being lost from mitochondria.

[^eee] `https://en.wikipedia.org/wiki/Embrace,_extend,_and_extinguish
`
### Multicellular Life

Most (not all) Eukaryotes are multicellular, an organism is made up of many,
many cells.
Every cell in an organism has the same DNA, the same programming, and what role it ends up performing depends on how it is specialized.

You can think of a the DNA as a docker container image which gets specialized at runtime.
The cells in your kidneys contain all the instructions needed to be a brain cell, they just don't use them, and vice-versa.

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

None of those letters are what they seem, instead they're a smattering of letters from Armenian, Cyrillic, Greek, Turkish and other alphabets and some other symbols and smallcaps thrown in [^1][^2].
This can help sneak messages past your spam filters while still remaining human readable

[^1] thanks to `https://util.unicode.org/UnicodeJsps/confusables.jsp`

[^2] this isn't just a problem with humans either, see `https://embracethered.com/blog/posts/2024/hiding-and-finding-text-with-unicode-tags/`

Similarly, substituting naturally occurring alternate "characters" such as pseudouridine for uridine in RNA can prevent an immune response to the mRNA, allowing it to be taken up by cells.

| nucleoside | modified nucleoside | 
|---|---|
| uridine (U) | pseudouridine (Ψ)<br>5-methyluridine (m5U)<br>2-thiouridine (s2U)|
| adenosine (A) | N6-methyladenosine (m6A) |
| cytidine (C) | 5-methylcytidine (m5C) |

Like the unicode characters, the modified nucleosides are different enough to evade spam filtering but similar enough to be "read" by RNA polymerases and used to make proteins, and those proteins go on to produce the desired immune response.

The technique of using pseudouridine to smuggle mRNA vaccines into cells[^3] was pioneered by Katalin Karikó in 2005, used in the Pfizer and Moderna COVID vaccines in 2020 and won Karikó a Nobel prize in 2023.

[^3] https://pmc.ncbi.nlm.nih.gov/articles/PMC2775451/ 