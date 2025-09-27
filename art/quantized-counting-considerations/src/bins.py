from matplotlib import pyplot
import numpy as np
from statistics import mean, stdev
import scipy.stats as stats

bin_counts = [
    ( 100, 250, 150, 0 ),
    ( 0, 450, 50, 0 ),
    ( 200, 125, 100, 75 ),
    ( 315, 0, 5, 180 ),
]

fig = pyplot.figure(layout='constrained', figsize=(6,12))
axs = fig.subplots(len(bin_counts))

for ax, bins in zip(axs, bin_counts):
    weights = [ i/len(bins) for i in range(1,len(bins)+1) ]

    ax.bar(weights, bins, width=1/(len(bins)+1))
    ax.set_xticks(weights)

    nums = [
        ww
        for n, w in zip(bins, weights)
        for ww in [ w ] * n
    ]

    mu = mean(nums)
    sigma = stdev(nums)

    ax.set_title("mean %.3f stdev %.3f" % (mu, sigma))
    ax2 = ax.twinx()
    ax2.yaxis.set_ticks([])
    x = np.linspace(0.125, 1.125, 100)
    ax2.plot(x, stats.norm.pdf(x, mu, sigma), color='orange')


#pyplot.show()
pyplot.savefig("bins.svg", bbox_inches="tight")
