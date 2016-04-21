import ROOT
import sys, os, copy, random, subprocess, datetime
from array import array
from Workspace.HEPHYPythonTools.xsec import xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getObjDict, getFileList
#from Workspace.RA4Analysis.cmgObjectSelection import cmgLooseLepIndices,ele_ID_eta, splitIndList, get_cmg_jets_fromStruct, splitListOfObjects
#from Workspace.RA4Analysis.convertHelpers import compileClass, readVar, printHeader, typeStr, createClassString
from Workspace.DegenerateStopAnalysis.cmgObjectSelection import cmgLooseLepIndices,ele_ID_eta, splitIndList, get_cmg_jets_fromStruct, splitListOfObjects, isGoodLepton
from Workspace.HEPHYPythonTools.convertHelpers import compileClass, readVar, printHeader, typeStr, createClassString
from Workspace.HEPHYPythonTools.helpers import  getChunks, deltaR, deltaR2, invMass
from math import *
from Workspace.HEPHYPythonTools.user import username,afsDataName

#from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_25ns import *
#from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_packedGenPart_tracks import *
#from Workspace.DegenerateStopAnalysis.cmgTuples_Data25ns import *
#from Workspace.DegenerateStopAnalysis.cmgTuples_Data25ns_fromArtur import *
from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_7412pass2 import *
import time
#from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_50ns import *
#from Workspace.DegenerateStopAnalysis.cmgTuples_Data50ns_1l import *
#from Workspace.DegenerateStopAnalysis.cmgTuples_Spring15_v1 import *

target_lumi = 10000 #pb-1
lepton_soft_hard_cut  = 30
tracks = True
pkdGenParts = False
verbose = False
break_for_debug = False
defSampleStr = "T2DegStop_300_270"
subDir = "postProcessed_7412pass2_test"


ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()



#branchKeepStrings = ["run", "lumi", "evt", "isData", "xsec", "puWeight", "nTrueInt", "genWeight", "rho", "nVert", "nJet25", "nBJetLoose25", "nBJetMedium25", "nBJetTight25", "nJet40", "nJet40a", "nBJetLoose40", "nBJetMedium40", "nBJetTight40", 
#                     "nLepGood20", "nLepGood15", "nLepGood10",  
#                     "GenSusyMScan1", "GenSusyMScan2", "GenSusyMScan3", "GenSusyMScan4", "GenSusyMGluino", "GenSusyMGravitino", "GenSusyMStop", "GenSusyMSbottom", "GenSusyMStop2", "GenSusyMSbottom2", "GenSusyMSquark", "GenSusyMNeutralino", "GenSusyMNeutralino2", "GenSusyMNeutralino3", "GenSusyMNeutralino4", "GenSusyMChargino", "GenSusyMChargino2", 
#                     "htJet25", "mhtJet25", "htJet40j", "htJet40", "mhtJet40", "nSoftBJetLoose25", "nSoftBJetMedium25", "nSoftBJetTight25", 
#                     "met_*","Flag_*",
#                     "nFatJet","FatJet_*", 
#                     "nLepOther", "LepOther_*", "nLepGood", "LepGood_*", "ngenLep", "genLep_*", "nTauGood", "TauGood_*", 
#                     "nGenPart", "GenPart_*","ngenPartAll","genPartAll_*" ,"ngenTau", "genTau_*", "nJet", "Jet_*", "ngenLepFromTau", "genLepFromTau_*",
#                      ]
                      
#"nGenP6StatusThree", "GenP6StatusThree_*", "nGenTop", "GenTop_*"




#branches to be kept for data and MC
branchKeepStrings_DATAMC = ["run", "lumi", "evt", "isData", "rho", "nVert", 
                     "nJet25", "nBJetLoose25", "nBJetMedium25", "nBJetTight25", "nJet40", "nJet40a", "nBJetLoose40", "nBJetMedium40", "nBJetTight40", 
                     "nLepGood20", "nLepGood15", "nLepGood10", "htJet25", "mhtJet25", "htJet40j", "htJet40", "mhtJet40", "nSoftBJetLoose25", "nSoftBJetMedium25", "nSoftBJetTight25", 
                     "met*","puppi*","Flag_*","HLT_*",
#                     "nFatJet","FatJet_*", 
                     "nJet", "Jet_*", 
                     "nLepGood", "LepGood_*", 
                     "nLepOther", "LepOther_*", 
                     "nTauGood", "TauGood_*",
                     "track_*", "isoTrack_*",
                     ] 
if tracks:
  #branchKeepStrings_DATAMC.extend(["track_*","isoTrack_*"])
  trackMinPtList= [1,1.5,2,2.5,3]

#branches to be kept for MC samples only
branchKeepStrings_MC = [ "nTrueInt", "genWeight", "xsec", "puWeight", 
                     "GenSusyMScan1", "GenSusyMScan2", "GenSusyMScan3", "GenSusyMScan4", "GenSusyMGluino", "GenSusyMGravitino", "GenSusyMStop", "GenSusyMSbottom", "GenSusyMStop2", "GenSusyMSbottom2", "GenSusyMSquark", "GenSusyMNeutralino", "GenSusyMNeutralino2", "GenSusyMNeutralino3", "GenSusyMNeutralino4", "GenSusyMChargino", "GenSusyMChargino2", 
                     "ngenLep", "genLep_*", 
                     "nGenPart", "GenPart_*",
                     "ngenPartAll","genPartAll_*" ,
                     "ngenTau", "genTau_*", 
                     "ngenLepFromTau", "genLepFromTau_*", 
                     "GenJet_*",
                      ]

if pkdGenParts:
  branchKeepStrings_MC.extend(["genPartPkd_*"])
  genPartMinPtList= [1,1.5,2]

#branches to be kept for data only
branchKeepStrings_DATA = []




