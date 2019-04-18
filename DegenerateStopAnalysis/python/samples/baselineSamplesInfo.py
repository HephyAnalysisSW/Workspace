# baselineSamplesInfo.py
# Baseline Lumis, Triggers, Filters, Cuts and Weight Options
import os, re
import collections

### sample names ###
sample_names = {
    # data
    'data'   :{'niceName':'Data'      , 'latexName':"Data"                   },

    # background mc
    'w'      :{'niceName':'WJets'      , 'latexName':'W+Jets'                 },
    'tt'     :{'niceName':'tt+Jets'    , 'latexName':'t#bar{t}'               },
    'tt_1l'  :{'niceName':'tt (1l)'    , 'latexName':'t#bar{t}(1l)'           },
    'tt_2l'  :{'niceName':'tt (2l)'    , 'latexName':'t#bar{t}(2l)'           }, 
    'tt_pow' :{'niceName':'tt (pow)'   , 'latexName':'t#bar{t}(Powheg)'       },
    'ttx'    :{'niceName':'ttX'        , 'latexName':'t#bar{t}X'              },
    'fakes'  :{'niceName':'Fakes'      , 'latexName':"Nonprompt"              },
    'z'      :{'niceName':'Zinv'       , 'latexName':'Z#rightarrow#nu#nu+Jets'},
    'qcd'    :{'niceName':'QCD'        , 'latexName':'QCD'                    },
    'dy'     :{'niceName':'DY (M50)'   , 'latexName':'Z#gamma*+Jets (M50)'    },
    'dy5to50':{'niceName':'DY (M5to50)', 'latexName':'Z#gamma*+Jets (M5to50)' },
    'vv'     :{'niceName':'Diboson'    , 'latexName':"VV"                     },
    'st'     :{'niceName':'Single Top' , 'latexName':'Single Top'             },
    'others' :{'niceName':'Others'     , 'latexName':"Rare"                   },
    'total'  :{'niceName':'Total'      , 'latexName':"Total"                  },
    
    # signals
    't2tt'   :{'niceName':'T2tt_'      , 'latexName':'T2tt'                   },
    't2bw'   :{'niceName':'T2bW_'      , 'latexName':'T2bW'                   },
    'hino'   :{'niceName':'Hino_'      , 'latexName':'Hino'                   },
    'n2c1h'  :{'niceName':'N2C1H_'     , 'latexName':'N2C1'                   },
    'c1c1h'  :{'niceName':'C1C1H_'     , 'latexName':'C1C1'                   },
    'c1n1h'  :{'niceName':'C1N1H_'     , 'latexName':'C1N1'                   },
    'n2n1h'  :{'niceName':'N2N1H_'     , 'latexName':'N2N1'                   },
    'tchiwz' :{'niceName':'TChiWZ_'    , 'latexName':'TChiWZ'                 },
    'allSig' :{'niceName':'All Signals', 'latexName':"All Signals"            },
}


for vv in ['vvinc','vv2', 'ww','zz','wz','wwNLO','wzNLO','zzNLO']:
    sample_names[vv]= {'latexName':vv.upper(), 'niceName':vv.upper() }

for short_name, sample_name in sample_names.items():
    sample_name['shortName'] = short_name

### luminosities ###
# bril calc res : /afs/cern.ch/user/n/nrad/public/bril_res/8025_mAODv2_v7/lumis.pkl

lumis = {
    '2016': {
        'Unblind': 4303.0,
        
        # MET PD
        #'MET':       35854.9, 
        #'MET_ICHEP': 12864.4,
       
        # SingleMu PD
        'SingleMu': 35808.7,

        # SingleEl PD
        'SingleEl': 35725.2,
        
        # SingleLep
        'SingleLep': 35767.0,
        
        # JetHT PD
        'JetHT': 35865.2,
    },

    '2017': {
        'Unblind': 4303.0,
        
        # MET PD
        'MET_Run2017_14Dec2018': 41529.0, # NOTE: from Twiki 
    }    
}

def makeLumiTag(lumi, latex=False):
    """ lumi given in pb """
    if latex:
        tag = "%0.1ffb^{-1}"%(round(lumi/1000.,2))
    else:
        tag = "%0.1ffbm1"%(round(lumi/1000.,2))
    return tag

