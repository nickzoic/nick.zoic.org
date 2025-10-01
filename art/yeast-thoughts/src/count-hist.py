from matplotlib import pyplot
import numpy as np
from scipy.optimize import curve_fit
import gzip
import csv
from collections import defaultdict
from math import sqrt
from scipy.optimize import curve_fit



with gzip.open("../dat/variant_counts.csv.gz", "rt") as fh:
    data = [
        int(row['count__sum__sum'])
        for row in csv.DictReader(fh)
        if row['protein'] not in ('p.=', 'p.Met1Arg', 'p.Ter516=', 'p.Ter516del')
    ]

pyplot.hist(data, bins=50, range=(1,200), log=True)

pyplot.show()
