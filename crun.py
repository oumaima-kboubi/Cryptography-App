import itertools
import re

l = list(map("".join, itertools.product('abcdefjhijklmnopqrstuvwyz.', repeat=5)))
f = open("output.txt", "a")
for row in l:
    if re.match("([a-z])+\.{1}([a-z])+", row):
        f.write(row + "@insat.ucar.tn")
        f.write("\n")
