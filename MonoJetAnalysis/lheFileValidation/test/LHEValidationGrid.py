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
# simple histogram-based validation of T2tt (with 4-body stop decay) LHEs
#   version for grid use (input files on SE)
#

# arguments:
#   directory (on SE)
#   comma-separated list of input files (relative to directory)

#
# simple class defining and holding pt, eta and mass histograms
#
class KinHistos:
  #
  # histogram name and binning
  #
  def __init__(self,name,binsPt=None,binsEta=None,binsM=None):
    if binsPt!=None:
      self.pt = ROOT.TH1F(name+"_pt",name+"_pt",binsPt[0],binsPt[1],binsPt[2])
    else:
      self.pt = None
    if binsEta!=None:
      self.eta = ROOT.TH1F(name+"_eta",name+"_eta",binsEta[0],binsEta[1],binsEta[2])
    else:
      self.eta = None
    if binsM!=None:
      self.m = ROOT.TH1F(name+"_m",name+"_m",binsM[0],binsM[1],binsM[2])
    else:
      self.m = None
  #
  # fill with values from a 4-vector
  #
  def fill(self,p4,absEta=True):
    if self.pt!=None:
      self.pt.Fill(p4.Pt())
    if self.eta!=None and p4.Pt()>0.001:
      eta = p4.Eta()
      if absEta:  eta = abs(eta)
      self.eta.Fill(eta)
    if self.m!=None:
      self.m.Fill(p4.M())

# filename can be xxx.lhe or xxx.lhe.gz
dirname = sys.argv[1]
filenames = sys.argv[2].split(",")

#outname = os.path.basename(dirname)
#outname += ".root"
outname = "histos.root"                    # constant output name for CRAB jobs
assert not os.path.exists(outname)
outfile = ROOT.TFile(outname,"recreate")

#
# list of histograms
#
ROOT.TH1.SetDefaultSumw2()

h_nisr = ROOT.TH1F("nisr","nisr",20,-0.5,19.5)
h_nw = ROOT.TH1F("nw","nw",20,-0.5,19.5)
h_ntop = ROOT.TH1F("ntop","ntop",20,-0.5,19.5)

h_stop = KinHistos("stop",binsPt=(200,0.,1000.),binsEta=(200,0.,5.),binsM=(200,0.,1000.))
h_blnu = KinHistos("blnu",binsPt=(200,0.,1000.),binsEta=(200,0.,5.),binsM=(250,0.,1000.))
h_lnu = KinHistos("lnu",binsPt=(200,0.,1000.),binsEta=(200,0.,5.),binsM=(200,0.,100.))
h_b = KinHistos("b",binsPt=(200,0.,1000.),binsEta=(200,0.,5.),binsM=None)
h_l = KinHistos("l",binsPt=(200,0.,1000.),binsEta=(200,0.,5.),binsM=None)
h_lsp = KinHistos("lsp",binsPt=(200,0.,1000.),binsEta=(200,0.,5.),binsM=(200,0.,1000.))
h_isr = KinHistos("isr",binsPt=(200,0.,1000.),binsEta=(200,0.,5.),binsM=(200,0.,1000.))
h_isrtot = KinHistos("isrtot",binsPt=(200,0.,1000.),binsEta=(200,0.,5.),binsM=(200,0.,1000.))
h_stopstop = KinHistos("stopstop",binsPt=(200,0.,1000.),binsEta=(200,0.,5.),binsM=(200,0.,5000.))
h_lsplsp = KinHistos("lsplsp",binsPt=(200,0.,1000.),binsEta=(200,0.,5.),binsM=(200,0.,5000.))

h_lpcosth = ROOT.TH1F("lpcosth","lpcosth",200,-1.,1.)
h_lmcosth = ROOT.TH1F("lmcosth","lmcosth",200,-1.,1.)

h_met = ROOT.TH1F("met","met",200,0.,1000.)
h_mt = ROOT.TH1F("mt","mt",200,0.,200.)

h_m2blnu_m2lnulsp = ROOT.TH2F("m2blnu_m2lnulsp","m2blnu_m2lnulsp",250,0.,1.,250,0.,1.)
h_m2bl_m2lnu = ROOT.TH2F("m2bl_m2lnu","m2bl_m2lnu",250,0.,1.,250,0.,1.)

w_decay_counts = { }
ww_decay_counts = { }


