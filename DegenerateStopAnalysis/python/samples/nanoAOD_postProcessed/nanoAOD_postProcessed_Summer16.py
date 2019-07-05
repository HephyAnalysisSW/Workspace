""" Sample definition file for nanoAOD post-processed ntuples using 2016 data and MC production at 25 ns for the degenerate stop analysis.
 
Each set of ntuples is produced with a git tag of HephySusySW.Workspace repository and and is saved in a directory:
  
   {path}/nanoTuples/{processingEra}/{processingTag}/{campaign}/{inc/soft/...}
   
    processingEra: postProcessed_mAODv2_v* (always starts with "postProcessed_")
    processingTag: 80X_postProcessing_v* (git tag of HephySusySW.Workspace)
    
    campaign:
        MC production campaign for MC samples  (e.g. RunIISpring16MiniAODv2, with _25ns added as additional identification)
        Energy, reconstruction tag, era for data (e.g. 13TeV_PromptReco_Collisions15_25ns, taken from JSON name file)
    
The corresponding py sample files are called: 
    RunIISpring16MiniAODv2_v*.py 
    Data2016_v*.py

"""

import copy
import os
import sys
import pickle
import importlib
 
# most recent paths, can be replaced when initializing the nanoPostProcessed class
ppDir = "/afs/hephy.at/data/mzarucki01/nanoAOD/DegenerateStopAnalysis/postProcessing/processing_RunII_v6_0/nanoAOD_v6_0-0"
mc_path     = ppDir + "/Summer16_05Feb2018"
data_path   = ppDir + "/Run2016_05Feb2018"

signal_path = mc_path

# Lumi that was used in the weight calculation of PostProcessing in pb-1
lumi_norm = 'lumi_norm' 

