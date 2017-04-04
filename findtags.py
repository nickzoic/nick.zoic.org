#!/usr/bin/env python
import sys
import re

all_tags = set()

for filename in sys.argv[1:]:
   with open(filename, "r") as f:
       s = f.read()

   r = re.compile(r"^tags:\s*((^    - (.*)\n)+)", re.M)
   x = re.search(r, s)
   if x:
     tags = [ re.sub('    - ', '', z) for z in re.split("\n", x.group(1)) if z ]
     for tag in tags: all_tags.add(re.sub("\s+", "-", tag))

for tag in sorted(all_tags):
   print tag
   with open("tag/%s.md" % tag, "w") as f:
     f.write("---\nlayout: tag\ntitle: %s\n---\n")


