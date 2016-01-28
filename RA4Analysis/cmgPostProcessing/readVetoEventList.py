import os
#from sets import Set


def evt_veto_list():
  file_to_read = "/data/easilar/EventVetoList_filters/csc2015_Dec01.txt"
  file_to_read1 = "/data/easilar/EventVetoList_filters/ecalscn1043093_Dec01.txt"
  file_to_read2 = "/data/easilar/EventVetoList_filters/muonBadTrack.txt"
  file_to_read3 = "/data/easilar/EventVetoList_filters/badResolutionTrack.txt"

  file_open = open(file_to_read,'r')
  run_lumi_evt = set()
  for line in file_open.readlines():
    run_lumi_evt.add(str(line))

  file_open1 = open(file_to_read1,'r')
  for line in file_open1.readlines():
    run_lumi_evt.add(str(line))

  
  file_open2 = open(file_to_read2,'r')
  for line in file_open2.readlines():
    run_lumi_evt.add(str(line))

  file_open3 = open(file_to_read3,'r')
  for line in file_open3.readlines():
    run_lumi_evt.add(str(line))

  return run_lumi_evt

#x = "254227:24:23350027\n"


#if x in run_lumi_evt:
#  print "YES!!"

