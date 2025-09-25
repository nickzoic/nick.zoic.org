from matplotlib import pyplot
import numpy as np
import scipy.stats as stats

bin_counts = [
    ( 100, 500, 150, 0 ),
    ( 100, 125, 100, 100 ),
    ( 0, 450, 50, 0 ),
    ( 315, 0, 5, 180 ),
]

fig, axs = pyplot.subplots(len(bin_counts))

for ax, bins in zip(axs, bin_counts):
    weights = [ i/len(bins) for i in range(1,len(bins)+1) ]
    ax.bar(weights, bins, width=1/(len(bins)+1))
    ax.set_xticks(weights)

    mu = 0.525
    sigma = 0.1

    ax2 = ax.twinx()
    x = np.linspace(0, 1, 100)
    ax2.plot(x, stats.norm.pdf(x, mu, sigma), color='orange')


pyplot.show()
