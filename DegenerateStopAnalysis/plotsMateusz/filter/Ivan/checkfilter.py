from ROOT import *
from math import *
import os, sys

fname = '/data/imikulec/gen15/tree.root'

f = TFile(fname)
t = f.Get('tree')


def getgenmet(e):
    psum =  TLorentzVector(1e-9,1e-9,1e-9,1e-9)
    for igp in xrange(e.ngenPartAll):
#        if e.genPartAll_status[igp] in [22,23] and (e.genPartAll_motherId[igp] == 2212 or e.genPartAll_grandmotherId[igp] == 2212):
        if e.genPartAll_status[igp] == 1 and abs(e.genPartAll_motherId[igp]) == 1000006 and abs(e.genPartAll_pdgId[igp]) in [12,14,16,1000022]:
            aux = TLorentzVector(1e-9,1e-9,1e-9,1e-9)
            aux.SetPtEtaPhiM(e.genPartAll_pt[igp],e.genPartAll_eta[igp],e.genPartAll_phi[igp],e.genPartAll_mass[igp])
            psum = psum + aux
    return psum.Pt()
    
def getmaxgenpt(e):
    maxpt = 0.
    for igp in xrange(e.ngenPartAll):
        if e.genPartAll_status[igp] in [23,71,73] and not abs(e.genPartAll_pdgId[igp]) in [12,14,16,1000022]:
            if e.genPartAll_pt[igp] > maxpt:
                maxpt = e.genPartAll_pt[igp]
    return maxpt
    
def getstopsumpt(e):
    psum =  TLorentzVector(1e-9,1e-9,1e-9,1e-9)
    for igp in xrange(e.ngenPartAll):
        if e.genPartAll_status[igp] == 62 and abs(e.genPartAll_pdgId[igp]) == 1000006:
            aux = TLorentzVector(1e-9,1e-9,1e-9,1e-9)
            aux.SetPtEtaPhiM(e.genPartAll_pt[igp],e.genPartAll_eta[igp],e.genPartAll_phi[igp],e.genPartAll_mass[igp])
            psum = psum + aux
    return psum.Pt()

def getgenht(e):
    psum =  TLorentzVector(1e-9,1e-9,1e-9,1e-9)
    for igp in xrange(e.ngenPartAll):
        if e.genPartAll_status[igp] in [1,2] and not abs(e.genPartAll_pdgId[igp]) in [12,14,16,1000022]:
            aux = TLorentzVector(1e-9,1e-9,1e-9,1e-9)
            aux.SetPtEtaPhiM(e.genPartAll_pt[igp],e.genPartAll_eta[igp],e.genPartAll_phi[igp],e.genPartAll_mass[igp])
            psum = psum + aux
    return psum.Pt()

Hall = TH1F('Hall','',1000,0,1000)
Hsel = TH1F('Hsel','',1000,0,1000)
Hdif = TH1F('Hdif','',1000,-500,500)

Hall2 = TH1F('Hall2','',1000,0,1000)
Hsel2 = TH1F('Hsel2','',1000,0,1000)
Hdif2 = TH1F('Hdif2','',1000,-500,500)

Hall3 = TH1F('Hall3','',1000,0,1000)
Hsel3 = TH1F('Hsel3','',1000,0,1000)
Hdif3 = TH1F('Hdif3','',1000,-500,500)

Hall4 = TH1F('Hall4','',1000,0,1000)
Hsel4 = TH1F('Hsel4','',1000,0,1000)
Hdif4 = TH1F('Hdif4','',1000,-500,500)



for ie,e in enumerate(t):
    mygenmet = getgenmet(e)
    Hall.Fill(mygenmet)
    Hall2.Fill(e.met_genPt)
    Hdif.Fill(e.met_pt-mygenmet)
    Hdif2.Fill(e.met_genPt-mygenmet)
    if e.met_pt>200.:
        Hsel.Fill(mygenmet)
        Hsel2.Fill(e.met_genPt)
        
    maxpt = getmaxgenpt(e)
    Hall3.Fill(maxpt)
    if e.nJet>0:
        Hdif3.Fill(e.Jet_pt[0]-maxpt)
        if e.Jet_pt[0]>110.:
            Hsel3.Fill(maxpt)
            
#    stopsumpt = getgenht(e)
    stopsumpt = getstopsumpt(e)
    Hall4.Fill(stopsumpt)
    Hdif4.Fill(e.htJet40-stopsumpt)
    if e.htJet40>300:
        Hsel4.Fill(stopsumpt)
    
Hall3.Draw()
Hsel3.SetLineColor(2)
Hsel3.Draw('same')
gPad.Update()
    
