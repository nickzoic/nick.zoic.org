from matplotlib import pyplot
import numpy as np
from scipy.optimize import curve_fit
from math import exp

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
scores = [0, 0.25, 0.5, 0.75, 0.9, 0.95, 1]
initial = [ 1, 1, 1, 1, 1, 1, 14 ]

def pop(a, b, t):
    return a * (1+b)**t

times = np.arange(0, 30, 0.1)

lines = [list() for _ in scores]

for t in times:
    pops = [pop(a, b, t) for a, b in zip(initial, scores)]
    total = sum(pops)

    for n, p in enumerate(pops):
        lines[n].append(p/total)

def func(t, a, b, c, d):
    #return a * (b-np.exp(c*t)) / (np.exp(d*t))
    #return (a * np.exp(c*t)-b) / np.exp(d*t)
    return a * ((1+b)**t-c) / d**t

pyplot.xlabel("time")
pyplot.ylabel("fraction")

for score, line, color in zip(scores, lines, colors):
    if score == 1.0: continue
    pyplot.plot(times, line, color=color, label="score %.2f" % score)
    popt, pcov = curve_fit(func, times, line, maxfev=100000)
    pyplot.plot(times, [ func(t, *popt) for t in times ], color=color, linestyle="dashed")
    print("score %.2f popt %s" % (score, popt))

pyplot.legend(loc="upper right", title="variants", reverse=True)
#pyplot.savefig("exp-fit.svg", bbox_inches="tight")
pyplot.show()
