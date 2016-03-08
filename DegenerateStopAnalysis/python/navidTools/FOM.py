import math 
import ROOT

from Workspace.HEPHYPythonTools.u_float import u_float



## --------------------------------------------------------------
##                        Figure of Merit Tools
## --------------------------------------------------------------

def AMSSYS (s,b,sysUnc=0.2):
  #print s, b
  sysUnc2=sysUnc*sysUnc
  b2 = b*b 
  if s==0: 
    return 0
  if b<=0: 
    return -1
  #return (lambda s,b : math.sqrt(2*( (s+b)*math.log(((s+b)*(b+sysUnc*b))/(b2+(s+b)*sysUnc*b))  - b2/(sysUnc*b)*math.log(1+sysUnc*b*s/(b*(b+sysUnc*b))) )) if b!=0 else -1)(s,b)
  ret = math.sqrt(2*( (s+b)*math.log(((s+b)*(b+ (sysUnc2*b2) ))/(b2+(s+b)* (sysUnc2*b2) ))  - b2/( (sysUnc2*b2) )*math.log(1+ (sysUnc2*b2) *s/(b*(b+ (sysUnc2*b2) ))))) 
  return ret 


def AMS1 (s,b,sysUnc=0.2):
    """
        Equations 20 and 21:
        http://www.jmlr.org/proceedings/papers/v42/cowa14.pdf
    """
    sysUnc2= sysUnc*sysUnc
    b0 = 0.5*( b - sysUnc2 + math.sqrt( (b-sysUnc2)*(b-sysUnc2)+4*(s+b)*(sysUnc2)   )  ) 
    ams1 = math.sqrt( 2* ((s+b)*math.log((s+b)/b0)-s-b+b0 )+ (b-b0)*(b-b0)/sysUnc2  )
    return ams1

def AMSc (s,b,sysUnc=0.2):
    """
        Equations 20 and 21:
        http://www.jmlr.org/proceedings/papers/v42/cowa14.pdf
    """
    #breg = sysUnc
    breg = 10
    amsc = math.sqrt( 2.*( (s+b+breg)*math.log(1+s/(b+breg) ) - s   ) )

    return amsc

def RATIO (s,b,sysUnc=0.2 ):
    #return lambda s,b, sysUnc: s/float(b) if b!=0 else -1
    return s/float(b) if b!=0 else -1



fomFuncs= {
                "SOB"         : lambda s,b,sysUnc  : s/math.sqrt(b) if b!=0 else -1 ,
                "SOBSYS"      : lambda s,b,sysUnc : s/math.sqrt(b+(sysUnc*sysUnc*b*b) ) if b!=0 else -1 ,
                "AMS"         : lambda s,b,sysUnc : math.sqrt(2*((s+b)*math.log(1+1.*s/b)-s) ) if b!=0 else -1 ,
                "AMSSYS"      : AMSSYS ,
                "AMS1"        : AMS1   ,
                "AMSc"        : AMSc   ,
                "RATIO"       : RATIO ,  
            }

def get_float(val):
    try:
        return float(val) 
    except AttributeError:     #might be a u_float
        return float(val.val)     
    except ValueError:
        if "+-" in val:
            split = val.rsplit("+-")
            return float( split[0] )

def calcFOMs(s,b,sysUnc=0.2,fom=None):

  s=get_float(s)
  b=get_float(b)

  #s=float(s)
  #b=float(b)
  if fom: 
    return fomFuncs[fom](float(s),float(b),sysUnc)
  else:
    ret = {}
    for f in fomFuncs:
      ret[f]=fomFuncs[f](s,b,sysUnc)
    return ret







def getFOMFromTH2F(sHist,bHist,fom="AMSSYS",sysUnc=0.2): 
  assert sHist.GetNbinsX() == bHist.GetNbinsX(), "xBins dont match" 
  assert sHist.GetNbinsY() == bHist.GetNbinsY(), "yBins don't match" 
  nBinX= sHist.GetNbinsX() 
  nBinY= sHist.GetNbinsY() 

  fomHist=sHist.Clone() 
  fomHist.Reset() 
  fomHist.SetMarkerSize(0.8) 
  fomHist.SetName("FOM_%s_"%fom+fomHist.GetName() ) 
  for x in range(1,nBinX+1): 
    for y in range(1,nBinY+1): 
      s=sHist.GetBinContent(x,y) 
      b=bHist.GetBinContent(x,y) 
      #print s,b,
      fomVal= fomFuncs[fom](s,b,sysUnc) 
      #print fomVal
      fomHist.SetBinContent(x,y,fomVal) 
  return fomHist   




