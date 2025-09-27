from matplotlib import pyplot
import numpy as np
from statistics import mean, stdev
import scipy.stats as stats
import random

score = 0.575
sigma = 0.2
count = 100

#sigmas = [ 0.03125, 0.0625, 0.125, 0.25]
sigmas = [ 0.01, 0.05, 0.1, 0.5 ]

weights = [ 0.25, 0.5, 0.75, 1.0 ]
thresholds = [ 0.375, 0.625, 0.875 ]

fig = pyplot.figure(layout='constrained', figsize=(6,12))
axs = fig.subplots(len(sigmas))

for ax, sigma in zip(axs, sigmas):
    ax.xaxis.set_ticks(weights)
    values = [
        random.normalvariate(mu=score, sigma=sigma)
        for _ in range(0, count)
    ]

    bins = [ 0 ] * (len(thresholds)+1)

    for v in values:
        for n, t in enumerate(thresholds):
            if v < t:
                bins[n]+=1
                break
        else:
            bins[-1]+=1

    xscore = sum(b * w for b, w in zip(bins, weights)) / sum(bins)
    print("mu %.3f sigma %.3f score %.3f" % (score, sigma, xscore))
    print("bins %s" % bins)

    ax.bar(weights, bins, width=1/(len(bins)+1))
    ax.set_title("mu %.3f sigma %.3f score %.3f" % (score, sigma, xscore))

    ax2 = ax.twinx()
    ax2.yaxis.set_ticks([])
    x = np.linspace(0.125, 1.125, 100)
    ax2.plot(x, stats.norm.pdf(x, score, sigma), color='orange')

#pyplot.show()
pyplot.savefig("fwd.svg", bbox_inches="tight")
