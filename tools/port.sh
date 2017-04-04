#!/bin/bash
# Porting articles from Pelican to Jekyll, for github pages.

set -e

for category in etc HTML5 Languages Python SQL Systems VR; do
   for filename in ~/Work/blogart/content/$category/*.rst; do
       slug=${filename%.rst}
       slug=${slug##*/}
       echo $category $slug

       mkdir -p art/$slug
       pandoc $filename -t markdown -o art/$slug/index.md -s -M category=$category -M slug=$slug -M redirect_from=/$category/$slug/ -M layout=article
   done
done

