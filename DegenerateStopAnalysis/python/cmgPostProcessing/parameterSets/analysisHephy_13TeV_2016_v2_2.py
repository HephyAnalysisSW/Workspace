''' Parameter set for HEPHY analysis at 13 TeV analysis.

'''

# imports python standard modules or functions
import collections
import operator
import copy


# imports user modules or functions
import Workspace.DegenerateStopAnalysis.tools.helpers as helpers

#


def treeVariables(args):
    '''Define variables and vectors.
    
    Most of the read and new variables are added automatically, depending on the selectors used.

    '''

    # define the branches and the variables to be kept and/or read for data
    # and MC

    # common branches for data and MC samples

    # common branches already defined in cmgTuples
    keepBranches_DATAMC = [
        'run', 'lumi', 'evt', 'isData', 'rho', 'nVert', 'rhoCN',
        'met*',
        'nJet', 'Jet_*',
        'nTauGood', 'TauGood_*',
    ]

    if (args.processLepAll and args.storeOnlyLepAll):
        keepBranches_DATAMC.extend([
            'nLepGood'#, 'nLepOther',
        ])
    else:
        keepBranches_DATAMC.extend([
            'nLepGood', 'LepGood_*',
            #'nLepOther', 'LepOther_*',
        ])

    # branches to drop:
    dropBranches_DATAMC = [
        'met_mass',
        'met_MuonEn*',
        'met_ElectronEn*',
        'met_TauEn*',
        'met_UnclusteredEn*',
        #'met_calo*',
        #"Jet_area",
        #"Jet_qgl",
        #"Jet_ptd",
        #"Jet_axis2",
        #"Jet_mult",
        #"Jet_nLeptons",
        #"Jet_puId",
        #"Jet_ctagCsvL",
        #"Jet_ctagCsvB",
    ]

    aliases_DATAMC = []
    aliases_DATAMC.extend([ 'met:met_pt', 'metPhi:met_phi'])

    # 
    readVariables_DATAMC = []
    newVariables_DATAMC = []

    readVectors_DATAMC = []
    newVectors_DATAMC = []
    
    readVariables_DATAMC.extend(['met_pt/F', 'met_phi/F'])
   
    # Flags used for vetoing events
    #  = 0: fails event
    #  = 1: pass event
    if not args.discardEvents:

        # flag from list of veto events
        if args.processEventVetoList:
            newVariables_DATAMC.extend([
                'Flag_Veto_Event_List/I/1',
            ])

        # flag for combination of event filters defined in parameterSet
        if args.processEventVetoFilters:
            newVariables_DATAMC.extend([
                'Flag_Filters/I/1',
            ])
        else:
            keepBranches_DATAMC.extend([
                'Flag_*',
            ])

        # flag for vetoing events for FastSim samples, as resulted from
        # 2016 "corridor studies" (kept in all samples for uniformity)
        if args.processEventVetoFastSimJets:
            newVariables_DATAMC.extend([
                'Flag_veto_event_fastSimJets/I/1',
            ])

    newVariables_DATAMC.extend([
        'weight/F/-999.',
        'puReweight/F/-999.',
        'puReweight_up/F/-999.',
        'puReweight_down/F/-999.',
        ])

   # MC samples only

    # common branches already defined in cmgTuples
    keepBranches_MC = [
        'nTrueInt', 'genWeight', 'xsec', #'LHEweight_original',
        'nIsr',
        'GenSusyMStop',
        'GenSusyMNeutralino',
        'LHEWeights_*',
        #'ngenLep', 'genLep_*',
        'nGenPart', 'GenPart_*',
        #'ngenPartAll', 'genPartAll_*',
        #'ngenTau', 'genTau_*',
        #'ngenLepFromTau', 'genLepFromTau_*',
        'nGenJet', 'GenJet_*',
    ]

    # branches to drop
    dropBranches_MC = []

    aliases_MC = []
    aliases_MC.extend(['genMet:met_genPt', 'genMetPhi:met_genPhi'])
    
     # 
    readVariables_MC = []
    newVariables_MC = []

    readVectors_MC = []
    newVectors_MC = []
    
    #readVariables_MC.extend(
    #    ['Jet_hadronFlavour/I', ]
    #)
   

    # data samples only

    # branches already defined in cmgTuples
    keepBranches_DATA = [
        'HLT_*',
    ]

    # branches to drop
    dropBranches_DATA = []

    aliases_DATA = []
    
     # 
    readVariables_DATA = []
    newVariables_DATA = []

    readVectors_DATA = []
    newVectors_DATA = []

    # define the named tuple to return the values
    rtuple = collections.namedtuple(
        'rtuple',
        [
            'keepBranches_DATAMC',
            'keepBranches_MC',
            'keepBranches_DATA',

            'dropBranches_DATAMC',
            'dropBranches_MC',
            'dropBranches_DATA',

            'aliases_DATAMC',
            'aliases_MC',
            'aliases_DATA',

            'readVariables_DATAMC',
            'readVariables_MC',
            'readVariables_DATA',

            'newVariables_DATAMC',
            'newVariables_MC',
            'newVariables_DATA',

            'readVectors_DATAMC',
            'readVectors_MC',
            'readVectors_DATA',

            'newVectors_DATAMC',
            'newVectors_MC',
            'newVectors_DATA',

        ]
    )

    treeVariables_rtuple = rtuple(
        keepBranches_DATAMC,
        keepBranches_MC,
        keepBranches_DATA,

        dropBranches_DATAMC,
        dropBranches_MC,
        dropBranches_DATA,

        aliases_DATAMC,
        aliases_MC,
        aliases_DATA,

        readVariables_DATAMC,
        readVariables_MC,
        readVariables_DATA,

        newVariables_DATAMC,
        newVariables_MC,
        newVariables_DATA,

        readVectors_DATAMC,
        readVectors_MC,
        readVectors_DATA,

        newVectors_DATAMC,
        newVectors_MC,
        newVectors_DATA
    )

    #
    return treeVariables_rtuple


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
        # branches for preselection (scalars or vectors) must be included in
        # readVar or readVectors
        metCut = "(met_pt>200)"
        leadingJet_pt = "((Max$(Jet_pt*(abs(Jet_eta)<2.4 && Jet_id) ) > 90 ) >=1)"
        HTCut = "(Sum$(Jet_pt*(Jet_pt>30 && abs(Jet_eta)<2.4 && (Jet_id))) >200)"

        skimPreselectCondition = "(%s)" % '&&'.join(
            [metCut, leadingJet_pt, HTCut])
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
        skimLeptonCondition = "(nLepGood >=1 || nLepOther >=1)"
    elif skimLepton == 'oneLepGood':
        skimLeptonCondition = "(nLepGood >=1)"
    elif skimLepton == 'oneLepGood20':
        skimLeptonCondition = "(( nLepGood >=1 && LepGood_pt[0] > 20 ))"
    elif skimLepton == 'oneLep20':
        skimLeptonCondition = "((nLepGood >=1 && LepGood_pt[0] > 20) || (nLepOther >=1 && LepOther_pt[0] > 20))"
    elif skimLepton == 'oneLepGood_HT800':
        skimLeptonCondition = "(nLepGood >=1 && (Sum$(Jet_pt*(Jet_pt > 30 && abs(Jet_eta) < 2.4 && (Jet_id))) > 800))"
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

    # add the variables and vectors to be kept or created, other than the one
    # defined for selectors

    treeVariables_rtuple = treeVariables(args)
    params['treeVariables'] = treeVariables_rtuple

    # Filters
    if args.processEventVetoFilters:

        filters = {
            'data': [
                'HBHENoiseFilter',
                'HBHENoiseIsoFilter',
                'EcalDeadCellTriggerPrimitiveFilter',
                'goodVertices',
                'eeBadScFilter',
                'globalTightHalo2016Filter',
                'badChargedHadronFilter',
                'badMuonFilter',
            ],

            'MC': [
                'badChargedHadronFilter',
                'badMuonFilter',
            ]
        }

        params['filters'] = filters

    # extendCollection list - add new branches to a given collection
    # 'eval_begin': 1
    #     function is evaluated at the begin of the event loop
    #     the function can use only pre-existing quantities, from the cmg tree or external quantities
    #     these quantities can be used to compute other quantities
    # 'eval_begin': 0
    #     function is evaluated at the end of the event loop
    #     the function can use quantities from cmg tree or attached to saveTree
    #     these quantities can NOT be used to compute other quantities

    extendCollectionList = []

    LepGood_extend = {
        'branchPrefix': 'LepGood',
        'sampleType': [ 'data'   , 'mc' ],
        # maximum number of objects kept
        'nMax': 16,
        # variables to add to a collection
        'extendVariables': [
            {
                'var': 'sf_mu_looseId/F/-999'  , 'function': 'extend_LepGood_func', 'args': [], 'eval_begin': 1
            },
            {
                'var': 'sf_el_vetoId/F/-999'  , 'function': 'extend_LepGood_func', 'args': [], 'eval_begin': 1
            },
            {
                'var': 'sf/F/-999'      , 'function': 'extend_LepGood_func', 'args': [], 'eval_begin': 0
            },
        ],
    }

    extendCollectionList.append(LepGood_extend)


    # selector list, to be evaluated in evaluateSelectors

    selectorList = []

    # lepton (muon and electron) selection

    # the lepton selectors required to be merged are given in mergeLeptonSelectors, a list of
    # tuples (mu selector, el selector) with the same branchPrefix and
    # selectorId

    mergeLeptonSelectors = []

    # Muons

    nMax_mu = 8
    branchesToRead_mu = [
        'pdgId/I',
        'pt/F', 'eta/F', 'phi/F',
        'relIso03/F', 'relIso04/F', 'absIso03/F', 'absIso/F', 'sip3d/F',
        'dxy/F', 'dz/F',
        'mass/F', 'Q80/F', 'mt/F', 'cosPhiLepMet/F',
        'looseMuonId/I',
    ]
    branchesToPrint_mu = helpers.getVariableNameList(branchesToRead_mu)

    LepGood_mu_def = { # Also corresponds to Tight in Fake Rate definition
        'branchPrefix': 'LepGood',
        'object': 'mu',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_mu,
        'branchesToPrint': branchesToPrint_mu,
        #
        # maximum number of objects kept
        'nMax': nMax_mu,
        #
        # object selector
        'selector': {
            'pdgId': ('pdgId', operator.eq, 13, operator.abs),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.4, operator.abs),
            'dxy': ('dxy', operator.lt, 0.02, operator.abs),
            'dz': ('dz', operator.lt, 0.1, operator.abs),
            'looseMuonId': ('looseMuonId', operator.ge, 1),
            'hybIso': {
                'ptSwitch': 25,
                'relIso': {
                    'type': 'relIso03',
                    'cut': 0.2
                },
                'absIso': 5
            },
        },
       'computeVariables': {
            'variableList': ['SF/F/1'],
            'function': 'processLeptonSF_func',
            'args': []
        },
    }

    selectorList.append(LepGood_mu_def)

    # Selector for Loose Fake Rate definition 

    LepGood_mu_loose_def = { #NOTE: should correspond exactly to CMG selection on LepGood and only split between electrons and muons
        'branchPrefix': 'LepGood',
        'object': 'mu',
        'selectorId': 'loose',
        'sampleType': ['data', 'mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_mu,
        'branchesToPrint': branchesToPrint_mu,
        #
        # maximum number of objects kept
        'nMax': nMax_mu,
        #
        # object selector
        'selector': {
            'pdgId': ('pdgId', operator.eq, 13, operator.abs),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.4, operator.abs),
            'dxy': ('dxy', operator.lt, 0.1, operator.abs), #loosened
            'dz': ('dz', operator.lt, 0.5, operator.abs), #loosened
            'looseMuonId': ('looseMuonId', operator.ge, 1),
            
            # ECAL gap masking
            'hybIso': {
                'ptSwitch': 25,
                'relIso': {
                    'type': 'relIso03',
                    'cut': 0.8 #loosened
                },
                'absIso': 20 #loosened
            },
        },
    }

    selectorList.append(LepGood_mu_loose_def)

    # Electrons

    nMax_el = 8
    branchesToRead_el = [
        'pdgId/I',
        'pt/F', 'eta/F', 'phi/F',
        'relIso03/F', 'relIso04/F' , 'absIso03/F', 'absIso/F', 'sip3d/F',
        'dxy/F', 'dz/F',
        'mass/F', 'Q80/F', 'mt/F', 'cosPhiLepMet/F',

        'SPRING15_25ns_v1/I', 'mvaIdSpring15/F',
        'hadronicOverEm/F',
        'dEtaScTrkIn/F', 'dPhiScTrkIn/F', 'eInvMinusPInv/F', 'lostHits/I',
        'convVeto/I',
        'etaSc/F',
    ]
    branchesToPrint_el = helpers.getVariableNameList(branchesToRead_el)

    LepGood_el_def = {# Also corresponds to Tight in Fake Rate definition
        'branchPrefix': 'LepGood',
        'object': 'el',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_el,
        'branchesToPrint': branchesToPrint_el,
        
        # maximum number of objects kept
        'nMax': nMax_el,
       
        # object selector
        
        # selection with Veto Electron ID
        # https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Spring15_selection_25ns
        'selector': {
            'pdgId': ('pdgId', operator.eq, 11, operator.abs),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.5, operator.abs),
            'dxy': ('dxy', operator.lt, 0.02, operator.abs), # synchronisation with muons
            'dz': ('dz', operator.lt, 0.1, operator.abs), # synchronisation with muons
            'SPRING15_25ns_v1': ('SPRING15_25ns_v1', operator.ge, 1), # EG POG Veto ID (no relIsoWithEA cut)

            # Hybrid isolation
            'hybIso': {
                'ptSwitch': 25,
                'relIso': {
                    'type': 'relIso03',
                    'cut': 0.2
                },
                'absIso': 5
            },

            # ECAL gap masking
            'evalRange_isGap': {
                'var': 'etaSc',
                'operVar': operator.abs,
                'lowRange': (operator.le, 1.4442),
                'highRange': (operator.ge, 1.566),
            },
        },
    }

    selectorList.append(LepGood_el_def)

    LepGood_el_loose_def = { #NOTE: should correspond exactly to CMG selection on LepGood and only split between electrons and muons
        'branchPrefix': 'LepGood',
        'object': 'el',
        'selectorId': 'loose',
        'sampleType': ['data', 'mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_el,
        'branchesToPrint': branchesToPrint_el,
        
        'nMax': nMax_el, # maximum number of objects kept
        
        # object selector
        
        # Selection with Veto Electron ID
        # https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Spring15_selection_25ns
        'selector': {
            'pdgId': ('pdgId', operator.eq, 11, operator.abs),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.5, operator.abs),
            'dxy': ('dxy', operator.lt, 0.1, operator.abs), # loosened 
            'dz': ('dz', operator.lt, 0.5, operator.abs), # loosened 
            'SPRING15_25ns_v1': ('SPRING15_25ns_v1', operator.ge, 1), # EG POG Veto ID (no relIsoWithEA cut)

            # Hybrid isolation
            'hybIso': {
                'ptSwitch': 25,
                'relIso': {
                    'type': 'relIso03',
                    'cut': 0.8 # loosened
                },
                'absIso': 20 # loosened
            },
            
            # ECAL gap masking
            'evalRange_isGap': {
                'var': 'etaSc',
                'operVar': operator.abs,
                'lowRange': (operator.le, 1.4442),
                'highRange': (operator.ge, 1.566),
            },
        },
    }

    selectorList.append(LepGood_el_loose_def)

    mergeLeptonSelectors.append((LepGood_mu_def, LepGood_el_def))
    mergeLeptonSelectors.append((LepGood_mu_loose_def, LepGood_el_loose_def))

    # jet selection
    #    bas: basic jets
    #    veto: jets used for QCD veto, selected from basic jets
    #    isr: ISR jets, selected from basic jets
    #    isrH: ISR jet, higher threshold for SR2, selected from basic jets
    # bjet: b jets, tagged with algorithm btag, separated in soft and hard b
    # jets

    # maximum number of objects to be kept - common quantities for all jet
    # types

    nMax_jets = 25
    branchesToRead_jets = [
        'pt/F', 'eta/F', 'phi/F', 'id/I', 'btagCSV/F', 'mass/F', 'chHEF/F', 'hadronFlavour/I' 
    ]
    branchesToPrint_jets = helpers.getVariableNameList(branchesToRead_jets)

    Jet_basJet_def = {
        'branchPrefix': 'Jet',
        'object': 'basJet',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_jets,
        'branchesToPrint': branchesToPrint_jets,
        
        'nMax': nMax_jets, # maximum number of objects kept
        #
        # object selector
        'selector': {
            'id': ('id', operator.ge, 1),
            'pt': ('pt', operator.gt, 30),
            'eta': ('eta', operator.lt, 2.4, operator.abs),
        },
        # compute variables depending on the this selector indices and on
        # quantities already existing in the tree
        'computeVariables': {
            'variableList': ['ht/F/-999.', 'dR_j1j2/F/-999.', 'dPhi_j1j2/F/-999.'],
            'function': 'processJets_func',
            'args': []
        },
    }

    selectorList.append(Jet_basJet_def)

    Jet_vetoJet_def = {
        'branchPrefix': 'Jet',
        'object': 'vetoJet',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': 'IndexJet_basJet_def',
        'branchesToRead': branchesToRead_jets,
        'branchesToPrint': branchesToPrint_jets,
        #
        # maximum number of objects kept
        'nMax': nMax_jets,
        #
        # object selector
        'selector': {
            'pt': ('pt', operator.gt, 60),
        },
        # compute variables depending on the this selector indices and on
        # quantities already existing in the tree
        'computeVariables': {
            'variableList': ['dPhi_j1j2/F/-999.'],
            'function': 'processJets_func',
            'args': []
        },
    }

    selectorList.append(Jet_vetoJet_def)

    Jet_isrJet_def = {
        'branchPrefix': 'Jet',
        'object': 'isrJet',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': 'IndexJet_basJet_def',
        'branchesToRead': branchesToRead_jets,
        'branchesToPrint': branchesToPrint_jets,
        #
        # maximum number of objects kept
        'nMax': nMax_jets,
        #
        # object selector
        'selector': {
            'pt': ('pt', operator.gt, 100),
        },
    }

    selectorList.append(Jet_isrJet_def)

    Jet_isrHJet_def = {
        'branchPrefix': 'Jet',
        'object': 'isrHJet',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': 'IndexJet_basJet_def',
        'branchesToRead': branchesToRead_jets,
        'branchesToPrint': branchesToPrint_jets,
        #
        # maximum number of objects kept
        'nMax': nMax_jets,
        #
        # object selector
        'selector': {
            'pt': ('pt', operator.gt, 325),
        },
    }

    selectorList.append(Jet_isrHJet_def)

    Jet_softJet_def = {
        'branchPrefix': 'Jet',
        'object': 'softJet',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': 'IndexJet_basJet_def',
        'branchesToRead': branchesToRead_jets,
        'branchesToPrint': branchesToPrint_jets,
        #
        # maximum number of objects kept
        'nMax': nMax_jets,
        #
        # object selector
        'selector': {
            'ptSoftHard':  ('pt', operator.le, 60),
        },
    }

    selectorList.append(Jet_softJet_def)

    Jet_hardJet_def = {
        'branchPrefix': 'Jet',
        'object': 'hardJet',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': 'IndexJet_basJet_def',
        'branchesToRead': branchesToRead_jets,
        'branchesToPrint': branchesToPrint_jets,
        #
        # maximum number of objects kept
        'nMax': nMax_jets,
        #
        # object selector
        'selector': {
            'ptSoftHard':  ('pt', operator.gt, 60),
        },
    }

    selectorList.append(Jet_hardJet_def)

    # b jets, pt sorted
    Jet_bJet_def = {
        'branchPrefix': 'Jet',
        'object': 'bJet',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': 'IndexJet_basJet_def',
        'branchesToRead': branchesToRead_jets,
        'branchesToPrint': branchesToPrint_jets,
        #
        # maximum number of objects kept
        'nMax': nMax_jets,
        #
        # object selector
        'selector': {
            'btag': ('btagCSV', operator.gt, 0.8484),
            #'btag': ('btagCSV', operator.gt, 0.800),
        },
    }

    selectorList.append(Jet_bJet_def)

    # b jets, discriminant sorted
    Jet_bJetDiscSort_def = {
        'branchPrefix': 'Jet',
        'object': 'bJetDiscSort',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': 'IndexJet_bJet_def',
        'branchesToRead': branchesToRead_jets,
        'branchesToPrint': branchesToPrint_jets,
        #
        # maximum number of objects kept
        'nMax': nMax_jets,
        #
        # object selector
        'selector': {
            'btag': ('btagCSV', operator.gt, 0.8484),
            #'btag': ('btagCSV', operator.gt, 0.800),
        },
        'sort': 'btagCSV',
    }

    selectorList.append(Jet_bJetDiscSort_def)

    # soft bjets, with separation soft - hard at ptSoftHard value
    Jet_bJetSoft_def = {
        'branchPrefix': 'Jet',
        'object': 'bJetSoft',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': 'IndexJet_bJet_def',
        'branchesToRead': branchesToRead_jets,
        'branchesToPrint': branchesToPrint_jets,
        #
        # maximum number of objects kept
        'nMax': nMax_jets,
        #
        # object selector
        'selector': {
            'ptSoftHard':  ('pt', operator.le, 60),
        },
    }

    selectorList.append(Jet_bJetSoft_def)

    # soft bjets, with separation soft - hard at ptSoftHard value
    Jet_bJetHard_def = {
        'branchPrefix': 'Jet',
        'object': 'bJetHard',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': 'IndexJet_bJet_def',
        'branchesToRead': branchesToRead_jets,
        'branchesToPrint': branchesToPrint_jets,
        #
        # maximum number of objects kept
        'nMax': nMax_jets,
        #
        # object selector
        'selector': {
            'ptSoftHard':  ('pt', operator.gt, 60),
        },
    }

    selectorList.append(Jet_bJetHard_def)

    # generated particles

    nMax_gen = 100
    branchesToRead_gen = [
        'pt/F', 'eta/F', 'phi/F', 'pdgId/I', 'mass/F', 'motherId/I',
    ]
    branchesToPrint_gen = helpers.getVariableNameList(branchesToRead_gen)

    GenPart_stop_def = {
        'branchPrefix': 'GenPart',
        'object': 'stop',
        'selectorId': 'def',
        'sampleType': ['mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_gen,
        'branchesToPrint': branchesToPrint_gen,
        #
        # maximum number of objects kept
        'nMax': nMax_gen,
        #
        # object selector
        'selector': {
            'pdgId': ('pdgId', operator.eq, 1000006, operator.abs),

        },
    }

    selectorList.append(GenPart_stop_def)

    GenPart_lsp_def = {
        'branchPrefix': 'GenPart',
        'object': 'lsp',
        'selectorId': 'def',
        'sampleType': ['mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_gen,
        'branchesToPrint': branchesToPrint_gen,
        #
        # maximum number of objects kept
        'nMax': nMax_gen,
        #
        # object selector
        'selector': {
            'pdgId': ('pdgId', operator.eq, 1000022, operator.abs),

        },
    }

    selectorList.append(GenPart_lsp_def)

    GenPart_b_def = {
        'branchPrefix': 'GenPart',
        'object': 'b',
        'selectorId': 'def',
        'sampleType': ['mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_gen,
        'branchesToPrint': branchesToPrint_gen,
        #
        # maximum number of objects kept
        'nMax': nMax_gen,
        #
        # object selector
        'selector': {
            'pdgId': ('pdgId', operator.eq, 5, operator.abs),

        },
    }

    selectorList.append(GenPart_b_def)

    GenPart_lep_def = {
        'branchPrefix': 'GenPart',
        'object': 'lep',
        'selectorId': 'def',
        'sampleType': ['mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_gen,
        'branchesToPrint': branchesToPrint_gen,
        #
        # maximum number of objects kept
        'nMax': nMax_gen,
        #
        # object selector ( len(keyValue) > 4 gives reverse evaluation, needed for contains)
        'selector': {
            'pdgId': ('pdgId', operator.contains, [11, 13], operator.abs, 1),

        },
    }
 
    selectorList.append(GenPart_lep_def)

    GenPart_tau_def = {
        'branchPrefix': 'GenPart',
        'object': 'tau',
        'selectorId': 'def',
        'sampleType': ['mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_gen,
        'branchesToPrint': branchesToPrint_gen,
        #
        # maximum number of objects kept
        'nMax': nMax_gen,
        #
        # object selector
        'selector': {
            'pdgId': ('pdgId', operator.eq, 15, operator.abs),

        },
    }

    selectorList.append(GenPart_tau_def)

    # criteria to veto events for FastSim samples, as resulted from 2016 "corridor studies
    # used to evaluate Flag_veto_event_fastSimJets
    # https://twiki.cern.ch/twiki/bin/view/CMS/SUSRecommendationsICHEP16

    nMax_fastSim_recoJet = 25
    branchesToRead_fastSim_recoJet = [
        'pt/F', 'eta/F', 'phi/F', 'id/I', 'btagCSV/F', 'mass/F', 'chHEF/F',
    ]
    branchesToPrint_fastSim_recoJet = helpers.getVariableNameList(
        branchesToRead_fastSim_recoJet)

    Jet_fastSim_recoJet = {
        'branchPrefix': 'Jet',
        'object': 'fastSim_recoJet',
        'selectorId': 'veto',
        'sampleType': ['mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_fastSim_recoJet,
        'branchesToPrint': branchesToPrint_fastSim_recoJet,
        #
        # maximum number of objects kept
        'nMax': nMax_fastSim_recoJet,
        #
        # object selector
        'selector': {
            'id': ('id', operator.ge, 1),
            'pt': ('pt', operator.gt, 20),
            'eta': ('eta', operator.lt, 2.5, operator.abs),
            'chHEF': ('chHEF', operator.lt, 0.1),
        },
    }

    selectorList.append(Jet_fastSim_recoJet)

    nMax_fastSim_genJet = nMax_fastSim_recoJet
    branchesToRead_fastSim_genJet = [
        'pt/F', 'eta/F', 'phi/F', 'mass/F',
    ]
    branchesToPrint_fastSim_genJet = helpers.getVariableNameList(
        branchesToRead_fastSim_genJet)

    Jet_fastSim_genJet = {
        'branchPrefix': 'Jet',
        'object': 'fastSim_genJet',
        'selectorId': 'veto',
        'sampleType': ['mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_fastSim_genJet,
        'branchesToPrint': branchesToPrint_fastSim_genJet,
        #
        # maximum number of objects kept
        'nMax': nMax_fastSim_genJet,
        #
        # object selector
        'selector': {
        },
    }

    selectorList.append(Jet_fastSim_genJet)

    # configuration to veto events for FastSim samples
    Veto_fastSimJets_conf = {
        'recoJet': Jet_fastSim_recoJet,
        'genJet': Jet_fastSim_genJet,
        'criteria': {
            'dR': ('dR', operator.lt, 0.3),
        }
    }

    params['Veto_fastSimJets_conf'] = Veto_fastSimJets_conf

    #
    #
    #   PU calculation:
    #   https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData#Calculating_Your_Pileup_Distribu
    #   https://hypernews.cern.ch/HyperNews/CMS/get/luminosity/611/2.html
    #
    #  FIXME could be moved to args

    pu_xsec = 63000   # in microbarn
    pu_xsec_unc = 0.05

    pileup_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing/pileup/"
    puWeightDict = {
        'up':         {'var': 'puReweight_up',   'xsec': pu_xsec * (1 + pu_xsec_unc), 'pu_root_file': pileup_dir + '/PU_ratio_23Sep2016_%s.root' % int(pu_xsec * (1 + pu_xsec_unc)), 'pu_hist_name': 'PU_ratio'},
        'central':    {'var': 'puReweight',      'xsec': pu_xsec,                     'pu_root_file': pileup_dir + '/PU_ratio_23Sep2016_%s.root' % int(pu_xsec), 'pu_hist_name': 'PU_ratio'},
        'down':       {'var': 'puReweight_down', 'xsec': pu_xsec * (1 - pu_xsec_unc), 'pu_root_file': pileup_dir + '/PU_ratio_23Sep2016_%s.root' % int(pu_xsec * (1 - pu_xsec_unc)), 'pu_hist_name': 'PU_ratio'},
    }
    params['puWeightDict'] = puWeightDict


    ##  lepton SFs

    leptonSFsDict = {
                       "sf_mu_looseId" : { "hist_file":"leptonSFs/MuonDataFulSimMCSF_12p9fbm1.root"      , "hist_name" : "histo2D"             , "maxPt" : 120 , "maxEta" : 2.4 ,  'requirement': lambda lepObj, ilep : abs( lepObj.pdgId[ilep] ) == 13  },
                       "sf_el_vetoId"  : { "hist_file":"leptonSFs/ElectronDataFullSimMCSF_12p9fbm1.root" , "hist_name" : "GsfElectronToVeto"   , "maxPt" : 200 , "maxEta" : 2.5 ,  'requirement': lambda lepObj, ilep : abs( lepObj.pdgId[ilep] ) == 11  },
                       "sf"            : { "merge_sfs": ["sf_mu_looseId", "sf_el_vetoId"]},
                     }

    params['leptonSFsDict'] = leptonSFsDict

    
    # btag weights configuration
        
    if args.processBTagWeights:
        BTagWeights_conf_def = {
            'bTagNames'         :  ['BTag', 'SBTag', 'HBTag'],
            'bTagWeightNames'   :  ['MC', 'SF', 'SF_b_Down', 'SF_b_Up', 'SF_l_Down', 'SF_l_Up', 'SF_FS_Up', 'SF_FS_Down'],
            'maxMultBTagWeight' :  2,
            'jetColl'           :  'Jet',
            'jet'               :  'IndexJet_basJet_def',
            'jetSoft'           :  'IndexJet_softJet_def',
            'jetHard'           :  'IndexJet_hardJet_def',
            'bjet'              :  'IndexJet_bJet_def', 
            'bJetSoft'          :  'IndexJet_bJetSoft_def',
            'bJetHard'          :  'IndexJet_bJetHard_def',
            'jetSelectorId'     :  'def',
        }
        params['BTagWeights_conf_def'] = BTagWeights_conf_def

        ExtraBTagSelectorIDs = ['lowpt']
        #ExtraBTagSelectorIDs = []

        for selectorId in ExtraBTagSelectorIDs:

            conf_name = 'BTagWeights_conf_%s'%selectorId
            params[conf_name]              = copy.deepcopy( BTagWeights_conf_def)
            params[conf_name]['jet'     ]  =  'IndexJet_basJet_%s'%selectorId
            params[conf_name]['bjet'    ]  =  'IndexJet_bJet_%s'%selectorId
            params[conf_name]['jetSoft' ]  =  'IndexJet_softJet_%s'%selectorId
            params[conf_name]['jetHard' ]  =  'IndexJet_hardJet_%s'%selectorId
            params[conf_name]['bJetSoft']  =  'IndexJet_bJetSoft_%s'%selectorId
            params[conf_name]['bJetHard']  =  'IndexJet_bJetHard_%s'%selectorId
            params[conf_name]['jetSelectorId'] = selectorId 
        #params.pop("BTagWeights_conf_def")
        #params['BTagWeights_conf_names'] = [ p for p in params.keys() if "BTagWeights_conf" in p ]
        params['BTagWeights_conf_names'] = ['BTagWeights_conf_def' ,'BTagWeights_conf_lowpt']
    # another set of selectors, with lower pt cuts

    #
    LepGood_mu_lowpt = copy.deepcopy(LepGood_mu_def)
    LepGood_mu_lowpt['selectorId'] = 'lowpt'
    LepGood_mu_lowpt['selector']['pt'] = ('pt', operator.gt, 3)

    selectorList.append(LepGood_mu_lowpt)

    #
    LepGood_el_lowpt = copy.deepcopy(LepGood_el_def)
    LepGood_el_lowpt['selectorId'] = 'lowpt'
    LepGood_el_lowpt['selector']['pt'] = ('pt', operator.gt, 3)

    selectorList.append(LepGood_el_lowpt)
    mergeLeptonSelectors.append((LepGood_mu_lowpt, LepGood_el_lowpt))

    #
    LepGood_mu_loose_lowpt = copy.deepcopy(LepGood_mu_loose_def)
    LepGood_mu_loose_lowpt['selectorId'] = 'loose_lowpt'
    LepGood_mu_loose_lowpt['selector']['pt'] = ('pt', operator.gt, 3)

    selectorList.append(LepGood_mu_loose_lowpt)
    #
    LepGood_el_loose_lowpt = copy.deepcopy(LepGood_el_loose_def)
    LepGood_el_loose_lowpt['selectorId'] = 'loose_lowpt'
    LepGood_el_loose_lowpt['selector']['pt'] = ('pt', operator.gt, 3)

    selectorList.append(LepGood_el_loose_lowpt)
    mergeLeptonSelectors.append((LepGood_mu_loose_lowpt, LepGood_el_loose_lowpt))

    #
    Jet_basJet_lowpt = copy.deepcopy(Jet_basJet_def)
    Jet_basJet_lowpt['selectorId'] = 'lowpt'
    Jet_basJet_lowpt['selector']['pt'] = ('pt', operator.gt, 20)

    selectorList.append(Jet_basJet_lowpt)

    #
    Jet_vetoJet_lowpt = copy.deepcopy(Jet_vetoJet_def)
    Jet_vetoJet_lowpt['selectorId'] = 'lowpt'
    Jet_vetoJet_lowpt['inputIndexList'] = 'IndexJet_basJet_lowpt'

    selectorList.append(Jet_vetoJet_lowpt)

    #
    Jet_isrJet_lowpt = copy.deepcopy(Jet_isrJet_def)
    Jet_isrJet_lowpt['selectorId'] = 'lowpt'
    Jet_isrJet_lowpt['inputIndexList'] = 'IndexJet_basJet_lowpt'

    selectorList.append(Jet_isrJet_lowpt)

    #
    Jet_isrHJet_lowpt = copy.deepcopy(Jet_isrHJet_def)
    Jet_isrHJet_lowpt['selectorId'] = 'lowpt'
    Jet_isrHJet_lowpt['inputIndexList'] = 'IndexJet_basJet_lowpt'

    selectorList.append(Jet_isrHJet_lowpt)

    #
    Jet_softJet_lowpt = copy.deepcopy(Jet_softJet_def)
    Jet_softJet_lowpt['selectorId'] = 'lowpt'
    Jet_softJet_lowpt['inputIndexList'] = 'IndexJet_basJet_lowpt'

    selectorList.append(Jet_softJet_lowpt)

    #
    Jet_hardJet_lowpt = copy.deepcopy(Jet_hardJet_def)
    Jet_hardJet_lowpt['selectorId'] = 'lowpt'
    Jet_hardJet_lowpt['inputIndexList'] = 'IndexJet_basJet_lowpt'

    selectorList.append(Jet_hardJet_lowpt)

    #
    Jet_bJet_lowpt = copy.deepcopy(Jet_bJet_def)
    Jet_bJet_lowpt['selectorId'] = 'lowpt'
    Jet_bJet_lowpt['inputIndexList'] = 'IndexJet_basJet_lowpt'

    selectorList.append(Jet_bJet_lowpt)

    #
    Jet_bJetDiscSort_lowpt = copy.deepcopy(Jet_bJetDiscSort_def)
    Jet_bJetDiscSort_lowpt['selectorId'] = 'lowpt'
    Jet_bJetDiscSort_lowpt['inputIndexList'] = 'IndexJet_bJet_lowpt'

    selectorList.append(Jet_bJetDiscSort_lowpt)

    #
    Jet_bJetSoft_lowpt = copy.deepcopy(Jet_bJetSoft_def)
    Jet_bJetSoft_lowpt['selectorId'] = 'lowpt'
    Jet_bJetSoft_lowpt['inputIndexList'] = 'IndexJet_bJet_lowpt'

    selectorList.append(Jet_bJetSoft_lowpt)

    #
    Jet_bJetHard_lowpt = copy.deepcopy(Jet_bJetHard_def)
    Jet_bJetHard_lowpt['selectorId'] = 'lowpt'
    Jet_bJetHard_lowpt['inputIndexList'] = 'IndexJet_bJet_lowpt'

    selectorList.append(Jet_bJetHard_lowpt)

    # add to params
    params['extendCollectionList'] = extendCollectionList
    params['selectorList'] = selectorList
    params['mergeLeptonSelectors'] = mergeLeptonSelectors

    return params
