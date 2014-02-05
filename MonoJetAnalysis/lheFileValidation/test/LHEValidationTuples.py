import sys, os, copy
import re, array, gzip
import copy
from ROOT import *
from LHEUtilities import *
from math import sqrt,cos

#
# transverse mass from 2 4-vectors
#
def mt(p,q):
  return sqrt(2*p.Pt()*q.Pt()*(1-cos(p.Phi()-q.Phi())))

#
# copy components between two  TLorentzVectors
#   (avoids creating a new object)
#
def setP4(a,b):
  a.SetVect(b.Vect())
  a.SetE(b.E())
#
# create tuples with 4-vectors + additional event info from LHE files
#

# arguments:
#   directory (on SE)
#   comma-separated list of input files (relative to directory)


# filename can be xxx.lhe or xxx.lhe.gz
dirname = sys.argv[1]
filenames = sys.argv[2].split(",")

#outname = os.path.basename(dirname)
#outname += ".root"
outname = "tuples.root"                    # constant output name for CRAB jobs
#assert not os.path.exists(outname)
outfile = ROOT.TFile(outname,"recreate")

#
# list of histograms
#
ROOT.TH1.SetDefaultSumw2()
#
# variables
#   all stop-related entries have index 1 or 2
#   with index 1 corresponding to pdgId = -1000006
#

# nisr, ntop, nw
counts = array.array('i', [0]*3 )
# met
mets = array.array('f', [0.] )
# mt, costh (only for leptonic "W" decays
mts = array.array('f', [0.]*2 )
cosths = array.array('f', [0.]*2 )

# pdgIds of the "W" decay products
#   "f" corresponds to the lower |pdgId|,
#   "fprime" to the second quark or the neutrino
fids = array.array('i',[0]*2)
fprimeids = array.array('i',[0]*2)

# 4-vectors of the (first two) ISR jets, the stops,
# the bs, the f and f's and the lsps
tp4Isrs = [ ]
tp4Stops = [ ]
tp4Bs = [ ]
tp4Fs = [ ]
tp4Fprimes = [ ]
tp4Lsps = [ ]
for i in range(2):
  tp4Isrs.append(ROOT.TLorentzVector())
  tp4Stops.append(ROOT.TLorentzVector())
  tp4Bs.append(ROOT.TLorentzVector())
  tp4Fs.append(ROOT.TLorentzVector())
  tp4Fprimes.append(ROOT.TLorentzVector())
  tp4Lsps.append(ROOT.TLorentzVector())
#
# create tree
#
tree = ROOT.TTree("lhe","lhe")
tree.Branch("counts",counts,"nisr/I:ntop/I:nw/I")
tree.Branch("met",mets,"met/F")
tree.Branch("mts",mts,"mt1/F:mt2/F")
tree.Branch("cosths",cosths,"costh1/F:costh2/F")
tree.Branch("fids",fids,"f1Id/I:f2Id/I")
tree.Branch("fprimeids",fprimeids,"fprime1Id/I:fprime2Id/I")
tree.Branch("stop1","TLorentzVector",tp4Stops[0],32000,1)
tree.Branch("stop2","TLorentzVector",tp4Stops[1],32000,1)
tree.Branch("b1","TLorentzVector",tp4Bs[0],32000,1)
tree.Branch("b2","TLorentzVector",tp4Bs[1],32000,1)
tree.Branch("f1","TLorentzVector",tp4Fs[0],32000,1)
tree.Branch("f2","TLorentzVector",tp4Fs[1],32000,1)
tree.Branch("fprime1","TLorentzVector",tp4Fprimes[0],32000,1)
tree.Branch("fprime2","TLorentzVector",tp4Fprimes[1],32000,1)
tree.Branch("lsp1","TLorentzVector",tp4Lsps[0],32000,1)
tree.Branch("lsp2","TLorentzVector",tp4Lsps[1],32000,1)
tree.Branch("isr1","TLorentzVector",tp4Isrs[0],32000,1)
tree.Branch("isr2","TLorentzVector",tp4Isrs[1],32000,1)
#
# initialization
#
event = None
nevent = 0
inEvent = False
#
# loop over files
#
localFiles = None
for fn in filenames:
  #
  # try two file sources (local and via rootd)
  #
  found = False
  if localFiles==None or localFiles==True:
    # try to use a local directory
    found = os.path.isfile(dirname+"/"+fn)
    if found:
      if localFiles==None:
        localFiles = True
      filename = dirname+"/"+fn
  if localFiles==False or ( not found ):
    # try copy from SE to working directory
    os.system("xrdcp root://hephyse.oeaw.ac.at/"+dirname+"/"+fn+" "+fn)
    found = os.path.isfile(fn)
    if found:
      if localFiles==None:
        localFiles = False
      filename = fn
  if not found:
    print "File not found :",fn
    sys.exit(1)
  # open file (via gzip, if necessary)
  print 'opening file ',filename
  if filename[-3:] == ".gz":
    filehandle = gzip.open(filename)
  else:
    filehandle = open(filename)
  #
  # loop over lines
  #
  for line in filehandle.readlines():
    line = line[:-1]
    #
    # start of event block
    #
    if( re.match('\<event\>', line) ):
      inEvent = True
      evlines = [ ]
      nevent+=1
    #
    # end of event block - process event
    #
    elif re.match('\<\/event\>',line):
      inEvent = False
      if (nevent%10000)==0:
        print "Creating event ",nevent
      #
      # reset inputs
      #
      for i in range(len(counts)):
        counts[i] = 0
      mets[0] = -999.
      for i in range(2):
        mts[i] = -999.
        cosths[i] = -999.
        tp4Stops[i] *= 0
        tp4Bs[i] *= 0
        tp4Fs[i] *= 0
        fids[i] = 0
        tp4Fprimes[i] *= 0
        fprimeids[i] = 0
        tp4Lsps[i] *= 0
        tp4Isrs[i] *= 0
      #
      # create LHEEvent object
      #
      event = LHEEvent(evlines)
