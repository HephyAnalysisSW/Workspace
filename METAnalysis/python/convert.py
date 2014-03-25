import ROOT 
import os
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import sqrt, sin, cos, atan2
from Workspace.HEPHYCommonTools.helpers import getVarValue

import ctypes
p_c_float = ctypes.c_float * 1

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--small", dest="small", action="store_true", help="Just do a small subset.")
parser.add_option("--fromPercentage", dest="fromPercentage", default="0", type="int", action="store", help="from (% of tot. events)")
parser.add_option("--toPercentage", dest="toPercentage", default="100", type="int", action="store", help="to (% of tot. events)")
parser.add_option("--inputDirectory", dest="idir", default="/data/schoef/MET_240314/Mu-DYJetsToLL-M50/", type="string", action="store", help="dpm or nfs directory")
parser.add_option("--outputDir", dest="odir", default="/data/schoef/convertedMETTuples_v1/Mu-DYJetsToLL-M50/", type="string", action="store", help="dpm or nfs directory")
(options, args) = parser.parse_args()
os.system('mkdir -p '+options.odir)
postfix=""
if options.small:
  postfix="_small"
if options.fromPercentage!=0 or options.toPercentage!=100:
  postfix += "_from"+str(options.fromPercentage)+"To"+str(options.toPercentage)
ofile = options.odir+"/histo"+postfix+".root"
ofile = ROOT.TFile(ofile, 'recreate')



print "Tupelizing",options.idir
prefix = ""
if options.idir[0:5] != "/dpm/":
  filelist = os.listdir(options.idir)
else:
  filelist = []
  allFiles = os.popen("rfdir %s | awk '{print $9}'" % (options.idir))
  for file in allFiles.readlines():
    file = file.rstrip()
    filelist.append(file)
  prefix = "root://hephyse.oeaw.ac.at/"
if options.small: filelist = filelist[:10]
filenames=[]
for tfile in filelist:
  filenames.append(options.idir+'/'+tfile)

start = int(options.fromPercentage/100.*len(filenames))
stop  = int(options.toPercentage/100.*len(filenames))

print "Reading percentage ",options.fromPercentage, "to",options.toPercentage, "which is range",start,"to",stop,"of",len(filenames),'files'
print ""
filelist=[]
c = ROOT.TChain('Events')
for f in filenames[start:stop]:
  filelist.append(prefix+f)
  c.Add(prefix+f)
  print prefix+f

def getVarName(v):
  return v.split('/')[0]

def getVarType(v):
  if v.count('/'): return v.split('/')[1]
  return 'F'

events = Events(filelist)
pfhandle = Handle("vector<reco::PFCandidate>")
events.toBegin()
labelpf = ("particleFlow")
#labelpfmet = ("pfMet")
labelpfmet = ("patPFMet")
#pfMethandle = Handle("vector<reco::PFMET>")
pfMethandle = Handle("float")

#pftypes = ["X", "h", "e", "mu", "gamma", "h0", "h_HF", "egamma_HF"]
label = {"X":0,"h":1, "e":2, "mu":3,"gamma":4, 'h0':5, 'h_HF':6, 'egamma_HF':7, 0:"X",1:"h", 2:"e", 3:"mu",4:"gamma", 5:'h0', 6:'h_HF', 7:'egamma_HF'}

categories = {\
  "h":[ ["h_mE", -3., -1.5  ],
        ["h_mB", -1.5, 0.   ],
        ["h_pB", 0., 1.5    ],
        ["h_pE", 1.5, 3.0    ]],
  'h0':[["h0_mE", -3., -1.4  ],
        ["h0_mB", -1.4, 0.   ],
        ["h0_pB", 0., 1.4    ],
        ["h0_pE", 1.4, 3.0    ]],
  'h_HF':[["h_HF_m", -5., -3.],
          ["h_HF_p", 3., 5.]],
  'egamma_HF':[["egamma_HF_m", -5., -3.],
               ["egamma_HF_p", 3., 5.]]
}


pftypes = categories.keys() 
storedVars = ['MEx/F', 'MEy/F', 'nCand/I']
extraVars = ['MEx/F', 'MEy/F', 'nCand/I', 'patMEx/F', 'patMEy/F']

tree = ROOT.TTree("Events","Events");
vars={}
for cat in categories.keys():
  for etab in categories[cat]:
    for vn in storedVars:
      name = getVarName(vn)+'_'+etab[0]
      vars[name]=None
      if getVarType(vn)=='F': vars[name] = ctypes.c_float(0.)
      if getVarType(vn)=='I': vars[name] = ctypes.c_int(0)
      tree.Branch(name,   ctypes.addressof(vars[name]),   vn)
for vn in extraVars:
  name = getVarName(vn)
  vars[name]=None
  if getVarType(vn)=='F': vars[name] = ctypes.c_float(0.)
  if getVarType(vn)=='I': vars[name] = ctypes.c_int(0)
  tree.Branch(name,   ctypes.addressof(vars[name]),   vn)
#tree = ROOT.TTree("Events","Events");
#for cat in categories:
#  for etab in categories[cat]:
#  for vn in storedVars:
#    name = getVarName(vn)+'_'+cat[0]
#    tree.Branch(name,   ctypes.addressof(vars[name]),   vn)

def calcMet(pfCands):
  return - sum(vecs[:-1],vecs[-1])

nEvents = c.GetEntries()
if options.small:
  if nEvents>1001:
    nEvents=1001

#print "Reading percentage ",options.fromPercentage, "to",options.toPercentage, "which is range",start,"to",stop,"of",nEvents
for i in range(nEvents):
  for k in vars.keys():
    vars[k].value=0
  c.GetEntry(i)
  if i%100==0:
    print "Event",i, "/",nEvents 

  patMET = getVarValue(c, 'patPFMet')
  patMETphi = getVarValue(c, 'patPFMetphi')
  vars['patMEx'].value = patMET*cos(patMETphi) 
  vars['patMEy'].value = patMET*sin(patMETphi) 

  events.to(i)
  events.getByLabel(labelpf,pfhandle)
  pfc = pfhandle.product()
  vecs={}
  for t in pftypes:
    vecs[t] = [] 
  for p in pfc:
    id = p.particleId()
    l = label[p.particleId()]
    p4 = p.p4()
    Et = p4.Et()
    phi = p4.phi()
    px = Et*cos(phi)
    py = Et*sin(phi)
    vars['MEx'].value -= px
    vars['MEy'].value -= py
    vars['nCand'].value += 1
    if l in pftypes: 
      eta = p4.eta()
      eb = None
      for etab in categories[l]:
        if eta>=etab[1] and eta<etab[2]:
          eb = etab[0]
          break
      if eb: 
        vars['MEx_'+eb].value -= px
        vars['MEy_'+eb].value -= py
        vars['nCand_'+eb].value += 1
#  print "\n"
#  print "Tot.:",vars['MEx'].value, vars['MEy'].value, vars['nCand'].value,"(patMEx/y:",vars['patMEx'].value,vars['patMEy'].value,")"
#  for cat in categories:
#    for etab in categories[cat]:
#      eb = etab[0]
#      print eb, vars['MEx_'+eb].value, vars['MEy_'+eb].value, vars['nCand_'+eb].value
  tree.Fill()
print "Writing",ofile
tree.Write()
ofile.Close()
