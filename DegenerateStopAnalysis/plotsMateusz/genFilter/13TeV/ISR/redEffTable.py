#redEffPlot.py script - Map of MET Gen. Filter Reduction Factor vs Efficiency on Reco Cut

import ROOT
import os
import numpy as np
#from array import array
#import scipy

#Root options

#ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Default") #Plain = sets empty TStyle

#ROOT.gStyle.SetOptStat(1) #prints statistics on plots
#ROOT.gStyle.SetOptFit(0) #gStyle->SetOptFit(1111); //prints fit results of plot
#ROOT.gStyle.SetTitleX(0.15) #sets x-coord of title
#gStyle->SetFuncWidth(1) #sets width of fit line
#gStyle->SetFuncColor(9) #sets colours of fit line
#gStyle->SetLineWidth(2)
#gStyle->SetOptTitle(0) #suppresses title box

#ROOT.gStyle.SetCanvasBorderMode(0);
#ROOT.gStyle.SetPadBorderMode(0);
#ROOT.gStyle.SetPadColor(0);
#ROOT.gStyle.SetCanvasColor(0);
#ROOT.gStyle.SetTitleColor(0);
#ROOT.gStyle.SetStatColor(0);

path = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/13TeV/" #ROI/
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/13TeV/reductionEfficiency/" #web directory http://www.hephy.at/user/mzarucki/plots/filter/

if not os.path.exists(savedir):
   os.makedirs(savedir)

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

files = []
buffer = []

outfile = open(savedir + "reductionEfficiencyTable.txt", "w")
outfile.write(\
"genMET Cut" + "   " + "genISRpt Cut" + "    " + "MET 1 Red. Factor" + "    " + "MET 1 Reco Eff." + "    " + "MET 2 Red. Factor" + "    " + "MET 2 Reco Eff." + "    " + "ISR 1 Red. Factor" + "    " + "ISR 1 Reco Eff." + "    " + "ISR 2 Red. Factor" + "    " + "ISR 2 Reco Eff." + "\n"\
)

#Gets all file paths with filter results
for dirname in sorted(os.listdir(path)): 
   if dirname.startswith("filter"):
      print dirname
      buffer = dirname.split("_")
      filename = 'reductionEfficiency_' + buffer[1] + '_' + buffer[2]  + '.txt'
      files.append(os.path.join(path,dirname,filename))

#Extraction of data from file
for filename in files:
   infile = open(filename, 'r') #.read() #opens data file
   print "Opening: ", infile.name

   #infile.seek(offset, [from]) # offset = number of bytes to be moved | [from] ref position from where bytes to be moved

   #infile.tell() #position in file

   for line in infile:
      #print line
      line = infile.next() 
      buffer = line.split()
      outfile.write(\
      str(buffer[0]) + "         " + str(buffer[1]) + "         " + str(buffer[2]) + "      " + str(buffer[3]) + "      " + str(buffer[4]) + "      " + str(buffer[5]) + "      " + str(buffer[6]) + "      " + str(buffer[7]) + "      " + str(buffer[8]) + "      " + str(buffer[9]) + "\n"\
      )
   infile.close()
   
outfile.close()

