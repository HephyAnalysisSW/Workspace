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

  def is2D(self):
    return False

  def createHistogram(self):
    return ROOT.TH1F(self.name,self.name,self.nbins,self.xmin,self.xmax)

class VariablePair:

  def __init__(self,xname,nbinsx,xmin,xmax,yname,nbinsy,ymin,ymax,uselog=True,suffix=None):
    assert xname.isalnum() and yname.isalnum()
    self.name = yname+"_vs_"+xname
    if suffix!=None:
      self.name += "_"+suffix
    self.varx = Variable(xname,nbinsx,xmin,xmax,scut='b')
    self.vary = Variable(yname,nbinsy,ymin,ymax,scut='b')
    self.uselog = uselog
    
  def is2D(self):
    return True

  def createHistogram(self):
    return ROOT.TH2F(self.name,self.name,self.varx.nbins,self.varx.xmin,self.varx.xmax, \
                       self.vary.nbins,self.vary.xmin,self.vary.xmax)
