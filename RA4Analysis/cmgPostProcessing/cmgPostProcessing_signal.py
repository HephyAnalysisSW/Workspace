import ROOT
import pickle
import sys, os, copy, random, subprocess, datetime
from array import array
from Workspace.RA4Analysis.cmgObjectSelection import cmgLooseLepIndices, splitIndList, get_cmg_jets_fromStruct, splitListOfObjects, cmgTightMuID, cmgTightEleID , get_cmg_genParts_fromStruct , get_matched_Jets, get_cmg_isoTracks_fromStruct
from Workspace.HEPHYPythonTools.xsec import xsec
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getObjDict, getFileList
from Workspace.HEPHYPythonTools.convertHelpers import compileClass, readVar, printHeader, typeStr, createClassString

from math import *
from Workspace.HEPHYPythonTools.user import username
from mt2_davis import get_mt2

ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.AutoLibraryLoader.enable()

from Workspace.HEPHYPythonTools.helpers import getChunks
#from Workspace.RA4Analysis.cmgTuples_Data25ns_miniAODv2 import *
from Workspace.RA4Analysis.cmgTuples_Spring16_MiniAODv2 import *
from systematics_helper import calc_btag_systematics, calc_LeptonScale_factors_and_systematics , getISRWeight , getISRWeight_new ,fill_branch_WithJEC , filter_crazy_jets
from btagEfficiency import *
from leptonFastSimSF2016 import leptonFastSimSF as leptonFastSimSF_

scaleFactorDir  = '$CMSSW_BASE/src/Workspace/RA4Analysis/cmgPostProcessing/data/'
bTagEffFile     = 'data/signal_inclusive_pkl'

try:
  mcEffDict = pickle.load(file(bTagEffFile))
except IOError:
  print 'Unable to load MC efficiency file!'
  mcEffDict = False

target_lumi = 3000 #pb-1

#maxConsideredBTagWeight = 2
#calcSystematics = True
separateBTagWeights = True

defSampleStr = "SMS_T5qqqqVV_TuneCUETP8M1"

###For PU reweight###
#PU_dir = "/data/easilar/tuples_from_Artur/JECv6recalibrateMET_2p2fb/PUhistos/"
#PU_File_66mb = ROOT.TFile(PU_dir+"/pileUp_66mb_map.root")
#PU_File_70mb = ROOT.TFile(PU_dir+"/pileUp_70mb_map.root")
#PU_File_74mb = ROOT.TFile(PU_dir+"/pileUp_74mb_map.root")
#PU_histo_66 = PU_File_66mb.Get("h_ratio_66")
#PU_histo_70 = PU_File_70mb.Get("h_ratio_70")
#PU_histo_74 = PU_File_74mb.Get("h_ratio_74")
PU_dir = scaleFactorDir
PU_File_59p85mb = ROOT.TFile(PU_dir+"/h_ratio_59p85.root")
PU_File_63mb = ROOT.TFile(PU_dir+"/h_ratio_63.root")
PU_File_66p15mb = ROOT.TFile(PU_dir+"/h_ratio_66p15.root")
PU_histo_59p85 = PU_File_59p85mb.Get("h_ratio")
PU_histo_63 = PU_File_63mb.Get("h_ratio")
PU_histo_66p15 = PU_File_66p15mb.Get("h_ratio")

#####################
###For Lepton SF#####
mu_mediumID_File  = ROOT.TFile(scaleFactorDir+'TnP_MuonID_NUM_MediumID_DENOM_generalTracks_VAR_map_pt_eta.root')
mu_looseID_File   = ROOT.TFile(scaleFactorDir+'TnP_MuonID_NUM_LooseID_DENOM_generalTracks_VAR_map_pt_eta.root')
mu_miniIso02_File = ROOT.TFile(scaleFactorDir+'TnP_MuonID_NUM_MiniIsoTight_DENOM_MediumID_VAR_map_pt_eta.root')
mu_sip3d_File     = ROOT.TFile(scaleFactorDir+'TnP_MuonID_NUM_TightIP3D_DENOM_MediumID_VAR_map_pt_eta.root')
mu_HIP_File       = ROOT.TFile(scaleFactorDir+'ratiosMuonHIP.root')
ele_kin_File      = ROOT.TFile(scaleFactorDir+'eleScaleFactorsUpdate2607.root')
ele_gsf_File      = ROOT.TFile(scaleFactorDir+'egammaEffi_txt_SF2D.root')
#

