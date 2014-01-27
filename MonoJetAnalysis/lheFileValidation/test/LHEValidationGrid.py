import sys, os, copy
import re, array, gzip
import copy
from ROOT import *
from LHEUtilities import *
from math import sqrt,cos

def mt(p,q):
  return sqrt(2*p.Pt()*q.Pt()*(1-cos(p.Phi()-q.Phi())))

#
# simple histogram-based validation of T2tt (with 4-body stop decay) LHEs
#   version for grid use (input files on SE)
#

# arguments:
#   directory (on SE)
#   comma-separated list of input files (relative to directory)

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

h_stop_pt = ROOT.TH1F("stop_pt","stop_pt",200,0.,1000.)
h_blnu_pt = ROOT.TH1F("blnu_pt","blnu_pt",200,0.,1000.)
h_lnu_pt = ROOT.TH1F("lnu_pt","lnu_pt",200,0.,1000.)
h_b_pt = ROOT.TH1F("b_pt","b_pt",200,0.,1000.)
h_l_pt = ROOT.TH1F("l_pt","l_pt",200,0.,1000.)
h_lsp_pt = ROOT.TH1F("lsp_pt","lsp_pt",200,0.,1000.)
h_isr_pt = ROOT.TH1F("isr_pt","isr_pt",200,0.,1000.)
h_isrtot_pt = ROOT.TH1F("isrtot_pt","isrtot_pt",200,0.,1000.)
h_stopstop_pt = ROOT.TH1F("stopstop_pt","stopstop_pt",200,0.,1000.)
h_lsplsp_pt = ROOT.TH1F("lsplsp_pt","lsplsp_pt",200,0.,1000.)

h_stop_eta = ROOT.TH1F("stop_eta","stop_eta",200,-5.,5.)
h_blnu_eta = ROOT.TH1F("blnu_eta","blnu_eta",200,-5.,5.)
h_lnu_eta = ROOT.TH1F("lnu_eta","lnu_eta",200,-5.,5.)
h_b_eta = ROOT.TH1F("b_eta","b_eta",200,-5.,5.)
h_l_eta = ROOT.TH1F("l_eta","l_eta",200,-5.,5.)
h_lsp_eta = ROOT.TH1F("lsp_eta","lsp_eta",200,-5.,5.)
h_isr_eta = ROOT.TH1F("isr_eta","isr_eta",200,-5.,5.)
h_isrtot_eta = ROOT.TH1F("isrtot_eta","isrtot_eta",200,-5.,5.)
h_stopstop_eta = ROOT.TH1F("stopstop_eta","stopstop_eta",200,-5.,5.)
h_lsplsp_eta = ROOT.TH1F("lsplsp_eta","lsplsp_eta",200,-5.,5.)

h_stop_m = ROOT.TH1F("stop_m","stop_m",200,0.,1000.)
h_blnu_m = ROOT.TH1F("blnu_m","blnu_m",250,0.,1000.)
h_lnu_m = ROOT.TH1F("lnu_m","lnu_m",200,0.,100.)
h_lsp_m = ROOT.TH1F("lsp_m","lsp_m",200,0.,1000.)
h_isr_m = ROOT.TH1F("isr_m","isr_m",200,0.,1000.)
h_isrtot_m = ROOT.TH1F("isrtot_m","isrtot_m",200,0.,1000.)
h_stopstop_m = ROOT.TH1F("stopstop_m","stopstop_m",200,0.,5000.)
h_lsplsp_m = ROOT.TH1F("lsplsp_m","lsplsp_m",200,0.,5000.)

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
#  print "xrdcp root://hephyse.oeaw.ac.at/"+dirname+"/"+filename+" "+filename
  # copy to working directory
  os.system("xrdcp root://hephyse.oeaw.ac.at/"+dirname+"/"+filename+" "+filename)
