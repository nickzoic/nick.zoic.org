from matplotlib import pyplot
import numpy as np

scores = [1, 0.9, 0.75, 0.5, 0]

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

pyplot.xlim([0, 30])
pyplot.ylim([0, 1])

pyplot.stackplot(times, *lines, labels=["score %.2f" % s for s in scores])

pyplot.legend(loc="upper right", title="variants", reverse=True)
pyplot.savefig("exp-stack.svg", bbox_inches="tight")
#pyplot.show()
