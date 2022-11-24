import os
import sys
import datetime
import numpy as np
from matplotlib import pyplot as plt

import csv

file = csv.reader(open('/Users/cesararguello/Dropbox (Dartmouth College)/harmonic-radar/raw-data/phone_0_cm_4700000000.0_Hz', 'r'))
n = []
for row in file:
    n.append(float(row[0]))

plt.plot(n)
plt.savefig("test_phone")
