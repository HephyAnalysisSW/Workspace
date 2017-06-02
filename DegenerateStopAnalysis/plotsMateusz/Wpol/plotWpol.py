from ROOT import *
from math import *
import os, sys, time, glob
from hist import *

#dir = "/home/run2/run16_v3/RunIISpring16MiniAODv2_v1/oneLep/filterW/"

dir = "/afs/hephy.at/data/mzarucki01/cmgTuples/postProcessed_mAODv2/8025_mAODv2_v7/80X_postProcessing_v0/analysisHephy_13TeV_2016_v2_4/step1/RunIISummer16MiniAODv2_v7"
outsubdir = 'HT300_ISR100/filter'

dir += "/" + outsubdir

sample = "WJetsToLNu_HT"

nb = 100
x1 = -1.
x2 = 1.
var = "cosThetaStar"
#nb = 100
#x1 = 0.
#x2 = 1000.
#var = "met_pt"

ptbins = [50.,100.,300.,500.,10000.]
etabins = [0.,1.,2.,5.]
qbins = ["neg","pos"]

weight = "weight"
#weight = "puWeight*weight"
#weight = "puReweight*weight"
cutstringbase = "ht_basJet_def>300.&&IndexJet_basJet_def>-1&&Jet_pt[IndexJet_basJet_def[0]]>100."

def getchain(tag):
    t = TChain("Events")
    
    thisdir = dir+"/"+tag
    flist = glob.glob(thisdir+"*/*.root")
    if flist == []: 
        print "WARNING: path",thisdir,"does not exist"
    
    for f in flist:
#        print f
        t.Add(f)

    return t

def book(tag,extratag):
    return h1f("H"+tag+extratag,nb,x1,x2)

def addoverflow(H):
    x1 = []
    x1.append(H.GetBinContent(nb))
    x1.append(H.GetBinError(nb))
    x2 = []
    x2.append(H.GetBinContent(nb+1))
    x2.append(H.GetBinError(nb+1))
    x3 = add(x1,x2)
    H.SetBinContent(nb,x3[0])
    H.SetBinError(nb,x3[1])
    H.SetBinContent(nb+1,0.)
    H.SetBinError(nb+1,0.)

def gethisto(tag,cutstring,weight="1.",extratag=""):
    fullcutstring = cutstring
    thisvar = var
    if True:
        print ">>>> ",tag
        print "var=", thisvar
        print "cut=", fullcutstring
        print "weight=", weight
    t.Draw(thisvar+">>H"+tag+extratag,"("+fullcutstring+")*("+weight+")","goff")
#    addoverflow(H)
#    gROOT.cd()
#    Hclone = H.Clone()
#    return Hclone
    return

def add(a1,a2):
    v = a1[0]+a2[0]
    e = sqrt( pow(a1[1],2) + pow(a2[1],2) )
    return [v,e]
    

t = getchain(sample)
f = TFile("Wpol.root","recreate")
histos = []
for iq in xrange(len(qbins)):
    for ipt in xrange(1,len(ptbins)):
        for ieta in xrange(1,len(etabins)):
            cutstringbin = "wgen_pt>{0:f}&&wgen_pt<={1:f}&&abs(wgen_eta)>={2:f}&&abs(wgen_eta)<{3:f}".format(ptbins[ipt-1],ptbins[ipt],etabins[ieta-1],etabins[ieta])
            if qbins[iq] == "neg":
                cutstringbin += "&&Sum$(GenPart_pdgId*(abs(GenPart_pdgId)==24))<0"
            else:
                cutstringbin += "&&Sum$(GenPart_pdgId*(abs(GenPart_pdgId)==24))>0"
            print cutstringbin
            cutstring = cutstringbase + "&&" + cutstringbin
            extratag = "pt{0:.0f}to{1:.0f}eta{2:.0f}to{3:.0f}W{4}".format(ptbins[ipt-1],ptbins[ipt],etabins[ieta-1],etabins[ieta],qbins[iq])

            H = book(sample,extratag)
            gethisto(sample,cutstring,weight,extratag)
            histos.append(H)

f.Write()
