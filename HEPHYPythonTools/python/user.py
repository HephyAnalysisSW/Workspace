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
  username = "nrad"

if os.environ['USER'] in ['mzarucki']:
  defaultPlotPath = "/afs/hephy.at/user/n/mzarucki/www/"
  saveDir         = defaultPlotPath 
  afsDataName  = "mzarucki01"
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