from optparse import OptionParser
parser = OptionParser()
parser.add_option("--samples", dest="allsamples", default=defSampleStr, type="string", action="store", help="samples:Which samples.")
parser.add_option("--inputTreeName", dest="inputTreeName", default="treeProducerSusySingleLepton", type="string", action="store", help="samples:Which samples.")
#parser.add_option("--targetDir", dest="targetDir", default="/data/"+username+"/cmgTuples/"+subDir+'/', type="string", action="store", help="target directory.")
parser.add_option("--targetDir", dest="targetDir", default="/afs/hephy.at/data/%s"%afsDataName+"/cmgTuples/"+subDir+'/', type="string", action="store", help="target directory.")
parser.add_option("--skim", dest="skim", default="", type="string", action="store", help="any skim condition?")
parser.add_option("--leptonSelection", dest="leptonSelection", default="inc", type="string", action="store", help="which lepton selection? 'soft', 'hard', 'inc', 'dilep'?")
parser.add_option("--preselect", dest="preselect", action="store_true", help="Apply preselection for the postprocessing")
parser.add_option("--small", dest="small", default = False, action="store_true", help="Just do a small subset.")
#parser.add_option("--overwrite", dest="overwrite", action="store_true", help="Overwrite?", default=True)
(options, args) = parser.parse_args()
assert options.leptonSelection in ['soft', 'hard', 'inc', 'dilep'], "Unknown leptonSelection: %s"%options.leptonSelection
skimCond = "(1)"
if options.skim.startswith('met'):
  skimCond = "met_pt>"+str(float(options.skim[3:]))
if options.skim=='HT400':
  skimCond = "Sum$(Jet_pt)>400"
if options.skim=='HT400ST200':   ##tuples have already ST200 skim
  skimCond = "Sum$(Jet_pt)>400&&(LepGood_pt[0]+met_pt)>200"

##In case a lepton selection is required, loop only over events where there is one 
#if options.leptonSelection.lower()=='soft':
#  #skimCond += "&&Sum$(LepGood_pt>5&&LepGood_pt<25&&LepGood_relIso03<0.4&&abs(LepGood_eta)<2.4)>=1"
#  print "----------------------------- THIS IS UNKNOWN TERRITORY DONT TRUST THE REUSLT! --------------------------------------"
#  skimCond += "&&(Sum$(LepGood_pt>5&&LepGood_pt<{ptCut} &&abs(LepGood_eta)<2.4)>=1 ||  Sum$(LepOther_pt>5&&LepOther_pt<{ptCut} && abs(LepOther_eta)<2.4)>=1 )".format(ptCut=lepton_soft_hard_cut)
#if options.leptonSelection.lower()=='hard':
#  #skimCond += "&&Sum$(LepGood_pt>25&&LepGood_relIso03<0.4&&abs(LepGood_eta)<2.4)>=1"
#  print "----------------------------- THIS IS UNKNOWN TERRITORY DONT TRUST THE REUSLT! --------------------------------------"
#  skimCond += "&&Sum$(LepGood_pt>%s&&abs(LepGood_eta)<2.4)>=1"%lepton_soft_hard_cut
#if options.leptonSelection.lower()=='dilep':
#  print "----------------------------- THIS IS UNKNOWN TERRITORY DONT TRUST THE REUSLT! --------------------------------------"
#  #skimCond += "&&Sum$(LepGood_pt>25&&LepGood_relIso03<0.4&&abs(LepGood_eta)<2.4)>=1"
#  skimCond += "&&Sum$(LepGood_pt>15&&abs(LepGood_eta)<2.4)>1"
if options.leptonSelection.lower()=='inc':
  skimCond += ""
if options.skim=='inc':
  skimCond = "(1)"
if options.preselect:
  #preselection = "(met_pt > 200 && Jet_pt[0]> 100 && Sum$(Jet_pt)>200 )"
  preselection = "(met_pt > 100 && Jet_pt[0]> 80 && Sum$(Jet_pt)>100 )"
  print "Applying Preselection", preselection
  skimCond += "&&%s"%preselection

if options.skim.lower()=='lhehthi':  
  print "Applying lheHTIncoming >=600     ---- you better know why!"
  skimCond += "lheHTIncoming>=600"
if options.skim.lower()=='lhehtlow':
  print "Applying lheHTIncoming < 600     ---- you better know why!"
  skimCond += "lheHTIncoming<600"


print "SkimCondition:"
print skimCond



if sys.argv[0].count('ipython'):
  options.small=True

def getTreeFromChunk(c, skimCond, iSplit, nSplit):
  if not c.has_key('file'):return
  rf = ROOT.TFile.Open(c['file'])
  assert not rf.IsZombie()
  rf.cd()
  tc = rf.Get("tree")
  nTot = tc.GetEntries()
  fromFrac = iSplit/float(nSplit)
  toFrac   = (iSplit+1)/float(nSplit)
  start = int(fromFrac*nTot)
  stop  = int(toFrac*nTot)
  ROOT.gDirectory.cd('PyROOT:/')
  print "Copy tree from source: total number of events found:",nTot,"Split counter: ",iSplit,"<",nSplit,"first Event:",start,"nEvents:",stop-start
  t = tc.CopyTree(skimCond,"",stop-start,start)
  tc.Delete()
  del tc
  rf.Close()
  del rf
  return t
   