histos_LS = {
'mu_mediumID_histo':  mu_mediumID_File.Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0"),\
'mu_looseID_histo':   mu_looseID_File.Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0"),\
'mu_miniIso02_histo': mu_miniIso02_File.Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_Medium2016_pass"),\
'mu_sip3d_histo':     mu_sip3d_File.Get("pt_abseta_PLOT_pair_probeMultiplicity_bin0_&_Medium2016_pass"),\
'mu_HIP_histo':       mu_HIP_File.Get("ratio_eta"),\
'ele_cutbased_histo': ele_kin_File.Get("GsfElectronToTight"),\
'ele_miniIso01_histo':ele_kin_File.Get("MVAVLooseElectronToMini"),\
'ele_gsf_histo':      ele_gsf_File.Get("EGamma_SF2D"),\
}

#####################

subDir = "postProcessing_Signals_Spring16_Moriond2017"

#branches to be kept for data and MC
branchKeepStrings_DATAMC = ["run", "lumi", "evt", "isData", "rho", "nVert", "nIsr" ,
                     "nJet25", "nBJetLoose25", "nBJetMedium25", "nBJetTight25", "nJet40", "nJet40a", "nBJetLoose40", "nBJetMedium40", "nBJetTight40", 
                     "nLepGood20", "nLepGood15", "nLepGood10", "htJet25", "mhtJet25", "htJet40j", "htJet40", "mhtJet40", 
                     "met*","Flag_*","HLT_*",
#                     "nFatJet","FatJet_*", 
                     "nJet", "Jet_*", 
                     "nLepGood", "LepGood_*", 
                     "nLepOther", "LepOther_*", 
                     "nTauGood", "TauGood_*",
                     ] 

#branches to be kept for MC samples only
branchKeepStrings_MC = [ "nTrueInt", "genWeight", "xsec", "puWeight", 
                     "GenSusyMScan1", "GenSusyMScan2", "GenSusyMScan3", "GenSusyMScan4", "GenSusyMGluino", "GenSusyMGravitino", "GenSusyMStop", "GenSusyMSbottom", "GenSusyMStop2", "GenSusyMSbottom2", "GenSusyMSquark", "GenSusyMNeutralino", "GenSusyMNeutralino2", "GenSusyMNeutralino3", "GenSusyMNeutralino4", "GenSusyMChargino", "GenSusyMChargino2", 
                     "nLHEweight","LHEweight_*",
                     "nJetForMET", "JetForMET_*",
                     "ngenLep", "genLep_*", 
                     "nGenPart", "GenPart_*",
                     "ngenPartAll","genPartAll_*" ,
                     "ngenTau", "genTau_*", 
                     "ngenLepFromTau", "genLepFromTau_*"]

#branches to be kept for data only
branchKeepStrings_DATA = []
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--samples", dest="allsamples", default=defSampleStr, type="string", action="store", help="samples:Which samples.")
parser.add_option("--inputTreeName", dest="inputTreeName", default="treeProducerSusySingleLepton", type="string", action="store", help="samples:Which samples.")
parser.add_option("--targetDir", dest="targetDir", default="/afs/hephy.at/data/"+username+"01/cmgTuples/"+subDir+'/', type="string", action="store", help="target directory.")
parser.add_option("--skim", dest="skim", default="signal", type="string", action="store", help="any skim condition?")
parser.add_option("--small", dest="small", default = False, action="store_true", help="Just do a small subset.")
parser.add_option("--overwrite", dest="overwrite", default = True, action="store_true", help="Overwrite?")
parser.add_option("--calcbtagweights", dest="systematics", default = False, action="store_true", help="Calculate b-tag weights for systematics?")
parser.add_option("--leptonFastSim", dest="leptonFastSim", default = False, action="store_true", help="Calculate weights for lepton fast sim scale factors?")
parser.add_option("--btagWeight", dest="btagWeight", default = 2, action="store", help="Max nBJet to calculate the b-tag weight for")
parser.add_option("--hadronicLeg", dest="hadronicLeg", default = False, action="store_true", help="Use only the hadronic leg of the sample?")
parser.add_option("--manScaleFactor", dest="manScaleFactor", default = 1, action="store", help="define a scale factor for the whole sample")
parser.add_option("--gluMass", dest="gluMass", default = 1000, action="store", help="gluino mass")

