import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
import Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo as sampleInfo
import pickle
import itertools
from collections import OrderedDict
OD = OrderedDict

anyIn = degTools.anyIn
whichIn = degTools.whichIn
whichOneIn = degTools.whichOneIn


bin_FR_basic_map = {
                         'ptVL' : [ 'ptVL' , 'r1vla', 'r1vlb', 'r1vlc' , 'r2vl' ] ,
                         'ptL'  : [ 'ptL'  , 'r1la',  'r1lb' , 'r1lc'  , 'r2l'  ] ,
                         'ptM'  : [ 'ptM'  , 'r1ma',  'r1mb' , 'r1mc'  , 'r2m'  ] ,
                         'ptH'  : [ 'ptH'  , 'r1ha',  'r1hb' , 'r1hc'  , 'r2h'  ] ,
                     #'pt_gt_30' : [ 'cr1', 'cr2' , 'crtt', ] ,
                     # '30-80'  : [ '_30to80' ] ,
                     '30-50'  : [ '_30to50' ] , 
                     '50-80'  : [ '_50to80' ] , 
                     '80-200' : [ '_80to200'] , 
                     '>200'   : [ '_gt_200' ] ,
                    } 

extended_regions = {
                    'r1ela' : ['r1vla', 'r1la' ],
                    'r1elb' : ['r1vlb', 'r1lb' ],
                    'r1elc' : ['r1vlc', 'r1lc' ],
                    'r2el'  : ['r2vl', 'r2l' ],
                   }




ct_tags         = ["X","Y"] 
cr_pt_tags      = ["_30to50", "_50to80", "_80to200", "_gt_200"]
sr_pt_tags2     = ['_ptVL', '_ptL', '_ptM', '_ptH']
sr_pt_tags      = [ 'vl'  ,'l'    , 'm'   ,'h']
sr_pt_tags_all  = ['el'] + sr_pt_tags 
sr_pt_old       = ['l','m','h']
sr_pt_ext       = ['el','m','h']
sr_pt_vl        = ['vl','l','m','h']

mt_tags         = ['a','b','c']
crtt_pt_tags    = cr_pt_tags + sr_pt_tags2
eta_tags        = [ "_barrel", "_endcap" ] 

sub_region_tags = cr_pt_tags + eta_tags  
cr2_tags  = [''.join(x) for x in degTools.itertools.product( * [['cr2'], eta_tags, cr_pt_tags] ) ]
crtt_tags = [''.join(x) for x in degTools.itertools.product( * [['crtt'], eta_tags, crtt_pt_tags]) ]
LnTTag = "_LnT"