for year in lumis:
    for dataset in lumis[year]:
        sample_names.update({dataset:{'niceName':dataset, 'latexName':"Data %s"%dataset}})
        lumiTag = makeLumiTag(lumis[year][dataset],latex=True) 
                
        if not sample_names[dataset]['latexName']:
            sample_names[dataset]['latexName'] = 'Data %s'%dataset 
        if not sample_names[dataset]['niceName']:
            sample_names[dataset]['niceName'] = dataset
                
        sample_names[dataset]['latexName'] += " (%s)"%lumiTag

dataset_dict = {
    'MET' : {
        '2016': {
            '05Feb2018' : { # set same as 03Feb2017 #FIXME: recalculate
                'B':{'lumi':5787.968           , 'runs': ('272007', '275376')}, 
                'C':{'lumi':2573.399           , 'runs': ('275657', '276283')}, 
                'D':{'lumi':4248.384           , 'runs': ('276315', '276811')}, 
                'E':{'lumi':4008.663           , 'runs': ('276831', '277420')}, 
                'F':{'lumi':3101.618           , 'runs': ('277772', '278808')}, 
                'G':{'lumi':7529.196           , 'runs': ('278820', '280385')}, 
                'H':{'lumi':8390.540 + 215.149 , 'runs': ('280919', '284044')},
            },
 
            '03Feb2017' : {
                'B':{'lumi':5787.968           , 'runs': ('272007', '275376')}, 
                'C':{'lumi':2573.399           , 'runs': ('275657', '276283')}, 
                'D':{'lumi':4248.384           , 'runs': ('276315', '276811')}, 
                'E':{'lumi':4008.663           , 'runs': ('276831', '277420')}, 
                'F':{'lumi':3101.618           , 'runs': ('277772', '278808')}, 
                'G':{'lumi':7529.196           , 'runs': ('278820', '280385')}, 
                'H':{'lumi':8390.540 + 215.149 , 'runs': ('280919', '284044')}, 
            },

            '23Sep2016' : {
                'B': {'lumi': 5667.931          , 'runs': ('272007', '275376')},
                'C': {'lumi': 2638.567          , 'runs': ('275657', '276283')},
                'D': {'lumi': 4353.448          , 'runs': ('276315', '276811')},
                'E': {'lumi': 3204.684          , 'runs': ('276831', '277420')},
                'F': {'lumi': 3185.971          , 'runs': ('277772', '278808')},
                'G': {'lumi': 7721.057          , 'runs': ('278820', '280385')},
                'H': {'lumi': 8635.591 + 221.442, 'runs': ('280919', '284044')},
            },
        }
    }
}

dataset_info = {
    'MET':
        [
        ['MET',        ['B','C','D','E','F','G','H'], {'shortName':'dBlind', 'niceName':'', 'latexName':''}],
        ['MET_ICHEP',  ['B','C','D']                , {'shortName':'dICHEP', 'niceName':'', 'latexName':''}],
        ['MET_BCDE',   ['B','C','D','E']            , {'shortName':'dBCDE' , 'niceName':'', 'latexName':''}],
        ['MET_BCDEF',  ['B','C','D','E','F']        , {'shortName':'dBCDEF', 'niceName':'', 'latexName':''}],
        ['MET_GH',     ['G', 'H']                   , {'shortName':'dGH'   , 'niceName':'', 'latexName':''}],
    ]
}

make_lumi_tag = lambda l: "%0.0fpbm1"%l

def getDataLumi(lumi_dict, eras) :
    lumi = sum([lumi_dict[era]['lumi'] for era in eras])
    return round(lumi,1)

names_dict = {}
for pd in dataset_info:
    for dataset_name, eras, name_dict in dataset_info[pd]:
        for year in dataset_dict[pd]:
            for campaign in dataset_dict[pd][year]:
                dataset_name_final = '%s_Run%s_%s'%(dataset_name, year, campaign)
                names_dict[dataset_name_final] = dict(name_dict)
 
                lumi = getDataLumi(dataset_dict[pd][year][campaign], eras)
                lumis[year][dataset_name_final] = lumi
                lumiTag = makeLumiTag(lumi,latex=True) 

                if not names_dict[dataset_name_final]['latexName']:
                    names_dict[dataset_name_final]['latexName'] = 'Data %s'%dataset_name_final 
                if not names_dict[dataset_name_final]['niceName']:
                    names_dict[dataset_name_final]['niceName'] = dataset_name_final

                names_dict[dataset_name_final]['latexName'] += " (%s)"%lumiTag
                sample_names.update(names_dict)

### filters ###

filters = ["Flag_Filters"] # NOTE: combination of filters as defined in post-processing

### triggers ###
triggers = {}

