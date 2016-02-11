import os
#from sets import Set


def evt_veto_list():
  file_to_read = "/data/easilar/EventVetoList_filters/csc2015_Dec01.txt"
  file_to_read1 = "/data/easilar/EventVetoList_filters/ecalscn1043093_Dec01.txt"
  file_to_read2 = "/data/easilar/EventVetoList_filters/muonBadTrack.txt"
  file_to_read3 = "/data/easilar/EventVetoList_filters/badResolutionTrack.txt"
  ultimate = set()
  file_open = open(file_to_read,'r')
  csc_list = set()
  for line in file_open.readlines():
    csc_list.add(str(line))
    ultimate.add(str(line))

  ecal_list = set()
  file_open1 = open(file_to_read1,'r')
  for line in file_open1.readlines():
    ecal_list.add(str(line))
    ultimate.add(str(line))
  
  muon_list = set()
  file_open2 = open(file_to_read2,'r')
  for line in file_open2.readlines():
    muon_list.add(str(line))
    ultimate.add(str(line))

  badreso_list = set()
  file_open3 = open(file_to_read3,'r')
  for line in file_open3.readlines():
    badreso_list.add(str(line))
    ultimate.add(str(line))

  return {"csc": csc_list , "ecal": ecal_list , "muon": muon_list , "badreso":badreso_list , "ultimate": ultimate }

#x = "254227:24:23350027\n"


#if x in run_lumi_evt:
#  print "YES!!"

