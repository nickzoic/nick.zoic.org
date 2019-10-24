import math

for dim in range(1,101):
    normies = 100 * .955 ** dim
    print("%0d,%0.1f,%0.1f" % (dim, normies, 100-normies))