triggers['MET'] = [ # MET PD
                 'HLT_PFMET100_PFMHT100_IDTight',
                 'HLT_PFMET110_PFMHT110_IDTight',
                 'HLT_PFMET120_PFMHT120_IDTight',
                 'HLT_PFMET90_PFMHT90_IDTight'
                  ]

triggers['Mu'] = "HLT_Mu50" # non-isolated trigger for SingleMu PD 
triggers['Mu2'] = "HLT_IsoMu24" # SingleMu PD

triggers['El'] = "HLT_Ele27_WPTight_Gsf" # SingleEl PD

triggers['Lep'] = [triggers['Mu2'], triggers['El']]

triggers['Jet'] = [ # JetHT PD
                      "HLT_PFHT800", 
                      "HLT_PFJet450", 
                      "HLT_AK8PFJet450"
                  ]

if type(filters) == type([]):
   filters = '(' + ' && '.join(filters) + ')' #NOTE: assuming we always want to use an 'AND' of filters

for pd in triggers:
    if type(triggers[pd]) == type([]):
        safetrigs = []
        for trig in triggers[pd]:
            safetrigs.append("Alt$(%s,0)"%trig) #NOTE: safety net if trigger is missing, setting it to zero. See https://root-forum.cern.ch/t/issue-when-adding-two-tchains-with-one-containing-a-subset-of-branches-and-using-the-draw-method/
        triggers[pd] = '(' + ' || '.join(safetrigs) + ')' #NOTE: assuming we always want to use an 'OR' of triggers
    else:
        triggers[pd] = "Alt$(%s,0)"%triggers[pd]

### cuts and weights options ###
def getCutWeightOptions(
    dataset = "MET",
    campaign = "05Feb2018",
    year = "2016",
    lepCol = "Lepton",
    lep = "lep",
    lepTag = "def",
    tightWP = "",
    jetTag = "def",
    btagSF = "SF",
    mvaId = None,
    bdtcut_sr = None,
    bdtcut_cr = None,
    options = ['isr_sig', 'sf', 'STXSECFIX', 'pu', 'isr_nIsr', 'isr_Wpt', 'trig_eff'],
    lumis = lumis,
    ):

    cutWeightOptions = {}
    cutWeightOptions['options']  = options 
    
    cutWeightOptions['settings'] = {
                'dataset':  dataset,
                'campaign': campaign,
                'year':     year,
                'lepCol':   lepCol,
                'lep':      lep,
                'lepTag':   lepTag,
                'tightWP':  tightWP,
                'jetTag':   jetTag,
                'btagSF':   btagSF,
                'mvaId':    mvaId,
                'bdtcut_sr':bdtcut_sr,
                'bdtcut_cr':bdtcut_cr,
            }
    
    # setting dataset lumi to target lumi
    dataset = '%s_Run%s_%s'%(cutWeightOptions['settings']['dataset'], cutWeightOptions['settings']['year'], cutWeightOptions['settings']['campaign'])
    lumis['target_lumi'] = lumis[cutWeightOptions['settings']['year']][dataset]
    cutWeightOptions['settings']['lumis'] = lumis
    cutWeightOptions['def_weights'] = ['weight_lumi', dataset]

    return cutWeightOptions

lhe_order = {
                'Q2central_central':'Q2central_central'   ,     ## <weight id="1001"> muR=1 muF=1 
                'Q2central_up'     :'Q2central_up'        ,     ## <weight id="1002"> muR=1 muF=2 
                'Q2central_down'   :'Q2central_down'      ,     ## <weight id="1003"> muR=1 muF=0.5 
                'Q2up_central'     :'Q2up_central'        ,     ## <weight id="1004"> muR=2 muF=1 
                #'Q2up_up'          :'Q2up_up'             ,     ## <weight id="1005"> muR=2 muF=2 
                'Q2up_down'        :'Q2up_down'           ,     ## <weight id="1006"> muR=2 muF=0.5 
                'Q2down_central'   :'Q2down_central'      ,     ## <weight id="1007"> muR=0.5 muF=1 
                'Q2down_up'        :'Q2down_up'           ,     ## <weight id="1008"> muR=0.5 muF=2 
                #'Q2down_down'      :'Q2down_down'         ,     ## <weight id="1009"> muR=0.5 muF=0.5 
              }



