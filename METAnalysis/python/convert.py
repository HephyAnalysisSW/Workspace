import ROOT 
import os
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math import sqrt, sin, cos, atan2, pi
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
ofilen = options.odir+"/histo"+postfix+".root"
ofile = ROOT.TFile(ofilen, 'recreate')

from commons import label, categories, pfTypes
occupancy = {}
energy = {}
for k in pfTypes:
  occupancy[k]  = ROOT.TH2D('occ_'+k,'occ_'+k, 50,-5.5,5.5,40,-pi,pi)
  energy[k]     = ROOT.TH2D('en_'+k,'en_'+k, 50,-5.5,5.5,40,-pi,pi)

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

mZ  = "sqrt(2.*muonsPt[0]*muonsPt[1]*(cosh(muonsEta[0] - muonsEta[1])- cos(muonsPhi[0] - muonsPhi[1]) ))"
#ptZ = "sqrt((muonsPt[0]*cos(muonsPhi[0]) + muonsPt[1]*cos(muonsPhi[1]))**2+(muonsPt[0]*sin(muonsPhi[0]) + muonsPt[1]*sin(muonsPhi[1]))**2)"
commoncf = "abs("+mZ+"-90.2)<12.&&muonsPt[0]>15 && muonsPt[1]>15 && muonsPFRelIso[0]<0.15 && muonsPFRelIso[1]<0.15"
#c.Scan(mZ,"muonsPt[0]>15 && muonsPt[1]>15 && muonsPFRelIso[0]<0.15 && muonsPFRelIso[1]<0.15")
c.Draw(">>eList", commoncf)
eList = ROOT.gDirectory.Get('eList')


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


usedPFTypes = categories.keys() 
storedVars = ['MEx/F', 'MEy/F', 'nCand/I']
extraVars = ['phiZ/F', 'ptZ/F', 'MEx/F', 'MEy/F', 'nCand/I', 'patMEx/F', 'patMEy/F', 'ngoodVertices/I']

tree = ROOT.TTree("Events","Events");
vars={}
for cat in categories.keys():
  for etab in categories[cat]+[['others']]:
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

nEvents = eList.GetN()
if options.small:
  if nEvents>1001:
    nEvents=1001

#print "Reading percentage ",options.fromPercentage, "to",options.toPercentage, "which is range",start,"to",stop,"of",nEvents
for i in range(nEvents):
  for k in vars.keys():
#    print k, vars['ptZ'].value
    vars[k].value=0
  c.GetEntry(eList.GetEntry(i))
  if i%100==0:
    print "Event",i, "/",nEvents 

  patMET = getVarValue(c, 'patPFMet')
  patMETphi = getVarValue(c, 'patPFMetphi')
  vars['patMEx'].value = patMET*cos(patMETphi) 
  vars['patMEy'].value = patMET*sin(patMETphi)
  vars['ptZ'].value = sqrt((getVarValue(c, "muonsPt", 0)*cos(getVarValue(c, "muonsPhi", 0)) + getVarValue(c, "muonsPt", 1)*cos(getVarValue(c, "muonsPhi", 1)))**2\
    +(getVarValue(c, "muonsPt", 0)*sin(getVarValue(c, "muonsPhi", 0)) + getVarValue(c, "muonsPt", 1)*sin(getVarValue(c, "muonsPhi", 1)))**2)
  vars['phiZ'].value = atan2( getVarValue(c, "muonsPt", 0)*sin(getVarValue(c, "muonsPhi", 0)) + getVarValue(c, "muonsPt", 1)*sin(getVarValue(c, "muonsPhi", 1)),\
                              getVarValue(c, "muonsPt", 0)*cos(getVarValue(c, "muonsPhi", 0)) + getVarValue(c, "muonsPt", 1)*cos(getVarValue(c, "muonsPhi", 1)))
  vars['ngoodVertices'].value = int(getVarValue(c, 'ngoodVertices'))
  events.to(eList.GetEntry(i))
  events.getByLabel(labelpf,pfhandle)
  pfc = pfhandle.product()
  vecs={}
  for t in usedPFTypes:
    vecs[t] = [] 
  for p in pfc:
    id = p.particleId()
    l = label[p.particleId()]
    p4 = p.p4()
    Et = p4.Et()
    phi = p4.phi()
    eta = p4.eta()
    occupancy[l].Fill(eta, phi)
    energy[l].Fill(eta, phi, Et)
    px = Et*cos(phi)
    py = Et*sin(phi)
    vars['MEx'].value -= px
    vars['MEy'].value -= py
    vars['nCand'].value += 1
    if l in usedPFTypes: 
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
      else:
        vars['MEx_others'].value -= px
        vars['MEy_others'].value -= py
        vars['nCand_others'].value += 1
    else:
      vars['MEx_others'].value -= px
      vars['MEy_others'].value -= py
      vars['nCand_others'].value += 1

#  MEx_control = 0.
#  MEy_control = 0.
##  print sqrt(vars['MEx_others'].value**2+ vars['MEy_others'].value**2), sqrt(vars['patMEx'].value**2+vars['patMEy'].value**2)
##  print vars.keys()
#  for k in vars.keys():
#    if k[:4]=='MEx_':
#      MEx_control+=vars[k].value
#    if k[:4]=='MEy_':
#      MEy_control+=vars[k].value
#  print "\n"
#  print "Tot.:",vars['MEx'].value, vars['MEy'].value, "(patMEx/y:",vars['patMEx'].value,vars['patMEy'].value,")",MEx_control, MEy_control
##  for cat in categories:
##    for etab in categories[cat]:
##      eb = etab[0]
##      print eb, vars['MEx_'+eb].value, vars['MEy_'+eb].value, vars['nCand_'+eb].value
  tree.Fill()
for k in pfTypes:
  occupancy[k].Scale(1./nEvents)
  energy[k].Scale(1./nEvents)
print "Writing",ofilen
ofile.cd()
tree.Write()
for k in pfTypes:
  occupancy[k].Write()
  energy[k].Write()
ofile.Close()
