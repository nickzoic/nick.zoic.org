import numpy as np

# np.random.Generator
rr = np.random.default_rng()

# total population in the turbidostat
tot = 1_000_000_000

# number of variants present
nvar = 10000

# variants, an array of scores between 0 and 1
var = rr.random(nvar)

# initial populations for the variants.
pop = rr.integers(9000, 10000, nvar)

gen = 100

dvars = 10
data = [ [] for _ in range(dvars) ]

for _ in range(gen):
    pop = pop * (1.1)**var
    pop = np.round(pop * tot / np.sum(pop))
    samp = rr.choice(range(nvar), size=1000000, p=pop/np.sum(pop))
    for n, c in enumerate(np.bincount(samp, minlength=nvar)[:dvars]):
        data[n].append(c)

from matplotlib import pyplot

for n, d in enumerate(data):
    pyplot.plot(range(gen), d, label="%.2f" % var[n])

pyplot.show()