(options, args) = parser.parse_args()
skimCond = "(1)"
ht500lt250 = "Sum$(Jet_pt)>500&&(LepGood_pt[0]+met_pt)>250"
#common_skim = "HT500LT250"
common_skim = "signal"

if options.manScaleFactor!=1:
  target_lumi = target_lumi*float(options.manScaleFactor)
  print
  print "target lumi scaled!"
  print "New lumi:", target_lumi

if options.skim=='inc':
  skimCond = "(1)"

if sys.argv[0].count('ipython'):
  options.small=True


maxConsideredBTagWeight = options.btagWeight
calcSystematics = options.systematics
leptonFastSim = options.leptonFastSim

if leptonFastSim:
  leptonFastSimSF = leptonFastSimSF_()

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
       
##gluino mass to be processed
mglu = options.gluMass 
print mglu
pickleDir = '/afs/hephy.at/data/easilar01/Ra40b/pickleDir/T5qqqqWW_mass_nEvents_xsec_V2_'+str(mglu)+'_pkl'

exec('allSamples=['+options.allsamples+']')
for isample, sample in enumerate(allSamples):
  chunks, sumWeight = getChunks(sample)
  mass_dict = pickle.load(file(pickleDir))
  print mass_dict
  #for mglu in mass_dict.keys():
  for mlsp in mass_dict.keys() :
    skimCond = "Sum$(abs(GenPart_pdgId)==1000022&&abs(GenPart_motherId)==1000024&&abs(GenPart_grandmotherId)==1000021)==2&&(Sum$(abs(GenPart_pdgId)==24)==2)"
    mass_point = mass_dict[mlsp]
    skimCond += "&&GenSusyMGluino=="+str(mglu)+"&&GenSusyMNeutralino=="+str(mlsp)
    outDir = options.targetDir+"/".join([common_skim, 'SMS_T5qqqqVV_TuneCUETP8M1',str(mglu)+"_"+str(mlsp)])
    if os.path.exists(outDir) and os.listdir(outDir) != [] and not options.overwrite:
      print "Found non-empty directory: %s -> skipping!"%outDir
      continue

    tmpDir = outDir+'/tmp/'
    os.system('mkdir -p ' + outDir) 
    os.system('mkdir -p '+tmpDir)
    os.system('rm -rf '+tmpDir+'/*')

    if sample['isData']: 
      lumiScaleFactor=1
      branchKeepStrings = branchKeepStrings_DATAMC + branchKeepStrings_DATA 
    else:
      if ("TTJets" in sample['dbsName']): lumiScaleFactor = xsec[sample['dbsName']]*target_lumi/float(sumWeight)
      else: lumiScaleFactor = target_lumi/float(sumWeight)
      branchKeepStrings = branchKeepStrings_DATAMC + branchKeepStrings_MC
    if ("T5qqqqVV" in sample['name']) : lumiScaleFactor = mass_point["xSec"]*target_lumi/mass_point["nEntry"]  
    
    sampleKey = 'signal_inclusive'
    #if sample["name"] in mcEffDict.keys():
    #  sampleKey = sample["name"]
    #  print '##########################################'
    #  print '# Found MC truth efficiencies dictionary #'
    #  print '##########################################'
    #  print sample["name"]
    #else: sampleKey = 'none'
    
    readVariables = ['met_pt/F', 'met_phi/F', 'met_eta/F','met_mass/F' ,'nVert/I', 'nIsr/F']
    newVariables = ['weight/F','muonDataSet/I','eleDataSet/I']
    aliases = [ "met:met_pt", "metPhi:met_phi"]

    readVectors = [\
      {'prefix':'LepGood', 'nMax':8, 'vars':['pt/F', 'eta/F', 'phi/F', 'charge/F','pdgId/I', 'relIso03/F','SPRING15_25ns_v1/I' ,'tightId/I', 'miniRelIso/F','mass/F','sip3d/F','mediumMuonId/I','ICHEPmediumMuonId/I', 'mvaIdSpring15/F','lostHits/I', 'convVeto/I', 'eleCBID_SPRING15_25ns_ConvVetoDxyDz/I']},\
      {'prefix':'isoTrack', 'nMax': 8, 'vars':['pt/F', 'eta/F', 'phi/F','charge/F', 'pdgId/F','mass/F']}
    ]
    newVariables.extend(['puReweight_true/F','puReweight_true_max4/F','puReweight_true_Down/F','puReweight_true_Up/F','weight_diLepTTBar0p5/F','weight_diLepTTBar2p0/F','weight_XSecTTBar1p1/F','weight_XSecTTBar0p9/F','weight_XSecWJets1p1/F','weight_XSecWJets0p9/F'])
    newVariables.extend(['ngenGluino/I','genGluGlu_pt/F','ISRSigUp/F/1','ISRSigDown/F/1'])
    newVariables.extend(['flag_crazy_jets/I/1','nISRJets_new/I','weight_ISR_new/F/1','ISRSigUp_stat_new/F/1','ISRSigDown_stat_new/F/1','ISRSigUp_sys_new/F/1','ISRSigDown_sys_new/F/1'])
    newVariables.extend(['lepton_muSF_HIP/D/1','lepton_muSF_looseID/D/1.','lepton_muSF_mediumID/D/1.','lepton_muSF_miniIso02/D/1.','lepton_muSF_sip3d/D/1.','lepton_eleSF_cutbasedID/D/1.','lepton_eleSF_miniIso01/D/1.','lepton_eleSF_gsf/D/1.'])
    newVariables.extend(['lepton_muSF_HIP_err/D/0.','lepton_muSF_looseID_err/D/0.','lepton_muSF_mediumID_err/D/0.','lepton_muSF_miniIso02_err/D/0.','lepton_muSF_sip3d_err/D/0.','lepton_eleSF_cutbasedID_err/D/0.','lepton_eleSF_miniIso01_err/D/0.', 'lepton_eleSF_gsf_err/D/0.', 'lepton_muSF_systematic/D/0.'])


    readVectors.append({'prefix':'GenPart',  'nMax':100, 'vars':['eta/F','pt/F','phi/F','mass/F','charge/F', 'pdgId/I', 'motherId/F', 'grandmotherId/F','status/F']})
    #readVectors.append({'prefix':'genPartAll',  'nMax':100, 'vars':['eta/F','pt/F','phi/F','mass/F','charge/F', 'pdgId/I', 'motherId/F', 'grandmotherId/F','status/F']})
    readVectors.append({'prefix':'JetForMET',  'nMax':100, 'vars':['rawPt/F','pt/F', 'eta/F', 'phi/F','mass/F' ,'id/I','hadronFlavour/F','btagCSV/F', 'btagCMVA/F','corr_JECUp/F','corr_JECDown/F','corr/F']})
    readVectors.append({'prefix':'Jet',  'nMax':100, 'vars':['rawPt/F','pt/F', 'eta/F', 'phi/F','mass/F' ,'id/I','hadronFlavour/F','btagCSV/F', 'btagCMVA/F','corr_JECUp/F','corr_JECDown/F','corr/F','chHEF/F']})

    aliases.extend(['genMet:met_genPt', 'genMetPhi:met_genPhi'])
    ### Vars for JEC ###
    corr = ["central", "up", "down"]
    vars_corr = ["ht","LT","MeT","deltaPhi_Wl"]
    vars_corr_1 = ["nJet","nBJet"]
    for corrJEC_str in corr:
      for vars_str in vars_corr:
        newVariables.extend(["jec_"+vars_str+"_"+corrJEC_str+"/F/-999."])
        #print "jec_"+vars_str+"_"+corrJEC_str+"/F/-999."
      for vars_str in vars_corr_1:
        newVariables.extend(["jec_"+vars_str+"_"+corrJEC_str+"/I/-999."])

    newVariables.extend( ['nLooseSoftLeptons/I', 'nLooseHardLeptons/I', 'nTightSoftLeptons/I', 'nTightHardLeptons/I'] )
    newVariables.extend( ['deltaPhi_Wl/F','nBJetMediumCSV30/I','nJet30/I','htJet30j/F','st/F'])
    newVariables.extend( ['flag_jetCleaning_eventfilter/I/-2'])
    newVariables.extend( ['leptonPt/F','leptonEt/F','leptonMiniRelIso/F','leptonRelIso03/F' ,\
    'leptonEta/F', 'leptonPhi/F','leptonSPRING15_25ns_v1/I/-2','leptonPdg/I/0', 'leptonInd/I/-1',\
   'leptonMass/F', 'singleMuonic/I', 'singleElectronic/I', 'singleLeptonic/I' ]) #, 'mt2w/F'] )
    newVariables.extend( ["iso_had/F", "iso_pt/F","iso_MT2/F","iso_Veto/F"] )
    if calcSystematics:
      #newVariables.extend( ["weightBTag/F", "weightBTag_SF/F", "weightBTag_SF_b_Up/F", "weightBTag_SF_b_Down/F", "weightBTag_SF_light_Up/F", "weightBTag_SF_light_Down/F"])
      for i in range(maxConsideredBTagWeight+1):
        newVariables.extend( ["weightBTag"+str(i)+"/F", "weightBTag"+str(i)+"_SF/F", "weightBTag"+str(i)+"_SF_b_Up/F", "weightBTag"+str(i)+"_SF_b_Down/F", "weightBTag"+str(i)+"_SF_light_Up/F", "weightBTag"+str(i)+"_SF_light_Down/F"])
        #if i>0:
        newVariables.extend( ["weightBTag"+str(i+1)+"p/F", "weightBTag"+str(i+1)+"p_SF/F", "weightBTag"+str(i+1)+"p_SF_b_Up/F", "weightBTag"+str(i+1)+"p_SF_b_Down/F", "weightBTag"+str(i+1)+"p_SF_light_Up/F", "weightBTag"+str(i+1)+"p_SF_light_Down/F"])
    if leptonFastSim:
      newVariables.extend(['reweightLeptonFastSimSF/F', 'reweightLeptonFastSimSFUp/F', 'reweightLeptonFastSimSFDown/F'])
    newVars = [readVar(v, allowRenaming=False, isWritten = True, isRead=False) for v in newVariables]
    
    readVars = [readVar(v, allowRenaming=False, isWritten=False, isRead=True) for v in readVariables]
    for v in readVectors:
      readVars.append(readVar('n'+v['prefix']+'/I', allowRenaming=False, isWritten=False, isRead=True))
      v['vars'] = [readVar(v['prefix']+'_'+vvar, allowRenaming=False, isWritten=False, isRead=True) for vvar in v['vars']]

    printHeader("Compiling class to write")
    writeClassName = "ClassToWrite_"+str(isample)
    writeClassString = createClassString(className=writeClassName, vars= newVars, vectors=[], nameKey = 'stage2Name', typeKey = 'stage2Type')
    s = compileClass(className=writeClassName, classString=writeClassString, tmpDir=options.targetDir+'/tmp/')

    readClassName = "ClassToRead_"+str(isample)
    readClassString = createClassString(className=readClassName, vars=readVars, vectors=readVectors, nameKey = 'stage1Name', typeKey = 'stage1Type', stdVectors=False)
    printHeader("Class to Read")
    r = compileClass(className=readClassName, classString=readClassString, tmpDir=options.targetDir+'/tmp/')

    filesForHadd=[]
    if options.small: chunks=chunks[:1]
    for chunk in chunks:
      sourceFileSize = os.path.getsize(chunk['file'])
      nSplit = 1+int(sourceFileSize/(400*10**6)) #split into 400MB
      if nSplit>1: print "Chunk too large, will split into",nSplit,"of appox 400MB"
      for iSplit in range(nSplit):
        cut = "("+skimCond+")&&("+sample['postProcessingCut']+")" if sample.has_key('postProcessingCut') else skimCond
        t = getTreeFromChunk(chunk, cut, iSplit, nSplit)
        #t.GetListOfBranches().ls()
        if not t: 
          print "Tree object not found:", t
          continue
        t.SetName("Events")
        nEvents = t.GetEntries()
        for v in newVars:
          v['branch'] = t.Branch(v['stage2Name'], ROOT.AddressOf(s,v['stage2Name']), v['stage2Name']+'/'+v['stage2Type'])
        for v in readVars:
          t.SetBranchAddress(v['stage1Name'], ROOT.AddressOf(r, v['stage1Name']))
        for v in readVectors:
          for var in v['vars']:
            t.SetBranchAddress(var['stage1Name'], ROOT.AddressOf(r, var['stage1Name']))
        for a in aliases:
          t.SetAlias(*(a.split(":")))
        print "File: %s Chunk: %s nEvents: %i (skim: %s) condition: %s lumiScaleFactor: %f"%(chunk['file'],chunk['name'], nEvents, options.skim, skimCond, lumiScaleFactor)
        
        for i in range(nEvents):
          if (i%10000 == 0) and i>0 :
            print i,"/",nEvents  , "name:" , chunk['name']
          s.init()
          r.init()
          t.GetEntry(i)
          genWeight = 1 if sample['isData'] else t.GetLeaf('genWeight').GetValue()
          xsec_branch = 1 if sample['isData'] else t.GetLeaf('xsec').GetValue()
          s.weight = lumiScaleFactor*genWeight
          if sample['isData']:
            if "Muon" in sample['name']:
              s.muonDataSet = True
              s.eleDataSet = False
            if "Electron" in sample['name']:
              s.muonDataSet = False
              s.eleDataSet = True

          nTrueInt = t.GetLeaf('nTrueInt').GetValue()
          
          if not sample['isData']:
            s.muonDataSet = False
            s.eleDataSet = False
            s.weight =xsec_branch*lumiScaleFactor*genWeight
            nTrueInt = t.GetLeaf('nTrueInt').GetValue()
            s.puReweight_true = PU_histo_63.GetBinContent(PU_histo_63.FindBin(nTrueInt))
            s.puReweight_true_max4 = min(4,s.puReweight_true)
            s.puReweight_true_Down = PU_histo_59p85.GetBinContent(PU_histo_59p85.FindBin(nTrueInt))
            s.puReweight_true_Up = PU_histo_66p15.GetBinContent(PU_histo_66p15.FindBin(nTrueInt))
            ngenLep = t.GetLeaf('ngenLep').GetValue()
            ngenTau = t.GetLeaf('ngenTau').GetValue()
            if ("TTJets" in sample['dbsName']):
              s.weight = lumiScaleFactor*genWeight
              s.weight_XSecTTBar1p1 = s.weight*1.1
              s.weight_XSecTTBar0p9 = s.weight*0.9
              if ngenLep+ngenTau == 2:
                s.weight_diLepTTBar2p0 = s.weight*2.0
                s.weight_diLepTTBar0p5 = s.weight*0.5
              else :
                s.weight_diLepTTBar2p0 = s.weight
                s.weight_diLepTTBar0p5 = s.weight
            else :
              s.weight_XSecTTBar1p1 = s.weight
              s.weight_XSecTTBar0p9 = s.weight
              s.weight_diLepTTBar2p0 = s.weight
              s.weight_diLepTTBar0p5 = s.weight
            if "WJets" in sample['dbsName']:
              s.weight_XSecWJets1p1 = s.weight*1.1
              s.weight_XSecWJets0p9 = s.weight*0.9
            else :
              s.weight_XSecWJets1p1 = s.weight
              s.weight_XSecWJets0p9 = s.weight       
          if ("T5qqqqVV" in sample['name']) : s.weight = lumiScaleFactor*genWeight
   
          #get all >=loose lepton indices
          looseLepInd = cmgLooseLepIndices(r) 
          #split into soft and hard leptons
          looseSoftLepInd, looseHardLepInd = splitIndList(r.LepGood_pt, looseLepInd, 25.)
          #select tight soft leptons (no special tight ID for now)
          tightSoftLepInd = looseSoftLepInd #No tight soft selection as of yet 
          #select tight hard leptons (use POG ID)
          tightHardLepInd = filter(lambda i:(abs(r.LepGood_pdgId[i])==11 and cmgTightEleID(r,i)) \
                                         or (abs(r.LepGood_pdgId[i])==13 and cmgTightMuID(r,i)), looseHardLepInd)  


          s.nLooseSoftLeptons = len(looseSoftLepInd)
          s.nLooseHardLeptons = len(looseHardLepInd)
          s.nTightSoftLeptons = len(tightSoftLepInd)
          s.nTightHardLeptons = len(tightHardLepInd)
          vars = ['pt', 'eta', 'phi', 'charge','miniRelIso','relIso03', 'pdgId', 'SPRING15_25ns_v1','eleCBID_SPRING15_25ns_ConvVetoDxyDz']
          allLeptons = [getObjDict(t, 'LepGood_', vars, i) for i in looseLepInd]
          looseSoftLep = [getObjDict(t, 'LepGood_', vars, i) for i in looseSoftLepInd] 
          looseHardLep = [getObjDict(t, 'LepGood_', vars, i) for i in looseHardLepInd]
          tightSoftLep = [getObjDict(t, 'LepGood_', vars, i) for i in tightSoftLepInd]
          tightHardLep =  [getObjDict(t, 'LepGood_', vars, i) for i in tightHardLepInd]
          leadingLepInd = None
          if s.nTightHardLeptons>=1:
            leadingLepInd = tightHardLepInd[0]
            s.leptonPt  = r.LepGood_pt[leadingLepInd]
            s.leptonMiniRelIso = r.LepGood_miniRelIso[leadingLepInd]
            s.leptonRelIso03 = r.LepGood_relIso03[leadingLepInd]
            s.leptonInd = leadingLepInd 
            s.leptonEta = r.LepGood_eta[leadingLepInd]
            s.leptonPhi = r.LepGood_phi[leadingLepInd]
            s.leptonPdg = r.LepGood_pdgId[leadingLepInd]
            s.leptonMass= r.LepGood_mass[leadingLepInd]
            #s.leptonSPRING15_25ns_v1= r.LepGood_SPRING15_25ns_v1[leadingLepInd]
            s.leptonSPRING15_25ns_v1= r.LepGood_eleCBID_SPRING15_25ns_ConvVetoDxyDz[leadingLepInd]
            s.st = r.met_pt + s.leptonPt
          s.singleLeptonic = s.nTightHardLeptons==1
          if s.singleLeptonic:
            lep_vec = ROOT.TLorentzVector()
            lep_vec.SetPtEtaPhiM(s.leptonPt,s.leptonEta,s.leptonPhi,s.leptonMass)
            s.leptonEt = lep_vec.Et()
            s.singleMuonic      =  abs(s.leptonPdg)==13
            s.singleElectronic  =  abs(s.leptonPdg)==11
          else:
            s.singleMuonic      = False 
            s.singleElectronic  = False 

          j_list=['eta','pt','phi','btagCMVA', 'btagCSV', 'id', 'chHEF']
          jets = filter(lambda j:j['pt']>30 and abs(j['eta'])<2.4 and j['id'], get_cmg_jets_fromStruct(r,j_list))
          lightJets,  bJetsCSV = splitListOfObjects('btagCSV', 0.800, jets)
          s.htJet30j = sum([x['pt'] for x in jets])
          s.nJet30 = len(jets)
          s.nBJetMediumCSV30 = len(bJetsCSV)
          #s.mt2w = mt2w.mt2w(met = {'pt':r.met_pt, 'phi':r.met_phi}, l={'pt':s.leptonPt, 'phi':s.leptonPhi, 'eta':s.leptonEta}, ljets=lightJets, bjets=bJetsCSV)
          s.deltaPhi_Wl = acos((s.leptonPt+r.met_pt*cos(s.leptonPhi-r.met_phi))/sqrt(s.leptonPt**2+r.met_pt**2+2*r.met_pt*s.leptonPt*cos(s.leptonPhi-r.met_phi))) 
          s.iso_had  = 999        
          s.iso_pt   = 999
          s.iso_MT2  = 999
          s.iso_Veto = True
          if s.nTightHardLeptons >=1 and r.nisoTrack>=1:
            #print lumi_branch , evt_branch
            #print "nLeptons:" , s.nTightHardLeptons
            #print "!!!!!nisoTrack!!!!!1" , r.nisoTrack
            #print "tight lepton pt: " , tightHardLep[0]["pt"] 
            var_list = ['pt', 'eta', 'phi','charge','pdgId','mass']
            tracks = get_cmg_isoTracks_fromStruct(r,var_list)
            met_4vec = ROOT.TLorentzVector()
            met_4vec.SetPtEtaPhiM(r.met_pt,r.met_eta,r.met_phi,r.met_mass)
            get_mt2(s,r,tightHardLep,tracks,met_4vec)
            #print "met pt :" , r.met_pt
            #print s.iso_had , s.iso_pt , s.iso_MT2 , s.iso_Veto

          g_list=['eta','pt','phi','mass','charge', 'pdgId', 'motherId', 'grandmotherId' , 'status']
          genParts = get_cmg_genParts_fromStruct(r,g_list)
          #genPartsAll = get_cmg_genPartsAll(c)
          ####
          #isrJets = get_matched_Jets(jets,genParts)
          nISR = r.nIsr
          #print "ISR" , nISR
          getISRWeight_new(s,nISR)
          s.flag_crazy_jets = filter_crazy_jets(jets,genParts)
          ####
          getISRWeight(s,genParts)
          fill_branch_WithJEC(s,r)
          calc_LeptonScale_factors_and_systematics(s,histos_LS)
          if calcSystematics: 
            calc_btag_systematics(t,s,r,mcEffDict,sampleKey,maxConsideredBTagWeight,separateBTagWeights, model='T5qqqqWW')
          
          if leptonFastSim:
            if s.nTightHardLeptons>=1:
              s.reweightLeptonFastSimSF     = leptonFastSimSF.get2DSF(pdgId=s.leptonPdg, pt=s.leptonPt, eta=s.leptonEta, nvtx = r.nVert)
              s.reweightLeptonFastSimSFUp   = leptonFastSimSF.get2DSF(pdgId=s.leptonPdg, pt=s.leptonPt, eta=s.leptonEta, nvtx = r.nVert, sigma = +1)
              s.reweightLeptonFastSimSFDown = leptonFastSimSF.get2DSF(pdgId=s.leptonPdg, pt=s.leptonPt, eta=s.leptonEta, nvtx = r.nVert, sigma = -1)
            else:
              s.reweightLeptonFastSimSF     = -999 
              s.reweightLeptonFastSimSFUp   = -999
              s.reweightLeptonFastSimSFDown = -999
            

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
        if size>(0.5*(10**9)) or f==filesForHadd[-1] or len(files)>200:
          ofile = outDir+'/'+sample['name']+'_'+options.skim+'_'+str(counter)+'.root'
          print "Running hadd on", tmpDir, files
          os.system('cd '+tmpDir+';hadd -f '+ofile+' '+' '.join(files))
          print "Written", ofile
          size=0
          counter+=1
          files=[]
      os.system("rm -rf "+tmpDir)