#      #
#      # check decay kinematics
#      #
#      if not event.checkDecays():
#        sys.exit(1)
      #
      # find stops and sort by pdgId
      #
      stops = filterByPdgId(event.particles,1000006)
      assert len(stops)==2 and stops[0].pdgId==-stops[1].pdgId
      stops.sort(key=lambda p: p.pdgId)
      
      for i,stop in enumerate(stops):
        setP4(tp4Stops[i],stop.p4())
        # all stop descendants
        stopDescendants = event.findDescendants(stop)
        tops = filterByPdgId(stopDescendants,6)
        counts[1] += len(tops)
        ws = filterByPdgId(stopDescendants,24)
        counts[2] += len(ws)
        # stop "final state"
        stopFinals = filterStable(event.findDescendants(stop))
        lsps = filterByPdgId(stopFinals,1000022)
        assert len(lsps)==1
        setP4(tp4Lsps[i],lsps[0].p4())
        # b from stop decay
        bs = filterByPdgId(stopFinals,5)
        assert len(bs)==1
        setP4(tp4Bs[i],bs[0].p4())
        # "W decay" products (stop decay - b - LSP)
        nonbs = filterByPdgIds(stopFinals,[5,1000022],invert=True)
        assert len(nonbs)==2
        nonbs.sort(key=lambda x: abs(x.pdgId))
        setP4(tp4Fs[i],nonbs[0].p4())
        fids[i] = nonbs[0].pdgId
        setP4(tp4Fprimes[i],nonbs[1].p4())
        fprimeids[i] = nonbs[1].pdgId
        #
        # check leptonic decays
        #
        lepton = None
        neutrino = None
        if abs(nonbs[0].pdgId) in [11,13,15]:
          lepton = nonbs[0]
          assert abs(nonbs[1].pdgId) in [12,14,16]
          neutrino = nonbs[1]
          p4lnu = sumP4([lepton,neutrino])
          p4blnu = sumP4([bs[0],lepton,neutrino])
          mts[i] = mt(lepton.p4(),neutrino.p4())
          #
          # polarization
          #
          # boost "W" to "top" rest system
          boostBlnu = -p4blnu.BoostVector()
          p4lnuBoostBlnu = p4lnu.Clone()
          p4lnuBoostBlnu.Boost(boostBlnu)
          # boost lepton to "W" rest system
          boostLnu = -p4lnu.BoostVector()
          p4lBoostLnu = lepton.p4().Clone()
          p4lBoostLnu.Boost(boostLnu)
          # angle between lepton in "W" rest system and
          #   "W" direction in "top" rest system
          p3lnuBoostBlnu = p4lnuBoostBlnu.Vect().Unit()
          p3lBoostLnu = p4lBoostLnu.Vect().Unit()
          cosThetaStar = p3lnuBoostBlnu.Dot(p3lBoostLnu)
          cosths[i] = cosThetaStar
      #
      # find undetectables
      #
      undetectables = filterByPdgIds(event.particles,[1000022,12,14,16])
      p4met = sumP4(undetectables)
      mets[0] = p4met.Pt()
      #
      # ISR
      #
      isrs = filterByPdgId(event.findPrimaries(),1000006,invert=True)
      isrs.sort(key=lambda p: p.p4().Pt(),reverse=True)
      counts[0] = len(isrs)
      for i in range(min(2,len(isrs))):
        setP4(tp4Isrs[i],isrs[i].p4())
      #
      # fill
      #
      tree.Fill()
    #
    # add one line to event
    #
    elif inEvent:
      evlines.append(line)
  #
  # close and remove local input file
  #
  filehandle.close()
  if localFiles==False:
    os.system("rm "+filename)
#
# write and close output file
#
outfile.Write()
outfile.Close()
   