card_regions_definitions =\
                    {
               'vw' : {
                       'all': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_tags_all ],   ['mt',mt_tags]  ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_tags_all ],   ['mt',mt_tags]  ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]  ]) ],
                               ['cr2' , OD( [                             ['mt',mt_tags]  ]) ],
                              ]),
                  'MTLepPtVL': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]    ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [                             ['mt',mt_tags]    ]) ],
                              ]),
                  'MTLepPtVL2': [ 
                               ('sr1' , OD( [ ['pt' , sr_pt_old ],       ['mt',['c']]         ]) ),
                               ('sr2' , OD( [ ['pt' , sr_pt_old ],       ['mt',['c']]         ]) ),
                               ('sr1' , OD( [ ['pt' , sr_pt_vl  ],       ['mt',['a','b']]     ]) ),
                               ('sr2' , OD( [ ['pt' , sr_pt_vl  ],       ['mt',['a','b']]     ]) ),
                               ('cr1' , OD( [                            ['mt',mt_tags]       ]) ),
                               ('cr2' , OD( [                            ['mt',mt_tags]       ]) ),
                              ],
                  'MTLepPtVL3': [ 
                               ('sr1' , OD( [ ['pt' , sr_pt_ext ],       ['mt',['c']]      ]) ),
                               ('sr2' , OD( [ ['pt' , sr_pt_ext ],       ['mt',['c']]      ]) ),
                               ('sr1' , OD( [ ['pt' , sr_pt_vl  ],       ['mt',['a','b']]  ]) ),
                               ('sr2' , OD( [ ['pt' , sr_pt_vl  ],       ['mt',['a','b']]  ]) ),
                               ('cr1' , OD( [                            ['mt',mt_tags]    ]) ),
                               ('cr2' , OD( [                            ['mt',mt_tags]    ]) ),
                              ],
                  'LepPtVL': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]   ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_vl ],                          ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]   ]) ],
                               ['cr2' , OD( [                                              ]) ],
                              ]),
                  'MTLepPtVL': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]    ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [                             ['mt',mt_tags]    ]) ],
                              ]),
                  'MTLepPtL': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_old ],        ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_old ],        ['mt',mt_tags]    ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [                             ['mt',mt_tags]    ]) ],
                              ]),
                  'MTLepPtExt': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_ext ],        ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_ext ],        ['mt',mt_tags]    ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [                             ['mt',mt_tags]    ]) ],
                              ]),
                  'MTLepPtSum': OD([ 
                               ['sr1' , OD( [  ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [  ['mt',mt_tags]    ]) ],
                               ['cr1' , OD( [  ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [  ['mt',mt_tags]    ]) ],
                              ]),
                    },                      

                  #'LepPtExt': OD([
                  #             ['sr1' , OD( [ ['pt' , sr_pt_ext ],        ['mt',mt_tags]  ]) ],
                  #             ['sr2' , OD( [ ['pt' , sr_pt_ext ],        ['mt',mt_tags]  ]) ],
                  #             ['cr1' , OD( [                             ['mt',mt_tags]  ]) ],
                  #             ['cr2' , OD( [                             ['mt',mt_tags]  ]) ],
                  #            ]),
                  #'LepPtVL': OD([ 
                  #             ['sr1' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]  ]) ],
                  #             ['sr2' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]  ]) ],
                  #             ['cr1' , OD( [                             ['mt',mt_tags]  ]) ],
                  #             ['cr2' , OD( [                             ['mt',mt_tags]  ]) ],
                  #            ]),
                  #'LepPtL': OD([ 
                  #             ['sr1' , OD( [ ['pt' , sr_pt_old ],        ['mt',mt_tags]  ]) ],
                  #             ['sr2' , OD( [ ['pt' , sr_pt_old ],        ['mt',mt_tags]  ]) ],
                  #             ['cr1' , OD( [                             ['mt',mt_tags]  ]) ],
                  #             ['cr2' , OD( [                             ['mt',mt_tags]  ]) ],
                  #            ]),
                  #'LepPtSum': OD([ 
                  #             ['sr1' , OD( [  ['mt',mt_tags]  ]) ],
                  #             ['sr2' , OD( [  ['mt',mt_tags]  ]) ],
                  #             ['cr1' , OD( [  ['mt',mt_tags]  ]) ],
                  #             ['cr2' , OD( [  ['mt',mt_tags]  ]) ],
                  #            ]),
                  #'LepPtVLbeta': OD([ 
                  #             ['sr1' , OD( [ ['pt' , sr_pt_old ],        ['mt',['a','b']]  ]) ],
                  #             ['sr2' , OD( [ ['pt' , sr_pt_old ],        ['mt',['a','b']]  ]) ],
                  #             ['sr1' , OD( [ ['pt' , sr_pt_vl  ],        ['mt',['c']    ]  ]) ],
                  #             ['sr2' , OD( [ ['pt' , sr_pt_vl  ],        ['mt',['c']    ]  ]) ],
                  #             ['cr1' , OD( [                             ['mt',mt_tags]  ]) ],
                  #             ['cr2' , OD( [                             ['mt',mt_tags]  ]) ],
                  #            ]),
               '' :{ 
                       'all': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_tags_all ],    ['mt',mt_tags]  , ['ct',ct_tags] ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_tags_all ],    ['mt',mt_tags]  , ['ct',ct_tags] ]) ],
                               ['cr1' , OD( [                              ['mt',mt_tags]  , ['ct',ct_tags] ]) ],
                               ['cr2' , OD( [                              ['mt',mt_tags]  , ['ct',ct_tags] ]) ],
                            ]),
                  #'MTCTLepPtExt': OD([
                  #             ['sr1' , OD( [ ['pt' , sr_pt_ext ],        ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                  #             ['sr2' , OD( [ ['pt' , sr_pt_ext ],        ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                  #             ['cr1' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                  #             ['cr2' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                  #            ]),
                  #'MTCTLepPtL': OD([ 
                  #             ['sr1' , OD( [ ['pt' , sr_pt_old ],        ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                  #             ['sr2' , OD( [ ['pt' , sr_pt_old ],        ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                  #             ['cr1' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                  #             ['cr2' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                  #            ]),
                  #'MTCTLepPtSum': OD([ 
                  #             ['sr1' , OD( [  ['mt',mt_tags]  , ['ct',ct_tags] ]) ],
                  #             ['sr2' , OD( [  ['mt',mt_tags]  , ['ct',ct_tags] ]) ],
                  #             ['cr1' , OD( [  ['mt',mt_tags]  , ['ct',ct_tags] ]) ],
                  #             ['cr2' , OD( [  ['mt',mt_tags]  , ['ct',ct_tags] ]) ],
                  #            ]),
                  #'LepPtOLD': OD([ 
                  #             ['sr1' , OD( [ ['pt' , sr_pt_old ],         ['mt',mt_tags] ]) ],
                  #             ['sr2' , OD( [ ['pt' , sr_pt_old ],         ]) ],
                  #             ['cr1' , OD( [                              ['mt',mt_tags] ]) ],
                  #             ['cr2' , OD( [                              ]) ],
                  #            ]),
                  #VL
                  'MTCTLepPtVL': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['cr2' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                              ]),
                  'MTCTLepPtVL2': [ 
                               ('sr1' , OD( [ ['pt' , sr_pt_old ],       ['mt',['c']]         ,['ct',ct_tags] ]) ),
                               ('sr2' , OD( [ ['pt' , sr_pt_old ],       ['mt',['c']]         ,['ct',ct_tags] ]) ),
                               ('sr1' , OD( [ ['pt' , sr_pt_vl  ],       ['mt',['a','b']]     ,['ct',ct_tags] ]) ),
                               ('sr2' , OD( [ ['pt' , sr_pt_vl  ],       ['mt',['a','b']]     ,['ct',ct_tags] ]) ),
                               ('cr1' , OD( [                            ['mt',mt_tags]       ,['ct',ct_tags] ]) ),
                               ('cr2' , OD( [                            ['mt',mt_tags]       ,['ct',ct_tags] ]) ),
                              ],
                  'MTCTLepPtVL3': [ 
                               ('sr1' , OD( [ ['pt' , sr_pt_ext ],       ['mt',['c']]         ,['ct',ct_tags] ]) ),
                               ('sr2' , OD( [ ['pt' , sr_pt_ext ],       ['mt',['c']]         ,['ct',ct_tags] ]) ),
                               ('sr1' , OD( [ ['pt' , sr_pt_vl  ],       ['mt',['a','b']]     ,['ct',ct_tags] ]) ),
                               ('sr2' , OD( [ ['pt' , sr_pt_vl  ],       ['mt',['a','b']]     ,['ct',ct_tags] ]) ),
                               ('cr1' , OD( [                            ['mt',mt_tags]       ,['ct',ct_tags] ]) ),
                               ('cr2' , OD( [                            ['mt',mt_tags]       ,['ct',ct_tags] ]) ),
                              ],
                  'CTLepPtVL': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_vl ],                            ['ct',ct_tags] ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['cr2' , OD( [                                                ['ct',ct_tags] ]) ],
                              ]),
                  'MTLepPtVL': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]    ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [                             ['mt',mt_tags]    ]) ],
                              ]),
                  'MTLepPtVL2': [ 
                               ('sr1' , OD( [ ['pt' , sr_pt_old ],       ['mt',['c']]          ]) ),
                               ('sr2' , OD( [ ['pt' , sr_pt_old ],       ['mt',['c']]          ]) ),
                               ('sr1' , OD( [ ['pt' , sr_pt_vl  ],       ['mt',['a','b']]      ]) ),
                               ('sr2' , OD( [ ['pt' , sr_pt_vl  ],       ['mt',['a','b']]      ]) ),
                               ('cr1' , OD( [                            ['mt',mt_tags]        ]) ),
                               ('cr2' , OD( [                            ['mt',mt_tags]        ]) ),
                              ],
                  'LepPtVL': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_vl ],         ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_vl ],                           ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [                                               ]) ],
                              ]),

                  #Ext
                  'MTCTLepPtExt': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_ext ],        ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_ext ],        ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['cr2' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                              ]),
                  'CTLepPtExt': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_ext ],        ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_ext ],                           ['ct',ct_tags] ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['cr2' , OD( [                                                ['ct',ct_tags] ]) ],
                              ]),
                  'MTLepPtExt': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_ext ],        ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_ext ],        ['mt',mt_tags]    ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [                             ['mt',mt_tags]    ]) ],
                              ]),
                  'LepPtExt': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_ext ],        ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_ext ],                          ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [                                               ]) ],
                              ]),

                  #L
                  'MTCTLepPtL': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_old ],        ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_old ],        ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['cr2' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                              ]),
                  'CTLepPtL': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_old ],        ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_old ],                           ['ct',ct_tags] ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['cr2' , OD( [                                                ['ct',ct_tags] ]) ],
                              ]),
                  'MTLepPtL': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_old ],        ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_old ],        ['mt',mt_tags]    ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [                             ['mt',mt_tags]    ]) ],
                              ]),
                  'LepPtL': OD([ 
                               ['sr1' , OD( [ ['pt' , sr_pt_old ],        ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [ ['pt' , sr_pt_old ],                          ]) ],
                               ['cr1' , OD( [                             ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [                                               ]) ],
                              ]),

                  #L
                  'MTCTLepPtSum': OD([ 
                               ['sr1' , OD( [  ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['sr2' , OD( [  ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['cr1' , OD( [  ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['cr2' , OD( [  ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                              ]),
                  'CTLepPtSum': OD([ 
                               ['sr1' , OD( [  ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['sr2' , OD( [                     ['ct',ct_tags] ]) ],
                               ['cr1' , OD( [  ['mt',mt_tags]   , ['ct',ct_tags] ]) ],
                               ['cr2' , OD( [                     ['ct',ct_tags] ]) ],
                              ]),
                  'MTLepPtSum': OD([ 
                               ['sr1' , OD( [  ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [  ['mt',mt_tags]    ]) ],
                               ['cr1' , OD( [  ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [  ['mt',mt_tags]    ]) ],
                              ]),
                  'LepPtSum': OD([ 
                               ['sr1' , OD( [ ['mt',mt_tags]    ]) ],
                               ['sr2' , OD( [                   ]) ],
                               ['cr1' , OD( [ ['mt',mt_tags]    ]) ],
                               ['cr2' , OD( [                   ]) ],
                              ]),
                      },
                    }
yield_regions_definitions =\
                    {
                'vw' : OD([ 
                         ['sr1' , OD( [ ['pt' , sr_pt_tags ] ,  ['mt',mt_tags]                                          ])],
                         ['sr2' , OD( [ ['pt' , sr_pt_tags ] ,  ['mt',mt_tags]  ,['eta',eta_tags]                       ])],
                         ['cr1' , OD( [                         ['mt',mt_tags]                    , ['pt' , cr_pt_tags] ])],
                         ['cr2' , OD( [                         ['mt',mt_tags]  ,['eta',eta_tags] , ['pt' , cr_pt_tags] ])],
                        ]),
               '' : OD([ 
                         ['sr1' , OD( [ ['pt' , sr_pt_tags ] ,  ['mt',mt_tags]  , ['ct',ct_tags]                                         ]) ],
                         ['sr2' , OD( [ ['pt' , sr_pt_tags ] ,  ['mt',mt_tags]  , ['ct',ct_tags]  ,['eta',eta_tags]                      ]) ],
                         ['cr1' , OD( [                         ['mt',mt_tags]  , ['ct',ct_tags]                   , ['pt' , cr_pt_tags] ]) ],
                         ['cr2' , OD( [                         ['mt',mt_tags]  , ['ct',ct_tags]  ,['eta',eta_tags], ['pt' , cr_pt_tags] ]) ],
                        ]),

                    }

card_regions_definitions[ 'vtt']  = card_regions_definitions[ '']
yield_regions_definitions['vtt']  = yield_regions_definitions['']
card_regions_definitions[ 'vb' ]  = card_regions_definitions[ '']
yield_regions_definitions['vb' ]  = yield_regions_definitions['']



def getRegionsTagsDict( region_definition, default = [''] ):
    #ret = { main_region: [ [y for y in x if y ] 
    #                       for x in itertools.product(* [ default + tg for tg in region_definition[main_region].values()] ) if x] 
    #                       for main_region in region_definition.keys() }
    if not hasattr( region_definition, "has_key"):
        proxy_dict = OD( region_definition )
        items = region_definition
    else:
        proxy_dict = region_definition
        items = proxy_dict.items()
    ret = { main_region:[] for main_region in proxy_dict.keys() }
    for main_region, tags  in items:
        #print main_region, tags 
        #tags = itertools.product(* [ default + tg for tg in proxy_dict[main_region].values()] )
        tags_product = itertools.product(* [ default + tg for tg in tags.values()] )
        for x in tags_product:
            if not x:
                continue
            ret[main_region].append( [y for y in x if y ] )

    return ret

def getRegionsFromTagsDict( region_tags_dict , prefix = '') :
    ret = [''.join([prefix, main_region] + tag) for main_region, tags in region_tags_dict.items() for tag in tags]
    return ret



def findPtBinFromRegionName( region_name, ptBinRegionMap = bin_FR_basic_map ):
    foundIt = None
    for ptb, region_templates in ptBinRegionMap.items():
        if degTools.anyIn( region_templates , region_name):
            if foundIt:
                raise Exception("Had already found this (%s), but now found this one (%s) too!!"%(foundIt, ptb))
            else:
                foundIt = ptb 
    return foundIt    


def uniqueList( l ):
    """ make a unique list while keeping the order"""
    return sorted( set(l), key = l.index )


def getRegionPrefix( region ):
    srcr = degTools.whichIn( ['sr','cr'], region) 
    if not srcr:
        return ''
    prefix = region.rsplit(srcr[0])[0]
    return prefix


class RegionsInfo():
    def __init__( self, yield_regions , yield_regions_definitions = yield_regions_definitions, card_regions_definitions = card_regions_definitions) :
        self.LnTTag = "_LnT"
        self.yield_regions = yield_regions
        prefix = list(set([getRegionPrefix(r) for r in yield_regions]))
        assert len(prefix)==1, "VAGUE PREFIX! %s"%prefix
        self.prefix = prefix[0]

        self.tight_LnT_map = { r.replace(LnTTag,""):r for r in self.yield_regions if LnTTag in r }


        self.yield_region_definition = yield_regions_definitions[self.prefix]
        self.yield_region_tags_dict  = getRegionsTagsDict( self.yield_region_definition ) 

        self.card_region_definition_options  = card_regions_definitions[self.prefix]
        self.card_region_definition  = card_regions_definitions[self.prefix]['all']
        self.card_region_tags_dict   = getRegionsTagsDict( self.card_region_definition ) 
        self.final_regions           = getRegionsFromTagsDict( self.card_region_tags_dict , prefix = self.prefix) 

        self.extentions = {'pt':{'el':['vl','l']}}
        self.extended_yield_definitions = degTools.deepcopy( self.yield_region_definition )
        for main_region, main_region_tags in self.extended_yield_definitions.items():
            for tag in main_region_tags:
                if tag in self.extentions and tag in self.card_region_definition[main_region]:
                    #print main_region, tag, self.card_region_definition[main_region].keys()
                    self.extended_yield_definitions[main_region][tag] =  self.card_region_definition[main_region][tag] 
        extention_keys  = [ k for x in  self.extentions.values() for k in x.keys()  ]
        self.extended_regions = [ r for r in self.final_regions if anyIn( extention_keys ,r )]

        self.card_regions_map = { r:self.getCompRegions(r) for r in self.final_regions if r not in self.extended_regions}
        self.card_regions_map.update({ r:self.getCompRegions(r, self.extended_yield_definitions ) for r in self.extended_regions} )

        self.region_types = { r:self.getRegionType(r) for r in self.final_regions if r not in self.extended_regions }
        self.region_types.update({ r:self.getRegionType(r, self.extended_yield_definitions ) for r in self.extended_regions} )    
    

    def getAllRegionTypes( self , region_definition = None, region_tags_dict = None ):
        region_definition = region_definition if region_definition else self.yield_region_definition
        region_tags_dict  = region_tags_dict  if region_tags_dict  else self.yield_region_tags_dict
        region_types = { r:self.getRegionType(r, region_definition, region_tags_dict) for r in self.yield_regions}
        return region_types

    def getRegionType( self, region , region_definition = None, region_tags_dict = None ):
        region_orig = region[:]
        region = region[:]
        region_definition = region_definition if region_definition else self.yield_region_definition
        region_tags_dict  = region_tags_dict  if region_tags_dict  else getRegionsTagsDict( region_definition )
        region_types = OrderedDict()
        main_region = whichOneIn( region_definition , region )
        region_types['prefix']      = self.prefix
        region_types['main_region'] = main_region
        if self.LnTTag in region:
            region = region.replace(self.LnTTag, "") 
            #region_types['LnT']         = self.LnTTag
            LnTTag = self.LnTTag
        else:
            LnTTag = ""
        main_region_tags      = region_definition[main_region]
        main_region_tags_dict = region_tags_dict[main_region]
        region_postfix = region.replace(self.prefix + main_region, "")
        region_tags = [ x for x in main_region_tags_dict if ''.join(x)==region_postfix ]
        assert len(region_tags) ==1, ( region_orig, region_postfix , main_region_tags , region_tags ) 
        region_tags   = region_tags[0]
        #tag_types = [ [tag_name, (region_tag if region_tag in tag_vals else '') ] for tag_name, tag_vals in main_region_tags.items()
        #                                     for region_tag in region_tags]
        #tag_types = [ [tag_name, whichOfTheseHaveAnyOfThose( tag_vals, region_tags, default=[''])[0]  ] for tag_name, tag_vals in main_region_tags.items() ]
        tag_types = []
        for tag_name , tag_vals in main_region_tags.items():
            tag = ''
            for v in tag_vals:
                if v in region_tags:
                    assert tag =='', "Found Multiple Matches between: %s, %s"%(tag_vals, region_tags)
                    tag = v
            tag_types.append( [ tag_name, tag] )
        region_types.update( tag_types )
        region_types['LnT'] = LnTTag
        assert region_orig  == ''.join(region_types.values()), "%s doesnt equal %s"%(region_orig,''.join(region_types.values()))
        return region_types 


    def getCompRegionTags( self, region , region_definition = None):
        region_definition = region_definition if region_definition else self.yield_region_definition
        region_types = self.getRegionType( region , region_definition )
        extended_types = {}
        for rtype in [ rtype_ for rtype_ in region_types if rtype_ in self.extentions]: # Check for extentions
            if region_types[rtype] in self.extentions[rtype]:
                extended_types.update( { rtype: self.extentions[rtype][region_types[rtype]] } )
    
        main_region  = region_types['main_region']
        prefix       = region_types['prefix']
        region_complement_types = [k_ for k_, v_ in region_types.items() if not v_]
        region_complement_tags = OrderedDict([ [k,v] for k,v in self.yield_region_definition[main_region].items() if k in region_complement_types ] )
        if extended_types:
            region_complement_tags.update( extended_types ) 
        return region_complement_tags

    def getCompRegions( self, region , region_definition = None):
        region_types      = self.getRegionType(region, region_definition )
        main_region       = region_types['main_region'] #region_types.pop('main_region')
        prefix            = region_types['prefix'] #region_types.pop('main_region')
        comp_region_tags  = self.getCompRegionTags( region , region_definition = region_definition) 
        region_types.update( comp_region_tags )
        comp_regions = [''.join(x) for x in itertools.product(* [ r if type(r)==list else [r] for r in region_types.values()] )]
        #comp_regions = [ main_region + ''.join(x) for x in itertools.product( *comp_region_tags.values() ) ] 
        #comp_regions = [ prefix + main_region + ''.join(x) for x in itertools.product( *region_types.values() ) ] 
        return comp_regions

    def getCardRegionsFromOption(self, region_definition, prefix=''):
        region_tags_dict = getRegionsTagsDict( region_definition, default = [] )
        region_names = getRegionsFromTagsDict( region_tags_dict, prefix = prefix )
        return self.sort_regions( region_names ) 

    def getCardRegionsMapFromOption(self, card_regions, prefix=''):

        pass

    def getCardInfo(self, opt ):
        region_definition = self.card_region_definition_options[opt]
        card_regions = self.getCardRegionsFromOption( region_definition, self.prefix)
        card_cr_sr_map = self.getCRSRMap( card_regions, self.region_types ) 
        card_sr_cr_map = {sr:[ cr for cr,srs in card_cr_sr_map.items() if sr in srs][0] for sr in [r for r in card_regions if 'sr' in r] } #sr_regions}
        ret = { 'card_regions': card_regions, 'card_cr_sr_map': card_cr_sr_map , 'card_sr_cr_map':card_sr_cr_map }
        return ret

    def getCRSRMap( self, card_regions, region_types ):
        cr_sr_map    = {}
        cr_regions   = [ r for r in card_regions if 'cr' in r]
        sr_regions   = [ r for r in card_regions if 'sr' in r]
        for cr in cr_regions:
            cr_sr_map[cr] = []
            cr_type = region_types[cr]
            for sr in sr_regions + cr_regions: #+ cr_regions:
                sr_type = region_types[sr]
                if sr==cr:
                    continue
                if 'rtt' in cr:
                    if cr_type['mt'] == sr_type['mt'] :
                        cr_sr_map[cr].append( sr )
                if not cr_type['main_region'] == sr_type['main_region'].replace('sr','cr'):
                    continue
                if '2' in cr:
                    if cr_type.get('ct') == sr_type.get('ct') and cr_type['mt'] == sr_type['mt']:
                        cr_sr_map[cr].append( sr )
                elif '1' in cr:
                    if cr_type.get('ct') == sr_type.get('ct') and cr_type['mt'] == sr_type['mt']:
                        cr_sr_map[cr].append( sr )

        return  cr_sr_map

    def sort_regions( self, regions , keys =[] , tags_sort_dict = None, region_types = {}):
        if not region_types:
            region_types = self.region_types
        if not keys:
            keys = [ 'pt', 'ct', 'mt' , 'main_region' ] 
        if not tags_sort_dict:
            tags_sort_dict = {
                            'ct'       : ct_tags,
                            'mt'       : ['a', 'b', 'c'],
                            'pt'       : ['el', 'vl', 'l', 'm', 'h'],
                          'main_region': ['sr1', 'sr2', 'cr1', 'cr2','crtt']
                        }
        indx = {}
        for r in regions:
            indx[r] = []
            for k in keys:
                #print r, k
                idx = 900
                if k in region_types[r]:
                    v = region_types[r][k]
                    #print k, v
                    if not v:
                        pass 
                    else:
                        v = v[0] if type(v) == type([]) else v
                        if v in tags_sort_dict[k] :
                            idx = tags_sort_dict[k].index(v)
                        else:
                            #print 'lllllllllllll', v
                            raise Exception( "value not in tags_sort_dict : %s,%s,%s : %s"%(r,k,v, tags_sort_dict ))
                indx[r].append(idx)
                #print indx[r]
            #print '----', r , len(indx[r])
        sorted_regions = sorted( indx, key = lambda x: sum([ (1+j)*10**(3*i) for i,j in enumerate(indx[x]) ])  )
        #print indx
        #import pprint as pp
        #pp.pprint( [ [x , indx[x] ] for x in sorted_regions ])
        return sorted_regions 


           
tags_dict= {}
def getMySRs( final_regions , main_region = 'sr1', wanted_tags = {'sr_pt':sr_pt_tags, 'ct':ct_tags},  tags_dict  = tags_dict):
    wanted_regions = []
    regions_types = {r:getRegionType(r , tags_dict) for r in final_regions }
    for r, types in regions_types.items():
        if not main_region == types.pop("main_region"):
            continue
        avail_types = [k for k,v in types.items() if v]
        if ( sorted(wanted_tags.keys()) == sorted( avail_types ) ) :
            if all( [types[c][0] in wanted_tags[c] for c in avail_types] ):
                #print r , avail_types , wanted_tags.keys()
                wanted_regions.append( r ) 
    #
    # check no dublicate subretions
    #
    regions_compositions = { wr : getCompRegions(wr, tags_dict) for wr in wanted_regions }
    regions_used = flatten( regions_compositions.values() ) 
    assert len(set(regions_used)) == len(regions_used) ,  regions_compositions

    return wanted_regions



def sort_regions( regions , keys =[] , tags_sort_dict = None):
    if not keys:
        keys = [ 'sr_pt', 'ct', 'mt' , 'main_region'] 
    if not tags_sort_dict:
        tags_sort_dict = {
                        'ct'      : ct_tags,
                        'mt'      : ['a', 'b', 'c'],
                        'sr_pt'   : ['el', 'vl', 'l', 'm', 'h'],
                      'main_region': ['sr1', 'sr2', 'cr1', 'cr2','crtt']
                    }
    rtypes = {r:getRegionType(r) for r in regions}
    indx = {}
    for r in regions:
        indx[r] = []
        for k in keys:
            idx = 998
            if k in rtypes[r]:
                v = rtypes[r][k]
                #print k, v
                if not v:
                    continue
                v = v[0] if type(v) == type([]) else v
                if v in tags_sort_dict[k] :
                    idx = tags_sort_dict[k].index(v)
                else:
                    raise Exception( "value not in tags_sort_dict : %s,%s,%s : %s"%(r,k,v, tags_sort_dict ))
            indx[r].append(idx)

    sorted_regions = sorted( indx, key = lambda x: sum([ (1+j)*10**(3*i) for i,j in enumerate(indx[x]) ])  )

    return sorted_regions


if __name__ == '__main__':
    final_regions = ['sr1elaX', 'sr1vlaX', 'sr1laX', 'sr1maX', 'sr1haX', 'sr1aX', 'sr1elaY', 'sr1vlaY', 'sr1laY', 'sr1maY', 'sr1haY', 'sr1aY', 'sr1ela', 'sr1vla', 'sr1la', 'sr1ma', 'sr1ha', 'sr1a', 'sr1elbX', 'sr1vlbX', 'sr1lbX', 'sr1mbX', 'sr1hbX', 'sr1bX', 'sr1elbY', 'sr1vlbY', 'sr1lbY', 'sr1mbY', 'sr1hbY', 'sr1bY', 'sr1elb', 'sr1vlb', 'sr1lb', 'sr1mb', 'sr1hb', 'sr1b', 'sr1elcX', 'sr1vlcX', 'sr1lcX', 'sr1mcX', 'sr1hcX', 'sr1cX', 'sr1elcY', 'sr1vlcY', 'sr1lcY', 'sr1mcY', 'sr1hcY', 'sr1cY', 'sr1elc', 'sr1vlc', 'sr1lc', 'sr1mc', 'sr1hc', 'sr1c', 'sr1elX', 'sr1vlX', 'sr1lX', 'sr1mX', 'sr1hX', 'sr1X', 'sr1elY', 'sr1vlY', 'sr1lY', 'sr1mY', 'sr1hY', 'sr1Y', 'sr1el', 'sr1vl', 'sr1l', 'sr1m', 'sr1h', 'sr1', 'sr2elaX', 'sr2vlaX', 'sr2laX', 'sr2maX', 'sr2haX', 'sr2aX', 'sr2elaY', 'sr2vlaY', 'sr2laY', 'sr2maY', 'sr2haY', 'sr2aY', 'sr2ela', 'sr2vla', 'sr2la', 'sr2ma', 'sr2ha', 'sr2a', 'sr2elbX', 'sr2vlbX', 'sr2lbX', 'sr2mbX', 'sr2hbX', 'sr2bX', 'sr2elbY', 'sr2vlbY', 'sr2lbY', 'sr2mbY', 'sr2hbY', 'sr2bY', 'sr2elb', 'sr2vlb', 'sr2lb', 'sr2mb', 'sr2hb', 'sr2b', 'sr2elcX', 'sr2vlcX', 'sr2lcX', 'sr2mcX', 'sr2hcX', 'sr2cX', 'sr2elcY', 'sr2vlcY', 'sr2lcY', 'sr2mcY', 'sr2hcY', 'sr2cY', 'sr2elc', 'sr2vlc', 'sr2lc', 'sr2mc', 'sr2hc', 'sr2c', 'sr2elX', 'sr2vlX', 'sr2lX', 'sr2mX', 'sr2hX', 'sr2X', 'sr2elY', 'sr2vlY', 'sr2lY', 'sr2mY', 'sr2hY', 'sr2Y', 'sr2el', 'sr2vl', 'sr2l', 'sr2m', 'sr2h', 'sr2', 'cr1aX', 'cr1aY', 'cr1a', 'cr1bX', 'cr1bY', 'cr1b', 'cr1cX', 'cr1cY', 'cr1c', 'cr1X', 'cr1Y', 'cr1', 'cr2aX', 'cr2aY', 'cr2a', 'cr2bX', 'cr2bY', 'cr2b', 'cr2cX', 'cr2cY', 'cr2c', 'cr2X', 'cr2Y', 'cr2']

    regions_info = RegionsInfo( final_regions ) 
