import os

#username is global, in case you have multiple accounts

if os.environ['USER'] in ['easilar']:
  defaultPlotPath = "/afs/hephy.at/user/e/easilar/www/"
  username = "easilar"
  somethingElse = "private for easilar" 

if os.environ['USER'] in ['schoef', 'rschoefbeck', 'schoefbeck']:
  defaultPlotPath = "/afs/hephy.at/user/r/rschoefbeck/www/"
  username = "rschoefbeck"

if os.environ['USER'] in ['dspitzbart', 'dspitzba']:
  defaultPlotPath = "/afs/hephy.at/user/d/dspitzbart/www/"
  username = "dspitzbart"

if os.environ['USER'] in ['nrad']:
  defaultPlotPath = "/afs/hephy.at/user/n/nrad/www/"
  saveDir         = defaultPlotPath 
  afsDataName  = "nrad01"
  combineLocation = "/afs/hephy.at/user/n/nrad/CMSSW/combine/CMSSW_7_4_12_patch4/src/" 
  username = "nrad"

if os.environ['USER'] in ['mzarucki']:
  defaultPlotPath = "/afs/hephy.at/user/n/mzarucki/www/"
  saveDir         = defaultPlotPath 
  afsDataName  = "mzarucki02"
  combineLocation = "/afs/hephy.at/work/m/mzarucki/CMSSW/CMSSW_7_4_12_patch4/src/"
  username = "mzarucki"

if os.environ['USER'] in ['dhandl']:
  defaultPlotPath = "/afs/hephy.at/user/d/dhandl/www/"
  saveDir         = defaultPlotPath
  username = "dhandl"

if os.environ['USER'] in ['vghete']:
  defaultPlotPath = "/afs/hephy.at/user/v/vghete/www/"
  saveDir         = defaultPlotPath 
  afsDataName  = 'vghete02'
  username = 'vghete'
