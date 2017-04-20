
import Workspace.DegenerateStopAnalysis.tools.degTools as degTools
import Workspace.DegenerateStopAnalysis.samples.baselineSamplesInfo as sampleInfo
import pickle
import itertools
from collections import OrderedDict
#sig2           =   'T2-4bd-300-220'
#sig1           =   'T2-4bd-300-270'

#ylds     = pickle.load( file(cfg.yieldPkls[ cfg.cutInstList[0].fullName]) )


bin_FR_basic_map = {
                         'ptVL' : [ 'ptVL' , 'r1vla', 'r1vlb', 'r1vlc' , 'r2vl' ] ,
                         'ptL'  : [ 'ptL'  , 'r1la',  'r1lb' , 'r1lc'  , 'r2l'  ] ,
                         'ptM'  : [ 'ptM'  , 'r1ma',  'r1mb' , 'r1mc'  , 'r2m'  ] ,
                         'ptH'  : [ 'ptH'  , 'r1ha',  'r1hb' , 'r1hc'  , 'r2h'  ] ,
                     #'pt_gt_30' : [ 'cr1', 'cr2' , 'crtt', ] ,
                     '30-80'  : [ '_30to80' ] ,
                     '30-80'  : [ '_30to80' ] , 
                     '80-200' : [ '_80to200'] , 
                     '>200'   : [ '_gt_200' ] , 
                     #'pt_gt_30' : [ 'cr1', 'cr2' , 'crtt', ] ,
                       }

bin_mt_map = {
                         'r1a' : [ 'r1vla', 'r1la' , 'r1ma' , 'r1ha' ] ,
                         'r1b' : [ 'r1vlb', 'r1lb' , 'r1mb' , 'r1hb' ] ,
                         'r1c' : [ 'r1vlc', 'r1lc' , 'r1mc' , 'r1hc' ] ,
                         'r2'  : [ 'r2vl' , 'r2l'  , 'r2m'  , 'r2h' ] ,
                       }

extended_regions = {
                    'r1ela' : ['r1vla', 'r1la' ],
                    'r1elb' : ['r1vlb', 'r1lb' ],
                    'r1elc' : ['r1vlc', 'r1lc' ],
                    'r2el'  : ['r2vl', 'r2l' ],
              }

def findPtBinFromRegionName( region_name, ptBinRegionMap = bin_FR_basic_map ):
    foundIt = None
    for ptb, region_templates in ptBinRegionMap.items():
        if degTools.anyIn( region_templates , region_name):
            if foundIt:
                raise Exception("Had already found this (%s), but now found this one (%s) too!!"%(foundIt, ptb))
            else:
                foundIt = ptb 
    return foundIt    


bin_FR_basic_map = {
                         'ptVL' : [ 'r1vla', 'r1vlb', 'r1vlc' , 'r2vl' ] ,
                         'ptL'  : [ 'r1la',  'r1lb' , 'r1lc'  , 'r2l'  ] ,
                         'ptM'  : [ 'r1ma',  'r1mb' , 'r1mc'  , 'r2m'  ] ,
                         'ptH'  : [ 'r1ha',  'r1hb' , 'r1hc'  , 'r2h'  ] ,
                     'pt_gt_30' : [ 'cr1', 'cr2' , 'crtt', ] ,
                       }

anyIn = degTools.anyIn
whichIn = degTools.whichIn
ct_tags         = ["X","Y" ] 
cr_pt_tags      = ["_30to80", "_80to200", "_gt_200"]
sr_pt_tags2      = ['_ptVL', '_ptL', '_ptM', '_ptH']
sr_pt_tags     = [ 'vl'  ,'l'    , 'm'   ,'h']
sr_pt_extended_tags     = ['el'] + sr_pt_tags 
mt_tags         = ['a','b','c']
crtt_pt_tags    = cr_pt_tags + sr_pt_tags2
eta_tags        = [ "_barrel", "_endcap" ] 

sub_region_tags = cr_pt_tags + eta_tags  
cr2_tags  = [''.join(x) for x in degTools.itertools.product( * [['cr2'], eta_tags, cr_pt_tags] ) ]
crtt_tags = [''.join(x) for x in degTools.itertools.product( * [['crtt'], eta_tags, crtt_pt_tags]) ]
LnTTag = "_LnT"


def getCommonRegion( region , sub_region_tags = sub_region_tags +["_LnT"]):
    region_ = region[:]
    for sub_region_tag in sub_region_tags:
        region_ = region_.replace(sub_region_tag, "")
    return region_ 

def uniqueList( l ):
    """ make a unique list """
    return sorted( set(l), key = l.index )