weight_choices = collections.OrderedDict()
weight_choices['nohiwgt']     = {'weight_name':'nohiwgt'   , 'tag': 'NoHiWgt',     'isWeightOpt' : True }
weight_choices['sf']          = {'weight_name':'sf'        , 'tag': 'SF'      ,    'isWeightOpt' : True , 'isInSettings':{'btagSF':'SF'           }}
weight_choices['sf_l_up']     = {'weight_name':'sf'        , 'tag': 'SF_L_Up' ,    'isWeightOpt' : True , 'isInSettings':{'btagSF':'SF_l_Up'      }}
weight_choices['sf_l_down']   = {'weight_name':'sf'        , 'tag': 'SF_L_Down',   'isWeightOpt' : True , 'isInSettings':{'btagSF':'SF_l_Down'    }}
weight_choices['sf_b_up']     = {'weight_name':'sf'        , 'tag': 'SF_b_Up' ,    'isWeightOpt' : True , 'isInSettings':{'btagSF':'SF_b_Up'      }}
weight_choices['sf_b_down']   = {'weight_name':'sf'        , 'tag': 'SF_b_Down',   'isWeightOpt' : True , 'isInSettings':{'btagSF':'SF_b_Down'    }}
weight_choices['sf_fs_up']    = {'weight_name':'sf'        , 'tag': 'SF_FS_Up' ,   'isWeightOpt' : True , 'isInSettings':{'btagSF':'SF_FS_Up'     }}
weight_choices['sf_fs_down']  = {'weight_name':'sf'        , 'tag': 'SF_FS_Down',  'isWeightOpt' : True , 'isInSettings':{'btagSF':'SF_FS_Down'   }}
weight_choices['noisrsig']    = {'weight_name':'isr_sig'   , 'tag': 'NoSigIsr'  ,  'isWeightOpt' : True }
weight_choices['prompt']      = {'weight_name':'prompt'    , 'tag': 'Prompt'  ,    'isWeightOpt' : True }
weight_choices['STXSECFIX']   = {'weight_name':'STXSECFIX' , 'tag': 'STXSECFIX' ,  'isWeightOpt' : True }
weight_choices['pu']          = {'weight_name':'pu'        , 'tag': 'PU'      ,    'isWeightOpt' : True }
weight_choices['pu_up']       = {'weight_name':'pu_up'     , 'tag': 'PU_Up'   ,    'isWeightOpt' : True }
weight_choices['pu_down']     = {'weight_name':'pu_down'   , 'tag': 'PU_Down' ,    'isWeightOpt' : True }
weight_choices['nvtx_gt_20']  = {'weight_name':'nvtx_gt_20', 'tag': 'NVTX_GT_20' , 'isWeightOpt' : True }
weight_choices['nvtx_lt_20']  = {'weight_name':'nvtx_lt_20', 'tag': 'NVTX_LT_20' , 'isWeightOpt' : True }
weight_choices['isr_nIsr']    = {'weight_name':'isr_nIsr'  , 'tag': 'TTIsr'   ,    'isWeightOpt' : True }
weight_choices['isr_Wpt'   ]  = {'weight_name':'isr_Wpt'   , 'tag': 'isr_Wpt' ,    'isWeightOpt' : True }
weight_choices['trig_eff']    = {'weight_name':'trig_eff'  , 'tag': 'TrigEff' ,    'isWeightOpt' : True }
weight_choices['trig_mc']     = {'weight_name':'trig_mc'   , 'tag': 'TrigMC'  ,    'isWeightOpt' : True }
weight_choices['lepSF']       = {'weight_name':'lepSF'     , 'tag': 'lepSF'   ,    'isWeightOpt' : True }
weight_choices['medmu']       = {'weight_name':'medmu'     , 'tag': 'MediumMu'   , 'isWeightOpt' : True }
weight_choices['genmet']      = {'weight_name':''          , 'tag': 'GenMet'  ,    'isWeightOpt' : False , 'isInSettings':{'corrs':'genMet'          }}
weight_choices['jec_up']      = {'weight_name':''          , 'tag': 'JEC_Up'  ,    'isWeightOpt' : False , 'isInSettings':{'corrs':'jec_up'          }}
weight_choices['jec_central'] = {'weight_name':''          , 'tag': 'JEC_Central', 'isWeightOpt' : False , 'isInSettings':{'corrs':'jec_central'     }}
weight_choices['jec_down']    = {'weight_name':''          , 'tag': 'JEC_Down',    'isWeightOpt' : False , 'isInSettings':{'corrs':'jec_down'        }}
weight_choices['jer_up']      = {'weight_name':''          , 'tag': 'JER_Up'  ,    'isWeightOpt' : False , 'isInSettings':{'corrs':'jer_up'          }}
weight_choices['jer_central'] = {'weight_name':''          , 'tag': 'JER_Central', 'isWeightOpt' : False , 'isInSettings':{'corrs':'jer_central'     }}
weight_choices['jer_down']    = {'weight_name':''          , 'tag': 'JER_Down',    'isWeightOpt' : False , 'isInSettings':{'corrs':'jer_down'        }}

