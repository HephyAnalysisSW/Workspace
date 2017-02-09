import ROOT
import pickle
import sys, os, copy, random, subprocess, datetime
from array import array
from Workspace.RA4Analysis.cmgObjectSelection import cmgLooseLepIndices, splitIndList, get_cmg_jets_fromStruct, splitListOfObjects, cmgTightMuID, cmgTightEleID , get_cmg_genParts_fromStruct , get_cmg_JetsforMEt_fromStruct , get_cmg_genLeps , get_cmg_genTaus
from Workspace.HEPHYPythonTools.xsec import xsec
from Workspace.HEPHYPythonTools.convertHelpers import compileClass, readVar, printHeader, typeStr, createClassString

from math import *
from Workspace.HEPHYPythonTools.user import username

from Workspace.HEPHYPythonTools.helpers import *
from Workspace.RA4Analysis.cmgTuples_Summer16_Moriond2017_MiniAODv2 import *
from btagEfficiency import *
import time, hashlib

ptBorders = [20,30, 50, 70, 100, 140, 200, 300, 600, 1000]
ptBins = [[0,20],[20,30],[30,50],[50,70],[70,100],[100,140],[140,200],[200,300],[300,600],[600,1000],[1000,-1]]
etaBorders = [0.8,1.6,2.4]
etaBins = [[0,0.8], [0.8,1.6], [ 1.6, 2.4]]

def getBTagMCTruthEfficiencies2D(c, cut="(1)"):
    from array import array
    mceff = {}
    if cut and cut.replace(" ","")!= "(1)":
        print "Setting Event List with cut: %s"%cut
        eListName = "eList_%s"%hashlib.md5("%s"%time.time()).hexdigest()
        c.Draw(">>%s"%eListName,cut)
        c.SetEventList( getattr(ROOT,eListName))

    passed_hists = {}
    total_hists = {}
    ratios = {}

    btag_var = "Jet_btagCSV"
    btag_wp  = "0.8484"
    jet_quality_cut = "Jet_id>0"

    flavor_cuts = {
                        'b':'abs(Jet_hadronFlavour)==5',
                        'c':'abs(Jet_hadronFlavour)==4',
                        'other':'(abs(Jet_hadronFlavour) < 4  || abs(Jet_hadronFlavour) > 5)',
                   }

    flavors = flavor_cuts.keys()

    for flavor in flavors:
        passed_name = 'passed_%s'%flavor
        passed_hists[flavor] = ROOT.TH2D( passed_name, passed_name , len(ptBorders)-1, array('d',ptBorders), len(etaBorders)-1, array('d', etaBorders) )
        total_name = 'total_%s'%flavor
        total_hists[flavor] = ROOT.TH2D( total_name, total_name , len(ptBorders)-1, array('d',ptBorders), len(etaBorders)-1, array('d', etaBorders) )
        c.Draw("abs(Jet_eta):Jet_pt>>%s"%passed_name, ' && '.join("(%s)"%x for x in [cut,jet_quality_cut, flavor_cuts[flavor], '%s>%s'%(btag_var, btag_wp)]))
        #c.Draw("abs(Jet_eta):Jet_pt>>%s"%total_name, ' && '.join("(%s)"%x for x in [cut,jet_quality_cut, flavor_cuts[flavor], '%s<%s'%(btag_var, btag_wp)]))
        c.Draw("abs(Jet_eta):Jet_pt>>%s"%total_name, ' && '.join("(%s)"%x for x in [cut,jet_quality_cut, flavor_cuts[flavor] ]))
        ratios[flavor] = passed_hists[flavor].Clone("ratio_%s"%flavor)
        ratios[flavor].Divide( total_hists[flavor])

    print ptBins
    print etaBins
    for ipt, ptBin in enumerate( ptBins ,1):
        mceff[tuple(ptBin)]={}
        for jeta, etaBin in enumerate( etaBins ,1):
            mceff[tuple(ptBin)][tuple(etaBin)] = {}
            for flavor in flavors:
                mceff[tuple(ptBin)][tuple(etaBin)][flavor] = ratios[flavor].GetBinContent(ipt, jeta)

    #return passed_hists, total_hists, ratios
    return mceff



singleLeptonic = "Sum$((abs(LepGood_pdgId)==13&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.2&&LepGood_mediumMuonId==1&&LepGood_sip3d<4.0)||(abs(LepGood_pdgId)==11&&LepGood_pt>=25&&abs(LepGood_eta)<2.4&&LepGood_miniRelIso<0.1&&LepGood_eleCBID_SPRING15_25ns_ConvVetoDxyDz==4))==1"

leptonVeto = '((abs(LepGood_pdgId)==11&&((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10&&abs(LepGood_eta)<2.4)&&LepGood_miniRelIso<0.4)==0&&(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<2.4))==1))\
             ||(abs(LepGood_pdgId)==13&&((Sum$(abs(LepGood_pdgId)==13&&LepGood_pt>=10&&abs(LepGood_eta)<2.4)&&LepGood_miniRelIso<0.4)==1&&(Sum$(abs(LepGood_pdgId)==11&&LepGood_pt>=10&&abs(LepGood_eta)<2.4))==0)))'




stStr = 'Sum$(LepGood_pt[0]+met_pt)'