def getCommonRegions( regions, sub_region_tags =  sub_region_tags + [LnTTag] ):
    #return list( set([ getCommonRegion(region, sub_region_tags) for region in regions ] ))
    ret = [ getCommonRegion(region, sub_region_tags) for region in regions ]
    return uniqueList(ret)

def getCommonRegionsMap( regions, sub_region_tags =  sub_region_tags + [LnTTag] ):
    ret = {}
    for reg_ in regions:
        reg = getCommonRegion( reg_ , sub_region_tags)
        if not reg in ret:
            ret[reg]=[]
        ret[reg].append(reg_)
    return ret






#def getRegionsInfo( all_regions , LnTTag = '_LnT'):
#    ret = {}
#    LnT_regions        = [ x for x in all_regions if LnTTag in x]
#    tight_regions      = [ x for x in all_regions if LnTTag not in x] 
#    sr_pt_regions_all  = [x for x in tight_regions if 'sr' in x]
#    cr_pt_regions_all     = [x for x in tight_regions if 'cr' in x]
#    card_regions_all   = [x for x in tight_regions if 'presel' not in x and anyIn(['l', 'vl', 'm','h', 'cr'], x) ]
#    card_regions       = getCommonRegions( card_regions_all , cr_pt_tags + sr_pt_tags2 + eta_tags + [LnTTag])
#
#    ret['card_regions']     = card_regions
#    ret['card_regions_all'] = card_regions_all
#    ret['cr_pt_regions_all']   = cr_pt_regions_all
#    
#
#    sr_pt_regions = []
#    for sr_pt_region in sr_pt_regions_all:
#        r = sr_pt_region.replace("_barrel","").replace("_endcap","")
#        if r not in sr_pt_regions:
#            sr_pt_regions.append( r ) 
#    cr_regions = [] 
#    for cr_region in card_regions:#cr_pt_regions_all:
#        #r = getCommonRegion( cr_pt_region)
#        #if cr_pt_region.endswith("_barrel") or cr_pt_region.endswith("_endcap"):
#        if anyIn( eta_tags+  cr_pt_tags + sr_pt_tags2 , cr_region ):
#            assert False
#        if 'cr' in cr_region:
#            cr_regions.append(cr_region)
#
#    main_sub_sr_regions = {}
#    main_sub_sr_regions_all = {}
#    main_sub_regions = {}
#    for region in sr_pt_regions_all:
#        mtr_ = findPtBinFromRegionName(region,  ptBinRegionMap = bin_mt_map)
#        if not mtr_:
#            print 'not mt region', region
#            continue
#        prefix = region.split('r')[0]
#        mtr = prefix + mtr_
#        if not main_sub_sr_regions_all.has_key(mtr):
#            main_sub_sr_regions_all[mtr] = []
#        main_sub_sr_regions_all[mtr].append( region ) 
#    for region , sub_regions in main_sub_sr_regions_all.items():
#        main_sub_sr_regions[region] = getCommonRegions(sub_regions)
#    all_regions_map  = getCommonRegionsMap( tight_regions , eta_tags + cr_pt_tags + [LnTTag]  )    
#
#    card_regions_map = {}
#    for region in card_regions:
#        if 'cr2' in region:
#            card_regions_map[region] = degTools.whichOfTheseHaveAnyOfThose( tight_regions, cr2_tags )
#            continue
#        if 'crtt' in region:
#            card_regions_map[region] = degTools.whichOfTheseHaveAnyOfThose( tight_regions, crtt_tags )
#            continue
#        if 'sr' in region or 'cr' in region:
#            sub_regions = [ r for r in all_regions_map[region] if not r == region]
#            if not sub_regions:
#                sub_regions = [region]
#            card_regions_map[region] = sub_regions 
#    card_regions_map.update( main_sub_sr_regions )
#    for eregion , esubregionstags in extended_regions.items():
#        extended_sub_regions = degTools.whichOfTheseHaveAnyOfThose( tight_regions, esubregionstags )
#        prefix  = list(set([r.rsplit("r")[0] for r in extended_sub_regions]))
#        assert len(prefix)==1,  "Seems like multiple regions for the extended region %s, %s, %s"%(eregion, extended_sub_regions , prefix)
#        new_region_name = prefix[0] + eregion
#        if new_region_name in card_regions_map: 
#            assert False, "region already exists %s, %s"%( new_region_name, card_regions_map )
#        card_regions_map[ new_region_name ] = extended_sub_regions
#    ret['card_regions_map'] = card_regions_map
#    
#    tight_LnT_map = { lnt.replace(LnTTag,""):lnt for lnt in LnT_regions }
#     
#    cr_bkg_map = {}
#    for cr in cr_regions:
#        if 'tt' in cr.lower():
#            cr_bkg_map[cr] = "TTJets"
#        elif 'r1' in cr or 'r2' in cr:
#            cr_bkg_map[cr] = "WJets"
#    ret['cr_bkg_map'] = cr_bkg_map
#    cr_sr_map     = {}
#    print 'got files'
#    card_sr_pt_regions = [ x for x in  card_regions_map.keys() if 'sr' in x]
#    for cr in cr_regions:
#        srtemp = cr.replace("cr","sr")
#        srbase = srtemp[:-1]
#        srpt   = srtemp[-1]
#        srs    = []
#        for sr in card_sr_pt_regions:
#            #print sr 
#            if sr[-1]==srpt and srbase in sr:
#                srs.append(sr)
#            elif 'tt' in cr:
#                srs.append(sr)
#            elif '2' in cr and '2' in sr:
#                srs.append(sr)
#        print cr, srs
#        cr_sr_map[cr]=srs
#    ret['cr_sr_map'] = cr_sr_map
#     
#
#
#    ret.update( {
#            'all_regions' : all_regions, 
#            'LnT_regions' : LnT_regions,
#            'tight_regions' : tight_regions,
#            'cr_regions' : cr_regions,
#            'sr_pt_regions' : sr_pt_regions,
#            'sr_pt_regions_all' : sr_pt_regions_all,
#            'main_sub_sr_regions' : main_sub_sr_regions,
#            'main_sub_sr_regions_all' : main_sub_sr_regions_all,
#            'tight_LnT_map'    : tight_LnT_map,
#            'main_sr_regions'  : main_sub_sr_regions.keys(),
#            'main_sr_cr_regions': main_sub_sr_regions.keys() + cr_regions,
#          })
#    return ret 


