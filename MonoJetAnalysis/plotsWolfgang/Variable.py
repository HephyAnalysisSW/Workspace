import ROOT

class Variable:

  def __init__(self,name,nbins,xmin,xmax,scut,uselog=True):
    assert name.isalnum()
    self.name = name
    self.nbins = nbins
    self.xmin = xmin
    self.xmax = xmax
    self.uselog = uselog
    self.scut = scut

  def createTH1(self):
    return ROOT.TH1F(self.name,self.name,self.nbins,self.xmin,self.xmax)

