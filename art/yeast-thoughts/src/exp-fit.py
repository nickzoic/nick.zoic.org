from matplotlib import pyplot
import numpy as np
from scipy.optimize import curve_fit

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
scores = [0, 0.5, 0.75, 0.9, 1]

def pop(a, t):
    return (1+a)**t

times = np.arange(0, 30, 0.1)

lines = [list() for _ in scores]

for t in times:
    pops = [pop(s, t) for s in scores]
    total = sum(pops)

    for n, p in enumerate(pops):
        lines[n].append(p/total)

def func(t, a, b, c, d):
    return a * (b-np.exp(c*t)) / (np.exp(d*t))

pyplot.xlabel("time")
pyplot.ylabel("fraction")

for score, line, color in zip(scores, lines, colors):
    pyplot.plot(times, line, color=color, label="score %.2f" % score)
    popt, pcov = curve_fit(func, times, line)
    pyplot.plot(times, [ func(t, *popt) for t in times ], color=color, linestyle="dashed")
    print("score %.2f popt %s" % (score, popt))

pyplot.legend(loc="upper left", title="variants", reverse=True)
pyplot.savefig("exp-fit.svg", bbox_inches="tight")
#pyplot.show()