tags_dict= {
        'ct' : ct_tags,
        'sr_pt' : sr_pt_tags,
        'cr_pt' : cr_pt_tags ,
        'crtt_pt' : crtt_pt_tags ,
        'mt': mt_tags,
        'eta' : eta_tags, 
    }
tags_dict_extpt = degTools.deepcopy(tags_dict)
tags_dict_extpt['sr_pt'] = ['el', 'm','h']



main_regions_tags_list = {
    'sr1' : [ 'sr_pt', 'mt', 'ct'  ] ,
    'sr2' : [ 'sr_pt', 'mt', 'ct', 'eta' ],  #SR2MT
    #'sr2' : [ 'sr_pt', 'ct', 'eta' ],
    'cr1' : [ 'mt', 'ct' , 'cr_pt' ] ,
    #'cr2' : [ 'ct',  'eta', 'cr_pt'] ,
    'cr2' : [ 'mt', 'ct',  'eta', 'cr_pt'] , #SR2MT
    'crtt': [ 'eta', 'crtt_pt'    ] ,
          } 


def getRegionsTagsOrderedDict( main_regions_tags_list, tags_dict) : 
    ret =  { main_region: 
                OrderedDict( [[t, tags_dict[t]] for t in tags] )  
                for main_region, tags in main_regions_tags_list.items()
              }
    return ret

main_regions_tags_ordered_dict = getRegionsTagsOrderedDict( main_regions_tags_list, tags_dict)




main_regions_sidetags = { main_region:
                          [''.join(x) for x in  itertools.product(  *[ [''] + tags_dict[tm] for tm in  tags])] 
                         
                         for main_region , tags in main_regions_tags_list.items()
                        }

main_regions_tags = { main_region:
                          [''.join(x) for x in  itertools.product( [main_region] , *[ [''] + tags_dict[tm] for tm in  tags])] 
                         
                         for main_region , tags in main_regions_tags_list.items()
                        }


#main_regions_tags_dict = { main_region:
#                          [ [y for y in x if y]  for x in  itertools.product( *[ [''] + tags_dict[tm] for tm in  tags]) if x]  
#                         for main_region , tags in main_regions_tags_list.items()
#                        }

def getRegionsTagsDict( main_regions_tags_list, tags_dict = tags_dict):
    ret = { main_region:
                          [ [y for y in x if y]  for x in  itertools.product( *[ [''] + tags_dict[tm] for tm in  tags]) if x]
                         for main_region , tags in main_regions_tags_list.items()
                        }
    return ret

main_regions_tags_dict = getRegionsTagsDict( main_regions_tags_list )  

#main_regions_tags_dict = { main_region:
#                          [ [x,  [y for y in x if y]]  for x in  itertools.product( *[ [''] + tags_dict[tm] for tm in  tags]) if x]
#                         for main_region , tags in main_regions_tags_list.items()
#                        }




final_regions_tags_list = {
    'sr1' : [ 'sr_pt', 'mt', 'ct'  ] ,
    #'sr2' : [ 'sr_pt', 'ct', ],
    'sr2' : [ 'sr_pt', 'mt', 'ct', ], #SR2MT
    'cr1' : [ 'mt', 'ct'  ] ,
    #'cr2' : [ 'ct'] ,
    'cr2' : [ 'mt', 'ct'] , #SR2MT
    'crtt': [   ] ,
          } 

