import os

#username is global, in case you have multiple accounts

if os.environ['USER'] in ['easilar']:
  defaultPlotPath = "/afs/hephy.at/user/e/easilar/www/"
  username = "easilar"
  somethingElse = "private for easilar" 

if os.environ['USER'] in ['schoef', 'rschoefbeck', 'schoefbeck']:
  defaultPlotPath = "/afs/hephy.at/user/r/rschoefbeck/www/"
  username = "rschoefbeck"