def getFOMFromTH1F(sHist,bHist,fom="AMSSYS",sysUnc=0.2,debug=False,norm=False): 
    if debug:
        print sHist,bHist
        sHist.Print('all')
        bHist.Print('all')

    if fom.lower()=="ratio": 
        retHist = sHist.Clone()
        retHist.Scale(1./retHist.Integral())
        denomHist = bHist.Clone()
        denomHist.Scale(1./denomHist.Integral())
        retHist.Divide(denomHist)
    else:
        assert sHist.GetNbinsX() == bHist.GetNbinsX(), "xBins dont match" 
        retHist=sHist.Clone() 
        nBinX= sHist.GetNbinsX() 
        retHist.Reset() 
        retHist.SetMarkerSize(0.8) 
        retHist.SetName("FOM_%s_"%fom+retHist.GetName() ) 
        for x in range(1,nBinX+1): 
            s=sHist.GetBinContent(x) 
            b=bHist.GetBinContent(x) 
            #print s,b,
            fomVal= fomFuncs[fom](s,b,sysUnc) 
            #print fomVal
            retHist.SetBinContent(x,fomVal) 

    if norm:
        sNorm = 1./ sHist.Integral()
        bNorm = 1./ bHist.Integral()
        totNorm = sNorm/bNorm
        retHist.Scale(totNrom)

    return retHist   



def getHistMax(hist):
  nBinX = hist.GetNbinsX()
  histMax= max( [(x,hist.GetBinContent(x)) for x in range(1, nBinX+1)] , key= lambda f: f[1] )
  return histMax

def getHistMin(hist,onlyPos=False):
  nBinX = hist.GetNbinsX()
  binContents = [ (x, hist.GetBinContent(x) ) for x in range(1, nBinX+1)]
  if onlyPos:
    binContents=filter( lambda x: x[1]>0, binContents )
  ret = min( binContents , key= lambda f: f[1] ) if binContents else [0,0]
  return ret
  #if not binContents: 
  #  print "?????????????", binContents, hist.GetName(), hist.Print("all")
  #  return 0 
  #else:
  #  histMin= min( binContents , key= lambda f: f[1] )
  #  return histMin

def getHisMinMax(hist):
    return getHistMin(hist), getHistMax(hist)


def getFOMFromTH1FIntegral(sHist,bHist,fom="AMSSYS",sysUnc=0.2, verbose=False, integral =True):
    if not sHist.GetNbinsX() == bHist.GetNbinsX():
        print sHist, sHist.GetNbinsX()
        print bHist, bHist.GetNbinsX()
        assert False, "xBins dont match"
    nBinX= sHist.GetNbinsX()
    fomHist = sHist.Clone()
    fomHist.Reset()
    fomHist.GetYaxis().SetTitle("_".join([fom,sHist.GetName(),bHist.GetName()]))
    fomHist.SetName("_".join([fom,sHist.GetName(),bHist.GetName()]))
    #nBins  = int( fomHist.GetNbinsX() )
    #lowBin = int( fomHist.GetBinLowEdge(1)  )
    #hiBin  = int( fomHist.GetBinLowEdge(fomHist.GetNbinsX()+1)  )
    #[ (x, sHist.GetBinLowEdge(x),  sHist.Integral( 1  , x   )  )  for x in range(nBins/2, nBins)   ]    
    #print "-----FOM INTEGRAL", sHist.GetName , nBins, lowBin, hiBin 


    for x in range(1,nBinX+1):
        
        if integral:        
            s=u_float(sHist.Integral(x,nBinX) )
            b=u_float(bHist.Integral(x,nBinX) )
        else:
            s=u_float( sHist.GetBinContent(x) , sHist.GetBinError(x) )
            b=u_float( bHist.GetBinContent(x) , bHist.GetBinError(x) )

        fomVal = fomFuncs[fom](s.val,b.val,sysUnc) 
        fomHist.SetBinContent(x,fomVal)
        if not integral:
            if b.sigma: fomHist.SetBinError(x, (s/b).sigma )
        if verbose:
            print "bin:", x
            print "     Signal: %s, Bkg: %s"%(sHist.GetBinContent(x),bHist.GetBinContent(x)) 
            print "     INTEGS: %s, %s"%(s,b)
            print "     FOM:", fomVal
    return fomHist