final_region_complement = { main_region: [t for t in main_regions_tags_list[main_region] if t not in tags] for main_region , tags in final_regions_tags_list.items() }


flatten = lambda l: [item for sublist in l for item in sublist]



card_regions_defs ={
                    'old' :   {'def':     [ 
                                      ['sr1' , {'sr_pt' : ['l','m','h']  ,'mt':mt_tags} ],
                                      ['sr2' , {'sr_pt' : ['l','m','h']  } ],
                                      ['cr1' , {'mt'    : mt_tags   } ],
                                      ['cr2' , {} ],
                                      ['crtt', {} ],
                                    ]},
                                    
                    'LepPtVL' : {'def': [   
                                      ['sr1' , {'sr_pt' : sr_pt_tags  ,'mt':mt_tags} ],
                                      ['sr2' , {'sr_pt' : sr_pt_tags               } ],
                                      ['cr1' , {'mt'    : mt_tags                  } ],
                                      ['cr2' , { } ],
                                      ['crtt', { } ],
                                    ] }, 
                                    
                    'CTLepPtVL' : {'def': [ 
                                      ['sr1' , {'sr_pt' : sr_pt_tags , 'ct':ct_tags ,'mt':mt_tags} ],
                                      ['sr2' , {'sr_pt' : sr_pt_tags , 'ct':ct_tags              } ],
                                      ['cr1' , {                       'ct':ct_tags ,'mt':mt_tags} ],
                                      ['cr2' , {                       'ct':ct_tags ,            } ],
                                      ['crtt', {} ],
                                    ] }, 
                    'MTCTLepPtVL' : {'def': [ 
                                      ['sr1' , {'sr_pt' : sr_pt_tags , 'ct':ct_tags ,'mt':mt_tags  } ],
                                      ['sr2' , {'sr_pt' : sr_pt_tags , 'ct':ct_tags , 'mt':mt_tags } ],
                                      ['cr1' , {                       'ct':ct_tags ,'mt':mt_tags  } ],
                                      ['cr2' , {                       'ct':ct_tags ,'mt':mt_tags  } ],
                                      ['crtt', {} ],
                                    ] }, 

                    #'LepPtExt' : {'def': [ 
                    #                  ['sr1' , {'sr_pt' : ['el','m','h']  ,'mt':mt_tags} ],
                    #                  ['sr2' , {'sr_pt' : ['el','m','h']               } ],
                    #                  ['cr1' , {'mt'    : mt_tags                  } ],
                    #                  ['cr2' , { } ],
                    #                  ['crtt', { } ],
                    #              ] ,
                    #               #'tags_dict': tags_dict_extpt,
                    #                } , 
                    #                
                   }


def getCRSRMap( card_regions ):
    cr_sr_map     = {}
    cr_regions = [ r for r in card_regions if 'cr' in r]
    sr_regions = [ r for r in card_regions if 'sr' in r]

    regions_types = {r:getRegionType(r , tags_dict) for r in card_regions }

    for cr in cr_regions:
        cr_sr_map[cr] = []
        cr_type = regions_types[cr]
        if 'tt' in cr:
            cr_sr_map[cr] = sr_regions + cr_regions
            continue
        for sr in sr_regions:
            sr_type = regions_types[sr]
            if not cr_type['main_region'] == sr_type['main_region'].replace('sr','cr'):
                continue
            if '2' in cr:
                if cr_type['ct'] == sr_type['ct'] and cr_type['mt'] == sr_type['mt']:
                    cr_sr_map[cr].append( sr )
            elif '1' in cr:
                if cr_type['ct'] == sr_type['ct'] and cr_type['mt'] == sr_type['mt']:
                    cr_sr_map[cr].append( sr )
    return  cr_sr_map
           

def getMySRs( final_regions , main_region = 'sr1', wanted_tags = {'sr_pt':sr_pt_tags, 'ct':ct_tags},  tags_dict  = tags_dict):
    wanted_regions = []
    regions_types = {r:getRegionType(r , tags_dict) for r in final_regions }
    for r, types in regions_types.items():
        if not main_region == types.pop("main_region"):
            continue
        avail_types = [k for k,v in types.items() if v]
        if ( sorted(wanted_tags.keys()) == sorted( avail_types ) ) :
            if all( [types[c][0] in wanted_tags[c] for c in avail_types] ):
                print r , avail_types , wanted_tags.keys()
                wanted_regions.append( r ) 
    #
    # check no dublicate subretions
    #
    regions_compositions = { wr : getCompRegions(wr, tags_dict) for wr in wanted_regions }
    regions_used = flatten( regions_compositions.values() ) 
    assert len(set(regions_used)) == len(regions_used) ,  regions_compositions

    return wanted_regions




