from matplotlib import pyplot
import numpy as np
from scipy.optimize import curve_fit
import gzip
import csv
from collections import defaultdict
from math import sqrt
from scipy.optimize import curve_fit

variants = set([
    #'p.=',
    'p.Ala300Met',
    #'p.Asp282Gln',
    #'p.Gln195Leu',
    'p.Phe237Ser',
    #'p.Phe241Pro',
    'p.Ala109Ter',
    #'p.Met267Ter',
])

replicates = ['3', '4']
totals = { r: defaultdict(int) for r in replicates }
counts = { r: defaultdict(lambda: defaultdict(int)) for r in replicates }
times = set()

with gzip.open("../dat/variant_counts.csv.gz", "rt") as fh:
    for row in csv.DictReader(fh):
        if row['rep'] in replicates:
            time = int(row['time'])
            times.add(time)
            count = int(row['count__sum__sum'])
            totals[row['rep']][time] += count
            if row['protein'] in variants:
                counts[row['rep']][time][row['protein']] += count

times = sorted(times)
time_range = range(min(times),max(times)+1)

freqs = {
    r: {
        v: { 
            t: counts[r][t][v] / totals[r][t]
            for t in times
        }
        for v in variants
    }
    for r in replicates
}

stdevs = {
    r: {
        v: {
            t: sqrt(counts[r][t][v] or 1) / totals[r][t]
            for t in times
        }
        for v in variants
    }
    for r in replicates
}

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange']

fig = pyplot.figure(layout='constrained', figsize=(6,10))
axs = fig.subplots(len(replicates))

def func(t, a, b, c, d):
    return (a - b/2**(c*t)) / 2**(d*t)



print("|replicate|variant|time<br>h|count|total|frequency<br>ppm|stdev<br>ppm|")
print("|---|---|---:|---:|---:|---:|---:|")

for ax, r in zip(axs, replicates):
    ax.set_title("Replicate %s" % r)
    ax.set_xlabel("time (h)")
    ax.set_xticks(times)
    ax.set_ylabel("fraction (ppm)")
    ax.yaxis.set_major_formatter(lambda y, _: "%.0f" % (y*1000000))

    for c, v in zip(colors, variants):
        y = [freqs[r][v][t] for t in times]
        e = [stdevs[r][v][t] for t in times]
        ax.errorbar(times, y, e, linestyle='None', marker='o', color=c, capsize=3)

        for t in times:
            print("|%s|%s|%s|%d|%d|%.3f|%.3f|" % (r, v, t, counts[r][t][v], totals[r][t], freqs[r][v][t] * 1000000, stdevs[r][v][t] * 1000000))
        
        #popt, pcov = curve_fit(func, times, y, maxfev=100000, bounds=(0,2))
        #ax.plot(times, [ func(t, *popt) for t in times ], color=c, label=v, linestyle="dotted")

        popt, pcov = curve_fit(func, times, y, sigma=e, maxfev=100000, bounds=(0,2))
        ax.plot(time_range, [ func(t, *popt) for t in time_range ], color=c, label=v, linestyle="dashed")

    ax.legend()

pyplot.xlabel("time")
pyplot.ylabel("fraction")
#pyplot.show()
pyplot.savefig("variants-stdev.svg", bbox_inches="tight")