event = None
nevent = 0
inEvent = False
#
# loop over files
#
for filename in filenames:
  # copy to working directory
  os.system("xrdcp root://hephyse.oeaw.ac.at/"+dirname+"/"+filename+" "+filename)
  # verify success of copy
  if not os.path.isfile(filename):
    print "File not found :",filename
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
      # create LHEEvent object
      #
      event = LHEEvent(evlines)
      #
      # check decay kinematics
      #
      if not event.checkDecays():
        sys.exit(1)
      #
      # find stops
      #
      stops = filterByPdgId(event.particles,1000006)
      assert len(stops)==2 and stops[0].pdgId==-stops[1].pdgId
      wdecays = [ ]
      leptons = [ ]
      for i,stop in enumerate(stops):
        h_stop.fill(stop.p4())
        # all stop descendants
        stopDescendants = event.findDescendants(stop)
        tops = filterByPdgId(stopDescendants,6)
        h_ntop.Fill(len(tops))
        ws = filterByPdgId(stopDescendants,24)
        h_nw.Fill(len(ws))
        # stop "final state"
        stopFinals = filterStable(event.findDescendants(stop))
        lsps = filterByPdgId(stopFinals,1000022)
        assert len(lsps)==1
        h_lsp.fill(lsps[0].p4())
        # b from stop decay
        bs = filterByPdgId(stopFinals,5)
        assert len(bs)==1
        h_b.fill(bs[0].p4())
        # "W decay" products (stop decay - b - LSP)
        nonbs = filterByPdgIds(stopFinals,[5,1000022],invert=True)
        assert len(nonbs)==2
        nonbs.sort(key=lambda x: abs(x.pdgId))
        #
        # check leptonic decays
        #
        lepton = None
        neutrino = None
        if abs(nonbs[0].pdgId) in [11,13,15]:
          lepton = nonbs[0]
          h_l.fill(lepton.p4())
          leptons.append(lepton)
          assert abs(nonbs[1].pdgId) in [12,14,16]
          neutrino = nonbs[1]
          p4lnu = sumP4([lepton,neutrino])
          h_lnu.fill(p4lnu)
          p4blnu = sumP4([bs[0],lepton,neutrino])
          h_blnu.fill(p4blnu)
          p4bl = sumP4([bs[0],lepton])
          p4lnulsp = sumP4([lepton,neutrino,lsps[0]])
          h_m2blnu_m2lnulsp.Fill(p4blnu.M2()/175**2,p4lnulsp.M2()/stop.p4().M2())
          h_m2bl_m2lnu.Fill(p4bl.M2()/175**2,p4lnu.M2()/80**2)
          h_mt.Fill(mt(lepton.p4(),neutrino.p4()))
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
          if lepton.pdgId>0:
            h_lmcosth.Fill(cosThetaStar)
          else:
            h_lpcosth.Fill(cosThetaStar)
        #
        # create list of W-decay daughter ids (smallest abs(pdgId) non-b daughter of stop)
        #
        wdecays.append(nonbs[0].pdgId)
        if not wdecays[-1] in w_decay_counts:
          w_decay_counts[wdecays[-1]] = 0
        w_decay_counts[wdecays[-1]] += 1
      #
      # pair of W-decay daughter ids
      #
      wdecays = tuple(sorted(wdecays,reverse=True))
      if not wdecays in ww_decay_counts:
        ww_decay_counts[wdecays] = 0
      ww_decay_counts[wdecays] += 1
      #
      # stop-stop system
      #
      p4stopstop = sumP4(stops)
      h_stopstop.fill(p4stopstop)
      #
      # find lsps
      #
      lsps = filterByPdgId(event.particles,1000022,sign=True)
      assert len(lsps)==2
      #
      # lsp-lsp system
      #
      p4lsplsp = sumP4(lsps)
      h_lsplsp.fill(p4lsplsp)
      #
      # find undetectables
      #
      undetectables = filterByPdgIds(event.particles,[1000022,12,14,16])
      p4met = sumP4(undetectables)
      h_met.Fill(p4met.Pt())
      #
      # ISR
      #
      isrs = filterByPdgId(event.findPrimaries(),1000006,invert=True)
      h_nisr.Fill(len(isrs))
      for isr in isrs:
        h_isr.fill(isr.p4())
      if len(isrs)>0:
        p4IsrTot = sumP4(isrs)
        h_isrtot.fill(p4IsrTot)
    #
    # add one line to event
    #
    elif inEvent:
      evlines.append(line)
  #
  # close and remove local input file
  #
  filehandle.close()
  os.system("rm "+filename)
#
# create and fill histogram with one bin / W-decay id
#
w_decays = sorted(w_decay_counts.keys())
h_w_decays = ROOT.TH1F("w_decays","w_decays",len(w_decays),0,len(w_decays))
h_ww_decays = ROOT.TH2F("ww_decays","ww_decays",len(w_decays),0,len(w_decays),
                        len(w_decays),0,len(w_decays))
#
# create and fill histogram with one bin / W-decay-id pair
#
x_w_decays = h_w_decays.GetXaxis()
x_ww_decays = h_ww_decays.GetXaxis()
y_ww_decays = h_ww_decays.GetYaxis()
for i,k in enumerate(w_decays):
  h_w_decays.SetBinContent(i+1,w_decay_counts[k])
  x_w_decays.SetBinLabel(i+1,str(k))
  x_ww_decays.SetBinLabel(i+1,str(k))
  y_ww_decays.SetBinLabel(i+1,str(k))
  for j,l in enumerate(w_decays):
    key = tuple(sorted([k,l],reverse=True))
    if key in ww_decay_counts:
      h_ww_decays.SetBinContent(h_ww_decays.GetBin(i+1,j+1),
                                ww_decay_counts[key])
#
# fit polarization histograms
#
n_lpcosth = h_lpcosth.GetEntries()
f_lpcosth = ROOT.TF1("f_lpcosth","[0]*(1+x)*(1+x)+[1]*(1-x)*(1-x)+2*[2]*(1-x*x)",-1.,1.)
f_lpcosth.SetParameters(n_lpcosth/1000.,n_lpcosth/1000.,n_lpcosth/1000.)
h_lpcosth.Fit(f_lpcosth,"0")
#
n_lmcosth = h_lmcosth.GetEntries()
f_lmcosth = ROOT.TF1("f_lmcosth","[0]*(1+x)*(1+x)+[1]*(1-x)*(1-x)+2*[2]*(1-x*x)",-1.,1.)
f_lmcosth.SetParameters(n_lmcosth/1000.,n_lmcosth/1000.,n_lmcosth/1000.)
h_lmcosth.Fit(f_lmcosth,"0")
#
# write and close output file
#
outfile.Write()
outfile.Close()
   