def getRegionsInfo2( all_regions , LnTTag):
    main_regions = uniqueList( [x.rsplit("_")[0] for x in all_regions if 'presel' not in x ]) 

    LnT_regions        = [ x for x in all_regions if LnTTag in x]
    tight_regions      = [ x for x in all_regions if LnTTag not in x]
    sr_pt_regions_all  = [x for x in tight_regions if 'sr' in x]
    cr_pt_regions_all  = [x for x in tight_regions if 'cr' in x]
    card_regions_all   = [x for x in tight_regions if 'presel' not in x and anyIn(['l', 'vl', 'm','h', 'cr'], x) ]
    card_regions       = getCommonRegions( card_regions_all , cr_pt_tags + sr_pt_tags2 + eta_tags + [LnTTag])

    #all_region_types_map = { region: getRegionType(region) for region in all_regions if 'presel' not in region and 'LnT' not in region }            

    final_regions = [  ''.join(x)   for main_region , tags in final_regions_tags_list.items()  
                                    for x in itertools.product( [main_region] , *[ [''] + tags_dict[tm] for tm in  tags])]
    
    #final_regions_compositions = { f:{  k:v.values() for k,v in all_region_types_map.items() if f in k} for f in final_regions}

    card_regions_map = { r:getCompRegions(r) for r in final_regions}           


    for eregion , esubregionstags in extended_regions.items():
        extended_sub_regions = degTools.whichOfTheseHaveAnyOfThose( tight_regions, esubregionstags )
        prefix  = list(set([r.rsplit("r")[0] for r in extended_sub_regions]))
        assert len(prefix)==1,  "Seems like multiple regions for the extended region %s, %s, %s"%(eregion, extended_sub_regions , prefix)
        new_region_name = prefix[0] + eregion
        if new_region_name in card_regions_map: 
            assert False, "region already exists %s, %s"%( new_region_name, card_regions_map )
        card_regions_map[ new_region_name ] = extended_sub_regions


    tight_LnT_map = { lnt.replace(LnTTag,""):lnt for lnt in LnT_regions }

    final_sr_regions = sorted( [r for r in final_regions if 'sr' in r] )
    final_cr_regions = sorted( [r for r in final_regions if 'cr' in r] )
    final_regions    = final_sr_regions + final_cr_regions 


    card_regions_options = {}
    card_regions_cr_sr_maps = {}
    for option , opt_info in card_regions_defs.items():
        definition = opt_info['def']
        tags_dict_to_use = opt_info.get('tags_dict', tags_dict ) 
        card_regions_options[option] = []
        for main_region , region_tags in definition:
            #print option 
            #print main_region, region_tags
            #print tags_dict_to_use
            #print final_regions
            regions = getMySRs( final_regions, main_region = main_region, wanted_tags = region_tags, tags_dict = tags_dict_to_use )
            card_regions_options[option].extend( sort_regions(regions) )
        card_regions_cr_sr_maps[option] = getCRSRMap( card_regions_options[option] )

    ret ={
            'card_regions_options' : card_regions_options , 
            #'getMySRs'    : getMySRs ,
            'card_regions_defs': card_regions_defs,
            'card_regions_cr_sr_maps' : card_regions_cr_sr_maps,
            'tags_dict'   : tags_dict , 
            'all_regions' : all_regions,
            'LnT_regions' : LnT_regions,
            'tight_LnT_map':tight_LnT_map,
            'tight_regions' : tight_regions,
            #'cr_regions' : cr_regions,
            #'sr_pt_regions' : sr_pt_regions,
            'sr_pt_regions_all' : sr_pt_regions_all,
            #'main_sub_sr_regions' : main_sub_sr_regions,
            #'main_sub_sr_regions_all' : main_sub_sr_regions_all,
            #'tight_LnT_map'    : tight_LnT_map,
            #'main_sr_regions'  : main_sub_sr_regions.keys(),
            #'main_sr_cr_regions': main_sub_sr_regions.keys() + cr_regions,
            'card_regions_map' : card_regions_map , 
            'final_regions'    : final_regions ,  
           'final_sr_regions'  : final_sr_regions ,
           'final_cr_regions'  : final_cr_regions ,
         }
    return ret




