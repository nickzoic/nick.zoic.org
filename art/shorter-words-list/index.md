---
date: '2020-05-15'
layout: article
tags:
    - crypto
    - python
title: 'A Shorter Words List'
summary: "Encoding cryptographic keys as passphrases, but easier to spell"
---

I have a need to encode a shared secret as something a regular person can type.
Lots of applications do, sometimes for
[passwords](/art/selfish-secret-logins-without-passwords/) or just to
establish a 
[shared secret](https://webwormhole.io/).  The difficulty is remembering 
and/or transmitting this information.

## PGP Word List

There's a [PGP Word List](https://en.wikipedia.org/wiki/PGP_word_list)
for this purpose, but quite a lot of these are long and hard to spell.
I don't want to be trying to explain how to spell "adroitness" down the phone.

Sure, if you wrote a specialized input method you could provide spelling
autocompletion and/or error correction, but that's not quite what I'm after:
I'd like people to be able to type these phrases into a URL or text message 
or whatever and get it right first time.

## EFF Word Lists

The [EFF](https://eff.org/) have published some
[Wordlists for Random Passphrases](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases) 
which I think are an improvement.
They're meant for use with 6-sided dice, to generate a secure passphrase.

The "long word list" has 7776 = 6<sup>5</sup> words of between 3 and 9 characters
with lots of consideration into removing homophones and profanity: check our their article.
They're still 7 characters long on average, and some of them are pretty hard to spell
(`affidavit`, `chihuahua`, `esophagus`).
There's also quite a lot of pairs of very similar words: `blaspheme`/`blasphemy` and
`boogeyman`/`boogieman` for example.
If I have to spell it out over the phone, it's no longer helping.

The "short word list" of 1296 = 6<sup>4</sup> words is much closer to what I'm
looking for, with lengths between 3 and 5 characters, 4.54 on average.
That's fewer bits per word, but slightly more bits per character typed
(2.28, over 1.85)

There's still some tricky words and some pairs I'm not happy about and 6<sup>4</sup>
is not a terribly convenient number for binary computers, so I thought about going
through by hand and trimming the list down to 1024 = 2<sup>10</sup> words, but 
being a Python hacker I figured there had to be an easier way.

## Soundex

There's an ancient but still handy library called "soundex" which I remember using in 
Perl back in the 90s to look for possibly misspelt author names, etc.  It reduces words
to a much smaller symbol space based on their approximate pronunciation, eg:

```
soundex('hello') => 'h4'
soundex('world') => 'w643'
soundex('hell') => 'h4'
soundex('hull') => 'h4'
soundex('heel') => 'h4'
```

It is very lossy, but then again, so are telephone conversations.  Perhaps it'd be useful.

There's a [Soundex library on PyPI](https://pypi.org/project/soundex/)
I mapped the 1296 short words through Soundex and that came up with 514 unique 
soundex strings.  Chucking away `i245` and `t651` for reasons of political fraughtness
left me with 512 unique sounds, some of which had several words mapping to them.

## Word frequencies

How to choose which word from each set?  There's also a
[Word Frequency library on PyPI](https://pypi.org/project/wordfreq/) so why not just 
grab the most commonly used word for each soundex?
This results in a neat list of 512 words, average length 4.6 characters, giving 1.95
bits per character typed, which is slightly worse than the EFF short word list but slightly
better than the EFF long word list.

## Alternating words

The PGP word list has one more trick up its sleeve: there's actually *two* word lists and 
they're used for alternating bytes. This means that you can never have the same word twice
in a row, and provides easier error detection for missing words. 

(They also have a neat trick going with different numbers of syllables, but my words are
too short for that)

512 words is just right to split in half and use to encode 8 bit bytes.
As a bonus, the list splits neatly into `aged` .. `koala` and `ladle` .. `zone`, 
making the split pretty easy to notice.

## Github Repo

Is there any project so small it doesn't get a Github repo?  Not this one.

* [github.com/nickzoic/word-list/](https://github.com/nickzoic/word-list/)

It might become a PyPI module and/or an NPM module at some point too.

## Files

### The word-list generation script

```python3
from soundex import Soundex
from collections import defaultdict
from wordfreq import word_frequency

soundex = Soundex().soundex

sound_words = defaultdict(set)

with open('eff_short_wordlist_1.txt','r') as fh:
    for line in fh:
        word = line.split()[1]
        sound = soundex(word)
        if len(sound) > 1: # and sound not in ('i245', 't651'):
            sound_words[sound].add(word)

for word_set in sound_words.values():
    if len(word_set) > 1:
        word_list = [ (word_frequency(word, 'en'), word) for word in word_set ]
        word_list.sort()
        print(word_list[-1][-1])
    else:
        print(list(word_set)[0])
```

### The word list itself

```
aged     acorn    acre     acts     afar     affix    agent    agile   
aging    agony    ahead    aids     aim      alarm    alike    alive   
alone    aloha    aloft    amend    ample    amuse    angel    anger   
apple    april    apron    awake    area     army     argue    armed   
armor    arson    art      atlas    atom     avert    avoid    bacon   
boots    basil    book     bust     baker    balmy    bunch    broke   
barn     both     baton    blade    blank    blast    blog     blend   
blimp    blob     blurt    bully    boned    bunny    broad    bribe   
bring    broil    civil    case     city     claim    come     canal   
candy    chief    card     crazy    carol    carry    crop     cedar   
crown    cost     clay     chump    comic    civic    cold     clamp   
clip     class    clasp    clear    cleft    clerk    cling    cover   
craft    cramp    crank    crisp    crust    cupid    cycle    deaf    
data     deal     draw     duke     doing    dent     drama    dried   
down     debt     debug    decaf    decal    decor    drive    dimly   
donor    ditch    drank    dress    drift    drill    dust     equal   
early    earth    east     eaten    edge     ebay     even     evoke   
essay    eel      elbow    elder    elk      elm      elude    elves   
email    emit     empty    emu      enter    envoy    erase    error   
erupt    evade    evict    evil     fable    fact     food     fall    
false    fancy    fox      femur    found    ferry    fetal    fetch   
fever    fifth    film     fled     final    five     flip     fling   
flint    flirt    flyer    foam     frail    from     fresh    fruit   
front    frost    gas      going    goal     game     gave     grew    
genre    gift     glass    given    giver    glad     golf     good    
grab     green    grant    grasp    grass    grid     grill    habit   
help     hull     halt     happy    harm     hug      hasty    hatch   
hate     haven    hazel    herbs    hers     human    hunt     hump    
hung     hurry    hurt     issue    icing    icon     igloo    image   
ion      iron     item     ivory    ivy      job      jam      juice   
july     jet      jolt     judge    jump     junky    jury     keep    
kick     kept     kilt     king     kitty    knee     knelt    koala   
ladle    late     lure     lake     lunch    land     level    large   
last     latch    left     legal    line     liver    life     lilac   
lily     limb     lunar    music    maker    mold     many     mango   
manor    move     march    mardi    marry    match    mouth    most    
motor    mount    mulch    mule     mumbo    mural    niece    nail    
name     navy     near     net      nerd     next     ninth    oak     
oat      ocean    oil      old      olive    onion    only     oval    
open     opera    opt      outer    ounce    push     pagan    poker   
palm     point    punch    pants    paper    press    party    pasta   
patch    photo    power    poem     puppy    perm     petal    petri   
plank    plant    plus     plot     pull     polar    prank    print   
prism    proof    props    pulp     pupil    quake    query    quiet   
quill    quilt    raft     risk     radar    radio    rule     ramp    
range    rant     robin    react    roman    reply    recap    relax   
rope     rerun    rigor    ritzy    river    stole    size     said    
send     salt     slam     silk     same     steam    speed    spray   
scale    scan     score    scrap    scope    scold    squad    scorn   
self     ship     serve    seven    share    shell    shirt    shrug   
siren    skirt    slang    slept    slurp    small    swing    smirk   
snap     snare    snarl    snort    speak    spent    spill    sport   
stage    stop     stamp    stand    sting    stark    start    stir    
storm    swirl    those    tall     talon    tamer    think    taper   
taps     trade    taste    tint     theft    theme    train    trap    
tweet    thumb    try      tidal    tiger    tilt     track    trend   
trial    trunk    tulip    tutor    uncle    uncut    unit     unify   
union    upon     upper    urban    used     user     utter    value   
vapor    vegan    venue    virus    vest     video    voice    viral   
visor    vocal    volt     voter    wheat    wafer    wager    wish    
wagon    walk     wind     wasp     watch    water    wife     whole   
widen    wilt     womb     wing     word     worry    wolf     work    
woven    wrist    xerox    yummy    yard     year     yeast    yelp    
yield    yodel    yoga     zebra    zero     zesty    zippy    zone   
```

### An encoding script

Takes a binary file on stdin and spits out words, 8 to a line.

```python3
with open("word_list.txt","r") as fh:
    words = [ w.strip() for w in fh.readlines() ]

import sys

while True:
    s = sys.stdin.buffer.read(8)
    if len(s) == 0: break
    ww = [ words[c+n%2*256] for n, c in enumerate(s) ]
    print(" ".join(ww))
```

### Demo

Let's make some passphrases:

```
$ dd if=/dev/urandom bs=8 count=5 status=none | python encode.py 
ivory stage erase radar ebay wind kept spent
enter yeast email video aging yoga deaf talon
going mouth cedar storm jury oak from raft
found pants hasty query grid oval cycle opera
knelt wind early ramp argue widen bacon rigor
```

## Further Work

Overall I'm pretty happy with the list: the only words which I've noticed
so far which seem out of place are the company names `ebay` and `xerox`,
the very similar pair `quill` and `quilt`, and the variably-spelled `mold`.

It'd be nice to use shorter words over longer words as well.
Perhaps some minor tweaks are in order.

Also I just noticed that the list isn't in alphabetical order, which is not
really a big deal but seems kinda nasty.

Proposed improved word list:

```
acorn    acre     acts     afar     affix    aged     agent    agile   
aging    agony    aide     aids     aim      alarm    alike    alive   
aloe     aloft    alone    amend    ample    amuse    angel    anger   
apple    april    apron    area     argue    armed    armor    army    
arson    art      atlas    atom     avert    avoid    axis     bacon   
baker    balmy    barn     basil    baton    bats     blank    blast   
blend    blimp    blob     blog     blurt    boil     bok      bolt    
bony     bribe    bring    broad    broil    broke    bud      bunch   
bunt     bust     calm     canal    candy    card     case     cedar   
chump    civic    civil    clamp    clasp    class    clay     clear   
cleft    clerk    cling    clip     cold     come     comic    cork    
cost     cover    craft    cramp    crank    crisp    crop     crown   
crust    cub      cupid    cure     curl     cut      cycle    dab     
dad      dart     deal     debt     debug    decaf    decal    decor   
dent     dig      dimly    ditch    doing    donor    down     drab    
drank    dress    drift    drill    drum     dry      dust     early   
earth    east     eaten    ebony    echo     edge     eel      elder   
elf      elk      elm      elude    elves    email    emit     empty   
emu      enter    envoy    equal    erase    error    erupt    evade   
even     evict    evil     evoke    fable    fact     fall     fang    
femur    fend     fetal    fetch    fever    fifth    film     final   
fit      five     flag     fled     fling    flint    flip     flirt   
flyer    foam     fox      frail    fray     fresh    from     front   
frost    fruit    gap      gas      gem      genre    gift     given   
giver    glad     glass    goal     golf     gong     grab     grant   
grasp    grass    green    grew     grid     grill    gut      habit   
halt     harm     hasty    hatch    haven    hazel    help     herbs   
hers     hub      hug      hull     human    hump     hung     hunt    
hurry    hurt     hut      ice      icing    icon     igloo    image   
ion      iron     item     ivory    ivy      jam      jet      job     
jog      jolt     judge    july     jump     junky    jury     keep    
keg      kept     kilt     king     kite     knee     knelt    koala   
ladle    lake     land     last     latch    left     legal    lens    
level    lid      lilac    lily     limb     line     lip      liver   
lunar    lure     lurk     maker    mango    manor    map      march   
mardi    marry    match    malt     mom      most     motor    mount   
mud      mug      mulch    mule     mumbo    mural    nag      nail    
name     nap      near     nerd     net      next     ninth    oak     
oat      ocean    oil      old      olive    omen     only     open    
opera    opt      ounce    outer    oval     pagan    palm     pants   
paper    park     party    patch    pep      perm     pest     petal   
petri    plank    plant    plot     plus     pod      poem     poker   
polar    pond     prank    print    prism    proof    props    pry     
pug      pull     pulp     punk     pupil    quake    query    quill
quit     rabid    radar    raft     ramp     rank     rant     recap   
relax    reply    rerun    rigor    ritzy    river    robin    rope    
rug      ruin     rule     rust     rut      salt     same     scale   
scan     scold    score    scorn    scrap    sect     self     send    
set      seven    share    shirt    shrug    silk     silo     sip     
siren    skip     skirt    sky      slam     slang    slept    slurp   
small    smirk    smog     snap     snare    snarl    snort    speak   
spent    spill    sport    spot     spur     stamp    stand    stark   
start    stem     sting    stir     stole    stop     storm    suds    
surf     swirl    tag      tall     talon    tamer    tank     taper   
taps     tart     taste    theft    thumb    tidal    tidy     tiger   
tilt     tint     tiny     train    trap     trek     trend    trial   
trunk    try      tulip    tutor    uncle    uncut    unify    union   
unit     upon     upper    urban    used     user     utter    value   
vapor    vegan    venue    vest     vice     viral    virus    visor   
vocal    void     volt     voter    wad      wafer    wager    wagon   
walk     wasp     watch    water    widen    wife     wilt     wind    
wing     wiry     wok      wolf     womb     wool     word     work    
woven    wrist    xerox    yam      yard     year     yeast    yelp    
yield    yodel    yoga     zebra    zero     zesty    zippy    zone
```

... this fixes those problems, and has a slightly shorter average length
of 4.4 characters per word, too, for 2.04 bits per character.

## Further Thoughts

* Instead of splitting alphabetically, could we make a list of 256 5 letter words
  and 256 4 letter words so they'd print neatly in columns?  This list has 267
  five letter words, so we're not far off.

## UPDATE 2020-08-07

This words list is now being used by the "tip" version of
[Web Wormhole](https://tip.webwormhole.io/)!
Okay so not exactly earth-shattering but given the year we're having ...
