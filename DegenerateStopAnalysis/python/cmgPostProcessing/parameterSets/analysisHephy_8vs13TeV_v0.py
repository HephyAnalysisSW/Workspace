''' Parameter set for HEPHY comparison of 8 TeV analysis with 13 TeV analysis.

'''
# imports python standard modules or functions
import collections
import operator


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
    parameterSet = args.parameterSet
    processTracks = args.processTracks

    # parameter set definitions
        
    params = collections.OrderedDict()
    
    
    # target luminosity (fixed value, given here)
    
    params['target_lumi'] = 10000  # pb-1

    # skimmimg parameters
    
    SkimParameters = {
        'lheHThigh': {
            'lheHTIncoming': 600
            },
        'lheHTlow': {
            'lheHTIncoming': 600
            },
        
        }
    
    params['SkimParameters'] = SkimParameters
    
    # lepton (electron and muon) selection
    
    LepSel = {
        # prefix, branches to be read and new branches to be written for leptons
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
                ],
            'common': [
                'pdgId/I',
                'pt/F', 'eta/F', 'phi/F',
                'relIso03/F', 'relIso04/F', 'miniRelIso/F', 'sip3d/F',
                'dxy/F', 'dz/F',
                'mass/F',
                ],
            },
        'newBranches': {
            'mu': [],
            'el': [],
            'common': [        
                'q80/F', 'cosdPhiLepMet/F',
                'lt/F', 'dPhiLepW/F',
                'mt/F',
                'absIso/F',
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
            'eta': ('eta', operator.lt, 2.1, operator.abs),
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
        #
        # electron selection
        'el': {
            'pdgId': ('pdgId', operator.eq, 11, operator.abs),
            'SPRING15_25ns_v1': ('SPRING15_25ns_v1', operator.ge, 2),
            },
        }
        
    params['LepSel'] = LepSel
     
        
    # jet selection
    #    bas: basic jets
    #    veto: jets used for QCD veto, selected from basic jets
    #    isr: ISR jets, selected from basic jets
    #    isrH: ISR jet, higher threshold for SR2, selected from basic jets
    #    bjet: b jets, tagged with algorithm btag, separated in soft and hard b jets 
        
    JetSel = {
        'branchPrefix': 'Jet',
        'branches': [
            'pt/F', 'eta/F', 'phi/F', 'id/I','btagCSV/F', 'mass/F'
            ],
        'nMax': 100,
        'bas': {
            'id': ('id', operator.ge, 1),
            'pt': ('pt', operator.gt, 30),
            'eta': ('eta', operator.lt, 2.4, operator.abs),
            },
        'veto': {
            'pt': ('pt', operator.gt, 60),
            },
        'isr': {
            'pt': ('pt', operator.gt, 110),
            },
        'isrH': {
            'pt': ('pt', operator.gt, 325),
            },
        'bjet': {
            'btag': ('btagCSV', operator.gt, 0.890),
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
        'nMax': 30,        
        }

    params['GenSel'] = GenSel
        
    #
    return params
