import numpy as np
from scipy.optimize import curve_fit
import gzip
import csv
from collections import defaultdict
from math import sqrt
from scipy.optimize import curve_fit
from statistics import median
import multiprocessing

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
            counts[row['rep']][row['protein']][time] += count

times = sorted(times)

def func(t, a, b, c, d):
    return (a - b/2**(c*t)) / 2**(d*t)

def raw_score(x):
    (r, v, counts, totals) = x
    freqs = [ counts[x] / totals[x] for x in times ]
    stdevs = [ sqrt(counts[x] or 1) / totals[x] for x in times ]
    try:
        popt, pcov = curve_fit(func, times, freqs, sigma=stdevs, maxfev=100000, bounds=(-1,1))
        return r, v, popt[-1]
    except RuntimeError:
        return r, v, None


scores = defaultdict(dict)

with multiprocessing.Pool(processes=16) as pool:
    variants = ( 
        (r, v, cc, totals[r])
        for r, vv in counts.items()
        for v, cc in vv.items()
    )
    for r, v, s in pool.imap_unordered(raw_score, variants):
        print("%s,%s,%s" % (r,v,s))
