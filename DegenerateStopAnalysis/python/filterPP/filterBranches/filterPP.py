# filterPP.py
# Simple script used to filter a root tuple
# Mateusz Zarucki 2016
# (based on Ivan's scripts) 

import ROOT
import argparse
import sys, os, time, getopt
import array
from Workspace.HEPHYPythonTools.user import username
from Workspace.DegenerateStopAnalysis.toolsMateusz.drawFunctions import makeLine

#if len(sys.argv)>1: infile = sys.argv[1]
#if len(sys.argv)>2: outfile = sys.argv[2]

def printbranches(tree):
   #f = ROOT.TFile(filename)
   #t = f.Get("Events")
   
   branches = tree.GetListOfBranches().Clone()
   
   outfile = open("branches.list", "w")
   
   for branch in branches:
      branchName = branch.GetName()
      outfile.write(branchName + "\n")
   
   outfile.close()
   print makeLine()
   print "All branches have been written to branches.list. Please edit this file correspondingly to keep only the desired ones."
   print makeLine()
   sys.exit(0)

def getlistofbranches(filename):
   f = open(filename,'r')
   outlist = []
   for branch in f:
      branch = branch.strip('\n')
      outlist.append(branch)
   f.close()
   return outlist

def dofilter(tree, outfile, branchfile = "branches.list"):
   #f = ROOT.TFile(infile)
   #tree = f.Get("Events")
   
   if not os.path.isfile(branchfile):
      printbranches(tree)
      return 
   else:
      branchlist = getlistofbranches(branchfile)  

   tree.SetBranchStatus("*", 0)
   
   for br in branchlist:
      tree.SetBranchStatus(br, 1)
   
   g = ROOT.TFile(outfile,"recreate")
   a = tree.CloneTree(0)
   
   for i in xrange(tree.GetEntries()):
      #if not i%1000000: print i,time.strftime('%X %x %Z')
      tree.GetEntry(i)
      a.Fill()
  
   g.cd()
   
   a.Write()
   g.Close()
   #f.Close()
   print makeLine()
   print "Filtered tuple %s has been saved."%outfile
   print makeLine()
