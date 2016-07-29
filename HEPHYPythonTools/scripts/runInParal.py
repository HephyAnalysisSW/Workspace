#!/usr/bin/env python
"""
Usage:
./runInPara.py path/to/file_with_commands  <nJobs>

Will read lines from the file_with_commands and run them in parralel <nJobs> at a time

"""

from optparse import OptionParser
import os
import multiprocessing

default_nProc=10   ## apparently nJobs should be less than 2*nCores

parser = OptionParser()
(options,args) = parser.parse_args()


if len(args)==2:
    pass
elif len(args)==1:
    args.append(default_nProc)
else:
    raise Exception("Needs two argument, first text file to read the jobs from and then number of jobs to run in parallel")


fname = args[0]
nProcesses = int(args[1])

commands = []
with open(fname) as f:
    for line in f.xreadlines():
        line.rstrip("\n")
        commands.append(line)

pool = multiprocessing.Pool(processes=nProcesses)
results = pool.map(os.system, commands)
pool.close()
pool.join()


