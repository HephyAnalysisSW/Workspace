import ROOT
from math import *

def smooth2DHisto(h, exclThreshold, requAbs, nbx, nby):
  if not nbx%2:nbx+=1
  if not nby%2:nby+=1
  
  resh = h.Clone(h.GetName()+"_smoothed")
  resh.Reset()

  for ix in range(1, h.GetNbinsX()+1):
    for iy in range(1, h.GetNbinsY()+1):
      res=0.
      count = 0
      for dx in [int(ceil(n - nbx/2.)) for n in range(nbx)]:    
        for dy in [int(ceil(n - nby/2.)) for n in range(nby)]:
          bx = ix+dx
          by = iy+dy
          if bx>=1 and by>=1 and bx<=h.GetNbinsX() and by<= h.GetNbinsY():
            v = h.GetBinContent(h.FindBin(bx,by))
            if ( (not requAbs) and (v>exclThreshold)) or (requAbs and abs(v)>abs(exclThreshold)):
              res+=v
              count+=1
        if count>0:
          res/=count
        resh.SetBinContent(resh.FindBin(ix, iy), res)
  return resh