htStr = 'Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))'
btagStr = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>0.8484)'
njetStr = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)'
cut_WW = "Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000024&&abs(GenPart_grandmotherId)==1000021)==2&&(Sum$(abs(GenPart_pdgId)==24)==2)"

#presel = singleLeptonic+'&&'+leptonVeto+'&&'+njetStr+'>2&&'+stStr+'>250&&'+htStr+'>500&&Jet_pt[1]>80&&'+cut_WW
presel = singleLeptonic + '&&' + leptonVeto + '&&' + njetStr+'>2&&'+stStr+'>250&&'+htStr+'>500'

wjetsSamples = [
            WJetsToLNu_HT1200to2500,
            WJetsToLNu_HT2500toInf,
            WJetsToLNu_HT400to600,
            WJetsToLNu_HT600to800,
            WJetsToLNu_HT800to1200,
            ]

ttjetsSamples = [
            TTJets_DiLepton,
            TTJets_LO_HT1200to2500,
            TTJets_LO_HT2500toInf,
            TTJets_LO_HT600to800,
            TTJets_LO_HT800to1200,
            TTJets_SingleLeptonFromT,
            TTJets_SingleLeptonFromTbar
            ]



ttjetsChunks = []
wjetsChunks = []

for sample in ttjetsSamples:
    ch, sw = getChunks(sample)
    ttjetsChunks.append(ch)

ttjetsChunksAll = [ x[0] for x in ttjetsChunks ]
cTT = getChain(ttjetsChunksAll, histname='', treeName='tree')

for sample in wjetsSamples:
    ch, sw = getChunks(sample)
    wjetsChunks.append(ch)

wjetsChunksAll = [ x[0] for x in wjetsChunks ]
cW = getChain(wjetsChunksAll, histname='', treeName='tree')

effTT = getBTagMCTruthEfficiencies2D(cTT, cut=presel)
effW = getBTagMCTruthEfficiencies2D(cW, cut=presel)

effs = {}
effs['TTJets'] = effTT
effs['WJets'] = effW
effs['none']    = getDummyEfficiencies()

dataDir = '/afs/hephy.at/data/dspitzbart02/RA4/btagEfficiency/'
bTagEffFile = dataDir + 'Moriond17.pkl'

pickle.dump(effs, file(bTagEffFile,'w'))
#ttjetsChunksAll = sum(ttjetsChunks)
#cTT = 


#chunks1, sumweight1 = getChunks(SMS_T5qqqqVV_TuneCUETP8M1_v1)
#chunks2, sumweight2 = getChunks(SMS_T5qqqqVV_TuneCUETP8M1_v2)
#allChunks = chunks1+chunks2
#
#cSignal = getChain(allChunks, histname='', treeName='tree')

#cSignal = getChain(chunks1[0:100], histname='', treeName='tree')

#massPoints = pickle.load(file('/afs/hephy.at/data/easilar01/Ra40b/pickleDir/T5qqqqWW_mass_nEvents_xsec_pkl'))
#
#allMassPoints = []
#
#for mgluino in massPoints.keys():
#  for mneutralino in massPoints[mgluino]:
#    allMassPoints.append((mgluino,mneutralino))
#
#deltaM = [1000,800,600,400,200,0]
#
#massPointDict = {}
#
#for dM in deltaM:
#  massPointDict[dM] = []
#
#for massPoint in allMassPoints:
#  for dM in deltaM:
#    if dM < (massPoint[0]-massPoint[1]): break
#  massPointDict[dM].append(massPoint)
#
#debug = False
#
#binBorders = [0,1000000]
##binBorders = [0,100000]
##if debug: binBorders = [0,5]
#bins = []
#
#for i,b in enumerate(binBorders):
#  lowerBound = binBorders[i]
#  print i
#  if i>len(binBorders)-2: upperBound = -1
#  else: upperBound = binBorders[i+1]
#  bins.append((lowerBound, upperBound))
#
#effs = {}
#
#for i,b in enumerate(bins):
#  print 'Measuring efficiencies for (mgl-mN) in',b
#  massWindowCut = '(GenSusyMGluino-GenSusyMNeutralino)>='+str(b[0])
#  if b[1]>0: massWindowCut += '&&(GenSusyMGluino-GenSusyMNeutralino)<'+str(b[1])
#  cut = presel + '&&' + massWindowCut
#  print 'Using this mass window cut',massWindowCut
#  #print cut
#  effs[b] = getBTagMCTruthEfficiencies2D(cSignal, cut = cut)
#  pickle.dump(effs, file('/data/dspitzbart/Spring16/btagEfficiency/FS_intermediate_pkl','w'))
#  print effs[b]
#  #if debug:
#  #  if i>0: break
#    
#
#pickle.dump(effs, file('/data/dspitzbart/Spring16/btagEfficiency/FS_full_pkl','w'))
#
#effs_update = {}
#for b in enumerate(bins):
#  newKey = 'Signal_deltaM_'
#  newKey += str(b[0])
#  if b[1]>0: newKey += 'to'+str(b[1])
#  else: newKey += 'plus'
#  effs_update[newKey] = effs[b]
#
#pickle.dump(effs_update, file('/data/dspitzbart/Spring16/btagEfficiency/FS_full_pkl','w'))