class nanoPostProcessed():

    def makeSample(self, sample):
        i = copy.deepcopy(sample)
        i['dir'] = os.path.join(i['dir'],         'inc', 'incLep')

        ol = copy.deepcopy(sample)
        ol['dir'] = os.path.join(ol['dir'],       'inc', 'oneLep')
        
        ol20 = copy.deepcopy(sample)
        ol20['dir'] = os.path.join(ol20['dir'],   'inc', 'oneLep20')
        
        tl = copy.deepcopy(sample)
        tl['dir'] = os.path.join(tl['dir'],       'inc', 'twoLep')
        
        oll = copy.deepcopy(sample)
        oll['dir'] = os.path.join(oll['dir'],     'inc', 'oneLepLoose')
        
        oll20 = copy.deepcopy(sample)
        oll20['dir'] = os.path.join(oll20['dir'], 'inc', 'oneLepLoose20')
        
        tll = copy.deepcopy(sample)
        tll['dir'] = os.path.join(tll['dir'],     'inc', 'twoLepLoose')
        
        olt = copy.deepcopy(sample)
        olt['dir'] = os.path.join(olt['dir'],     'inc', 'oneLepTight')
        
        olt20 = copy.deepcopy(sample)
        olt20['dir'] = os.path.join(olt20['dir'], 'inc', 'oneLepTight20')
        
        tlt = copy.deepcopy(sample)
        tlt['dir'] = os.path.join(tlt['dir'],     'inc', 'twoLepTight')
        
        met200 = copy.deepcopy(sample)
        met200['dir'] = os.path.join(met200['dir'], 'met200',             'incLep')

        pil = copy.deepcopy(sample)
        pil['dir'] = os.path.join(pil['dir'],       'met200_ht200_isr90', 'incLep')
        
        return {
            'inc': i,
            'oneLep': ol,
            'twoLep': tl,
            'oneLep20': ol20,
            'oneLepLoose': oll,
            'oneLepLoose20': oll20,
            'twoLepLoose': tll,
            'oneLepTight': olt,
            'oneLepTight20': olt20,
            'twoLepTight': tlt,
            'met200': met200,
            'preIncLep': pil,
            }

    def getDataSample(self, name, bins):
        s = self.makeSample({
            "name" : name,
            "bins" : [bins] if type(bins)==type("") else bins,
            'dir' : self.data_path,
            })
        #
        return s

    def getSignalSample(self, signal, sampleId=0):
        return {
            "name" : signal,
            "chunkString": signal,
            'dir' : self.signal_path,
            'bins':[signal],
            'sampleId' : sampleId,
            }

    def __init__(self, mc_path=mc_path, signal_path=signal_path, data_path=data_path, lumi_norm=lumi_norm , ichepdata=False):

        self.mc_path = mc_path
        self.signal_path = signal_path
        self.data_path = data_path
        self.lumi = lumi_norm
        self.ichepdata = ichepdata
        sampleDefFile = os.path.abspath(__file__)

        print "\n=================================================================================\n"
        print "Getting samples from", sampleDefFile, "\n"
        print "MC directory:    ", self.mc_path
        print "Signal directory:", self.signal_path
        print "Data directory:  ", self.data_path
        print "\n=================================================================================\n"

        self.TTJets_SingleLepton = self.makeSample({
            "name" : "TTJets_SingleLepton",
            "bins" : [
                         'TTJets_SingleLeptonFromT_comb',
                         'TTJets_SingleLeptonFromTbar_comb',
                ],
            'dir' : self.mc_path,
            'sampleId': 65,
            })

        self.TTJets_DiLepton = self.makeSample({
            "name" : "TTJets_DiLepton",
            "bins" : [
                         'TTJets_DiLept_comb',
                ],
            'dir' : self.mc_path,
            'sampleId': 70,
            })

        self.TTX = self.makeSample({
            "name" : "TTX",
            "bins" : [
                        'TTW_LO',
                        'TTZ_LO',
                ],
            'dir' : self.mc_path,
            'sampleId': 90,
            })

        self.WJetsHT = self.makeSample({
            "name" : "WJetsHT",
            "bins" : [
                      'WJetsToLNu_HT70to100',
                      'WJetsToLNu_HT100to200_comb',
                      'WJetsToLNu_HT200to400_comb',
                      'WJetsToLNu_HT400to600_comb',
                      'WJetsToLNu_HT600to800_comb',
                      'WJetsToLNu_HT800to1200_comb',
                      'WJetsToLNu_HT1200to2500',
                      'WJetsToLNu_HT2500toInf_comb',

                    ],
            'dir' : self.mc_path,
            'sampleId' : 10,
            })

        self.QCD = self.makeSample({
            "name" : "QCD",
            "bins" :  [
                        'QCD_HT50to100',
                        'QCD_HT100to200',
                        'QCD_HT200to300_comb',
                        'QCD_HT300to500_comb',
                        'QCD_HT500to700_comb',
                        'QCD_HT700to1000_comb',
                        'QCD_HT1000to1500_comb',
                        'QCD_HT1500to2000_comb',
                        'QCD_HT2000toInf_comb'

                ],
            'dir' : self.mc_path,
            'sampleId' : 30,

        })


        self.ZJetsHT = self.makeSample({
            "name" : "ZJetsHT",
            "bins" :  [
                       'ZJetsToNuNu_HT100to200_comb',
                       'ZJetsToNuNu_HT200to400_comb',
                       'ZJetsToNuNu_HT400to600_comb',
                       'ZJetsToNuNu_HT600to800',
                       'ZJetsToNuNu_HT800to1200',
                       #'ZJetsToNuNu_HT1200to2500',
                       'ZJetsToNuNu_HT1200to2500_ext',
                       'ZJetsToNuNu_HT2500toInf',

                      ] ,
            'dir' : self.mc_path ,
            'sampleId': 40,
            })


        self.DYJetsM5to50 = self.makeSample({
            "name" : "DYJetsM5to50",
            "bins" :  [
                       'DYJetsToLL_M5to50_HT100to200_comb',
                       'DYJetsToLL_M5to50_HT200to400_comb',
                       'DYJetsToLL_M5to50_HT400to600_comb',
                       'DYJetsToLL_M5to50_HT600toInf_comb',
                      ] ,
            'dir' : self.mc_path
            })


        self.DYJetsM50HT = self.makeSample({
            "name" : "DYJetsM50HT",
            "bins" :  [
                        "DYJetsToLL_M50_HT70to100",
                        "DYJetsToLL_M50_HT100to200_comb",
                        "DYJetsToLL_M50_HT200to400_comb",
                        "DYJetsToLL_M50_HT400to600_comb",
                        "DYJetsToLL_M50_HT600to800"  ,
                        "DYJetsToLL_M50_HT800to1200" ,
                        "DYJetsToLL_M50_HT1200to2500",
                        "DYJetsToLL_M50_HT2500toInf" ,

                ] ,
            'dir' : self.mc_path,
            'sampleId': 50,
            })

        self.VV = self.makeSample({
        "name" : "VV",
        "bins" :  [
                   "WWTo2L2Nu",
                   "WWToLNuQQ_comb",
                   'WWTo1L1Nu2Q', # FIXME: Not used before?
    
                   "ZZTo2L2Nu",
                   "ZZTo2Q2Nu",
                   "ZZTo4L",
                   "ZZTo2L2Q",

                   #"WZTo1L3Nu", # NOTE: missing
                   "WZTo1L1Nu2Q",
                   #"WZTo2L2Q", # NOTE: missing
                   "WZTo3LNu_comb", # FIXME: prblm?
                   ],
        'dir' : self.mc_path
        })

        self.ST = self.makeSample({
        "name" : "SingleTop",
        "bins" :  [
                   'T_tWch_ext',
                   'T_tch_powheg',
                   'TBar_tWch_ext',
                   'TBar_tch_powheg',
                  ] ,
        'dir' : self.mc_path
        })

        ######################################################################################################
        #####################################                  ###############################################
        #####################################       DATA       ###############################################
        #####################################                  ###############################################
        ######################################################################################################

        dataSamples = {
            "MET_Run2016_05Feb2018": {
                'bins': 
                    [
                    "MET_Run2016B_05Feb2018_ver2",
                    "MET_Run2016C_05Feb2018",
                    "MET_Run2016D_05Feb2018", 
                    "MET_Run2016E_05Feb2018",
                    "MET_Run2016F_05Feb2018", 
                    "MET_Run2016G_05Feb2018",
                    "MET_Run2016H_05Feb2018_ver2",
                    "MET_Run2016H_05Feb2018_ver3",
                    ]
            },
        }

        for dataset in dataSamples:
            sample = self.getDataSample(dataset, dataSamples[dataset]['bins'])
            setattr(self, dataset, sample)

            for bin in dataSamples[dataset]['bins']:
                sample = self.getDataSample(bin, bin)
                setattr(self, bin, sample)

        # signal samples

        allSignalStrings = [
            "T2tt_mStop_850_mLSP_100",
            "T2tt_mStop_500_mLSP_325",
            #"T2DegStop_300_270",
            #"T2DegStop_300_290_FastSim",
            #"T2DegStop_300_270_FastSim",
            #"T2DegStop_300_240_FastSim",
            #"T2tt_300_270_FastSim",
            ]

        for s in allSignalStrings:
            sm = self.makeSample(self.getSignalSample(s))
            setattr(self, s, sm)

        signals_info = {
                             "SMS_T2tt_dM_10to80":                                   {'mass_template':'SMS_T2tt_mStop_%s_mLSP_%s',              'pkl':'SMS_T2tt_dM_10to80_genHT_160_genMET_80_mass_dict.pkl',               'scanId':1,   'shortName':'t2tt%s_%s', 'niceName':'T2tt_%s_%s'},
                             #"SMS_T2tt_dM_10to80_genHT_160_genMET_80":              {'mass_template':'SMS_T2tt_mStop_%s_mLSP_%s',              'pkl':'SMS_T2tt_dM_10to80_genHT_160_genMET_80_mass_dict.pkl',               'scanId':1,   'shortName':'t2ttold%s_%s', 'niceName':'T2tt_%s_%s_mWMin5'},
                             #"SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1":{'mass_template':'SMS_T2bW_X05_mStop_%s_mLSP_%s_mWMin0p1', 'pkl':'SMS_T2bW_X05_dM_10to80_genHT_160_genMET_80_mWMin_0p1_mass_dict.pkl', 'scanId':2,   'shortName':'t2bw%s_%s',    'niceName':'T2bW_%s_%s'},
                             #"SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1":    {'mass_template':'SMS_T2tt_mStop_%s_mLSP_%s_mWMin0p1',     'pkl':'SMS_T2tt_dM_10to80_genHT_160_genMET_80_mWMin_0p1_mass_dict.pkl',     'scanId':3,   'shortName':'t2tt%s_%s',    'niceName':'T2tt_%s_%s'},
                             #"SMS_TChiWZ_genHT_160_genMET_80":                      {'mass_template':'SMS_TChiWZ_Chipm2_%s_mLSP_%s',           'pkl':'SMS_TChiWZ_genHT_160_genMET_80_mass_dict.pkl',                       'scanId':4,   'shortName':'tchiwz%s_%s',  'niceName':'TChiWZ_%s_%s'},
                             #"SMS_TChiWZ_genHT_160_genMET_80_3p":                   {'mass_template':'SMS_TChiWZ_Chipm2_%s_mLSP_%s',           'pkl':'SMS_TChiWZ_genHT_160_genMET_80_3p_mass_dict.pkl',                    'scanId':4,   'shortName':'tchiwz%s_%s',  'niceName':'TChiWZ_%s_%s'},
                             #"MSSM_higgsino_genHT_160_genMET_80":                   {'mass_template':'MSSM_higgsino_mu_%s_M1_%s',              'pkl':'MSSM_higgsino_genHT_160_genMET_80_mass_dict.pkl',                    'scanId':5,   'shortName':'hino%s_%s',    'niceName':'Hino_%s_%s'},
                             #"MSSM_higgsino_genHT_160_genMET_80_3p":                {'mass_template':'MSSM_higgsino_mu_%s_M1_%s',              'pkl':'MSSM_higgsino_genHT_160_genMET_80_3p_mass_dict.pkl',                 'scanId':5,   'shortName':'hino%s_%s',    'niceName':'Hino_%s_%s'},
                             #"SMS_C1C1_higgsino_genHT_160_genMET_80_3p":            {'mass_template':'SMS_C1C1_mChipm1_%s_mLSP_%s',            'pkl':'SMS_C1C1_higgsino_genHT_160_genMET_80_3p_mass_dict.pkl',             'scanId':123, 'shortName':'c1c1h%s_%s',   'niceName':'C1C1_%s_%s'},
                             #"SMS_C1N1_higgsino_genHT_160_genMET_80_3p":            {'mass_template':'SMS_C1N1_mChipm1_%s_mLSP_%s',            'pkl':'SMS_C1N1_higgsino_genHT_160_genMET_80_3p_mass_dict.pkl',             'scanId':123, 'shortName':'c1n1h%s_%s',   'niceName':'C1N1_%s_%s'},
                             #"SMS_N2C1_higgsino_genHT_160_genMET_80_3p":            {'mass_template':'SMS_N2C1_mChi02_%s_mChipm01_%s',         'pkl':'SMS_N2C1_higgsino_genHT_160_genMET_80_3p_mass_dict.pkl',             'scanId':123, 'shortName':'n2c1h%s_%s',   'niceName':'N2C1_%s_%s'},
                             #"SMS_N2N1_higgsino_genHT_160_genMET_80_3p":            {'mass_template':'SMS_N2N1_mChi02_%s_mLSP_%s',             'pkl':'SMS_N2N1_higgsino_genHT_160_genMET_80_3p_mass_dict.pkl',             'scanId':123, 'shortName':'n2n1h%s_%s',   'niceName':'N2N1_%s_%s'},
                       }
  
        self.signals_info = signals_info
        
        #cmgVersion = os.path.splitext(os.path.basename(__file__))[0].split('_')[2]
        #cmg_MC_path =   'Workspace.DegenerateStopAnalysis.samples.cmgTuples.RunIISummer16MiniAODv2_%s'%cmgVersion
        #cmg_MC = importlib.import_module(cmg_MC_path)
        #sample_path = cmg_MC.sample_path

        sample_path = "" # FIXME: specify mass_dict path

        for signal_name, signal_info in signals_info.items():
            mass_template            = signal_info['mass_template']
            scanId                   = signal_info['scanId']
            signal_mass_dict         = signal_info['pkl']
            
            mass_dict_path           = os.path.join(sample_path, "mass_dicts")
            mass_dict_pickle_file    = os.path.join(mass_dict_path, signal_mass_dict)
            signal_info['mass_dict'] = mass_dict_pickle_file 

            if os.path.isfile(mass_dict_pickle_file):
                mass_dict_pickle = mass_dict_pickle_file
                mass_dict        = pickle.load(open(mass_dict_pickle,"r"))
            else:
                print "!!!!! WARNING !!!!! NO MASS DICT FOUND! %s"%mass_dict_pickle_file
                print "!!!!! If no other fix available, enable useProxyMassDict and set mass_dict_pickle by hand!"
                mass_dict_pickle = None
                mass_dict        = {}

                useProxyMassDict = False
                if useProxyMassDict:
                    mass_dict_pickle = "/afs/hephy.at/data/nrad01/cmgTuples/postProcessed_mAODv2/8012_mAODv2_v3/80X_postProcessing_v10/analysisHephy_13TeV_2016_v0/step1/RunIISpring16MiniAODv2_v3/SMS_T2tt_dM_10to80_genHT_160_genMET_80_mass_dict.pkl"
                    mass_dict        = pickle.load(open(mass_dict_pickle,"r"))
                    print "!!!!!!!!!!! DOUBLE WARNING! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! USING PROXY MASS PICKLE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
             
            mass_scan = {}

            for mstop in mass_dict:
                for mlsp in mass_dict[mstop]:
                    #mass_point = "SMS_T2tt_mStop_%s_mLSP_%s" % (mstop, mlsp)
                    mass_point = mass_template % (mstop, mlsp)
                    mass_scan[mass_point] = {
                        "name" : mass_point.replace(".","p"),
                        "bins": [mass_point.replace(".","p")],
                        'dir' : self.signal_path,
                        'sampleId': "%s%s%s" % (scanId, mstop, mlsp)
                        }


            for sig in mass_scan:
                sm = self.makeSample(mass_scan[sig])
                setattr(self, sig.replace(".","p"), sm)

if __name__=="__main__":
    PP = nanoPostProcessed(mc_path, signal_path, data_path)