for lheWeight, shortName in lhe_order.items():
    weight_choices[shortName] = { 'weight_name':lheWeight , 'tag':lheWeight, 'isWeightOpt':True}

def evalInputWeights( weights_input,  lumiWeight , weight_choices = weight_choices):
    good_weights  = [weight_choices[w] for w in weights_input ] # just to make sure no bad weights given
    weight_list   = [w for w in weight_choices if w in weights_input ]  # keeping the order of weight_choices
    
    weight_tag_list = []
    weight_opts     = []
    
    def_weights = ['weight'  , lumiWeight]
    options     = ['isr_sig']
    settings_update = {} 

    for w in weight_list:       # split into options or def_weights
        wname = weight_choices[w]['weight_name']
        if weight_choices[w].get('isInSettings'):
            new_setting = weight_choices[w]['isInSettings']
            assert len( new_setting.keys() + settings_update.keys() ) == len( set ( new_setting.keys() + settings_update.keys()  )) ## make sure no duplicate settings
            settings_update.update( new_setting ) 
        if weight_choices[w].get( 'isWeightOpt'):
            weight_opts.append( wname )
            if w=='noisrsig':
                options.remove(wname)
            elif wname not in options: 
                options.append( wname)
        else:
            if wname  not in def_weights:
                def_weights.append( wname  )
        weight_tag_list.append( weight_choices[w]['tag'] )
      
    def_weights = filter( lambda x: x , def_weights )
    weight_tag = "_".join(wgt for wgt in weight_tag_list if wgt)
    return {
            'weight_tag'      : weight_tag , 
            'weight_tag_list' : weight_tag_list, 
            'def_weights'     : def_weights, 
            'options'         : options, 
            'settings_update' : settings_update,
           }

def get_filename(f):
    return os.path.splitext(os.path.basename(f))[0]

def intOrFloat(v):
    v=float(v)
    if int(v) == float(v):
        ret =  int(v)
    else:
        ret = float(v)
    return ret

def getMasses(string, returnModel = False):
    masses = []
    string = get_filename(string)
    string = string.replace("-","_")
    #splitted = re.split("_|-", string)
    #splitted = string.rsplit("_"):
    
    #s = string[-7:]
    #masses = re.split("_", s)

    search = re.search("(\d\d\d_\d\d\dp\d\d)|(\d\d\d_\d\d\dp\d)|(\d\d\d_\d\d\d\d)|(\d\d\d_\d\d\d)|(\d\d\d_\d\d)", string)
    #search = re.search("(\d\d\d_\d\d\dp\d\d)|(\d\d\d_\d\d\dp\d)|(\d\d\d_\d\d\d\d)|(\d\d\d_\d\d\d)|(\d\d\d\d\d_\d\d\d)", string)
    if search:
        model  = string.replace(search.group(),"")
        masses = search.group().replace("p",".").rsplit("_")
    if len(masses)!=2 : #or intOrFloat(masses[0]) < intOrFloat(masses[1]):
        return False
        #raise Exception("Failed to Extract masses from string: %s , only got %s "%(string, masses))
    if returnModel:
        return [model.replace("_","") ] + [intOrFloat(m) for m in masses]
    else:
        return [intOrFloat(m) for m in masses]

def sampleName(name, sample_names = sample_names, name_opt="niceName", isSignal = False, verbose = False):
    """
    name_opt should be one of ['niceName', 'latexName', 'shortName']
    """
    
    orig_name = name[:] 
    if isSignal:
        model, m1, m2 = getMasses(name, returnModel = True)
        name = model

    possibleNames = {}
    for n, ndict in sample_names.iteritems():
        possibleNames[n] = ndict.values()
    foundIt = False 
    for n, pNames in possibleNames.iteritems():
        if name in pNames:
            if foundIt:
                raise Exception("found multiple matches to the name %s"%name)
            foundIt = n
    if not foundIt:
        raise Exception("Did not find a sample corresponding to: %s"%name)
    wantedName = sample_names[foundIt][name_opt]
    if isSignal:
        wantedName = "%s%s_%s"%( wantedName, m1, m2 )
        wantedName = wantedName.replace(".","p")
    if verbose: print "choose", wantedName, " for ", orig_name
    return wantedName
