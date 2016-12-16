import ROOT
import time
import itertools
import array
import operator

from math import pi, sqrt, cos, sin, sinh, cosh

from Workspace.HEPHYPythonTools.helpers import deltaR, deltaR2, deltaPhi

ROOT.gROOT.ProcessLine(".L ../../HEPHYPythonTools/scripts/root/Davismt2.cpp+")

def get_mt2(s,r,tightHardLep,tracks,met_4vec):

  mt2 = ROOT.Davismt2()

  minDR = 0.1
  # MT2 cuts for hadronic and leptonic veto tracks
  hadMT2cut = 60
  lepMT2cut = 80
  filtered_tracks = [ track for track in tracks if not ((tightHardLep[0]['charge']==track['charge']) or deltaR(tightHardLep[0],track)<minDR) ]
  #filtered_tracks = filter(lambda t:not((tightHardLep[0]['charge']==t['charge']) and deltaR(tightHardLep[0],t)<minDR) ,tracks)
  sorted_tracks = sorted(filtered_tracks, key=lambda k: k['pt'], reverse=True)
  #print sorted_tracks
  if len(sorted_tracks)>0:
    t = sorted_tracks[0]
    p1 = ROOT.TLorentzVector()
    p1.SetPtEtaPhiM(tightHardLep[0]['pt'],tightHardLep[0]['eta'],tightHardLep[0]['phi'],tightHardLep[0]['mass'])
    p2 = ROOT.TLorentzVector()
    p2.SetPtEtaPhiM(t['pt'],t['eta'],t['phi'],t['mass'])
    a=array.array('d', [ p1.M(), p1.Px(), p1.Py() ])                    
    b=array.array('d', [ p2.M(), p2.Px(), p2.Py() ])                    
    c=array.array('d', [ met_4vec.M(), met_4vec.Px(), met_4vec.Py() ])                    
    mt2.set_momenta( a, b, c )
    mt2.set_mn(0)
    s.iso_MT2 = mt2.get_mt2()
    s.iso_pt = p2.Pt()
    #print "iso_mt2:",s.iso_MT2
    if abs(t['pdgId'])>10 and abs(t['pdgId'])<14:
        s.iso_had = 0  #leptonic
        cut=lepMT2cut
    else: 
        s.iso_had = 1  #hadronic track
        cut=hadMT2cut
    if s.iso_MT2 <= cut: s.iso_Veto = False   #this will veto
    #print s.iso_Veto 
  del mt2
