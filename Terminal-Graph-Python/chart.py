#!/usr/bin/env python3.7
import math
import sys
import random

#Globals
ROW = 10
COLUMNS = 10
MAXINT = 999

data = [random.randint(0,MAXINT) for i in range(COLUMNS)]


minimum = min(data)
maximum = max(data)
chart = []

# Chart Structure
for row in range(ROW):
    chart.append([])
    chart[row].append(math.ceil((maximum / ROW) * row))
    for d in data:
        chart[row].append('   ')

# Input Value
for r_in , row in enumerate(chart):
    for c_in , col in enumerate(data,start = 1):
        if col >= int(row[0]):
            chart[r_in][c_in] = " _ "

chart.reverse()

# Print Chart
for row in chart :
    for col in row :
        sys.stdout.write(f"{str(col).rjust(5)} ")
    sys.stdout.write("\n")
sys.stdout.write("\t")
for d in data :
    sys.stdout.write(f"{str(d).ljust(6)}")
