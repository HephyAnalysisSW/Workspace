# class for floats with asymetric uncertainties around the central value
# using a method from Garwood (1936) to obtain correct coverage
# 1 sigma (68.27%) uncertainties are used by default

from math import *
import scipy.stats as stats

def getValErrString(val,errUp, errDown=0, precision=3):
  # maybe format output string for nicer printing
  if errDown==0:
    return str(round(val,precision))+' +/- '+str(round(errUp,precision))
  else:
    return str(round(val,precision))+' + '+str(round(errUp,precision))+' - '+str(round(errDown,precision))

class asym_float:
  def __init__(self, central, up=0, down=0, poisson=True, forcePoisson=False, cl=0.682689492):
    self.central  = central
    if (up==0 and type(central)==int and poisson) or forcePoisson:
      upper = stats.chi2.ppf((1+cl)/2,2*(central+1))/2
      self.up = upper - central
      if central==0:
        self.down = 0
      else:
        lower = stats.chi2.ppf((1-cl)/2, 2*central)/2
        self.down = central - lower
    else:
      self.up       = up
      if down==0:
        self.down   = up
      else:
        self.down   = down
  
  def __add__(self,other):
    if not type(other)==type(self):
      raise ValueError( "Can't add, two objects should be asym_float but is %r."%(type(other)) )
    central = self.central+other.central
    up      = sqrt(self.up**2 + other.up**2)
    down    = sqrt(self.down**2 + other.down**2)
    return asym_float(central,up,down)
  
  def __radd__(self,other):
    if other is 0: other=asym_float(0,0,0)
    return self.__add__(other)
  
  def __neg__(self):
    central = -self.central
    return asym_float(central, self.up, self.down)

  def __sub__(self,other):
    return self.__add__(-other)

  def __mul__(self,other):
    if not ( type(other)==int or type(other)==float or type(other)==type(self)):
      raise ValueError( "Can't multiply, two objects should be asym_float but is %r."%(type(other)) )
    if type(other)==type(self):
      central = self.central * other.central
      up = sqrt((self.up * other.central)**2 + (self.central * other.up)**2)
      down = sqrt((self.down * other.central)**2 + (self.central * other.down)**2)
    elif type(other)==int or type(other)==float:
      central = self.central * other
      up = self.up * other
      down = self.down * other
    else:
      raise NotImplementedError("This should never happen.")
    return asym_float(central,up,down)
  
  def __rmul__(self,other):
    return self.__mul__(other)
  
  def __div__(self,other):
    if not ( type(other)==int or type(other)==float or type(other)==type(self)):
      raise ValueError( "Can't divide, %r is not a float, int or asym_float"%type(other) )
    if type(other)==type(self):
      central = self.central/other.central
      up = (1./other.central)*sqrt(self.up**2+((self.central*other.up)/other.central)**2)
      down = (1./other.central)*sqrt(self.down**2+((self.central*other.down)/other.central)**2)
    elif type(other)==int or type(other)==float:
      central = self.central/other
      up = self.up/other
      down = self.down/other
    else:
      raise NotImplementedError("This should never happen.")
    return asym_float(central, up, down)
  
  def __str__(self):
    return str(self.central)+'+'+str(self.up)+'-'+str(self.down)
  
  def __repr__(self):
    return self.__str__()

  def __gt__(self, other):
    if not ( type(other)==int or type(other)==float or type(other)==type(self)):
      raise ValueError( "Can't compare, %r is not a float, int or asym_float"%type(other) )
    if type(other)==type(self):
      return self.central>other.central
    elif type(other)==int or type(other)==float:
      return self.central>other

  def __lt__(self, other):
    if not ( type(other)==int or type(other)==float or type(other)==type(self)):
      raise ValueError( "Can't compare, %r is not a float, int or asym_float"%type(other) )
    if type(other)==type(self):
      return self.central<other.central
    elif type(other)==int or type(other)==float:
      return self.central<other

  def __float__(self):
    return self.central
  
  def round(self, n=2):
    return asym_float(round(self.central,n), round(self.up,n), round(self.down,n))
  
  def isSymmetric(self):
    return self.up==self.down

  def printValues(self):
    return getValErrString(self.central, self.up, self.down)

  def getTexString(self, acc=2):
    if self.up==self.down:
      s = "$"+str(round(self.central,acc))+str('\pm')+str(round(self.up,acc))+"$"
      return s
    else:
      s = "$"+str(round(self.central,acc))+"^{+"+str(round(self.up,acc))+"}_{-"+str(round(self.down,acc))+"}$"
      return s

