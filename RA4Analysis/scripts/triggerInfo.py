#! /usr/bin/env python
import sys, os, re
import commands

#   Disclaimer: This is private code, so it might not work for all your needs, although I think it can do some useful things.
#   Feel free to manipulate, dubplicate, copy or do anything else with the code. You can also give it away as a birthday present.
#   If you have any major complaints or if you find a bug: mdunser@cern.ch
#   Cheers,
#   -marc

def usage():
  print 'Usage as follows:'
  print '           Option --help shows this message\n'
  print 'You have to specify either a runnumber OR a whole JSON file!'
  print '           Option -j or -json specifies the JSON input file.'
  print '           Option -r or -run specifies the run.\n'
  print 'You have to specify either an HLT-path OR a dataset!'
  print '           Option -p or -path specifies the HLT-path'
  print '           Option -d or -dataset specifies the dataset\n'
  print 'Examples: '
  print 'If you\'re searching for a certain trigger and it\'s prescales: specify options -r/-j AND -p. This will also show the PD in which the path is contained (For Run2011A)'
  print 'If you know the PD of the path you\'re looking for: give -r/-j AND BOTH -p AND -d. This gives also the prescales of the path and is way faster than in the previous exmple.'
  print 'If you want to search for all triggers in a dataset with their prescales specify -r/-j AND -d.'
  print 'Examples: '
  print './triggerInfo.py -json myjson.txt -d SingleMu -p HLT_Mu15_v* would give you the prescales of HLT_Mu15 (in all versions) in all runs contained in myjson.txt '
  print '------------------------------------------------------------------'
  print 'ATTENTION with wildcards: Use of * only works with version numbers. E.g. you can specify HLT_Mu15_v* and get useful results, but HLT_Mu*_v* would not work.'
  sys.exit()

def arguments(args):
  runs = []
  path = False
  dataset = False
  if ('--help' in args) or ('-h' in args):
    usage()
  if '-j' in args:
    jsonDict = eval(file(args[args.index('-j')+1],'r').read())
    for key in jsonDict.keys():
      runs.append(int(key))
    runs.sort()
  if '-json' in args:
    jsonDict = eval(file(args[args.index('-json')+1],'r').read())
    for key in jsonDict.keys():
      runs.append(int(key))
    runs.sort()
  if '-r' in args:
    runs.append(int(args[args.index('-r')+1]))
  if '-run' in args:
    runs.append(int(args[args.index('-run')+1]))
  if '-p' in args:
    tmppath = args[args.index('-p')+1]
    path = tmppath.rstrip('*')
  if '-path' in args:
    tmppath = args[args.index('-path')+1]
    path = tmppath.rstrip('*')
  if '-d' in args:
    dataset = args[args.index('-d')+1]
  if '-dataset' in args:
    dataset = args[args.index('-dataset')+1]
  return runs, path, dataset

runs    = arguments(sys.argv)[0]
path    = arguments(sys.argv)[1]
dataset = arguments(sys.argv)[2]

#Define your default datasets. As of now (July 2011) all 2011A datasets and some 2010 PDs are in this list.
#You can just add PDs here, although the script is slower the longer this list is
defaultPDs = ['HT', 'METBTag', 'Jet', 'MultiJet', 'SingleMu', 'DoubleMu', 'MuOnia', 'MuEG', 'MuHad', 'SingleElectron', 'DoubleElectron', 'Photon', 'ElectronHad', 'PhotonHad', 'Tau', 'TauPlusX', 'Commissioning', 'Cosmics', 'MinBias', 'JetHT']

if not runs or (not path and not dataset):
  usage()

if dataset and not path:
  print '--------------------------------------------------------------------------'
  print '--------------------------------------------------------------------------'
  print 'Searching for dataset', dataset, 'in specified runs'
  for run in runs:
    print '--------------------------------------------------------------------------'
    #print '||  Run   || Primary Dataset    | | Prescales'
    print '||  Run   || Primary Dataset   ||     L1 seed        | | Pathname + Prescales'
    print '--------------------------------------------------------------------------'
    for testpath in os.popen('edmConfigFromDB --runNumber ' + str(run) + ' --format streams.list:A.'+dataset):
      if testpath.find(testpath) != -1:
        prescale = os.popen('edmConfigFromDB --runNumber '+ str(run) +' --format summary.ascii --paths '+testpath.rstrip()).readlines()
        searchl1 = re.compile('L1_\w*')
#        print "Prescale:",'edmConfigFromDB --runNumber ' + str(run) + ' --format streams.list:A.'+dataset 
        for line in prescale:
          if 'L1_' in line:
            l1seed = searchl1.search(line)
        print '|| %6d || %17s ||  %17s |' % (run, dataset, l1seed.group()), prescale[-4].rstrip()

if path:
  print '--------------------------------------------------------------------------'
  print '--------------------------------------------------------------------------'
  i=0
  ds = ['0']
  pdList = defaultPDs
  if dataset:
    pdList = [dataset]
    print 'Searching for path', path, ' in dataset', dataset
  else:
    print 'Searching for path', path, ' in all default datasets (Run2011A)'
  for run in runs:
    for pd in pdList:
      searchpaths = []
      goodpath = ''
      for trig in os.popen('edmConfigFromDB --runNumber ' + str(run) + ' --format streams.list:A.'+pd):
        searchpaths.append(trig.rstrip('\n'))
      for searchpath in searchpaths:
        if path in searchpath:
          goodpath = searchpath
      if goodpath == '':
        if dataset:
          print '|| %6d || %17s ||  %s |' % (run, pd, 'Path didn\'t exist in this run and dataset.')
        continue
      ds.append(pd)
      if ds[i+1] != ds[i]:
        print '--------------------------------------------------------------------------'
        print '||  Run   || Primary Dataset   ||     L1 seed        | | Pathname + Prescales'
        print '--------------------------------------------------------------------------'
      i=i+1
      prescale = os.popen('edmConfigFromDB --runNumber '+ str(run) +' --format summary.ascii --paths '+goodpath.rstrip()).readlines()
      searchl1 = re.compile('L1_\w*')
      for line in prescale:
        if 'L1_' in line:
          l1seed = searchl1.search(line)
      print '|| %6d || %17s ||  %17s |' % (run, pd, l1seed.group()), prescale[-4].rstrip()
          