#  os.system("ls")
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
      outgoing = event.findOutgoing()
      for p in outgoing:
        if not p.isStable():
          sump4 = sumP4(event.findDaughters(p))
          if abs(sump4.Px()-p.p4().Px())>0.001 or \
                abs(sump4.Py()-p.p4().Py())>0.001 or \
                abs(sump4.Pz()-p.p4().Pz())>0.001 or \
                abs(sump4.E()-p.p4().E())>0.001 or \
                abs(sump4.M()-p.p4().M())>0.001:
            print  "Inconsistency in decay of ",p
            print  "  incoming x,y,z,e,m = ",p.p4().Px(),p.p4().Py(),p.p4().Pz(),p.p4().E(),p.p4().M()
            print  "  outgoing x,y,z,e,m = ",sump4.Px(),sump4.Py(),sump4.Pz(),sump4.E(),sump4.M()
            sys.exit(1)

      #
      # find stops
      #
      stops = filterByPdgId(event.particles,1000006)
      assert len(stops)==2 and stops[0].pdgId==-stops[1].pdgId
      wdecays = [ ]
      leptons = [ ]
      for i,stop in enumerate(stops):
        h_stop_pt.Fill(stop.p4().Pt())
        h_stop_eta.Fill(stop.p4().Eta())
        h_stop_m.Fill(stop.p4().M())
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
        h_lsp_pt.Fill(lsps[0].p4().Pt())
        h_lsp_eta.Fill(lsps[0].p4().Eta())
        h_lsp_m.Fill(lsps[0].p4().M())
        # b from stop decay
        bs = filterByPdgId(stopFinals,5)
        assert len(bs)==1
        h_b_pt.Fill(bs[0].p4().Pt())
        h_b_eta.Fill(bs[0].p4().Eta())
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
          h_l_pt.Fill(lepton.p4().Pt())
          h_l_eta.Fill(lepton.p4().Eta())
          leptons.append(lepton)
          assert abs(nonbs[1].pdgId) in [12,14,16]
          neutrino = nonbs[1]
          p4lnu = sumP4([lepton,neutrino])
          h_lnu_pt.Fill(p4lnu.Pt())
          h_lnu_eta.Fill(p4lnu.Eta())
          h_lnu_m.Fill(p4lnu.M())
          p4blnu = sumP4([bs[0],lepton,neutrino])
          h_blnu_pt.Fill(p4blnu.Pt())
          h_blnu_eta.Fill(p4blnu.Eta())
          h_blnu_m.Fill(p4blnu.M())
          p4bl = sumP4([bs[0],lepton])
          p4lnulsp = sumP4([lepton,neutrino,lsps[0]])
          h_m2blnu_m2lnulsp.Fill(p4blnu.M2()/175**2,p4lnulsp.M2()/stop.p4().M2())
          h_m2bl_m2lnu.Fill(p4bl.M2()/175**2,p4lnu.M2()/80**2)
          h_mt.Fill(mt(lepton.p4(),neutrino.p4()))
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
      h_stopstop_pt.Fill(p4stopstop.Pt())
      if p4stopstop.Pt()>0.001:
        h_stopstop_eta.Fill(p4stopstop.Eta())
      h_stopstop_m.Fill(p4stopstop.M())
      #
      # find lsps
      #
      lsps = filterByPdgId(event.particles,1000022,sign=True)
      assert len(lsps)==2
      #
      # lsp-lsp system
      #
      p4lsplsp = sumP4(lsps)
      h_lsplsp_pt.Fill(p4lsplsp.Pt())
      h_lsplsp_eta.Fill(p4lsplsp.Eta())
      h_lsplsp_m.Fill(p4lsplsp.M())
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
        h_isr_pt.Fill(isr.p4().Pt())
        h_isr_eta.Fill(isr.p4().Eta())
        h_isr_m.Fill(isr.p4().M())
      if len(isrs)>0:
        p4IsrTot = sumP4(isrs)
        h_isrtot_pt.Fill(p4IsrTot.Pt())
        h_isrtot_eta.Fill(p4IsrTot.Eta())
        h_isrtot_m.Fill(p4IsrTot.M())
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
# write and close output file
#
outfile.Write()
outfile.Close()
   
