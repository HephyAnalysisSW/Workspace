''' Parameter set for HEPHY analysis at 13 TeV analysis.

'''

# imports python standard modules or functions
import collections
import operator
import copy


# imports user modules or functions

#

def getParameterSet(args):
    '''Return a dictionary containing all the parameters used for post-processing.
    
    Define in this function all the parameters used for post-processing. 
    No hard-coded values are allowed in the functions of post-processing module, 
    explicitly or via "default value"
    
    More sets of parameters can be defined, with the set used in a job chosen via the argument parser,
    with the argument --parameterSet. 
    '''

    #
    # arguments to build the parameter set
    skimGeneral = args.skimGeneral
    skimLepton = args.skimLepton
    skimPreselect = args.skimPreselect

    processTracks = args.processTracks
    processLepAll = args.processLepAll
    
    # parameter set definitions
        
    params = collections.OrderedDict()
    
    
    # target luminosity (fixed value, given here)

    params['target_lumi'] = 10000  # pb-1

    # skimmimg parameters

    if skimPreselect:
        # branches for preselection (scalars or vectors) must be included in readVar or readVectors
        metCut = "(met_pt>200)"
        leadingJet_pt = "((Max$(Jet_pt*(abs(Jet_eta)<2.4 && Jet_id) ) > 90 ) >=1)"
        HTCut = "(Sum$(Jet_pt*(Jet_pt>30 && abs(Jet_eta)<2.4 && (Jet_id)) ) >200)"

        skimPreselectCondition = "(%s)" % '&&'.join([metCut, leadingJet_pt, HTCut])
    else:
        skimPreselectCondition = ''
        pass

    # lepton skimming
    #
    # branches (scalars or vectors) used here must be included in readVar or readVectors via
    # LepGood 'common' branches
    if skimLepton == 'incLep':
        # keep an empty string for inclusive lepton
        skimLeptonCondition = ''
    elif skimLepton == 'oneLep':
        skimLeptonCondition = " ((nLepGood >=1 && LepGood_pt[0] > 20) || (nLepOther >=1 && LepOther_pt[0] > 20))"
    else:
        pass

    SkimParameters = {
        'lheHThigh': {
            'lheHTIncoming': 600
            },
        'lheHTlow': {
            'lheHTIncoming': 600
            },
        'skimPreselect': skimPreselectCondition,
        'skimLepton': skimLeptonCondition,
        }

    params['SkimParameters'] = SkimParameters

    # lepton (electron and muon) selection
    
    LepGoodSel = {
        # prefix, existing branches to be read (to be used in post-processing and/or printed in debug mode) 
        # and new branches to be written for leptons (printed also in debug mode)
        # 'common' 'branches' and 'newBranches' are common for electron and muons 
        'branchPrefix': 'LepGood',
        'branches': {
            'mu': [
                'tightId/I', 'mediumMuonId/I',
                ],
            'el': [
                'SPRING15_25ns_v1/I', 'mvaIdSpring15/F',
                'hadronicOverEm/F',
                'dEtaScTrkIn/F', 'dPhiScTrkIn/F', 'eInvMinusPInv/F', 'lostHits/I',
                'convVeto/I',
                'etaSc/F',
                ],
            'common': [
                'pdgId/I',
                'pt/F', 'eta/F', 'phi/F',
                'relIso03/F', 'relIso04/F', 'miniRelIso/F', 'absIso03/F', 'absIso/F', 'sip3d/F',
                'dxy/F', 'dz/F',
                'mass/F', 'Q80/F', 'mt/F', 'cosPhiLepMet/F',
                ],
            },
        'newBranches': {
            'mu': [],
            'el': [],
            'common': [        
                'lt/F', 'dPhiLepW/F', 
                'isLepGood/I/0', 'isLepOther/I/0',
                ],
            },
        #
        # maximum number of objects kept
        'nMax': 8,
        #
        # muon selection
        'mu': {
            'pdgId': ('pdgId', operator.eq, 13, operator.abs),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.4, operator.abs),
            'dxy': ('dxy', operator.lt, 0.02, operator.abs),
            'dz': ('dz', operator.lt, 0.5, operator.abs),
            'hybIso': {
                'ptSwitch': 25, 
                'relIso': {
                    'type': 'relIso03',
                    'cut': 0.2
                    },
                'absIso': 5
                },
            },
        
         'mu2': { #muon selection without hybIso cut
            'pdgId': ('pdgId', operator.eq, 13, operator.abs),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.4, operator.abs),
            'dxy': ('dxy', operator.lt, 0.02, operator.abs),
            'dz': ('dz', operator.lt, 0.5, operator.abs),
            },
        
        #
        # electron selection
        # https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Spring15_selection_25ns
        'el': { #selection with Veto Electron ID
            'pdgId': ('pdgId', operator.eq, 11, operator.abs),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.5, operator.abs),
            'dxy': ('dxy', operator.lt, 0.02, operator.abs), #synchronisation with muons
            'dz': ('dz', operator.lt, 0.5, operator.abs), #synchronisation with muons
            'SPRING15_25ns_v1': ('SPRING15_25ns_v1', operator.ge, 1), #EG POG Veto ID
            
            'hybIso': {
                'ptSwitch': 25, 
                'relIso': {
                    'type': 'relIso03',
                    'cut': 0.2
                    },
                'absIso': 5
                },
            
            'evalRange_isGap': {
                'var': 'etaSc',
                'operVar': operator.abs,
                'lowRange': (operator.le, 1.4442),
                'highRange': (operator.ge, 1.566),
                },
            },
        
        'el2': { #selection with Veto Electron ID (without sigmaEtaEta cut) and no hybIso cut
            'pdgId': ('pdgId', operator.eq, 11, operator.abs),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.5, operator.abs),
            'dxy': ('dxy', operator.lt, 0.02, operator.abs), #synchronisation with muons
            'dz': ('dz', operator.lt, 0.5, operator.abs), #synchronisation with muons
           
            'evalRange_isGap': {
                'var': 'etaSc',
                'operVar': operator.abs,
                'lowRange': (operator.le, 1.4442),
                'highRange': (operator.ge, 1.566),
                },
            
            'convVeto': ('convVeto', operator.eq, 1),
            
            'elWP': { #EG POG Veto ID without sigmaEtaEta
                'eta_EB': 1.479, 'eta_EE': 2.5,
                'vars': {
                    'hadronicOverEm': {
                        'EB': 0.181, 'EE': 0.116, 'opCut': operator.lt, 'opVar': None,
                        },
                    'dEtaScTrkIn': {
                        'EB': 0.0152, 'EE': 0.0113, 'opCut': operator.lt, 'opVar': operator.abs,
                        },
                    'dPhiScTrkIn': {
                        'EB': 0.216, 'EE': 0.237, 'opCut': operator.lt, 'opVar': operator.abs,
                        },
                    'eInvMinusPInv': {
                        'EB': 0.207, 'EE':  0.174, 'opCut': operator.lt, 'opVar': operator.abs,
                        },
                    'dxy': {
                        'EB': 0.0564, 'EE': 0.222, 'opCut': operator.lt, 'opVar': operator.abs,
                        },
                    'dz': {
                        'EB': 0.472, 'EE': 0.921, 'opCut': operator.lt, 'opVar': operator.abs,
                        },
                    'lostHits': {
                        'EB': 2, 'EE': 3, 'opCut': operator.le, 'opVar': None,
                        },
                    },
                },
            },
        }

    params['LepGoodSel'] = LepGoodSel

    if processLepAll:
        LepOtherSel = copy.deepcopy(LepGoodSel)
        LepOtherSel['branchPrefix'] = 'LepOther'
        
        params['LepOtherSel'] = LepOtherSel

    # jet selection
    #    bas: basic jets
    #    veto: jets used for QCD veto, selected from basic jets
    #    isr: ISR jets, selected from basic jets
    #    isrH: ISR jet, higher threshold for SR2, selected from basic jets
    #    bjet: b jets, tagged with algorithm btag, separated in soft and hard b jets 
        
    JetSel = {
        'branchPrefix': 'Jet',
        'branches': [
            'pt/F', 'eta/F', 'phi/F', 'id/I','btagCSV/F', 'mass/F' , 'chHEF/F',
            ],
        'nMax': 25,
        'bas': {
            'id': ('id', operator.ge, 1),
            'pt': ('pt', operator.gt, 30),
            'eta': ('eta', operator.lt, 2.4, operator.abs),
            },
        'veto': {
            'pt': ('pt', operator.gt, 60),
            },
        'isr': {
            'pt': ('pt', operator.gt, 100),
            },
        'isrH': {
            'pt': ('pt', operator.gt, 325),
            },
        'bjet': {
            'btag': ('btagCSV', operator.gt, 0.800),
            },
        'bjetSep': {
            'ptSoftHard':  ('pt', operator.gt, 60),
            },
        }

    params['JetSel'] = JetSel


    # track selection
    # FIXME the analysis of tracks (reconstructed and generated) needs a serious clean up...
    
    if args.processTracks:
        TracksSel = {
            'branchPrefix': 'Tracks',
            'branches': [
                'pt/F', 'eta/F', 'phi/F', 'dxy/F', 'dz/F', 'pdgId/I', 'fromPV/I', 
                'matchedJetIndex/I', 'matchedJetDr/F', 'CosPhiJet1/F', 'CosPhiJet12/F', 'CosPhiJetAll/F',
                'mcMatchId/I', 'mcMatchIndex/I', 'mcMatchPtRatio/F', 'mcMatchDr/F',
                ],
            'nMax': 300,
            'bas': {
                'pt': 1.0,
                'eta': 2.5,
                'dxy': 0.1,
                'dz': 0.1,
                'pdgId': [11, 13],
                },
            'dRLepTrack': 0.1,
            'ratioPtLepTrackMin': 0.9,
            'ratioPtLepTrackMax': 1.1,
            'dRmatchJetTrack': 0.4,
            'ptMatchJet': 30,
            'trackMinPtList':  [1, 1.5, 2, 2.5, 3, 3.5],
            'hemiSectorList': [ 270, 180, 90, 60, 360],  
            'nISRsList': ['1', '12', 'All'],
            }
    else:
        TracksSel = {            
            'nMax': 300,
            'trackMinPtList': [],
            'hemiSectorList': [],
            'nISRsList': [],
            }
    
    params['TracksSel'] = TracksSel

    if args.processGenTracks:
        GenTracksSel = {
            'branchPrefix': 'GenTracks',
            'branches': [
                'pt/F', 'eta/F', 'phi/F', 'dxy/F', 'dz/F', 'pdgId/I', 'fromPV/I', 
                'matchedJetIndex/I', 'matchedJetDr/F', 'CosPhiJet1/F', 'CosPhiJet12/F', 'CosPhiJetAll/F',
                'mcMatchId/I', 'mcMatchIndex/I', 'mcMatchPtRatio/F', 'mcMatchDr/F',
                ],
            'nMax': 300,
            'bas': {
                'pt': 1.0,
                'eta': 2.5,
                },
            'genPartMinPtList': [1,1.5,2]
            }
        
        params['GenTracksSel'] = GenTracksSel

    # generated particles
        
    GenSel = {
        'branchPrefix': 'GenPart',
        'branches': [
            'pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'mass/F', 'motherId/I',
            ],
        'nMax': 100,        
        }

    params['GenSel'] = GenSel
    
    # criteria to veto events for FastSim samples, as resulted from 2016 "corridor studies
    # used to evaluate Flag_veto_event_fastSimJets
    # https://twiki.cern.ch/twiki/bin/view/CMS/SUSRecommendationsICHEP16
        
    Veto_fastSimJets_recoJet = {
        'branchPrefix': 'Jet',
        'branches': [
            'pt/F', 'eta/F', 'phi/F', 'id/I','btagCSV/F', 'mass/F', 'chHEF',
            ],
        'nMax': 25,
        'recoJet': {
            'id': ('id', operator.ge, 1),
            'pt': ('pt', operator.gt, 20),
            'eta': ('eta', operator.lt, 2.5, operator.abs),
            'chHEF': ('chHEF', operator.lt, 0.1),
            },
        }

    Veto_fastSimJets_genJet = {
        'branchPrefix': 'GenJet',
        'branches': [
            'pt/F', 'eta/F', 'phi/F', 'mass/F',
            ],
        'nMax': 25,
        'genJet': {
            },
        }
    
    Veto_fastSimJets = {
        'recoJet': Veto_fastSimJets_recoJet,
        'genJet': Veto_fastSimJets_genJet,
        'criteria': {
            'dR': ('dR', operator.lt, 0.3),
            }
        }

    params['Veto_fastSimJets'] = Veto_fastSimJets

    #
    #
    #   PU calculation:
    #   https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData#Calculating_Your_Pileup_Distribu
    #   https://hypernews.cern.ch/HyperNews/CMS/get/luminosity/611/2.html
    #

    #  FIXME could be moved to args
    pu_xsec     = 63000   # in microbarn
    pu_xsec_unc = 0.05    

    pileup_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing/pileup"
    puWeightDict = {    
                 'up'      :    {'var': 'puReweight_up'    , 'xsec': pu_xsec*(1+pu_xsec_unc)   , 'pu_root_file': pileup_dir + '/PU_ratio_%s.root'%int(pu_xsec*(1+pu_xsec_unc))   , 'pu_hist_name':'PU_ratio'},    
                 'central' :    {'var': 'puReweight'       , 'xsec': pu_xsec                   , 'pu_root_file': pileup_dir + '/PU_ratio_%s.root'%int(pu_xsec                )   , 'pu_hist_name':'PU_ratio'},
                 'down'    :    {'var': 'puReweight_down'  , 'xsec': pu_xsec*(1-pu_xsec_unc)   , 'pu_root_file': pileup_dir + '/PU_ratio_%s.root'%int(pu_xsec*(1-pu_xsec_unc))   , 'pu_hist_name':'PU_ratio'},
                }
    params['puWeightDict'] = puWeightDict

    return params