def getRegionType(region , tags_dict = tags_dict):
    region_types = OrderedDict()
    #main_region  = region.rsplit("_")[0]
    main_region = whichIn( main_regions_tags_list , region )
    assert len( main_region ) == 1, (region, main_region)
    main_region = main_region[0]
    region_types['main_region'] = main_region
    main_region_tags = main_regions_tags_list[main_region]
    region_postfix = region.replace(main_region, "")
    main_regions_tags_dict = getRegionsTagsDict( main_regions_tags_list , tags_dict = tags_dict)  
    main_region_tag_labels = main_regions_tags_dict[main_region]
    region_tags = [ x for x in main_region_tag_labels if ''.join(x)==region_postfix ]
    assert len(region_tags) ==1, (region_postfix , main_region_tag_labels , region_tags ) 
    region_tags = region_tags[0]
    #region_types = {k:whichIn(region_tags,v)[0] for k, v in tags_dict.items()  if anyIn(region_tags, v) if k in main_region_tags}
    #region_types.update( OrderedDict( [ [k,whichIn(region_tags,v)[0]] for k, v in tags_dict.items()  if anyIn(region_tags, v) if k in main_region_tags] ) )
    #region_types.update( OrderedDict( 
    #                    [ [k,[whichIn(region_tags,v)[0]]] for k, v in main_regions_tags_ordered_dict[main_region].items()  
    #                    if anyIn(region_tags, v) ] ) )
    main_regions_tags_ordered_dict = getRegionsTagsOrderedDict( main_regions_tags_list, tags_dict)
    region_types.update( OrderedDict( 
                         [ [k,whichIn(region_tags,v)] for k, v in main_regions_tags_ordered_dict[main_region].items() ] 
                        ) )
    return region_types

def getCompRegionTags(region, tags_dict = tags_dict ): 
    region_types = getRegionType(region, tags_dict = tags_dict )
    main_region  = region_types["main_region"]
    #region_complement_types = [ k for k in main_regions_tags_list[main_region] if k not in [k_ for k_,v_ in region_types.items() if v_] ]
    region_complement_types = [k_ for k_,v_ in region_types.items() if not v_]
    #region_complement_types = [ k for k in region_types.keys() if k not in final_regions_tags_list[main_region] ]
    region_complement_tags = OrderedDict([ [k,v] for k,v in main_regions_tags_ordered_dict[main_region].items() if k in region_complement_types ] )
    return region_complement_tags

def getCompRegions( region, tags_dict  = tags_dict):
    region_types      = getRegionType(region , tags_dict = tags_dict)
    main_region       = region_types.pop('main_region')
    comp_region_tags  = getCompRegionTags( region, tags_dict = tags_dict ) 
    region_types.update( comp_region_tags )
    #comp_regions = [ main_region + ''.join(x) for x in itertools.product( *comp_region_tags.values() ) ] 
    comp_regions = [ main_region + ''.join(x) for x in itertools.product( *region_types.values() ) ] 
    return comp_regions






