import ROOT
from math import sqrt

class Variable:

  def __init__(self,name,nbins,xmin,xmax,scut,uselog=True,uoflow="uo"):
    assert name.isalnum()
    self.name = name
    self.nbins = nbins
    self.xmin = xmin
    self.xmax = xmax
    self.uselog = uselog
    self.scut = scut
    self.uoflow = uoflow.lower()

  def is2D(self):
    return False

  def createHistogram(self):
    return ROOT.TH1F(self.name,self.name,self.nbins,self.xmin,self.xmax)

  def moveBinContent(self,h,i,j):
    ci = h.GetBinContent(i)
    ei = h.GetBinError(i)
    cj = h.GetBinContent(j)
    ej = h.GetBinError(j)
    h.SetBinContent(i,0.)
    h.SetBinError(i,0.)
    h.SetBinContent(j,ci+cj)
    h.SetBinError(j,sqrt(ei**2+ej**2))

  def moveUnderOverFlow(self,h):
    if self.uoflow.find("u"):
      self.moveBinContent(h,0,1)
    if self.uoflow.find("o"):
      nb = h.GetNbinsX()
      self.moveBinContent(h,nb+1,nb)

class VariablePair:

  def __init__(self,xname,nbinsx,xmin,xmax,yname,nbinsy,ymin,ymax,uselog=True,suffix=None, \
                 xuoflow="uo",yuoflow="uo"):
    assert xname.isalnum() and yname.isalnum()
    self.name = yname+"_vs_"+xname
    if suffix!=None:
      self.name += "_"+suffix
    self.varx = Variable(xname,nbinsx,xmin,xmax,scut='b')
    self.vary = Variable(yname,nbinsy,ymin,ymax,scut='b')
    self.uselog = uselog
    self.xuoflow = xuoflow.lower()
    self.yuoflow = yuoflow.lower()
    
  def is2D(self):
    return True

  def createHistogram(self):
    return ROOT.TH2F(self.name,self.name,self.varx.nbins,self.varx.xmin,self.varx.xmax, \
                       self.vary.nbins,self.vary.xmin,self.vary.xmax)

  def moveBinContent(self,h,ix,iy,jx,jy):
    i = h.GetBin(ix,iy)
    j = h.GetBin(jx,jy)
    ci = h.GetBinContent(i)
    ei = h.GetBinError(i)
    cj = h.GetBinContent(j)
    ej = h.GetBinError(j)
    h.SetBinContent(i,0.)
    h.SetBinError(i,0.)
    h.SetBinContent(j,ci+cj)
    h.SetBinError(j,sqrt(ei**2+ej**2))

  def moveUnderOverFlow(self,h):
    nbx = h.GetNbinsX()
    nby = h.GetNbinsY()
    if self.xuoflow.find("u"):
      for i in range(nby):
        self.moveBinContent(h,0,i+1,1,i+1)
    if self.xuoflow.find("o"):
      for i in range(nby):
        self.moveBinContent(h,nbx+1,i+1,nbx,i+1)
    if self.yuoflow.find("u"):
      for i in range(nbx):
        self.moveBinContent(h,i+1,0,i+1,1)
    if self.yuoflow.find("o"):
      for i in range(nbx):
        self.moveBinContent(h,i+1,nby+1,i+1,nby)
    if self.xuoflow.find("u") and self.yuoflow.find("u"):
      self.moveBinContent(h,0,0,1,1)
    if self.xuoflow.find("u") and self.yuoflow.find("o"):
      self.moveBinContent(h,0,nby+1,1,nby)
    if self.xuoflow.find("o") and self.yuoflow.find("u"):
      self.moveBinContent(h,nbx+1,0,nbx,1)
    if self.xuoflow.find("o") and self.yuoflow.find("o"):
      self.moveBinContent(h,nbx+1,nby+1,nbx,nby)
    # currently not implemented
    return
