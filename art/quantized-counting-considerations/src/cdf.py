from scipy.stats import norm
from scipy.optimize import curve_fit
from matplotlib import pyplot
import numpy as np

weights = [0.25, 0.5, 0.75, 1]
thresholds = [ 0.375, 0.625, 0.875 ]

def func(i, mu, sigma):
    # calculate the expected cumulative probability for bin `i`.
    # (0 <= i <= len(thresholds))
    #a = norm.cdf(thresholds[i], loc=mu, scale=sigma) if i < len(thresholds) else 1
    #b = norm.cdf(thresholds[i-1], loc=mu, scale=sigma) if i > 0 else 0
    #return a - b
    f_1 = norm.cdf(3/8, loc=mu, scale=sigma)
    f_2 = norm.cdf(5/8, loc=mu, scale=sigma) - f_1
    f_3 = norm.cdf(7/8, loc=mu, scale=sigma) - f_1 - f_2
    f_4 = 1 - f_1 - f_2 - f_3
    return (f_1, f_2, f_3, f_4)

def func2(ii, mu, sigma):
    # this is an alternative version of the fit function which treats
    # boundary conditions differently
    n = len(weights)
    return [
        norm.cdf((i*2+3)/n/2, loc=mu, scale=sigma) - norm.cdf((i*2+1)/n/2, loc=mu, scale=sigma)
        for i in ii
    ]

samples = [
    (100,250,150,0),
    (0,450,50,0),
    (200,125,100,75),
    (315,0,5,180),
]

fig = pyplot.figure(layout='constrained', figsize=(6,10))
axs = fig.subplots(len(samples))

for ax, sample in zip(axs, samples):
    total = sum(sample)
    scaled_sample = [ s / total for s in sample ]
    popt, pcov = curve_fit(func, [0,1,2,3], scaled_sample, maxfev=100000)
    ax.bar(weights, sample, width=(1/(len(sample)+1)))
    ax.xaxis.set_ticks(weights)
    ax2 = ax.twinx()
    x = np.linspace(0.125, 1.125, 100)
    ax2.plot(x, norm.pdf(x, popt[0], popt[1]), color='orange')

    title = "mu %.6f sigma %.6f var(mu) %.6f" % (popt[0], popt[1], pcov[0][0])
    ax.set_title(title)

#pyplot.show()
pyplot.savefig("../img/cdf.svg", bbox_inches="tight")
