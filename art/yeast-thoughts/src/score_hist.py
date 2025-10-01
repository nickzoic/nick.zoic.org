from matplotlib import pyplot
import csv
from collections import defaultdict

data = defaultdict(list)

with open("../dat/scoring.csv", "rt") as fh:
    for row in csv.DictReader(fh):
        try:
            data[row['replicate']].append(float(row['raw_score']))
        except ValueError:
            pass

fig = pyplot.figure(layout='constrained', figsize=(6,10))
axs = fig.subplots(len(data))

for ax, (r, ss) in zip(axs, sorted(data.items())):
    ax.set_title("Replicate %s" % r)

    ax.hist(ss, bins=50)

pyplot.show()