exec('allSamples=['+options.allsamples+']')
for isample, sample in enumerate(allSamples):
  
  #chunks, sumWeight = getChunks(sample, options.inputTreeName)
  chunks, sumWeight = getChunks(sample)
  #chunks, nTotEvents = getChunksFromDPM(sample, options.inputTreeName)
  #print "Chunks:" , chunks 
  print "Here is what the first chunk looks like: (out of %s):"%len(chunks)
  print chunks[0]
  outDir = options.targetDir+'/'+"/".join([options.skim, options.leptonSelection, sample['name']])
  tmpDir = outDir+'/tmp/'
  os.system('mkdir -p ' + outDir) 
  os.system('mkdir -p '+tmpDir)
  os.system('rm -rf '+tmpDir+'/*')
  
  if sample['isData']: 
    prelumiWeight=1
    branchKeepStrings = branchKeepStrings_DATAMC + branchKeepStrings_DATA
    #branchKeepStrings = ["run", "lumi", "evt", "isData", "rho", "nVert", "nJet25", "nBJetLoose25", "nBJetMedium25", "nBJetTight25", "nJet40", "nJet40a", "nBJetLoose40", "nBJetMedium40", "nBJetTight40",
    #                 "nLepGood20", "nLepGood15", "nLepGood10",  
    #                 "htJet25", "mhtJet25", "htJet40j", "htJet40", "mhtJet40", "nSoftBJetLoose25", "nSoftBJetMedium25", "nSoftBJetTight25",
    #                 "met_*","Flag_*",
    #                 "nFatJet","FatJet_*", 
    #                 "nLepOther", "LepOther_*", "nLepGood", "LepGood_*", "nTauGood", "TauGood_*",
    #                 "nJet", "Jet_*"] 
  else:
    print "sumWeight", sumWeight
    sampleXsec = sample['xsec'] if sample.has_key('xsec') else xsec[sample['dbsName']]
    
    #prelumiWeight = xsec[sample['dbsName']]*target_lumi/float(sumWeight)
    prelumiWeight = sampleXsec*target_lumi/float(sumWeight)
    branchKeepStrings = branchKeepStrings_DATAMC + branchKeepStrings_MC

    #branchKeepStrings = ["run", "lumi", "evt", "isData", "xsec", "puWeight", "nTrueInt", "genWeight", "rho", "nVert", "nJet25", "nBJetLoose25", "nBJetMedium25", "nBJetTight25", "nJet40", "nJet40a", "nBJetLoose40", "nBJetMedium40", "nBJetTight40",  
    #                 "nLepGood20", "nLepGood15", "nLepGood10",  
    #                 "GenSusyMScan1", "GenSusyMScan2", "GenSusyMScan3", "GenSusyMScan4", "GenSusyMGluino", "GenSusyMGravitino", "GenSusyMStop", "GenSusyMSbottom", "GenSusyMStop2", "GenSusyMSbottom2", "GenSusyMSquark", "GenSusyMNeutralino", "GenSusyMNeutralino2", "GenSusyMNeutralino3", "GenSusyMNeutralino4", "GenSusyMChargino", "GenSusyMChargino2",
    #                 "htJet25", "mhtJet25", "htJet40j", "htJet40", "mhtJet40", "nSoftBJetLoose25", "nSoftBJetMedium25", "nSoftBJetTight25",
    #                 "met_*","Flag_*",
    #                 "nFatJet","FatJet_*", 
    #                 "nLepOther", "LepOther_*", "nLepGood", "LepGood_*", "ngenLep", "genLep_*", "nTauGood", "TauGood_*",
    #                 "nGenPart", "GenPart_*","ngenPartAll","genPartAll_*" ,"ngenTau", "genTau_*", "nJet", "Jet_*", "ngenLepFromTau", "genLepFromTau_*"] 
  #print "sample['dbsName']:" , sample['dbsName']
  readVariables = ['met_pt/F', 'met_phi/F']
  #newVariables = ['weight/F']
  newVariables = []
  aliases = [ "met:met_pt", "metPhi:met_phi"]

  readVectors = [\
    {'prefix':'LepOther',  'nMax':8, 'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'relIso03/F', 'tightId/I', 'miniRelIso/F','mass/F','sip3d/F','mediumMuonId/I', 'mvaIdPhys14/F','lostHits/I', 'convVeto/I']},
    {'prefix':'LepGood',  'nMax':8, 'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'relIso03/F', 'tightId/I', 'miniRelIso/F','mass/F','sip3d/F','mediumMuonId/I', 'mvaIdPhys14/F','lostHits/I', 'convVeto/I']},
    {'prefix':'Jet',  'nMax':100, 'vars':['pt/F', 'eta/F', 'phi/F', 'id/I','btagCSV/F', 'btagCMVA/F', 'mass/F']},
  ]
  if tracks: 
    readVectors.append(
            {'prefix':'track'  , 'nMax':1000, 'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I' , 'dxy/F', 'dz/F', 'fromPV/I'] },
                      )
  if pkdGenParts: 
    readVectors.extend([
            {'prefix':'genPartPkd'  , 'nMax':1000, 'vars':['pt/F', 'eta/F', 'phi/F', 'pdgId/I' ] },
            {'prefix':'GenJet'  , 'nMax':100, 'vars':['pt/F', 'eta/F', 'phi/F', 'mass/F' ] },

                      ])
  if not sample['isData']: 
    #newVariables = ['weight/F','weight_XSecTTBar1p1/F','weight_XSecTTBar0p9/F']
    newVariables = ['weight/F']
    aliases.extend(['genMet:met_genPt', 'genMetPhi:met_genPhi'])
    #readVectors[1]['vars'].extend('partonId/I')
    if pkdGenParts:
      newVariables.extend([
                           'genPartPkd_ISRdPhi/F' , 'genPartPkd_CosISRdPhi/F' ,"ngenPartPkd_1p5/I/0","ngenPartPkd_1/I/0","ngenPartPkd_2/I/0",
                           'ngenPartPkdOppJet1_1/F','ngenPartPkdOppJet1_1p5/F', 'ngenPartPkdOppJet1_2/F','ngenPartPkdO90isr_1/F', 'ngenPartPkdO90isr_1p5/F', 'ngenPartPkdO90isr_2/F', 

                          ] )
  if options.leptonSelection.lower() in ['soft', 'hard','inc']:
    newVariables.extend( ['nLooseSoftLeptons/I', 'nLooseSoftPt10Leptons/I', 'nLooseHardLeptons/I', 'nTightSoftLeptons/I', 'nTightHardLeptons/I'] )
    newVariables.extend( ['deltaPhi_Wl/F','nBJetMediumCSV30/I', "nSoftBJetsCSV/F", "nHardBJetsCSV/F",  'nJet30/I','htJet30j/F',"nJet60/I","nJet110/I","nJet325/I" ,'st/F', 'singleMuonic/I', 'singleElectronic/I', 'singleLeptonic/I', 
                          'leptonPt/F','leptonMiniRelIso/F','leptonRelIso03/F' ,'leptonEta/F',  'leptonPhi/F', 'leptonPdg/I/0', 'leptonInd/I/-1', 'leptonMass/F', 'leptonDz/F', 'leptonDxy/F', 
                          'lepGoodPt/F','lepGoodMiniRelIso/F','lepGoodRelIso03/F' , 'lepGoodRelIso04/F',"lepGoodAbsIso/F" ,'lepGoodEta/F',  'lepGoodPhi/F', 'lepGoodPdgId/I/0', 'lepGoodInd/I/-1', 'lepGoodMass/F', 'lepGoodDz/F', 'lepGoodDxy/F','lepGoodMedMuId/I','lepGoodSip3d/F',
                          'lepOtherPt/F','lepOtherMiniRelIso/F','lepOtherRelIso03/F' , 'lepOtherRelIso04/F',"lepOtherAbsIso/F" ,'lepOtherEta/F',  'lepOtherPhi/F', 'lepOtherPdgId/I/0', 'lepOtherInd/I/-1', 'lepOtherMass/F', 'lepOtherDz/F', 'lepOtherDxy/F','lepOtherMedMuId/I','lepOtherSip3d/F',
                          'lepPt/F','lepMiniRelIso/F','lepRelIso03/F' , 'lepRelIso04/F',"lepAbsIso/F" ,'lepEta/F',  'lepPhi/F', 'lepPdgId/I/0', 'lepInd/I/-1', 'lepMass/F', 'lepDz/F', 'lepDxy/F','lepMedMuId/I','lepSip3d/F','nlep/I',
                          'Q80/F','CosLMet/F','deltaPhi_j12/F','mt/F',

                          "J2Mass/F","J3Mass/F", "dRJet1Jet2/F","jet2Pt/F","jet2Eta/F","jet2Phi/F","JetLepMass/F","dRJet1Lep/F","jet1Pt/F","jet1Eta/F","jet1Phi/F","J2Mass_tlv/F",

                          ]) #, 'mt2w/F'] )

    if tracks:
      newTrackVars = []
      for minTrkPt in trackMinPtList:
        ptString = str(minTrkPt).replace(".","p")
        newTrackVars.extend( [ x%ptString for x in  [ "ntracks_%s/I" ,"ntrackOppJet1_%s/I" ,"ntrackOppJet12_%s/I" , "ntrackOppJetAll_%s/I" ] ] )
      newVariables.extend(newTrackVars)
      #newVariables.extend( [
      #                     'track_ISRdPhi/F' , 'track_CosISRdPhi/F' ,"ntrack_1p5/I/0","ntrack_1/I/0","ntrack_2/I/0",
      #                     'ntrackOppJet1_1/F','ntrackOppJet1_1p5/F', 'ntrackOppJet1_2/F','ntrackO90isr_1/F', 'ntrackO90isr_1p5/F', 'ntrackO90isr_2/F', 
      #                     ["ntrackOppJetAll_%s"%minTrkPt.replace(".","p") ]

      #                     ]) 




    
  newVars = [readVar(v, allowRenaming=False, isWritten = True, isRead=False) for v in newVariables]

  
  readVars = [readVar(v, allowRenaming=False, isWritten=False, isRead=True) for v in readVariables]
  for v in readVectors:
    readVars.append(readVar('n'+v['prefix']+'/I', allowRenaming=False, isWritten=False, isRead=True))
    v['vars'] = [readVar(v['prefix']+'_'+vvar, allowRenaming=False, isWritten=False, isRead=True) for vvar in v['vars']]

  printHeader("Compiling class to write")
  writeClassName = "ClassToWrite_"+str(isample)
  writeClassString = createClassString(className=writeClassName, vars= newVars, vectors=[], nameKey = 'stage2Name', typeKey = 'stage2Type')
#  print writeClassString
  s = compileClass(className=writeClassName, classString=writeClassString, tmpDir='/data/'+username+'/tmp/')

  readClassName = "ClassToRead_"+str(isample)
  readClassString = createClassString(className=readClassName, vars=readVars, vectors=readVectors, nameKey = 'stage1Name', typeKey = 'stage1Type', stdVectors=False)
  printHeader("Class to Read")
#  print readClassString
  r = compileClass(className=readClassName, classString=readClassString, tmpDir='/data/'+username+'/tmp/')

  filesForHadd=[]
  if options.small: chunks=chunks[:1]
  #print "CHUNKS:" , chunks
  for chunk in chunks:
    if break_for_debug: 
      print "!!!!!!!!!!!!!!!!!!! BREAKING FOR INTERACTIVE DEBUG !!!!!!!!!!!!!!!!!!!!!!!!!!!!"
      break
    sourceFileSize = os.path.getsize(chunk['file'])
    nSplit = 1+int(sourceFileSize/(200*10**6)) #split into 200MB
    if nSplit>1: print "Chunk too large, will split into",nSplit,"of appox 200MB"
    for iSplit in range(nSplit):
      t = getTreeFromChunk(chunk, skimCond, iSplit, nSplit)
      if not t: 
        print "Tree object not found:", t
        continue
      t.SetName("Events")
      nEvents = t.GetEntries()
      for v in newVars:
#        print "new VAR:" , v
        v['branch'] = t.Branch(v['stage2Name'], ROOT.AddressOf(s,v['stage2Name']), v['stage2Name']+'/'+v['stage2Type'])
      for v in readVars:
#        print "read VAR:" , v
        t.SetBranchAddress(v['stage1Name'], ROOT.AddressOf(r, v['stage1Name']))
      for v in readVectors:
        for var in v['vars']:
          t.SetBranchAddress(var['stage1Name'], ROOT.AddressOf(r, var['stage1Name']))
      for a in aliases:
        t.SetAlias(*(a.split(":")))
      print "File",chunk['file'],'chunk',chunk['name'],"found", nEvents, '(skim:',options.skim,') condition:', skimCond,' with weight',prelumiWeight, 'in Chain -> post processing...'

      t1 = time.time()      
      for ievt in range(nEvents):
        if break_for_debug: 
          print "!!!!!!!!!!!!!!!!!!! BREAKING FOR INTERACTIVE DEBUG !!!!!!!!!!!!!!!!!!!!!!!!!!!!"
          break
        if (ievt%10000 == 0) and ievt>0 :
          checkmark = time.time()
          print ievt,"/",nEvents, "(%s s)"%(checkmark-t1)  , "name:" , chunk['name']
          t1 = checkmark
        s.init()
        r.init()
        t.GetEntry(ievt)
        if not sample['isData']:
          genWeight = t.GetLeaf('genWeight').GetValue()
          s.weight = prelumiWeight*genWeight
          #print "reweighted:" , s.weight
          #if "TTJets_" in sample['dbsName']:
          #  s.weight_XSecTTBar1p1 = s.weight*1.1 
          #  s.weight_XSecTTBar0p9 = s.weight*0.9
          #else :
          #  s.weight_XSecTTBar1p1 = s.weight
          #  s.weight_XSecTTBar0p9 = s.weight

        
        if options.leptonSelection.lower() in ['soft','hard','inc']:
          looseLepInd = cmgLooseLepIndices(r, ptCuts=(7,5), absEtaCuts=(2.5,2.4), ele_MVAID_cuts={'eta08':0.35 , 'eta104':0.20,'eta204': -0.52} )    ##Tight ele_MVAID_cuts={'eta08':0.73 , '
          looseSoftLepInd, looseHardLepInd = splitIndList(r.LepGood_pt, looseLepInd, 30.)
          tightHardLepInd = filter(lambda i:(abs(r.LepGood_pdgId[i])==11 and r.LepGood_miniRelIso[i]<0.1 and ele_ID_eta(r,nLep=i,ele_MVAID_cuts={'eta08':0.73 , 'eta104':0.57,'eta204':  0.05}) and r.LepGood_tightId[i]>=3) \
                                         or (abs(r.LepGood_pdgId[i])==13 and r.LepGood_miniRelIso[i]<0.2  and r.LepGood_tightId[i]), looseHardLepInd)  
          s.nTightHardLeptons = len(tightHardLepInd)
          #looseLepInd = cmgLooseLepIndices(r, ptCuts=(7,5), absEtaCuts=(2.5,2.4), ele_MVAID_cuts={'eta08':0.35 , 'eta104':0.20,'eta204': -0.52} )    ##Tight ele_MVAID_cuts={'eta08':0.73 , 'eta104':0.57,'eta204':  0.05}
          vars = ['pt', 'eta', 'phi', 'miniRelIso','relIso03',"relIso04", "dxy", "dz", 'pdgId', "sip3d","mediumMuonId"]

          lepGoods =   [getObjDict(t, 'LepGood_',vars, i ) for i in range(r.nLepGood)]
          lepOthers =  [getObjDict(t, 'LepOther_',vars, i ) for i in range(r.nLepOther)]
          allLeptons = lepGoods + lepOthers

          #selectedLepOthers = filter( isGoodLepton , lepOthers )
          #selectedLepOthers = sorted( selectedLepOthers ,key= lambda lep: lep['pt'], reverse=True)

          #selectedLepGoods = filter( isGoodLepton , lepGoods )
          #selectedLepGoods = sorted( selectedLepGoods ,key= lambda lep: lep['pt'], reverse=True)

          selectedLeptons = filter( isGoodLepton , allLeptons )
          selectedLeptons = sorted( selectedLeptons ,key= lambda lep: lep['pt'], reverse=True)

          ## then pt sort them
          if verbose:
            print "nlepGood, nlepOther" , r.nLepGood, r.nLepOther
            print "selected: ", selectedLeptons 
            print "%%%%%%%%%%" , len(selectedLeptons) , len(allLeptons), "    (" , len([getObjDict(t, 'LepGood_',vars, i ) for i in range(r.nLepGood)]) , len([getObjDict(t, 'LepOther_',vars, i ) for i in range(r.nLepOther)]) 
            print "###########################\n"
          #looseSoftLep = [getObjDict(t, 'LepGood_', vars, i) for i in looseSoftLepInd] 
          #looseHardLep = [getObjDict(t, 'LepGood_', vars, i) for i in looseHardLepInd]
          #looseSoftPt10Lep = [getObjDict(t, 'LepGood_', vars, i) for i in looseSoftPt10LepInd]
          #tightSoftLep = [getObjDict(t, 'LepGood_', vars, i) for i in tightSoftLepInd]
          #tightHardLep =  [getObjDict(t, 'LepGood_', vars, i) for i in tightHardLepInd]
          #print "tightHardLep" , tightHardLep 
          leadingLepInd = None

          varsToKeep = vars +[]
          if selectedLeptons:
            lep= selectedLeptons[0]
            lepName = "lep"
            for var in varsToKeep:
              varName = lepName + var.title()
              setattr(s,varName,lep[var])
            s.lepAbsIso = lep['relIso04']*lep['pt'] 

          #for lep in selectedLeptons:
          #if selectedLepGoods:
          #  lep= selectedLepGoods[0]
          #  lepName = "lepGood"
  
          #  for var in varsToKeep:
          #    varName = lepName + var.title()
          #    setattr(s,varName,lep[var])
          #  s.lepGoodAbsIso = lep['relIso04']*lep['pt'] 

          #if selectedLepOthers:
          #  lep= selectedLepOthers[0]
          #  lepName = "lepOther"
  
          #  for var in varsToKeep:
          #    varName = lepName + var.title()
          #    setattr(s,varName,lep[var])
          #  s.lepOtherAbsIso = lep['relIso04']*lep['pt'] 
            #s.lepPt     = lep['pt']
            #s.lepEta    = lep['eta'] 
            #s.lepPhi    = lep['phi'] 
            #s.lepDxy    = lep['dxy'] 
            #s.lepDz     = lep['dz']  
            #s.lepPdgId  = lep['pdgId']
            #s.lepEta    = lep['eta'] 
            #s.lepMedMuId= lep['mediumMuonId']
            #s.lepSip3d  = lep['sip3d']
            #s.lepRelIso04=  lep['relIso04']
            #s.lepRelIso03=  lep['relIso03']
            #s.lepMiniRelIso =  lep['miniRelIso']
            #s.nlep  = len(selectedLeptons)
            #s.singleMuonic = s.nlep==1

        #if options.leptonSelection=='hard':
        #  if s.nTightHardLeptons>=1:
        #    leadingLepInd = tightHardLepInd[0]
        #    #print "highest pt: " , r.LepGood_pt[0]
        #    s.leptonPt  = r.LepGood_pt[leadingLepInd]
        #    s.leptonMiniRelIso = r.LepGood_miniRelIso[leadingLepInd]
        #    s.leptonRelIso03 = r.LepGood_relIso03[leadingLepInd]
        #    #print s.leptonMiniRelIso ,s.leptonPt, 'met:', r.met_pt, r.nLepGood, r.LepGood_pt[leadingLepInd],r.LepGood_eta[leadingLepInd], r.LepGood_phi[leadingLepInd] , r.LepGood_pdgId[leadingLepInd], r.LepGood_relIso03[leadingLepInd], r.LepGood_tightId[leadingLepInd], r.LepGood_mass[leadingLepInd]
        #    s.leptonInd = leadingLepInd 
        #    s.leptonEta = r.LepGood_eta[leadingLepInd]
        #    s.leptonPhi = r.LepGood_phi[leadingLepInd]
        #    s.leptonPdg = r.LepGood_pdgId[leadingLepInd]
        #    s.leptonMass= r.LepGood_mass[leadingLepInd]
        #    s.leptonDz = r.LepGood_Dz[leadingLepInd]
        #    s.leptonDxy= r.LepGood_Dxy[leadingLepInd]
        #    s.st = r.met_pt + s.leptonPt
        #  s.singleLeptonic = s.nTightHardLeptons==1
        #  if s.singleLeptonic:
        #    s.singleMuonic      =  abs(s.leptonPdg)==13
        #    s.singleElectronic  =  abs(s.leptonPdg)==11
        #  else:
        #    s.singleMuonic      = False 
        #    s.singleElectronic  = False 

        #if options.leptonSelection in ['soft', 'inc']:
        #  #Select hardest tight lepton among soft leptons
        #  if s.nTightSoftLeptons>=1:
        #    leadingLepInd = tightSoftLepInd[0]
  #     #     print s.leptonPt, r.LepGood_pt[leadingLepInd],r.LepGood_eta[leadingLepInd], leadingLepInd
        #    s.leptonPt  = r.LepGood_pt[leadingLepInd]
        #    s.leptonInd = leadingLepInd 
        #    s.leptonEta = r.LepGood_eta[leadingLepInd]
        #    s.leptonPhi = r.LepGood_phi[leadingLepInd]
        #    s.leptonPdg = r.LepGood_pdgId[leadingLepInd]
        #    s.leptonMass= r.LepGood_mass[leadingLepInd]
        #    s.leptonDz = r.LepGood_Dz[leadingLepInd]
        #    s.leptonDxy= r.LepGood_Dxy[leadingLepInd]
        #    s.st = r.met_pt + s.leptonPt
          #s.singleLeptonic = s.nTightSoftLeptons==1
          #if s.singleLeptonic:
          #  s.singleMuonic      =  abs(s.leptonPdg)==13
          #  s.singleElectronic  =  abs(s.leptonPdg)==11
          #else:
          #  s.singleMuonic      = False 
          #  s.singleElectronic  = False 
  #      print "Selected",s.leptonPt
        if options.leptonSelection in ['soft','hard','inc']:
          j_list=['eta','pt','phi','btagCMVA', 'btagCSV', 'id','mass']
          #if not sample['isData']: j_list.extend('partonId')
          jets = filter(lambda j:j['pt']>30 and abs(j['eta'])<2.4 and j['id'], get_cmg_jets_fromStruct(r,j_list))
          
          lightJets,  bJetsCSV = splitListOfObjects('btagCSV', 0.890, jets)
          #lightJets,  bJetsCSV = filter(lambda j:j['btagCSV']<0.814 and -1<j['btagCSV'] , jetscopy)
          #print "bjetsCMVA:" , bJetsCMVA , "bjetsCSV:" ,  bJetsCSV

          s.htJet30j = sum([x['pt'] for x in jets])
          s.nJet30 = len(jets)
          jets60   = filter(lambda j:j['pt']>60 and abs(j['eta'])<2.4 and j['id'], get_cmg_jets_fromStruct(r,j_list))  ## maybe use jets instead

          bJets = filter( lambda j: j["btagCSV"] > 0.890 , jets )
          softBJetsCSV,  hardBJetsCSV = splitListOfObjects('pt', 60, bJets)

          s.nSoftBJetsCSV = len(softBJetsCSV)
          s.nHardBJetsCSV = len(hardBJetsCSV)

          s.nJet60 = len( jets60)
          jets110 = filter(lambda j:j['pt']>110 and abs(j['eta'])<2.4 and j['id'], get_cmg_jets_fromStruct(r,j_list))
          s.nJet110 = len( jets110  )
          s.nJet325 = len( filter(lambda j: j["pt"] > 325 , jets110) )

          if s.nJet30 > 0:    
            s.jet1Pt        =   jets[0]['pt']
            s.jet1Eta       =   jets[0]['eta']
            s.jet1Phi       =   jets[0]['phi']
  
            if selectedLeptons:
              s.dRJet1Lep   =   deltaR(jets[0],lep)
              s.JetLepMass  =   invMass(jets[0],lep)
              
            
            if s.nJet30 >1:
              s.jet2Pt        =   jets[1]['pt']
              s.jet2Eta       =   jets[1]['eta']
              s.jet2Phi       =   jets[1]['phi']
              s.dRJet1Jet2  = deltaR(jets[0],jets[1])
              s.J2Mass      = invMass(jets[0],jets[1])

              if s.nJet30 > 2:              
                j1 =ROOT.TLorentzVector() 
                j1.SetPtEtaPhiM(jets[0]['pt'],jets[0]['eta'],jets[0]['phi'],jets[0]['mass'] )
                j2 =ROOT.TLorentzVector() 
                j2.SetPtEtaPhiM(jets[1]['pt'],jets[1]['eta'],jets[1]['phi'],jets[1]['mass'] )
                j3 =ROOT.TLorentzVector()
                j3.SetPtEtaPhiM(jets[2]['pt'],jets[2]['eta'],jets[2]['phi'],jets[2]['mass'] )
                jt = j1+j2+j3
                #break_for_debug = True  

                s.J2Mass_tlv = (j1+j2).M()  ## apparently this is a bit different from invMass

                #if s.J2Mass != (j1+j2).M():
                #  print "! ", s.J2Mass, (j1+j2).M()
                #if s.J2Mass == (j1+j2).M():
                #  print "==",s.J2Mass, (j1+j2).M()
                s.J3Mass    =  jt.M()
            #s.dRJetHBLep =
            #s.jetHBpt

        ###############################       track variables
        if tracks:
          vars = ['pt', 'eta', 'phi', "dxy", "dz", 'pdgId' , "matchedJetIndex", "matchedJetDr", "CosPhiJet1", "CosPhiJet12", "CosPhiJetAll"]
          tracks =   (getObjDict(t, 'track_',vars, i ) for i in range(r.ntrack))

          ntrack={ minPt : 0 for minPt in trackMinPtList}
          ntrackOppJet1={ minPt : 0 for minPt in trackMinPtList}
          ntrackOppJet12={ minPt : 0 for minPt in trackMinPtList}
          ntrackOppJetAll={ minPt : 0 for minPt in trackMinPtList}
          ntrackOpp90Jet1={ minPt : 0 for minPt in trackMinPtList}
          ntrackOpp90Jet12={ minPt : 0 for minPt in trackMinPtList}
          ntrackOpp90JetAll={ minPt : 0 for minPt in trackMinPtList}

          #goodTracks = filter( )
          for track in tracks:
            if not (abs(track['eta']) < 2.5 and abs(track['dxy']) < 0.02 and abs( track['dz'] ) < 0.5 and track['pt']>=1.0) :
              continue
            if not ( track["matchedJetIndex"]==-1  and track['matchedJetDr']>0.4  ):## also check jet pt  ## vetoing tracks that are matched to a jet 
              continue
            for minTrkPt in trackMinPtList:
              if track['pt'] > minTrkPt:
                ntrack[minTrkPt]+=1
                if track['CosPhiJet1'] < 0:
                  ntrackOppJet1[minTrkPt]+=1
                if track['CosPhiJet12'] < 0:
                  ntrackOppJet12[minTrkPt]+=1
                if track['CosPhiJetAll'] < 0:
                  ntrackOppJetAll[minTrkPt]+=1
          #break_for_debug = True        

              



            #print track

            #if cos(track['phi']-s.jet1Phi) < 0:
            #  for trackMinPt in trackMinPtList:
            #    if track['pt'] > trackMinPt:
            #      ntracksOppJet1[trackMinPt]+=1
            #  if cos(track['phi']-s.jet1Phi) <  -sqrt(2)/2:
            #    for trackMinPt in trackMinPtList:
            #      if track['pt'] > trackMinPt:
            #        ntracksOpp90ISR[trackMinPt]+=1

            #for trackMinPt in trackMinPtList:
            #  if track['pt'] > trackMinPt:
            #    ntracks[trackMinPt]+=1
            #    #print "added one track to", trackMinPt, ntracks[trackMinPt]
          
          
          for minTrkPt in trackMinPtList:
            trkPtString = str(minTrkPt).replace(".","p")
            setattr(s,"ntracks_%s"         %trkPtString         ,  ntrack[minTrkPt]   )
            setattr(s,"ntrackOppJet1_%s"  %trkPtString  ,  ntrackOppJet1[minTrkPt]   )
            setattr(s,"ntrackOppJet12_%s" %trkPtString ,  ntrackOppJet12[minTrkPt]   )  
            setattr(s,"ntrackOppJetAll_%s"%trkPtString,  ntrackOppJetAll[minTrkPt]   )

          
 


        if pkdGenParts:
          vars = ['pt', 'eta', 'phi', 'pdgId' ]
          genPartPkds =   (getObjDict(t, 'genPartPkd_',vars, i ) for i in range(r.ngenPartPkd))
          ngenPartPkds={ minPt : 0 for minPt in genPartMinPtList}
          ngenPartPkdsOppJet1={ minPt : 0 for minPt in genPartMinPtList}
          ngenPartPkdsOpp90ISR={ minPt : 0 for minPt in genPartMinPtList}
          ngenPartPkdsOppJet12={ minPt : 0 for minPt in genPartMinPtList}
          ngenPartPkdsOpp90ISR2={ minPt : 0 for minPt in genPartMinPtList}
          for genPartPkd in genPartPkds:
            if not (abs(genPartPkd['eta']) < 2.5 and genPartPkd['pt']>=1.0) :
              continue
            #print genPartPkd

            if cos(genPartPkd['phi']-s.jet1Phi) < 0:
              for genPartPkdMinPt in genPartMinPtList:
                if genPartPkd['pt'] > genPartPkdMinPt:
                  ngenPartPkdsOppJet1[genPartPkdMinPt]+=1
              if cos(genPartPkd['phi']-s.jet1Phi) <  -sqrt(2)/2:
                for genPartPkdMinPt in genPartMinPtList:
                  if genPartPkd['pt'] > genPartPkdMinPt:
                    ngenPartPkdsOpp90ISR[genPartPkdMinPt]+=1

            for genPartPkdMinPt in genPartMinPtList:
              if genPartPkd['pt'] > genPartPkdMinPt:
                ngenPartPkds[genPartPkdMinPt]+=1
                #print "added one genPartPkd to", genPartPkdMinPt, ngenPartPkds[genPartPkdMinPt]
          
          s.ngenPartPkd_1    = ngenPartPkds[1]    
          s.ngenPartPkd_1p5    = ngenPartPkds[1.5]    
          s.ngenPartPkd_2    = ngenPartPkds[2]    
          
 
          s.ngenPartPkdOppJet1_1 = ngenPartPkdsOppJet1[1]  
          s.ngenPartPkdOppJet1_1p5 = ngenPartPkdsOppJet1[1.5]  
          s.ngenPartPkdOppJet1_2 = ngenPartPkdsOppJet1[2]  

          s.ngenPartPkdO90isr_1 = ngenPartPkdsOpp90ISR[1]  
          s.ngenPartPkdO90isr_1p5 = ngenPartPkdsOpp90ISR[1.5]  
          s.ngenPartPkdO90isr_2 = ngenPartPkdsOpp90ISR[2]  

########################################################

#         s.nBJetMediumCMVA30 = len(bJetsCMVA)
          s.nBJetMediumCSV30 = len(bJetsCSV)
          #print "nbjetsCMVA:" , s.nBJetMediumCMVA30  ,"nbjetsCSV:" ,  s.nBJetMediumCSV30
          #s.mt2w = mt2w.mt2w(met = {'pt':r.met_pt, 'phi':r.met_phi}, l={'pt':s.leptonPt, 'phi':s.leptonPhi, 'eta':s.leptonEta}, ljets=lightJets, bjets=bJetsCSV)
          s.deltaPhi_Wl = acos((s.leptonPt+r.met_pt*cos(s.leptonPhi-r.met_phi))/sqrt(s.leptonPt**2+r.met_pt**2+2*r.met_pt*s.leptonPt*cos(s.leptonPhi-r.met_phi))) 
          #s.Q80         = 1-80**2/(2*s.leptonPt*r.met_pt)
          #s.CosLMet     = cos(s.leptonPhi-r.met_phi)
          #s.mt          = sqrt( 2* s.leptonPt * r.met_pt *( 1- s.CosLMet  ))
          s.Q80         = 1-80**2/(2*s.lepPt*r.met_pt)
          s.CosLMet     = cos(s.lepPhi-r.met_phi)
          s.mt          = sqrt( 2* s.lepPt * r.met_pt *( 1- s.CosLMet  ))
          
          if s.nJet60 == 0:
            s.deltaPhi_j12 = 999
            #print "#################################"
            #print s.nJet60, s.deltaPhi_j12
          elif s.nJet60 == 1:
            s.deltaPhi_j12 = 0
          else:
            s.deltaPhi_j12 = min( 2*pi- abs(jets60[1]['phi'] - jets60[0]['phi'] ) ,  abs(jets60[1]['phi'] - jets60[0]['phi'] ) )
          
                 
          #print "deltaPhi:" , s.deltaPhi_Wl
  #          print "Warning -> Why can't I compute mt2w?", s.mt2w, len(jets), len(bJets), len(allTightLeptons),lightJets,bJets, {'pt':s.type1phiMet, 'phi':s.type1phiMetphi}, {'pt':s.leptonPt, 'phi':s.leptonPhi, 'eta':s.leptonEta}
          
        for v in newVars:
          v['branch'].Fill()
      newFileName = sample['name']+'_'+chunk['name']+'_'+str(iSplit)+'.root'
      filesForHadd.append(newFileName)
      if not options.small:
      #if options.small:
        f = ROOT.TFile(tmpDir+'/'+newFileName, 'recreate')
        t.SetBranchStatus("*",0)
        for b in branchKeepStrings + [v['stage2Name'] for v in newVars] +  [v.split(':')[1] for v in aliases]:
          t.SetBranchStatus(b, 1)
        t2 = t.CloneTree()
        t2.Write()
        f.Close()
        print "Written",tmpDir+'/'+newFileName
        del f
        del t2
        t.Delete()
        del t
      for v in newVars:
        del v['branch']

  print "Event loop end"
  if not options.small: 
    size=0
    counter=0
    files=[]
    for f in filesForHadd:
      size+=os.path.getsize(tmpDir+'/'+f)
      files.append(f)
      if size>(0.5*(10**9)) or f==filesForHadd[-1]:
        ofile = outDir+'/'+sample['name']+'_'+str(counter)+'.root'
        print "Running hadd on", tmpDir, files
        os.system('cd '+tmpDir+';hadd -f '+ofile+' '+' '.join(files))
        print "Written", ofile
        size=0
        counter+=1
        files=[]
    os.system("rm -rf "+tmpDir)

