#!/usr/bin/env python
import sys
import re

def split_tags(s):
   return 'tags:\n' + '\n'.join("    - %s" % x.lower() for x in re.split(r',\s*', s))

for filename in sys.argv[1:]:
   with open(filename, "r") as f:
       s = f.read()

   r = re.compile(r"^tags: '(.*)'", re.M)
   s, n = re.subn(r, lambda m: split_tags(m.group(1)), s)

   if n:
     with open(filename, "w") as f:
       f.write(s)
