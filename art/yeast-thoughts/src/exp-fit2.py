from matplotlib import pyplot
import numpy as np
from scipy.optimize import curve_fit

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange']
scores = [0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1]
starts = [3, 4, 5, 6, 4.5, 3.5, 5.5, 4.5]

def pop(a, b, t):
    return a * (1+b)**t

times = np.arange(0, 30, 0.1)

lines = [list() for _ in scores]

for t in times:
    pops = [pop(a, b, t) for a, b in zip(starts, scores)]
    total = sum(pops)

    for n, p in enumerate(pops):
        lines[n].append(p/total)

def func(t, a, b, c, d):
    #return (a * (1+b)**t - c) / (1+d)**t
    return (1-a*(b+1)**-t) * (c*(2-d)**-t)
    #return (1-a/(b+1)**t) * c / (2-d)**t
    #return (a - b/(c+1)**t) / (2-d)**t

pyplot.xlabel("time")
pyplot.ylabel("fraction")

for score, start, line, color in zip(scores, starts, lines, colors):
    pyplot.plot(times, line, color=color, label="score %.2f" % score)
    popt, pcov = curve_fit(func, times, line, maxfev=100000, bounds=(0,1.1))
    pyplot.plot(times, [ func(t, *popt) for t in times ], color=color, linestyle="dashed")
    print("score %.2f start %.2f popt %s" % (score, start/sum(starts), popt))

pyplot.legend(loc="upper left", title="variants", reverse=True)
pyplot.savefig("exp-fit2.svg", bbox_inches="tight")
pyplot.show()