def getCutEff(hist,rej=False):
  ''' rej=False will return 1-eff ''' 
  nBinX= hist.GetNbinsX()
  effHist = hist.Clone()
  effHist.Reset()
  tot = hist.Integral()
  #print "tot:", tot
  for x in range(1,nBinX+1):
    eff = hist.Integral(x,nBinX)/float(tot)
    if rej:
      effHist.SetBinContent(x,1-eff)
    else:
      effHist.SetBinContent(x,eff)
  return {"hist":effHist,'tot':tot}


def getEffFomPlot(sHist,bHist,fom="AMSSYS", sysUnc=0.2,savePath=''):
  canv = ROOT.TCanvas()
  sEff = getCutEff(sHist)['hist'] 
  bEff = getCutEff(bHist)['hist'] 
  fom  = getFOMFromTH1FIntegral(sHist,bHist)
  fomMax = getHistMax(fom)
  maxDict = {
             "maxFOM":fomMax[1],
              "bin":fomMax[0],
              "sEff":sEff.GetBinContent(fomMax[0]),
              "bEff":bEff.GetBinContent(fomMax[0]),
            }

  bEff.SetLineColor(bEff.GetFillColor())
  bEff.SetFillColor(0)

  fomColor = ROOT.kRed

  rightmax = 1.1*fom.GetMaximum();
  scale = canv.GetUymax()/rightmax
  fom.Scale(scale)
  bEff.Draw()
  sEff.Draw('same')
  fom.SetLineColor(fomColor)
  fom.Draw('same')

  fom.SetLineWidth(2)
  sHist.SetLineWidth(2)
  bHist.SetLineWidth(2)

  xmin= 20 # (ROOT.gPad.GetUxmax()
  ymin= 0  # ROOT.gPad.GetUymin()
  xmax= 20 # ROOT.gPad.GetUxmax() 
  ymax= 1.05 # ROOT.gPad.GetUymax()
  axis = ROOT.TGaxis( xmin, ymin, xmax, ymax ,0,rightmax,510,"+L")
  axis.SetLabelColor(fomColor)
  axis.SetTitle("FOM")
  axis.SetTitleColor(fomColor)
  axis.Draw()
  print "canv:", canv.GetUxmax()
  print "after:",  (ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymin(), ROOT.gPad.GetUxmax(), ROOT.gPad.GetUymax() )
  if savePath:
    canv.SaveAs(savePath)
  return {"canv":canv,"sEff":sEff,"bEff":bEff,"fom":fom,"axis":axis, "max":maxDict }



def get2DEffFOM(sHist,bHist,nBinsX=20,nBinsY=20,bkgRej=True,fom="AMSYS"):
    sTot = sHist.Integral()
    bTot = bHist.Integral()
    effFOMHist = ROOT.TH2D("effFOM","effFOM",nBinsX,0,1,nBinsY,0,1)
    yTitle = "Bkg Rej" if bkgRej else "Bkg Eff"

    xDiv, yDiv = 1/float(nBinsX), 1/float(nBinsY)
    xMid, yMid = xDiv/2., yDiv/2.
    for x in range(1,nBinsX+1):
        xMidVal = xDiv/2. + (x-1)*xDiv
        #print "--- x", xMidVal
        for y in range(1,nBinsY+1):
            yMidVal = yDiv/2. + (y-1)*yDiv
            if bkgRej:
                fomVal = calcFOMs(sTot*xMidVal,bTot*(1-yMidVal), fom=fom)
            else:
                fomVal = calcFOMs(sTot*xMidVal,bTot*(yMidVal) , fom=fom)
            #effFOMHist.SetBinContent(x,y,fomVal)
            #print "  ", xMidVal, yMidVal , fomVal
            effFOMHist.Fill(xMidVal,yMidVal,fomVal)
    effFOMHist.GetXaxis().SetTitle("Signal Eff")
    effFOMHist.GetYaxis().SetTitle(yTitle)
    return effFOMHist

def getROC(sHist, bHist, graphName='', fom="AMSSYS", sysUnc=0.2,savePath=''):
  s = getCutEff(sHist)
  b = getCutEff(bHist,rej=True)
  sEffHist = s['hist']
  bRejHist = b['hist']
  sTot = s['tot']
  bTot = b['tot']
  roc = ROOT.TGraph()
  for x in range(1,sEffHist.GetNbinsX()+1):
    sEff = sEffHist.GetBinContent(x)
    bRej = bRejHist.GetBinContent(x)
    roc.SetPoint(x,sEff,bRej)
  return {'roc':roc,'sTot':sTot, 'bTot':bTot}
  #return roc





