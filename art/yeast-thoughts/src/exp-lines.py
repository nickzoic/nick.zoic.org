from matplotlib import pyplot
import numpy as np

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

pyplot.xlabel("time")
pyplot.ylabel("fraction")

for score, line in zip(scores, lines):
    pyplot.plot(times, line, label="score %.2f" % score)

pyplot.legend(loc="upper left", title="variants", reverse=True)
pyplot.savefig("../img/exp-lines.svg", bbox_inches="tight")
#pyplot.show()
