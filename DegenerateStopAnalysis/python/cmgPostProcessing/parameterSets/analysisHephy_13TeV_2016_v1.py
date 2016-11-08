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

    '''

    # define the branches and the variables to be kept and/or read for data
    # and MC

    # common branches for data and MC samples

    # common branches already defined in cmgTuples
    keepBranches_DATAMC = [
        'run', 'lumi', 'evt', 'isData', 'rho', 'nVert', 'rhoCN',
        'met*',
        'Flag_*', 'HLT_*',
        'nJet', 'Jet_*',
        'nTauGood', 'TauGood_*',
    ]

    if (args.processLepAll and args.storeOnlyLepAll):
        keepBranches_DATAMC.extend([
            'nLepGood', 'nLepOther',
        ])
    else:
        keepBranches_DATAMC.extend([
            'nLepGood', 'LepGood_*',
            'nLepOther', 'LepOther_*',
        ])

    # branches to drop:
    dropBranches_DATAMC = [
        'met_mass',
        'met_MuonEn*',
        'met_ElectronEn*',
        'met_TauEn*',
        'met_UnclusteredEn*',
        'met_calo*',
        "Jet_area",
        "Jet_qgl",
        "Jet_ptd",
        "Jet_axis2",
        "Jet_mult",
        "Jet_nLeptons",
        "Jet_puId",
        "Jet_ctagCsvL",
        "Jet_ctagCsvB",
    ]

    # MC samples only

    # common branches already defined in cmgTuples
    keepBranches_MC = [
        'nTrueInt', 'genWeight', 'xsec', 'LHEweight_original',
        'nIsr',
        'GenSusyMStop',
        'GenSusyMNeutralino',
        'LHEWeights_*',
        'ngenLep', 'genLep_*',
        'nGenPart', 'GenPart_*',
        'ngenPartAll', 'genPartAll_*',
        'ngenTau', 'genTau_*',
        'ngenLepFromTau', 'genLepFromTau_*',
        'nGenJet', 'GenJet_*',
    ]

    # branches to drop
    dropBranches_MC = []

    # data samples only

    # branches already defined in cmgTuples
    keepBranches_DATA = []

    # branches to drop
    dropBranches_DATA = []

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
        ]
    )

    treeVariables_rtuple = rtuple(
        keepBranches_DATAMC,
        keepBranches_MC,
        keepBranches_DATA,
        dropBranches_DATAMC,
        dropBranches_MC,
        dropBranches_DATA
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
        HTCut = "(Sum$(Jet_pt*(Jet_pt>30 && abs(Jet_eta)<2.4 && (Jet_id)) ) >200)"

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

    # add the variables and vectors to be kept or created, other than the one
    # defined for selectors

    treeVariables_rtuple = treeVariables(args)
    params['treeVariables'] = treeVariables_rtuple

    # selector list, to be evaluated in evaluateSelectors

    selectorList = []

    # lepton (muon and electron) selection

    # the lepton selectors required to be merged are given in mergeLeptonSelectors, a list of
    # tuples (mu selector, el selector) with the same branchPrefix and
    # selectorId

    mergeLeptonSelectors = []

    # muons

    nMax_mu = 8
    branchesToRead_mu = [
        'pdgId/I',
        'pt/F', 'eta/F', 'phi/F',
        'relIso03/F', 'relIso04/F', 'miniRelIso/F', 'absIso03/F', 'absIso/F', 'sip3d/F',
        'dxy/F', 'dz/F',
        'mass/F', 'Q80/F', 'mt/F', 'cosPhiLepMet/F',
        'looseMuonId/I',
    ]
    branchesToPrint_mu = helpers.getVariableNameList(branchesToRead_mu)

    LepGood_mu_def = {
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
            'dz': ('dz', operator.lt, 0.5, operator.abs),
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
    }

    selectorList.append(LepGood_mu_def)

    # selector for QCD background computation

    LepGood_mu_qcd = {
        'branchPrefix': 'LepGood',
        'object': 'mu',
        'selectorId': 'qcd',
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
            #'dxy': ('dxy', operator.lt, 0.02, operator.abs),
            'dz': ('dz', operator.lt, 0.5, operator.abs),
            'looseMuonId': ('looseMuonId', operator.ge, 1),
        },
    }

    selectorList.append(LepGood_mu_qcd)

    # electrons

    nMax_el = 8
    branchesToRead_el = [
        'pdgId/I',
        'pt/F', 'eta/F', 'phi/F',
        'relIso03/F', 'relIso04/F', 'miniRelIso/F', 'absIso03/F', 'absIso/F', 'sip3d/F',
        'dxy/F', 'dz/F',
        'mass/F', 'Q80/F', 'mt/F', 'cosPhiLepMet/F',

        'SPRING15_25ns_v1/I', 'mvaIdSpring15/F',
        'hadronicOverEm/F',
        'dEtaScTrkIn/F', 'dPhiScTrkIn/F', 'eInvMinusPInv/F', 'lostHits/I',
        'convVeto/I',
        'etaSc/F',
    ]
    branchesToPrint_el = helpers.getVariableNameList(branchesToRead_el)

    LepGood_el_def = {
        'branchPrefix': 'LepGood',
        'object': 'el',
        'selectorId': 'def',
        'sampleType': ['data', 'mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_el,
        'branchesToPrint': branchesToPrint_el,
        #
        # maximum number of objects kept
        'nMax': nMax_el,
        #
        # object selector
        # https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Spring15_selection_25ns
        # selection with Veto Electron ID
        'selector': {
            'pdgId': ('pdgId', operator.eq, 11, operator.abs),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.5, operator.abs),
            # synchronisation with muons
            'dxy': ('dxy', operator.lt, 0.02, operator.abs),
            # synchronisation with muons
            'dz': ('dz', operator.lt, 0.5, operator.abs),
            # EG POG Veto ID
            'SPRING15_25ns_v1': ('SPRING15_25ns_v1', operator.ge, 1),

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
    }

    selectorList.append(LepGood_el_def)

    LepGood_el_qcd = {
        'branchPrefix': 'LepGood',
        'object': 'el',
        'selectorId': 'qcd',
        'sampleType': ['data', 'mc'],
        'inputIndexList': None,
        'branchesToRead': branchesToRead_el,
        'branchesToPrint': branchesToPrint_el,
        #
        # maximum number of objects kept
        'nMax': nMax_el,
        #
        # object selector
        # https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Spring15_selection_25ns
        # selection with Veto Electron ID (without sigmaEtaEta cut) and no
        # hybIso cut
        'selector': {
            'pdgId': ('pdgId', operator.eq, 11, operator.abs),
            'pt': ('pt', operator.gt, 5),
            'eta': ('eta', operator.lt, 2.5, operator.abs),
            # synchronisation with muons
            'dxy': ('dxy', operator.lt, 0.02, operator.abs),
            # synchronisation with muons
            'dz': ('dz', operator.lt, 0.5, operator.abs),
            # EG POG Veto ID
            'SPRING15_25ns_v1': ('SPRING15_25ns_v1', operator.ge, 1),

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
    }

    selectorList.append(LepGood_el_qcd)

    mergeLeptonSelectors.append((LepGood_mu_def, LepGood_el_def))
    mergeLeptonSelectors.append((LepGood_mu_qcd, LepGood_el_qcd))

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
        'pt/F', 'eta/F', 'phi/F', 'id/I', 'btagCSV/F', 'mass/F', 'chHEF/F', 'hadronFlavour/I',
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
        #
        # maximum number of objects kept
        'nMax': nMax_jets,
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
            'btag': ('btagCSV', operator.gt, 0.800),
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
            'btag': ('btagCSV', operator.gt, 0.800),
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

    Veto_fastSimJets_recoJet = {
        'branchPrefix': 'Jet',
        'object': 'fastSim_recoJet',
        'selectorId': 'def',
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

    selectorList.append(Veto_fastSimJets_recoJet)

    nMax_fastSim_genJet = nMax_fastSim_recoJet
    branchesToRead_fastSim_genJet = [
        'pt/F', 'eta/F', 'phi/F', 'mass/F',
    ]
    branchesToPrint_fastSim_genJet = helpers.getVariableNameList(
        branchesToRead_fastSim_genJet)

    Veto_fastSimJets_genJet = {
        'branchPrefix': 'Jet',
        'object': 'fastSim_genJet',
        'selectorId': 'def',
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

    selectorList.append(Veto_fastSimJets_genJet)

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
    pu_xsec = 63000   # in microbarn
    pu_xsec_unc = 0.05

    pileup_dir = "$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing/pileup"
    puWeightDict = {
        'up':    {'var': 'puReweight_up', 'xsec': pu_xsec * (1 + pu_xsec_unc), 'pu_root_file': pileup_dir + '/PU_ratio_%s.root' % int(pu_xsec * (1 + pu_xsec_unc)), 'pu_hist_name': 'PU_ratio'},
        'central':    {'var': 'puReweight', 'xsec': pu_xsec, 'pu_root_file': pileup_dir + '/PU_ratio_%s.root' % int(pu_xsec), 'pu_hist_name': 'PU_ratio'},
        'down':    {'var': 'puReweight_down', 'xsec': pu_xsec * (1 - pu_xsec_unc), 'pu_root_file': pileup_dir + '/PU_ratio_%s.root' % int(pu_xsec * (1 - pu_xsec_unc)), 'pu_hist_name': 'PU_ratio'},
    }
    params['puWeightDict'] = puWeightDict

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

    params['selectorList'] = selectorList
    params['mergeLeptonSelectors'] = mergeLeptonSelectors

    return params
