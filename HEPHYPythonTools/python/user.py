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
  username = "nrad"

