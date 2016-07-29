from cardFileWriter import cardFileWriter
#from limit_helper import plotsignif , plotLimit , signal_bins_3fb
from math import exp,sqrt
import os,sys
import ROOT
import pickle
#import array
#from Workspace.RA4Analysis.signalRegions import *
import argparse

regionToDPhi_2015 = {
  (5, 5) : {
    (250, 350) : {
      (500, -1) : 1.00
     }, 
    (350, 450) : {
      (500, -1) : 1.00
      }, 
    (450, -1) : {
      (500, -1) : 1.00
      }
    }, 
  (6, 7) : {
    (250, 350) : {
      (500, 750) : 1.00, (750, -1) : 1.00
     }, 
    (350, 450) : {
      (500, 750) : 1.00, (750, -1) : 1.00
      }, 
    (450, -1) : {
      (500, 1000) : 0.75, (1000, -1) : 0.75
      }
    }, 
  (8, -1) : {
    (250, 350) : {
      (500, 750) : 1.00, (750, -1) : 1.00
     }, 
    (350, 450) : {
      (500, -1) : 0.75
      }, 
    (450, -1) : {
      (500, -1) : 0.75
      }
    }

}
regionToDPhi = {(5,5): {(250, 350): {(500, 750):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},
                             (350, 450): {(500, 750):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                             (450, -1):  {(500, 750):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'},                  
                                          (750, 1000):  {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT2', 'tex':'\\textrm{LT3}, \\textrm{HT2}'},                  
                                          (1000, -1):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT3', 'tex':'\\textrm{LT3}, \\textrm{HT3}'}}},                            
                     (6,7): {(250, 350): {(500, 750):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},                              
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},               
                             (350, 450): {(500, 750):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},                            
                             (450, -1):  {(500, 750):   {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'},                              
                                          (750, 1000):  {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT2', 'tex':'\\textrm{LT3}, \\textrm{HT2}'},                              
                                          (1000, -1):   {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT3', 'tex':'\\textrm{LT3}, \\textrm{HT3}'}}},       
                     (8,-1): {(250, 350):{(500, 750):   {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},               
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},             
                              (350, 450):{(500, 750):   {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                              (450, -1): {(500, 1000):  {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'},
                                          (1000, -1):   {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT3','HT': 'HT23', 'tex':'\\textrm{LT3}, \\textrm{HT23}'}}}}

worstCaseSyst = {
  (5, 5) : {
    (250, 350) : {
      (500, -1) : 0.25
     }, 
    (350, 450) : {
      (500, -1) : 0.35
      }, 
    (450, -1) : {
      (500, -1) : 0.45
      }
    }, 
  (6, 7) : {
    (250, 350) : {
      (500, 750) : 1.00, (750, -1) : 0.30,
      (750, -1) : 1.00, (750, -1) : 0.30
     }, 
    (350, 450) : {
      (500, 750) : 1.00, (750, -1) : 0.40,
      (500, 750) : 1.00, (750, -1) : 0.55
      }, 
    (450, -1) : {
      (500, 1000) : 0.75, (1000, -1) : 0.30,
      (1000, -1) : 0.75, (1000, -1) : 0.80
      }
    }, 
  (8, -1) : {
    (250, 350) : {
      (500, 750) : 0.70, 
      (750, -1) : 0.60,
     }, 
    (350, 450) : {
      (500, -1) : 0.65
      }, 
    (450, -1) : {
      (500, -1) : 0.70
      }
    }

}

def dphiLimitToLabel(dphi):
  ndphi = int(100*dphi+0.5)
  result = None
  if ndphi==75:
    result = "1"
  elif ndphi==100:
    result = "2"
  assert result!=None
  return "D"+result

def njetBinToLabel(njBin):
  # simplified to lower boundary
  result = None
  if njBin[1]!=-1:
    result = "".join([str(x) for x in range(njBin[0],njBin[1]+1)])
  else:
    result = str(njBin[0])+"p"
  assert result!=None
  return "J"+result[0]
#  return "J"+result

def ltBinToLabel(ltBin):
  idxs = [ None, None ]
  for i in range(2):
    if ltBin[i]==250:
      idxs[i] = 1
    elif ltBin[i]==350:
      idxs[i] = 2
    elif ltBin[i]==450:
      idxs[i] = 3
    elif ltBin[i]==-1:
      idxs[i] = 4
    assert idxs[i]!=None
  return "L"+"".join([str(x) for x in range(idxs[0],idxs[1])])

def htBinToLabel(htBin):
  # simplified to lower limit
  idx = None
  if htBin == (500,750):
    idx = 1
  elif htBin == (500,1000):
    idx = 2
  elif htBin == (750, 1000):
    idx = 3
  elif htBin == (500,-1):
    idx = 4
  elif htBin == (750,-1):
    idx = 5
  elif htBin == (1000,-1):
    idx = 6
  assert idx!=None
  return "H"+str(idx)
#  return "H"+"".join([str(x) for x in range(idxs[0],idxs[1])])

parser = argparse.ArgumentParser()
parser.add_argument('--nolimit', help='do not run limit', action='store_true')
parser.add_argument('--blind', help='use blind mode', action='store_true')
parser.add_argument('-f', '--force', dest='force', help='replace output files', action='store_true')
parser.add_argument('-d', '--dir', dest='dir', help='output directory', default=None)
#parser.add_argument('--SRonly', help='use only SRs', action='store_true')
parser.add_argument('--method', help='limit setting method', dest='method', \
                      choices=['CalcSingleLimit','CalcLimitSRonly','CalcAbcdLimit'],default=['CalcSingleLimit'])
parser.add_argument('--bins', help='list of bin indices to be used', 
                    dest='bins', default=None)
parser.add_argument('--signals', help='list of signal indices to be used', 
                    dest='signals', default=None)
parser.add_argument('--masses', help='gluino,lsp masses of a signal point', 
                    dest='masses', default=None)
args = parser.parse_args()
useBinIndices = set()
if args.bins!=None:
  for f in args.bins.split(","):
    if f.find("-")>=0:
      gs = f.split("-")
      assert len(gs)==2
      for i in range(int(gs[0]),int(gs[1])+1):
        useBinIndices.add(i)
    else:
        useBinIndices.add(int(f))
assert not ( args.signals!=None and args.masses!=None )
useSignalIndices = set()
if args.signals!=None:
  for f in args.signals.split(","):
    if f.find("-")>=0:
      gs = f.split("-")
      assert len(gs)==2
      for i in range(int(gs[0]),int(gs[1])+1):
        useSignalIndices.add(i)
    else:
        useSignalIndices.add(int(f))
useSignalMasses = None
if args.masses!=None:
  ms = [ int(x) for x in args.masses.split(",") ]
  assert len(ms)==2
  useSignalMasses = ( ms[0], ms[1] )

#if args.SRonly:
#  from CalcLimitSRonly import *
#else:
#  from CalcSingleLimit import *
if args.method=='CalcSingleLimit':
  from CalcSingleLimit import *
elif args.method=='CalcLimitSRonly':
  from CalcLimitSRonly import *
elif args.method=='CalcAbcdLimit':
  from CalcAbcdLimit import *
  
#ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/Workspace/HEPHYPythonTools/scripts/root/tdrstyle.C")
#ROOT.setTDRStyle()

path = os.environ["HOME"]+"/www/combine_tests/"
if not os.path.exists(path):
  os.makedirs(path)

path_table = os.environ["HOME"]+"/www/combine_tests/"
if not os.path.exists(path_table):
  os.makedirs(path_table)

text_path = "text_files"
if not os.path.exists(text_path):
  os.makedirs(text_path)

options = ['signif' , 'limit']
option = options[1]

lumi_bins = [1,2,3,4,5,6,7,8,9,10]
#lumi_bins = [1,2,3,4]
#lumi_bins = [3,10]
lumi_origin = 3




##################################

#res = pickle.load(file(os.path.expandvars("singleLeptonic_Spring15__estimationResults_pkl_kappa_corrected-150116.pkl")))
#sigres = pickle.load(file(os.path.expandvars("resultsFinal_withSystematics_andSignals_NewStructure_150120.pkl")))
#sigres = pickle.load(file(os.path.expandvars("pickles150121/allSignals_2p3_pkl")))
#bkgres = pickle.load(file(os.path.expandvars("pickles150121/resultsFinal_withSystematics_pkl")))
#sigres = pickle.load(file(os.path.expandvars("pickles150125/allSignals_2p3_v2_pkl")))
#sigres = pickle.load(file(os.path.expandvars("pickles160130/allSignals_2p25_syst_pkl")))
#bkgres = pickle.load(file(os.path.expandvars("pickles150125/resultsFinal_withSystematics_pkl")))
#sigres = pickle.load(file(os.path.expandvars("pickles160218/allSignals_2p25_allSyst_approval_pkl")))
#bkgres = pickle.load(file(os.path.expandvars("pickles160218/resultsFinal_withSystematics_pkl")))
#sigres = pickle.load(file(os.path.expandvars("pickles160223/allSignals_2p25_allSyst_approval_pkl")))
#bkgres = pickle.load(file(os.path.expandvars("pickles160223/resultsFinal_withSystematics_pkl")))
#sigres = pickle.load(file(os.path.expandvars("pickles160303/allSignals_2p3_allSyst_pkl")))
#sigres = pickle.load(file(os.path.expandvars("/data/easilar/Spring15/25ns/allSignals_2p3_allSyst_VV_pkl")))
sigres = pickle.load(file(os.path.expandvars("/afs/hephy.at/data/easilar01/Ra40b/pickleDir/allSignals_12p88_2015Syst_pkl")))
#bkgres = pickle.load(file(os.path.expandvars("pickles160303/resultsFinal_withSystematics_pkl")))
bkgres = pickle.load(file(os.path.expandvars("/data/dspitzbart/Results2016/Prediction_Spring16_templates_SR2016_v2_lep_data_12p9/resultsFinal_withSystematics_pkl")))

#pdg = 'pos'
#pdg = 'neg'
#pdg = 'both'

#
# consistency
#
njetBins = [ ]
ltBins = [ ]
htBins = [ ]
for nj in bkgres.keys():
  if type(nj)!=type(()):
    print "Rejecting key",nj
    continue
  njetBins.append(nj)
  for lt in bkgres[nj]:
    if not lt in ltBins:
      ltBins.append(lt)
    for ht in bkgres[nj][lt]:
      if not ht in htBins:
        htBins.append(ht)
njetBins.sort()
ltBins.sort()
htBins.sort()
#print njetBins
#print ltBins
#print htBins
#for njet in njetBins:
#  print njetBinToLabel(njet)
#for lt in ltBins:
#  print ltBinToLabel(lt)
#for ht in htBins:
#  print htBinToLabel(ht)

signals = [
          {'color': ROOT.kBlue ,'name': 's1500' , 'mglu' : 1500, 'mlsp' : 100, 'label': 'T5q^{4} 1.5/0.8/0.1'}, \
          {'color': ROOT.kRed  ,'name': 's1200' , 'mglu' : 1200, 'mlsp' : 800, 'label': 'T5q^{4} 1.2/1.0/0.8'}, \
#          {'color': ROOT.kBlack ,'name': 's1000' , 'mglu' : 1000, 'mlsp' : 700, 'label': 'T5q^{4} 1.0/0.85/0.7'}, \
          {'color': ROOT.kBlack ,'name': 's1000' , 'mglu' : 1000, 'mlsp' : 100, 'label': 'T5q^{4} 1.0/0.55/0.1'}, \
         ]

#signal = signals[2]


#
# prepare bins
#

#nbins = 0
#for njet in njetBins[:]:
#  for lt in ltBins[:]:
#    if not lt in bkgres[njet]:
#      continue
#    for ht in htBins[:]:
#      if not ht in bkgres[njet][lt]:
#        continue
#      nbins += 1

if os.path.exists("results.log"):
  os.system("rm results.log; touch results.log")

sbBinNames = [ ]
sbBins = { }
mbBinNames = [ ]
mbBins = { }
for njet in njetBins[:]:
  for lt in ltBins[:]:
    if not lt in bkgres[njet]:
      continue
    for ht in htBins[:]:
      if not ht in bkgres[njet][lt]:
        continue
      dphiLimit = dphiLimitToLabel(regionToDPhi[njet][lt][ht]['deltaPhi'])
      print njetBinToLabel(njet) , ltBinToLabel(lt) , htBinToLabel(ht) , dphiLimit
      print njet , lt , ht , regionToDPhi[njet][lt][ht]['deltaPhi']
      bNameBase = njetBinToLabel(njet) + ltBinToLabel(lt) + htBinToLabel(ht) + dphiLimit
      bName = bNameBase
      print "bname:" , bName
      print "bNameBase" , bNameBase
      assert not bName in mbBinNames
      mbBinNames.append(bName)
      mbBins[bName] = ( njet, lt, ht )
      for sb in [ "W", "tt" ]:
        if sb=="W":
          sbName = "J3"  + ltBinToLabel(lt) + htBinToLabel(ht) + dphiLimit
          if not sbName in sbBinNames:
            sbBinNames.append(sbName)
            sbBins[sbName] = ( njet, lt, ht )
        elif sb=="tt":
          sbName = "J4"  + ltBinToLabel(lt) + htBinToLabel(ht) + dphiLimit
          if not sbName in sbBinNames:
            sbBinNames.append(sbName)
            sbBins[sbName] = ( njet, lt, ht )            

print mbBinNames
print sbBinNames                

sigmasses = set()
for nj in sigres:
  for lt in sigres[nj]:
    for ht in sigres[nj][lt]:
      for mglu in sigres[nj][lt][ht]["signals"]:
        for mlsp in sigres[nj][lt][ht]["signals"][mglu]:
          masses = ( mglu, mlsp )
          if not masses in sigmasses:
            sigmasses.add(masses)

signals = [ ]
for masses in sorted(sigmasses):
  mglu, mlsp = masses
  fmgluTeV = float(mglu)/1000.
  fmlspTeV = float(mlsp)/1000.
  label = 'T5q^{4}VV '
  label += '{0:3.1f}/{1:3.1f}/{2:3.1f}'.format(fmgluTeV,(fmgluTeV+fmlspTeV)/2.,fmlspTeV)
  signals.append({ 'color': ROOT.kBlack, 'name': 'S_'+str(mglu)+"_"+str(mlsp), \
                     'mglu': mglu, 'mlsp': mlsp, 'label': label })

for isig,signal in enumerate(signals):
  if args.signals!=None and not (isig in useSignalIndices):
    continue
  if useSignalMasses!=None and ( signal["mglu"]!=useSignalMasses[0] or signal["mlsp"]!=useSignalMasses[1] ):
    continue
  print signal
  calc = CalcSingleLimit(bkgres,sbBinNames,sbBins,mbBinNames,mbBins,sigres,signal)
  calc.name = "limit_"+str(signal["mglu"])+"_"+str(signal["mlsp"])
  calc.runLimit = not args.nolimit
  calc.runBlind = args.blind
  calc.force = args.force
  if args.dir==None:
    calc.dir = "."
  else:
    if not os.path.isdir(args.dir):
      os.mkdir(args.dir)
    calc.dir = args.dir
  if args.bins!=None:
    calc.useBins = sorted(useBinIndices)
  calc.limitSinglePoint()