def sort_regions( regions , keys =[] , tags_sort_dict = None):
    if not keys:
        keys = [ 'sr_pt', 'ct', 'mt' , 'main_region'] 
    if not tags_sort_dict:
        tags_sort_dict = {
                        'ct'      : ['X', 'Y'],
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




if False:
    for tag_type, tags_list in tags_dict.items():
        relevant_tag = whichIn(tags_list, region)
        assert len(relevant_tag)<=1 , relevant_tag
        if relevant_tag:
            region_types[tag_type] = relevant_tag
    #return region_types 
    
    #for main_bin, tm in tag_map.items():
    #    bins = [''.join(x) for x in  itertools.product( [main_bin] , *[ [''] + tm for tm in  tag_map[main_bin]]  ) ] 
    #    for b in bins:
    #        tags_info[b] = {} 
    #        for tag in tags:
    #            relevant_bins = filter( lambda x: b in x , [ x.replace(b,'') for x in tight_regions if 'x' in ] )     


def fakeEstimate( cfg, args ):
#if True:
    """
        Calculate contribution due to fake backgrounds
        Need to have el, mu yields, and the FRs
    """

    yld_pkl_file_lep   = cfg.yieldPkls[ cfg.cutInstList[0].fullName]
    cutName            = cfg.cutInstList[0].name 
    saveDir            = cfg.saveDirs[cfg.cutInstList[0].fullName ] 
    if not "lep" in yld_pkl_file_lep or 'loose' in yld_pkl_file_lep:
        raise Exception("Run with the lep=lep option")
    #
    # getting Yield Instance pickles for lep, mu, el (lep will not be used for the final results) 
    #
    yld_pkls_files = {
                       'lep': yld_pkl_file_lep , 
                        'mu': yld_pkl_file_lep.replace("lep", "mu") ,
                        'el': yld_pkl_file_lep.replace("lep", "el") ,
                     }
    yld_pkls    = degTools.dict_function( yld_pkls_files , lambda f: pickle.load(file(f)) ) 
    yld_dicts   = degTools.dict_function( yld_pkls       , lambda yld: yld.getNiceYieldDict() ) 
    yldsByBin   = degTools.dict_function( yld_pkls       , lambda yld: yld.getByBins( yld.getNiceYieldDict()) ) 
    ylds_lep = yld_pkls['lep']
    
    
    
    LnTTag = "_LnT"
    all_regions = ylds_lep.cutNames
    regions = getRegionsInfo2(all_regions, LnTTag) 
 
    LnT_regions      =  regions['LnT_regions'     ] 
    tight_regions    =  regions['tight_regions'   ] 
    card_regions_map =  regions['card_regions_map'   ] 
    #sr_pt_regions    =  regions['sr_pt_regions'   ]  
    #main_sub_sr_regions =  regions['main_sub_sr_regions']    
    #main_sub_sr_regions_all =  regions['main_sub_sr_regions_all']    
    tight_LnT_map    =  regions['tight_LnT_map'   ]  

    sampleNames = ylds_lep.sampleNames
    bkgList  = ylds_lep.bkgList
    w        = [bkg for bkg in bkgList if 'w' in bkg]
    tt       = [bkg for bkg in bkgList if 'tt' in bkg]
    others   = [bkg for bkg in bkgList if bkg not in w+tt]
    sigs     = ylds_lep.sigList
    data     = ylds_lep.dataList
    
    samps = {
             'w'     : w        ,
             'tt'    : tt       ,
             'others': others   ,
             'sigs'  : sigs     ,
             'data'  : data     ,
            data[0]  : data     ,
          #'t2tt300_270' : ['t2tt300_270'], 
            }
    for sig in sigs:
        samps[sig] = [sig]
    
    #
    # Getting the FakeRate pickles
    #

    #FR_file_template = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final/{cmgTag}/{ppTag}/measurement1/tightToLooseRatio_measurement1_data-EWK_%s.pkl".format(cmgTag = cfg.cmgTag, ppTag = cfg.ppTag)
    FR_file_template = "/afs/hephy.at/user/m/mzarucki/public/results2017/fakeRate/final/{cmgTag}/{ppTag}/measurement1/tightToLooseRatio_measurement1_MC_%s.pkl".format(cmgTag = cfg.cmgTag, ppTag = cfg.ppTag)
    
    flavors = ['mu', 'el']
    FR_pkls_files = { flav: FR_file_template%flav for flav in flavors }
    FR_pkls     = degTools.dict_function( FR_pkls_files  , lambda f: pickle.load(file(f)) )

    def getRegionFakeEstimate( binYlds ,  FR ):
        return degTools.dict_operator( binYlds, sampleNiceNames['data'] + ['Total'] , lambda data, prompts  : (data-prompts) * FR/(degTools.u_float(1)-FR) )
    sampleNiceNames = { s: [ sampleNames[s_] for s_ in samps[s] ]  for s in samps}
    
    flav = 'lep'
    
    #sig = [ "t2tt300_270" ]
    
    prompt_fake_yields = {'mu':{},'lep':{}, 'el':{}}
    prompt_fake_yields_all = {'mu':{},'lep':{}, 'el':{}}
    FR_dicts = {'mu':{}, 'el':{} } 
    for tight_region , LnT_region in tight_LnT_map.iteritems():
        for flav in ['mu', 'el']:
            yields_LnT      = yldsByBin[flav][LnT_region] 
            yields_prompt   = yldsByBin[flav][tight_region] 
            ptBin        = findPtBinFromRegionName( LnT_region)
            if ptBin: 
                FR           = FR_pkls[flav].get(ptBin)
            #assert FR.val > 0 , "Negative FakeRate %s"%FR
            if not ptBin:
                print "didn't find a pt bin for: " , flav, LnT_region
            if not FR or not ptBin:
                print "no FR found", flav, LnT_region, ptBin
                FR = degTools.u_float(-9999999,-9999999)
            FR_dicts[flav][tight_region] = FR
            fakeEstimate = getRegionFakeEstimate( yields_LnT , FR)
            #fakeEstimate = degTools.u_float( 0 ) if  fakeEstimate.val < 0 else fakeEstimate 
            #fakeEstimate = degTools.u_float( 0 ) if  fakeEstimate.val < 0 else fakeEstimate 
            prompt_fake_yields_all[flav][tight_region] = {}
            for prompt_samp in ['w', 'tt', 'others' ] + data + sigs :
                sname = sampleInfo.sampleName( prompt_samp )
                slist = sampleNiceNames[ prompt_samp ] 
                prompt_fake_yields_all[flav][tight_region][ sname ] = degTools.dict_operator( yields_prompt , slist ) 
            prompt_fake_yields_all[flav][tight_region]['Fakes'] = fakeEstimate
            prompt_fake_yields_all[flav][tight_region]['Total'] = degTools.dict_operator( prompt_fake_yields_all[flav][tight_region] , ['Fakes']+[sampleInfo.sampleName(s_) for s_ in ['w','tt','others']] ) 

    #comb main SR1s
    for flav in ['mu', 'el']:
        #for main_region, sub_regions in main_sub_sr_regions_all.items():
        for main_region, sub_regions in card_regions_map.items():
            if main_region in  prompt_fake_yields_all[flav]:
                print main_region
                continue #False
            #print main_region
            #print prompt_fake_yields_all[flav].keys()
            #print sub_regions
            prompt_fake_yields_all[flav][main_region] = degTools.dict_manipulator(  
                                                    [ prompt_fake_yields_all[flav][r] for r in sub_regions ] , func = lambda *args: sum(args) )
    # combine el mu to lep 
    for flav in ['mu', 'el']:
        for main_region, sub_regions in card_regions_map.items():
            prompt_fake_yields[flav][main_region] = degTools.dict_manipulator(
                                                    [ prompt_fake_yields_all[flav][r] for r in sub_regions ] , func = lambda *args: sum(args) )        

    prompt_fake_yields_all['lep'] = degTools.dict_manipulator( [prompt_fake_yields_all['mu'] , prompt_fake_yields_all['el']], degTools.yield_adder_func ) 
    prompt_fake_yields['lep'] = degTools.dict_manipulator( [prompt_fake_yields['mu'] , prompt_fake_yields['el']], degTools.yield_adder_func ) 
    fake_yields_summary_all = { flav:{b:prompt_fake_yields_all[flav][b]['Fakes'] for b in prompt_fake_yields_all[flav].keys()} for flav in ['mu','el', 'lep']  }
    fake_yields_summary     = { flav:{b:prompt_fake_yields[flav][b]['Fakes'] for b in prompt_fake_yields[flav].keys()} for flav in ['mu','el', 'lep']  }

    outputDir = cfg.results_dir+"/"+cfg.baseCutSaveDir
    pickle.dump( fake_yields_summary, file("%s/fake_yields_summary_%s.pkl"%( outputDir, cutName) ,"w"))
    pickle.dump( prompt_fake_yields_all, file("%s/yields_summary_allregions_%s.pkl"%(outputDir , cutName) ,"w"))
    pickle.dump( prompt_fake_yields, file("%s/yields_summary_%s.pkl"%(outputDir, cutName),"w"))
    print "FakeEstimation Results:\n %s"%outputDir


    ret = {
            'FR_regions_dict'    : FR_dicts,
            'fake_yields_summary': fake_yields_summary,
            'prompt_fake_yields_all' : prompt_fake_yields_all, 
            'prompt_fake_yields' : prompt_fake_yields, 
            'FRs':FR_pkls ,
            'regions':regions  ,
          }
    pickle.dump( ret, file( '%s/fakeEstimateOutput_%s.pkl'%(outputDir, cutName) , "w") )

    return ret

if __name__ == "__main__":
    ## after running degStop.py
    fakeEstimateOutput = fakeEstimate(cfg,args)
    
    if False:
        prompt_fake_yields_all = fakeEstimateOutput['prompt_fake_yields_all']

        sample_list = prompt_fake_yields_all['lep']['vcr1a'].keys()
        yldByBin  = prompt_fake_yields_all['lep']
        yieldDict = { samp: { b: yldByBin[b][samp] for b in yldByBin.keys()}  for samp in sample_list}
        bkgList= ["WJets","TTJets","Fakes", "Others" ]#,"Others"] 
        
        from Workspace.DegenerateStopAnalysis.tools.CombineCard import CombinedCard
        map_name_niceName  = {
                          'w'       :  'WJets'      ,
                          'tt'      :  'TTJets'   ,
                          'z'       :  'ZJetsInv' ,
                          'qcd'     :  'QCD'     ,
                          'dy'      :  'DYJetsM50',
                          'vv'      :  'Diboson'  ,
                          'st'      :   'ST'      ,
                          #'other'   :   'Other'      ,
                          }
        niceProcessNames = map_name_niceName
    
        bins_order = tight_LnT_map.keys()
        CombineCard = Workspace.DegenerateStopAnalysis.tools.CombineCard.CombinedCard 
        cfw   =  CombinedCard( niceProcessNames = niceProcessNames  );
        cfw.addBins( bkgList , yieldDict['WJets'].keys() )
    
        cfw.specifyObservations(           yieldDict , "DataBlind")
        cfw.specifyBackgroundExpectations( yieldDict , bkgList )
        cfw.specifySignalExpectations(     yieldDict , "T2tt300_270"  )
        cfw.specifyUncertaintiesFromDict( {'wpt':syst_dict}, ['wpt'], bkgList)
        #cfw.addStatisticalUncertainties(yieldDict= yieldDict)
        cardname = ""
        cfw.writeToFile("testcard.txt")
