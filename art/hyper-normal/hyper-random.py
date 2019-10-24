import random
samples = 1000000

for dim in range(1,101):
    count = 0
    for n in range(0,samples):
        vec = [ random.normalvariate(0,1) for _ in range(0,dim) ]
        if all(-2 < v < 2 for v in vec):
            count += 1
    normies = count*100./samples
    print("%0d,%0.1f,%0.1f" % (dim, normies, 100-normies))

