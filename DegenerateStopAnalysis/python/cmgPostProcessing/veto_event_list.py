import os
#from sets import Set


veto_lists_dict = {
                  "csc":  "/data/easilar/EventVetoList_filters/csc2015_Dec01.txt",
                  "ecal":   "/data/easilar/EventVetoList_filters/ecalscn1043093_Dec01.txt",
                  "muon":   "/data/easilar/EventVetoList_filters/muonBadTrack.txt",
                  "badresol":   "/data/easilar/EventVetoList_filters/badResolutionTrack.txt",
                  }




def get_veto_list(veto_lists_dict=veto_lists_dict):
    evt_veto_lists = {"all":set()}
    evt_veto_lists.update({x:set() for x in veto_lists_dict})

    for vl in veto_lists_dict:
        fopen = open(veto_lists_dict[vl])
        for line in fopen.readlines():
            evt_veto_lists[vl].add(str(line))
            evt_veto_lists['all'].add(str(line))

    return evt_veto_lists


#import numpy as np
#def get_veto_list2(veto_lists_dict=veto_lists_dict):
#    evt_veto_lists = {"all":np.array()}
#    evt_veto_lists.update({x:set() for x in veto_lists_dict})
#
#    for vl in veto_lists_dict:
#        fopen = open(veto_lists_dict[vl])
#        for line in fopen.readlines():
#            evt_veto_lists[vl].add(str(line))
#            evt_veto_lists['all'].add(str(line))
#
#    return evt_veto_lists


#def processEventVetoList(readTree, 
