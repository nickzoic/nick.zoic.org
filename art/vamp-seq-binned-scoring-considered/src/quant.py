from matplotlib import pyplot
import numpy as np
from statistics import mean, stdev
import scipy.stats as stats
import random

score = 0.575
sigma = 0.2
count = 200

sigmas = [ 0.025, 0.05, 0.1, 0.2, 0.5, 1.0 ]

weights = [ 0.25, 0.5, 0.75, 1.0 ]
thresholds = [ 0.375, 0.625, 0.875 ]

fig = pyplot.figure(layout='constrained', figsize=(6,12))
axs = fig.subplots(len(sigmas))

for ax, sigma in zip(axs, sigmas):
    ax.xaxis.set_ticks(weights)

    scores = np.linspace(0.25,1.0,100)

    outputs = []
    for score in scores:
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

        outputs.append(sum( b * w for b, w in zip(bins, weights) ) / count)

    ax.plot(scores, outputs)
    ax.set_title("sigma %.3f" % sigma)

#pyplot.show()
pyplot.savefig('quant.svg', bbox_inches='tight')
