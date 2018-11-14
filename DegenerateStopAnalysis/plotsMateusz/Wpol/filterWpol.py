from math import *
import os, sys, time, getopt
import array
from ROOT import *

#infile = "/data/run2/run16_v10/RunIISpring16MiniAODv2_v3/skimPreselect/filter/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1_Chunks_1_2_0.root"
#outfile = "filterWpol.root"

if len(sys.argv)>1: infile = sys.argv[1]
if len(sys.argv)>2: outfile = sys.argv[2]

newvars = ["cosThetaStar","wgen_pt","wgen_eta"]

strstr = "struct newvars_t {"

for var in newvars:
    strstr += "Double_t "+var+";"

strstr += "}"
gROOT.ProcessLine(strstr)
nv = newvars_t()

def boostlep(lep,W):
    beta = W.BoostVector()
    lepWRF = lep
    lepWRF.Boost(-beta)
    return lepWRF

def costh(lepWRF,W):
    return cos(lepWRF.Angle(W.Vect()))

def dofilter(infile,outfile):
    infilename = infile
    outfilename = outfile
    f = TFile(infilename)
    t = f.Get("Events")
    t.SetBranchStatus("*", 1)

    g = TFile(outfilename,"recreate")
    a = t.CloneTree(0)
    for brnew in newvars:
        a.Branch(brnew,AddressOf(nv,brnew),brnew+"/D")

    print t.GetEntries()
    for i in xrange(t.GetEntries()):
#        if i>10: break
        if not i%1000000: print i,time.strftime('%X %x %Z')
        t.GetEntry(i)

        for var in newvars:
            exec('nv.'+var+' = -999.')
            
        W = TLorentzVector(1e-9,1e-9,1e-9,1e-9)
        lep = TLorentzVector(1e-9,1e-9,1e-9,1e-9)
        
        
#        print "event",t.evt,"--------------------------------------"
        for igp in xrange(t.nGenPart):
#            print t.GenPart_pdgId[igp],t.GenPart_pt[igp],t.GenPart_eta[igp],t.GenPart_phi[igp],t.GenPart_mass[igp]
            if abs(t.GenPart_pdgId[igp])==24:
#                print t.GenPart_pdgId[igp],t.GenPart_pt[igp],t.GenPart_eta[igp],t.GenPart_phi[igp],t.GenPart_mass[igp]
                W.SetPtEtaPhiM(t.GenPart_pt[igp],t.GenPart_eta[igp],t.GenPart_phi[igp],t.GenPart_mass[igp])
                nv.wgen_pt = t.GenPart_pt[igp]
                nv.wgen_eta = t.GenPart_eta[igp]
            if abs(t.GenPart_pdgId[igp]) in [11,13] and abs(t.GenPart_motherId[igp])==24:
#                print t.GenPart_pdgId[igp],t.GenPart_pt[igp],t.GenPart_eta[igp],t.GenPart_phi[igp],t.GenPart_mass[igp]
                lep.SetPtEtaPhiM(t.GenPart_pt[igp],t.GenPart_eta[igp],t.GenPart_phi[igp],t.GenPart_mass[igp])

#        W.Print()
#        lep.Print()
                
        if W.Pt() > 1.e-8 and lep.Pt() > 1.e-8:
            lepWRF = boostlep(lep,W)
            nv.cosThetaStar = costh(lepWRF,W)
#            lepWRF.Print()
            
            a.Fill()

    g.cd()

    a.Write()
    g.Close()
    f.Close()

print 'start time:',time.strftime('%X %x %Z')  
dofilter(infile,outfile) 
print 'end time:',time.strftime('%X %x %Z')  
