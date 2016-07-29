from cardFileWriter import cardFileWriter
#from limit_helper import plotsignif , plotLimit , signal_bins_3fb
from math import exp,sqrt,isnan
import os,sys
import ROOT

def relErrForLimit(value,variance,sign=1):
    result = 1.+sign*sqrt(variance)/value
    if result<0.:
        result = 0.01
    return result

def relErrorsOnFractions(yields,varYields):
    ny = len(yields)
    assert ny==len(varYields)
    sy = sum(yields)
    a = ROOT.TMatrixD(ny,ny)
    c = ROOT.TMatrixDSym(ny)
    for i in range(ny):
        rai = ROOT.TMatrixDRow(a,i)
        rci = ROOT.TMatrixDRow(c,i)
        for j in range(ny):
            if j==i:
                rci[j] = varYields[i]
            else:
                rci[j] = 0.
            raj = ROOT.TMatrixDRow(a,i)
            v = -yields[i]
            if j==i:
                v += sy
            v /= sy*sy
            rai[j] = v
    d = c.Similarity(a)
    result = [ ]
    for i in range(ny):
        result.append(sqrt(d[i][i])/(yields[i]/sy))
    return result
#    for i in range(ny):
#        line = ""
#        for j in range(ny):
#            if j==i:
#                line += "{0:8.4f}".format(sqrt(d[i][j]))
#            else:
#                line += "{0:8.4f}".format(d[i][j]/sqrt(d[i][i]*d[j][j]))
#        print line
            
    
class CalcSingleLimit:

    def __init__(self,bkgres,sbBinNames,sbBins,mbBinNames,mbBins,sigres,signal):

        self.name = "calc_single_limit"
        self.runLimit = False
        self.runBlind = False
        self.force = False
        self.dir = "."
        self.useBins = range(len(mbBinNames))
        self.procNames = [ "W", "tt", "other", "QCD" ]

        self.bkgres = bkgres
        self.sbBinNames = sbBinNames
        self.sbBins = sbBins
        self.mbBinNames = mbBinNames
        self.mbBins = mbBins

        self.sigres = sigres
        self.signal = signal
        self.mglu = signal["mglu"]
        self.mlsp = signal["mlsp"]

        self.c = cardFileWriter()
        self.c.defWidth=10
        self.c.precision=3
        self.c.maxUncNameWidth = 17
        self.c.maxUncStrWidth = 15

        self.yieldsW = { }
        self.yieldstt = { }
        self.kappaVars = { }
        self.paramLines = [ ]
        self.rateParamLines = [ ]
        self.allRateParams = [ ]
        self.allRateParamValues = { }
        self.yWtts = { }

    def subDict(self,d,bins):
        return d[bins[0]][bins[1]][bins[2]]

    def sigSubDict(self,d):
        return d["signals"][self.mglu][self.mlsp]

    def rateParamName(self,name,p):
        result = name[0].lower()
        result += name[1:]
        result += p
        return result

    def paramName(self,name,p):
        result = "k"
        result += name
        result += p
        return result


    def addKappaVar(self,name,p,err):
        n = self.paramName(name,p)
        if not n in self.kappaVars:
            self.kappaVars[n] = 0.
        self.kappaVars[n] += err**2

    def crFormulaLine(self,nameMB,nameSB,p,yWtt):
        result = self.rateParamName(nameMB+"C",p)
        if result in self.allRateParams:
            print "duplicate",result
        assert not result in self.allRateParams
        self.allRateParams.append(result)
        result += " rateParam "
        result += nameMB + "C " + p + " (" + "{0:8.3f}".format(yWtt[p]).strip() + "*(1"
        result += "+" if yWtt["e"+p]>0 else "-"
        result += "{0:8.3f}".format(abs(yWtt["e"+p])).strip() + "*@0)) "
        result += "yWtt"+nameMB
        return result

    def srFormulaLine(self,nameMB,nameSB,p):
        result = self.rateParamName(nameMB+"S",p)
        if result in self.allRateParams:
            print "duplicate",result
        assert not result in self.allRateParams
        self.allRateParams.append(result)
        result += " rateParam "
        result += nameMB + "S " + p + " (@0*@1/@2*@3) "
        params = [ self.rateParamName(nameMB+"C",p), self.rateParamName(nameSB+"S",p),  \
                       self.rateParamName(nameSB+"C",p), self.paramName(nameMB+"S",p) ]
        result += ",".join(params)
        return result

    def paramValueLine(self,name,p,val,err=0.20):
        result = self.paramName(name,p)
        assert not result in self.allRateParams
        self.allRateParams.append(result)
        result += " param "
        result += "{0:8.4f}".format(val) + " "
        #result += "{0:8.3f}".format(err)
        return result

    def paramValueLine1(self,name,val,err):
        result = name[:]
        assert not result in self.allRateParams
        self.allRateParams.append(result)
        result += " param "
        result += "{0:8.4f}".format(val) + " "
        result += "{0:8.3f}".format(err)
        return result

    def rateParamValueLine(self,name,p,val,comment=False):
        result = self.rateParamName(name,p)
        if not comment:
            assert not result in self.allRateParams
            self.allRateParams.append(result)
            self.allRateParamValues[result] = val
        result += " rateParam "
        result += name + " " + p + " "
        result += "{0:8.3f}".format(val) + " "
        result += "[0.," + "{0:8.3f}".format(3*val).strip() + "]"
        #result += "[" + "{0:8.3f}".format(0.5*val).strip() + ","
        #result += "{0:8.3f}".format(2*val).strip() + "]"
        if comment:
            result = "#" + result
        return result

    def limitSinglePoint(self):

      mbBinNames = [ ]
      for i,n in enumerate(self.mbBinNames):
          if i in self.useBins:
              mbBinNames.append(n)
      sbBinNames = [ ]
      for n in self.sbBinNames:
          for m in mbBinNames:
              if n[2:]==m[2:]:
                  sbBinNames.append(n)
                  break
      print "Using mb bins ",mbBinNames
      print "Using sb bins ",sbBinNames
      #
      # scale signal cross section for low masses
      #
      xsecFactor = 1
      if self.mglu<1000:
          xsecFactor = 0.1
      #
      # bin definition; observed and expected counts
      #
      for sbname in sbBinNames:
        sbnameC = sbname + "C"
        self.c.addBin(sbnameC,self.procNames,sbnameC)
        sbnameS = sbname + "S"
        self.c.addBin(sbnameS,self.procNames,sbnameS)
        sbres = self.subDict(self.bkgres,self.sbBins[sbname])
        print "Setting sbres to ",self.sbBins[sbname]
        sbsigres = self.subDict(self.sigres,self.sbBins[sbname])["signals"][self.mglu][self.mlsp]
        #
        # debug
        #
        #if sbname.startswith("J4"):
        #    numerator = sbres["y_crNJet_1b_highDPhi"] - sbres["yQCD_crNJet_1b_highDPhi"]
        #    denominator = sbres["y_crNJet_1b_lowDPhi"] - sbres["yQCD_crNJet_1b_lowDPhi"]
        #    print "ttbar SB :",numerator,denominator,numerator/denominator,sbres["rCS_crLowNJet_1b"]
        #    print sbres["rCS_crLowNJet_1b"]["rCS"],sbres["rCS_crLowNJet_1b_kappa"]["rCS"], \
        #        sbres["rCS_crLowNJet_1b_onlyTT"]["rCS"],sbres["rCS_srNJet_0b_onlyTT"]["rCS"]
        #
        for r in [ "C", "S" ]:
            rDPhi = "low" if r=="C" else "high"
            rDPhi += "DPhi"
            rSig = "CR" if r=="C" else "SR"
            # calculate missing numbers for both low and high dPhi
            # yield (W) = observed - estimated tt # others are neglected in yield
            wYield = sbres["y_crNJet_0b_"+rDPhi] - sbres["yTT_crNJet_0b_"+rDPhi]
                # - sbres["yRest_crNJet_0b_"+rDPhi+"_truth"]
            sbres["yW_crNJet_0b_"+rDPhi] = wYield
            # error on wYield
            # yield (W) = observed - estimated tt # others are neglected in yield
            wVar = sbres["y_Var_crNJet_0b_"+rDPhi] + sbres["yTT_Var_crNJet_0b_"+rDPhi]
              # + sbres["yRest_Var_crNJet_0b_"+rDPhi+"_truth"]
            sbres["yW_Var_crNJet_0b_"+rDPhi] = wVar
            #
            # define W sideband
            #
            if sbnameS[:2]=="J3":
              # observation
              # currently: derive from truth (!*! assume no QCD in SB/SR)
              #y_truth = sbres["yW_crNJet_0b_"+rDPhi+"_truth"] + \
              #    sbres["yTT_crNJet_0b_"+rDPhi+"_truth"] + \
              #    sbres["yRest_crNJet_0b_"+rDPhi+"_truth"]
              self.c.specifyObservation(sbname+r,int(sbres["y_crNJet_0b_"+rDPhi]+0.5))
              print "Setting observation for ",sbname+r,"to",sbres["y_crNJet_0b_"+rDPhi]
              self.c.specifyExpectation(sbname+r,"signal",sbsigres['yield_SB_W_'+rSig]*xsecFactor)
              # self.c.specifyExpectation(sbnameS,"W",sbres["yW_crNJet_0b_"+rDPhi])
              yW = sbres["yW_crNJet_0b_"+rDPhi]
              self.c.specifyExpectation(sbname+r,"W",1.)
              self.rateParamLines.append(self.rateParamValueLine(sbname+r,"W",yW))
              assert not (sbname+r) in self.yieldsW
              self.yieldsW[sbname+r] = yW
              self.c.specifyExpectation(sbname+r,"tt",sbres["yTT_crNJet_0b_"+rDPhi])
              self.c.specifyExpectation(sbname+r,"other",sbres["yRest_crNJet_0b_"+rDPhi+"_truth"])
              self.c.specifyExpectation(sbname+r,"QCD",0.001) # QCD is neglected in yield
              if r=="C":
                  self.c.addUncertainty("tt"+sbname,"lnN",group="yWtt")
              self.c.specifyUncertainty("tt"+sbname,sbname+r,"tt",relErrForLimit(sbres["yTT_crNJet_0b_"+rDPhi],
                                                                                 sbres["yTT_Var_crNJet_0b_"+rDPhi]))
            #
            # define tt sideband
            # 
            elif sbnameS[:2]=="J4":
              # observation
              #y_truth = sbres["yW_crNJet_1b_"+rDPhi+"_truth"] + \
              #    sbres["yTT_crNJet_1b_"+rDPhi+"_truth"] + \
              #    sbres["yRest_crNJet_1b_"+rDPhi+"_truth"]
              self.c.specifyObservation(sbname+r,int(sbres["y_crNJet_1b_"+rDPhi]+0.5))
              self.c.specifyExpectation(sbname+r,"signal",sbsigres['yield_SB_tt_'+rSig]*xsecFactor)
              self.c.specifyExpectation(sbname+r,"W",0.001)
              # self.c.specifyExpectation(sbnameS,"tt",sbres["y_crNJet_1b_"+rDPhi])
              ytt = sbres["y_crNJet_1b_"+rDPhi] - sbres["yQCD_crNJet_1b_"+rDPhi]
              self.c.specifyExpectation(sbname+r,"tt",1.)
              self.rateParamLines.append(self.rateParamValueLine(sbname+r,"tt",ytt))
              assert not (sbname+r) in self.yieldstt
              self.yieldstt[sbname+r] = ytt
              self.c.specifyExpectation(sbname+r,"other",0.001) 
#              self.c.specifyExpectation(sbname+r,"other",sbres["yRest_crNJet_1b_"+rDPhi+"_truth"]) 
              self.c.specifyExpectation(sbname+r,"QCD",sbres["yQCD_crNJet_1b_"+rDPhi])

      #
      # (anti-)correlations from fitted W/tt yields
      #
      for mbname in mbBinNames:
        bname = mbname[2:]
        mbnameC = mbname + "C"
        mbnameS = mbname + "S"
        mbres = self.subDict(self.bkgres,self.mbBins[mbname])
        # mbsigres = self.subDict(self.sigres,self.mbBins[mbname])

        sbWname = "J3" + bname
        sbWnameS = sbWname + "S"
        #uncName = "yWtt" + sbWnameS
        #if not uncName in self.c.uncertainties:
        if sbWnameS:
            #
            # anticorrelated W/tt yields from fit (translated from low dphi region)
            #   use errors on fraction (total normalization is included in Poisson error of bin)
            #
            sbWres = self.subDict(self.bkgres,self.sbBins[sbWname])
            ys = [ sbWres["yW_crNJet_0b_lowDPhi"], sbWres["yTT_crNJet_0b_lowDPhi"], sbWres["yRest_crNJet_0b_lowDPhi_truth"] ]
            vys = [ sbWres["yW_Var_crNJet_0b_lowDPhi"], sbWres["yTT_Var_crNJet_0b_lowDPhi"], sbWres["yRest_Var_crNJet_0b_lowDPhi_truth"] ]
            fracErrs = relErrorsOnFractions(ys,vys)
            #self.c.addUncertainty(uncName,"lnN",group="yWtt")
            #self.c.specifyUncertainty(uncName,sbWnameS,"W",1.+fracErrs[0])
            #self.c.specifyUncertainty(uncName,sbWnameS,"tt",1.-fracErrs[1])
        # !*! need to change from error on yield to error on fraction since total normalization fluctuation
        #     already accounted for!!!
        # !*! should be correlated between MB SR and CR
        #
        ys = [ mbres["yW_srNJet_0b_lowDPhi"], mbres["yTT_srNJet_0b_lowDPhi"], \
                   mbres["yRest_srNJet_0b_lowDPhi_truth"],  mbres["yQCD_srNJet_0b_lowDPhi"] ]
        # temporary fix for QCD variance 
        vQCD = mbres["yQCD_Var_srNJet_0b_lowDPhi"]
        if isnan(vQCD):
            print "Replacing nan for yQCD_Var_srNJet_0b_lowDPhi in ",mbnameC
            vQCD =  mbres["yQCD_srNJet_0b_lowDPhi"]**2
        vys = [ mbres["yW_Var_srNJet_0b_lowDPhi"], mbres["yTT_Var_srNJet_0b_lowDPhi"], \
                   mbres["yRest_Var_srNJet_0b_lowDPhi_truth"],  vQCD ]
        fracErrs = relErrorsOnFractions(ys,vys)
        # fracErrs = [ ]
        # fracErrs.append(sqrt(mbres["yW_Var_srNJet_0b_lowDPhi"])/mbres["yW_srNJet_0b_lowDPhi"])
        # fracErrs.append(sqrt(mbres["yTT_Var_srNJet_0b_lowDPhi"])/mbres["yTT_srNJet_0b_lowDPhi"])
        #uncName = "yWtt" + mbnameC
        #self.c.addUncertainty(uncName,"lnN",group="yWtt")
        #self.c.specifyUncertainty(uncName,mbnameC,"W",1.+fracErrs[0])
        #self.c.specifyUncertainty(uncName,mbnameC,"tt",1.-fracErrs[1])
        assert not mbname in self.yWtts
        ytt = mbres["yTT_srNJet_0b_lowDPhi"]
        yW = mbres["yW_srNJet_0b_lowDPhi"]
        self.yWtts[mbname] = { "W" : yW, \
                               "tt" : ytt, \
                               "eW" : fracErrs[0], "ett" : -fracErrs[1] }
        # self.c.specifyUncertainty(uncName,mbnameS,"W",1.+fracErrs[0])
        # self.c.specifyUncertainty(uncName,mbnameS,"tt",1.-fracErrs[1])


      for mbname in mbBinNames:
        mbres = self.subDict(self.bkgres,self.mbBins[mbname])
        mbsigres = self.subDict(self.sigres,self.mbBins[mbname])["signals"][self.mglu][self.mlsp]
        #
        # low dPhi (CR)
        #
        mbnameC = mbname + "C"
        self.c.addBin(mbnameC,self.procNames,mbnameC)
        rDPhi = "lowDPhi"
        # observation
        #y_truth = mbres["yW_srNJet_0b_"+rDPhi+"_truth"] + \
        #    mbres["yTT_srNJet_0b_"+rDPhi+"_truth"] + \
        #    mbres["yRest_srNJet_0b_"+rDPhi+"_truth"] + \
        #    mbres["yQCD_srNJet_0b_"+rDPhi+"_truth"]
        self.c.specifyObservation(mbnameC,int(mbres["y_srNJet_0b_lowDPhi"]+0.5))
        # expectation
        self.c.specifyExpectation(mbnameC,"signal",mbsigres['yield_MB_CR']*xsecFactor)
        # self.c.specifyExpectation(mbnameC,"tt",mbres["yTT_srNJet_0b_"+rDPhi])
        # self.c.specifyExpectation(mbnameC,"W",mbres["yW_srNJet_0b_"+rDPhi])
        self.c.specifyExpectation(mbnameC,"tt",1.)
        self.c.specifyExpectation(mbnameC,"W",1.)
        ytt = mbres["yTT_srNJet_0b_"+rDPhi]
        yW = mbres["yW_srNJet_0b_"+rDPhi]
        #self.rateParamLines.append(self.rateParamValueLine(mbnameC,"tt",ytt))
        #self.rateParamLines.append(self.rateParamValueLine(mbnameC,"W",yW))
        self.paramLines.append(self.crFormulaLine(mbname,sbname,"tt",self.yWtts[mbname]))
        self.paramLines.append(self.crFormulaLine(mbname,sbname,"W",self.yWtts[mbname]))
        assert not mbnameC in self.yieldstt
        self.yieldstt[mbnameC] = ytt
        assert not mbnameC in self.yieldsW
        self.yieldsW[mbnameC] = yW
        self.c.specifyExpectation(mbnameC,"tt",1.)
        self.c.specifyExpectation(mbnameC,"W",1.)
        self.c.specifyExpectation(mbnameC,"other",mbres["yRest_srNJet_0b_"+rDPhi+"_truth"])
        self.c.specifyExpectation(mbnameC,"QCD",mbres["yQCD_srNJet_0b_"+rDPhi])
        #
        # high dPhi
        #
        mbnameS = mbname + "S"
        self.c.addBin(mbnameS,self.procNames,mbnameS)
        rDPhi = "highDPhi"
        # observation
        #y_truth = mbres["W_truth"] +  mbres["TT_truth"] + mbres["Rest_truth"]
        self.c.specifyObservation(mbnameS,int(mbres["y_srNJet_0b_highDPhi"]+0.5))
        # expectation
        self.c.specifyExpectation(mbnameS,"signal",mbsigres['yield_MB_SR']*xsecFactor)
        # self.c.specifyExpectation(mbnameS,"tt",mbres["TT_pred_final"])
        # self.c.specifyExpectation(mbnameS,"W",mbres["W_pred_final"])
        ytt = mbres["TT_pred_final"]
        yW = mbres["W_pred_final"]
        self.c.specifyExpectation(mbnameS,"tt",1.)
        self.c.specifyExpectation(mbnameS,"W",1.)
        self.rateParamLines.append(self.rateParamValueLine(mbnameS,"tt",ytt,comment=True))
        self.rateParamLines.append(self.rateParamValueLine(mbnameS,"W",yW,comment=True))
        assert not mbnameS in self.yieldstt
        self.yieldstt[mbnameS] = ytt
        assert not mbnameS in self.yieldsW
        self.yieldsW[mbnameS] = yW
        self.c.specifyExpectation(mbnameS,"other",mbres["Rest_truth"])
        self.c.specifyExpectation(mbnameS,"QCD",0.001)

      #
      # global uncertainties
      #
      # self.c.addUncertainty("worst","lnN")
      self.c.addUncertainty("lumi","lnN")
      self.c.addUncertainty("xsecOther","lnN",group="xsec")
      self.c.addUncertainty("xsecsFit","lnN",group="xsec")
      self.c.addUncertainty("trigger","lnN")
      # self.c.addUncertainty("scales","lnN")
      self.c.addUncertainty("isr","lnN")
      for bname in sbBinNames:
        sbname = bname + "S"
        sbsigres = self.subDict(self.sigres,self.sbBins[bname])["signals"][self.mglu][self.mlsp]
        self.c.specifyUncertainty("lumi",sbname,"signal",1.+sbsigres["syst_lumi"])
        #self.c.specifyUncertainty("lumi",sbname,"signal",1.027)
#        self.c.specifyUncertainty("sigSyst",sbname,"signal",1.20) # to be corrected!
#        self.c.specifyUncertainty("lumi",sbname,"other",1.+sbsigres["syst_lumi"])
        self.c.specifyUncertainty("trigger",sbname,"signal",1.+sbsigres["syst_trigger"])
        self.c.specifyUncertainty("isr",sbname,"signal",1+sbsigres["syst_ISR"])
        # self.c.specifyUncertainty("scales",sbname,"signal",1.+sbsigres["syst_Q2"])
        # apply small correction to 50% cross section for TTV fraction (to be scaled by 100%)
        self.c.specifyUncertainty("xsecOther",sbname,"other",1.55)
      for bname in sbBinNames:
        sbname = bname + "C"
        sbsigres = self.subDict(self.sigres,self.sbBins[bname])["signals"][self.mglu][self.mlsp]
        self.c.specifyUncertainty("lumi",sbname,"signal",1.+sbsigres["syst_lumi"])
        #self.c.specifyUncertainty("lumi",sbname,"signal",1.027)
        self.c.specifyUncertainty("trigger",sbname,"signal",1.+sbsigres["syst_trigger"])
        self.c.specifyUncertainty("isr",sbname,"signal",1+sbsigres["syst_ISR"])
        self.c.specifyUncertainty("xsecOther",sbname,"other",1.55)
        sbres = self.subDict(self.bkgres,self.sbBins[bname])
        xwtt = sbres["yW_crNJet_0b_lowDPhi"] + sbres["yTT_crNJet_0b_lowDPhi"]
        xoth = self.c.expectation[(sbname,"other")] + self.c.expectation[(sbname,"QCD")]
        self.c.specifyUncertainty("xsecsFit",sbname,"W",1.+xoth/(xwtt+xoth))
        self.c.specifyUncertainty("xsecsFit",sbname,"tt",1.+xoth/(xwtt+xoth))
      for bname in mbBinNames:
        for r in [ "C", "S" ]:
          mbname = bname + r
          mbsigres = self.subDict(self.sigres,self.mbBins[bname])["signals"][self.mglu][self.mlsp]
          self.c.specifyUncertainty("lumi",mbname,"signal",1.+mbsigres["syst_lumi"])
          #self.c.specifyUncertainty("lumi",mbname,"signal",1.027)
#          self.c.specifyUncertainty("sigSyst",mbname,"signal",1.20) # to be corrected!
          self.c.specifyUncertainty("lumi",mbname,"other",1.+mbsigres["syst_lumi"])
          #self.c.specifyUncertainty("lumi",mbname,"other",1.027)
          self.c.specifyUncertainty("trigger",mbname,"signal",1.+mbsigres["syst_trigger"])
          # self.c.specifyUncertainty("scales",mbname,"signal",1.+mbsigres["syst_Q2"])
          self.c.specifyUncertainty("isr",mbname,"signal",1+mbsigres["syst_ISR"])
          # apply small correction to 50% cross section for TTV fraction (to be scaled by 100%)
          self.c.specifyUncertainty("xsecOther",mbname,"other",1.55)
          if r=="C":
              mbres = self.subDict(self.bkgres,self.mbBins[bname])
              xwtt = mbres["yW_srNJet_0b_lowDPhi"] + mbres["yTT_srNJet_0b_lowDPhi"]
              xoth = self.c.expectation[(mbname,"other")] + self.c.expectation[(mbname,"QCD")]
              self.c.specifyUncertainty("xsecsFit",mbname,"W",1.+xoth/(xwtt+xoth))
              self.c.specifyUncertainty("xsecsFit",mbname,"tt",1.+xoth/(xwtt+xoth))
              
                                                        
      #
      # correlations between MB/SR and MB/CR or SB/SR
      #
      for mbname in mbBinNames:
        bname = mbname[2:]
        mbnameC = mbname + "C"
        mbnameS = mbname + "S"
        mbres = self.subDict(self.bkgres,self.mbBins[mbname])
        mbsigres = self.subDict(self.sigres,self.mbBins[mbname])["signals"][self.mglu][self.mlsp]

        sbWname = "J3" + bname
        sbWnameS = sbWname + "S"
        sbWresS = self.subDict(self.bkgres,self.sbBins[sbWname])

        sbttname = "J4" + bname
        sbttnameS = sbttname + "S"
        sbttresS = self.subDict(self.bkgres,self.sbBins[sbttname])
        #
        # correlation W regions: B and F / E and F
        #
        # uncName = "corrWBF" + mbname
        # self.c.addUncertainty(uncName,self.corrSystPdf,group="corr")
        # self.c.specifyUncertainty(uncName,"J3"+bname+"S","W",self.corrSystSize)
        # self.c.specifyUncertainty(uncName,mbnameS,"W",self.corrSystSize)
        # uncName = "corrWEF" + mbname
        # self.c.addUncertainty(uncName,self.corrSystPdf,group="corr")
        # self.c.specifyUncertainty(uncName,mbnameC,"W",self.corrSystSize)
        # self.c.specifyUncertainty(uncName,mbnameS,"W",self.corrSystSize)
        # kappaW = (self.yieldsW[mbnameS]/self.yieldsW[mbnameC])/(self.yieldsW["J3"+bname+"S"]/self.yieldsW["J3"+bname+"C"])
        kappaW = mbres["W_kappa"]
        self.paramLines.append(self.paramValueLine(mbnameS,"W",kappaW))
        # self.rateParamLines.append(self.srFormulaLine(mbname,"J3"+bname,"W"))
        self.rateParamLines.append(self.srFormulaLine(mbname,"J3"+bname,"W"))
        self.paramLines.append(self.paramValueLine1("yWtt"+mbname,0.,1.))
        #
        # correlation tt regions: D and F / E and F
        #
        # uncName = "corrTTDF" + mbname
        # self.c.addUncertainty(uncName,self.corrSystPdf,group="corr")
        # self.c.specifyUncertainty(uncName,"J4"+bname+"S","tt",self.corrSystSize)
        # self.c.specifyUncertainty(uncName,mbnameS,"tt",self.corrSystSize)
        # uncName = "corrTTEF" + mbname
        # self.c.addUncertainty(uncName,self.corrSystPdf,group="corr")
        # self.c.specifyUncertainty(uncName,mbnameC,"tt",self.corrSystSize)
        # self.c.specifyUncertainty(uncName,mbnameS,"tt",self.corrSystSize)
        # kappatt = (self.yieldstt[mbnameS]/self.yieldstt[mbnameC])/(self.yieldstt["J4"+bname+"S"]/self.yieldstt["J4"+bname+"C"])
        kappatt = mbres["TT_kappa"]*mbres["TT_rCS_fits_MC"]["k_0b/1b_btag"]
        self.paramLines.append(self.paramValueLine(mbnameS,"tt",kappatt))
        # self.rateParamLines.append(self.srFormulaLine(mbname,"J4"+bname,"tt"))
        self.rateParamLines.append(self.srFormulaLine(mbname,"J4"+bname,"tt"))

      #
      # other systematics on (total) prediction in MB/SR
      #
      for mbname in mbBinNames:
        bname = mbname[2:]
        mbnameC = mbname + "C"
        mbnameS = mbname + "S"
        mbres = self.subDict(self.bkgres,self.mbBins[mbname])
        mbsigres = self.subDict(self.sigres,self.mbBins[mbname])["signals"][self.mglu][self.mlsp]

        sbWname = "J3" + bname
        # sbWnameC = sbWnameBase + "C"
        # sbWresC = self.subDict(self.bkgres,self.sbBins[sbWnameC])
        sbWnameS = sbWname + "S"
        sbWresS = self.subDict(self.bkgres,self.sbBins[sbWname])

        sbttname = "J4" + bname
        # sbttnameC = sbttnameBase + "C"
        # sbttresC = self.subDict(self.bkgres,self.sbBins[sbttname])
        sbttnameS = sbttname + "S"
        sbttresS = self.subDict(self.bkgres,self.sbBins[sbttname])
        # uncertainty on RCS_W (e+mu)/mu
        uncName = "rcsWemu" + mbnameS
        self.c.addUncertainty(uncName,"lnN",group="rcs")
        self.c.specifyUncertainty(uncName,mbnameS,"W",1.+mbres["systematics"]["ratio_mu_elemu"])
        # rcs.addKappaVar(mbnameS,"W",mbres["systematics"]["ratio_mu_elemu"])
        # uncertainty on b tagging
        if not "btag" in self.c.uncertainties:
            self.c.addUncertainty("btag","lnN")
        self.c.specifyUncertainty("btag",mbnameS,"signal",1.+sqrt(mbsigres["syst_B"]**2+mbsigres["syst_light"]**2))
        self.c.specifyUncertainty("btag",mbnameS,"W",1.+mbres["systematics"]["btagSF"])
        self.c.specifyUncertainty("btag",mbnameS,"tt",1.+mbres["systematics"]["btagSF"])
        self.c.specifyUncertainty("btag",mbnameS,"other",1.+mbres["systematics"]["btagSF"])
        # uncertainty on top pt (!*! should rescale total rel. uncertainty for application on ttbar only)
        if not "topPt" in self.c.uncertainties:
            self.c.addUncertainty("topPt","lnN")
        self.c.specifyUncertainty("topPt",mbnameS,"W",1.+mbres["systematics"]["topPt"])
        self.c.specifyUncertainty("topPt",mbnameS,"tt",1.+mbres["systematics"]["topPt"])
        self.c.specifyUncertainty("topPt",mbnameS,"other",1.+mbres["systematics"]["topPt"])
        # uncertainty on lepton SFs
        if not "leptonSF" in self.c.uncertainties:
            self.c.addUncertainty("leptonSF","lnN")
        self.c.specifyUncertainty("leptonSF",mbnameS,"signal",1.+mbsigres["syst_lepton"])
        self.c.specifyUncertainty("leptonSF",mbnameS,"W",1.+mbres["systematics"]["lepSF"])
        self.c.specifyUncertainty("leptonSF",mbnameS,"tt",1.+mbres["systematics"]["lepSF"])
        self.c.specifyUncertainty("leptonSF",mbnameS,"other",1.+mbres["systematics"]["lepSF"])
        # stat uncertainty on kappaW, kappaTT and kappa_b
        # self.c.addUncertainty("kappaW"+mbnameS,"lnN",group="kappa")
        # self.c.specifyUncertainty("kappaW"+mbnameS,mbnameS,"W",1.+mbres["systematics"]["kappa_W"])
        self.addKappaVar(mbnameS,"W",mbres["systematics"]["kappa_W"])
        # self.c.addUncertainty("kappaTT"+mbnameS,"lnN",group="kappa")
        # self.c.specifyUncertainty("kappaTT"+mbnameS,mbnameS,"tt",1.+mbres["systematics"]["kappa_TT"])
        self.addKappaVar(mbnameS,"tt",mbres["systematics"]["kappa_TT"])
        # self.c.addUncertainty("kappab"+mbnameS,"lnN",group="kappa")
        # self.c.specifyUncertainty("kappab"+mbnameS,mbnameS,"tt",1.+mbres["systematics"]["kappa_b"])
        self.addKappaVar(mbnameS,"tt",mbres["systematics"]["kappa_b"])
        # Rcs systematics W and tt ("linear fit")
        uncName = "rcsW"
        if not uncName in self.c.uncertainties:
            self.c.addUncertainty(uncName,"lnN",group="rcs")
        self.c.specifyUncertainty(uncName,mbnameS,"W",1.+mbres["systematics"]["rcs_W"])
        #self.addKappaVars(mbnameS,"W",mbres["systematics"]["rcs_W"])
        uncName = "rcsTT"
        if not uncName in self.c.uncertainties:
            self.c.addUncertainty(uncName,"lnN",group="rcs")
        self.c.specifyUncertainty(uncName,mbnameS,"tt",1.+mbres["systematics"]["rcs_tt"])
        #self.addKappaVars(mbnameS,"tt",mbres["systematics"]["rcs_tt"])
        # QCD systematics
        self.c.addUncertainty("QCD"+mbnameS,"lnN")
        self.c.specifyUncertainty("QCD"+mbnameS,mbnameS,"W",1.+mbres["systematics"]["QCD"])
        self.c.specifyUncertainty("QCD"+mbnameS,mbnameS,"tt",1.+mbres["systematics"]["QCD"])
        self.c.specifyUncertainty("QCD"+mbnameS,mbnameS,"other",1.+mbres["systematics"]["QCD"])
        # dilepton
        uncName = "diLep"
        if not uncName in self.c.uncertainties:
            self.c.addUncertainty(uncName,"lnN")
        self.c.specifyUncertainty(uncName,mbnameS,"W",1.+mbres["systematics"]["dilep"])
        self.c.specifyUncertainty(uncName,mbnameS,"tt",1.+mbres["systematics"]["dilep"])
        self.c.specifyUncertainty(uncName,mbnameS,"other",1.+mbres["systematics"]["dilep"])
        # PU systematics
        if not "PU" in self.c.uncertainties:
            self.c.addUncertainty("PU","lnN")
        self.c.specifyUncertainty("PU",mbnameS,"signal",1.+mbsigres["syst_PU"])
        self.c.specifyUncertainty("PU",mbnameS,"W",1.+mbres["systematics"]["pileup"])
        self.c.specifyUncertainty("PU",mbnameS,"tt",1.+mbres["systematics"]["pileup"])
        self.c.specifyUncertainty("PU",mbnameS,"other",1.+mbres["systematics"]["pileup"])
        # Cross sections & W polarization
        if not "xsecW" in self.c.uncertainties:
            self.c.addUncertainty("xsecW","lnN",group="xsec")
        self.c.specifyUncertainty("xsecW",mbnameS,"W",1.+mbres["systematics"]["Wxsec"])
        self.c.specifyUncertainty("xsecW",mbnameS,"tt",1.+mbres["systematics"]["Wxsec"])
        self.c.specifyUncertainty("xsecW",mbnameS,"other",1.+mbres["systematics"]["Wxsec"])
        if not "xsecTT" in self.c.uncertainties:
            self.c.addUncertainty("xsecTT","lnN",group="xsec")
        self.c.specifyUncertainty("xsecTT",mbnameS,"W",1.+mbres["systematics"]["TTxsec"])
        self.c.specifyUncertainty("xsecTT",mbnameS,"tt",1.+mbres["systematics"]["TTxsec"])
        self.c.specifyUncertainty("xsecTT",mbnameS,"other",1.+mbres["systematics"]["TTxsec"])
        if not "WPol" in self.c.uncertainties:
            self.c.addUncertainty("WPol","lnN")
        self.c.specifyUncertainty("WPol",mbnameS,"W",1.+mbres["systematics"]["Wpol"])
        self.c.specifyUncertainty("WPol",mbnameS,"tt",1.+mbres["systematics"]["Wpol"])
        self.c.specifyUncertainty("WPol",mbnameS,"other",1.+mbres["systematics"]["Wpol"])
        # stat. uncertainty on signal efficiency
        uncName = "statSeff" + mbnameS
        self.c.addUncertainty(uncName,"lnN",group="statSeff")
        if mbsigres["yield_MB_SR"]>0.001:
            self.c.specifyUncertainty(uncName,mbnameS,"signal", \
                                          1+mbsigres["err_MB_SR"]/mbsigres["yield_MB_SR"])
        else:
            self.c.specifyUncertainty(uncName,mbnameS,"signal",1.20)
        ## trigger uncertainty on signal efficiency
        #uncName = "trigger"
        #if not "trigger" in self.c.uncertainties:
        #    self.c.addUncertainty("trigger","lnN")
        #self.c.specifyUncertainty("trigger",mbnameS,"signal",1.+mbsigres["syst_trigger"])
        # scale uncertainty on signal efficiency
        uncName = "scale"
        if not "scale" in self.c.uncertainties:
            self.c.addUncertainty("scale","lnN")
        self.c.specifyUncertainty("scale",mbnameS,"signal",1.+mbsigres["syst_Q2"])
        # ISR uncertainty on signal efficiency
        uncName = "isr"
        if not uncName in self.c.uncertainties:
            self.c.addUncertainty(uncName,"lnN")
        self.c.specifyUncertainty(uncName,mbnameS,"signal",1+mbsigres["syst_ISR"])
        # JEC uncertainty on signal efficiency
        uncName = "jec"
        if not uncName in self.c.uncertainties:
            self.c.addUncertainty(uncName,"lnN")
        self.c.specifyUncertainty(uncName,mbnameS,"signal",1+mbsigres["syst_JEC"])
        self.c.specifyUncertainty(uncName,mbnameS,"W",1+mbres["systematics"]["JEC"])
        self.c.specifyUncertainty(uncName,mbnameS,"tt",1+mbres["systematics"]["JEC"])
        self.c.specifyUncertainty(uncName,mbnameS,"other",1+mbres["systematics"]["JEC"])
        #self.addKappaVar(mbnameS,"tt",mbres["systematics"]["JEC"])
        #self.addKappaVar(mbnameS,"W",mbres["systematics"]["JEC"])
      #      # WORST CASE SYST
      #      uncName = "worst"+mbnameS
      #      self.c.addUncertainty(uncName,"lnN")
      #      self.c.specifyUncertainty(uncName,mbnameS,"W",1+worstCaseSyst[self.mbBins[mbname][0]][self.mbBins[mbname][1]][self.mbBins[mbname][2]])



      #
      # QCD uncertainties in CR / SB (!*! double counting?)
      #
      useAddQCD = False
      if useAddQCD:
          for sbname in sbBinNames:
            sbnameS = sbname + "S"
            sbres = self.subDict(self.bkgres,self.sbBins[sbname])
            self.c.addUncertainty("qcd"+sbnameS,"lnN")
            if sbname.startswith("J3"):
                self.c.specifyUncertainty("qcd"+sbnameS,sbnameS,"QCD",2.0)
            elif sbname.startswith("J4"):
                vQCD = sbres["yQCD_Var_crNJet_1b_highDPhi"]
                if isnan(vQCD):
                    print "Replacing nan for sbres yQCD_Var_crNJet_1b_highDPhi in ",sbnameS
                    vQCD =  sbres["yQCD_crNJet_1b_highDPhi"]**2
                print "QCD",sbname,sbres["yQCD_crNJet_1b_highDPhi"],sbres["yQCD_Var_crNJet_1b_highDPhi"]
                self.c.specifyUncertainty("qcd"+sbnameS,sbnameS,"QCD", \
                                              relErrForLimit(sbres["yQCD_crNJet_1b_highDPhi"],vQCD))
          for mbname in mbBinNames:
            mbnameS = mbname + "C"
            mbres = self.subDict(self.bkgres,self.mbBins[mbname])
            self.c.addUncertainty("qcd"+mbnameC,"lnN")
            # temporary fix for QCD variance 
            vQCD = mbres["yQCD_Var_srNJet_0b_lowDPhi"]
            if isnan(vQCD):
                vQCD =  mbres["yQCD_srNJet_0b_lowDPhi"]**2
            self.c.specifyUncertainty("qcd"+mbnameC,mbnameC,"QCD", \
                                          relErrForLimit(sbres["yQCD_srNJet_0b_lowDPhi"],vQCD))

          
      txtname = os.path.join(self.dir,self.name+".txt")
      logname = os.path.join(self.dir,self.name+".log")
      outname = os.path.join(self.dir,self.name+".out")
      if os.path.exists(txtname) or os.path.exists(logname) or os.path.exists(outname):
          if not self.force:
              print "Output file(s) exist for ",self.name," - skipping"
              return
          
      #
      # comments
      #
      if xsecFactor!=1:
          self.c.addExtraLine("#")
          self.c.addExtraLine("# ************************")
          self.c.addExtraLine("# Signal rates have been scaled by "+str(xsecFactor)+" !!!!!!")
          self.c.addExtraLine("#")

      self.c.addExtraLine("")
      for l in sorted(self.rateParamLines):
          self.c.addExtraLine(l+"")

      self.c.addExtraLine("")
      for l in sorted(self.paramLines):
          if l.startswith("k"):
              k = l.split()[0]
              kv = float(l.split()[2]
              l += "{0:8.3f}".format(sqrt(self.kappaVars[k])*kv)
          self.c.addExtraLine(l+"")

      self.c.writeToFile(txtname)

#      txt.write("#\n")
#      txt.write("# List of uncertainties\n")
#      txt.write("#\n")
#      txt.write("# corrWBFJxLyHzDu ... correlation W: SB/highDPhi with MB/highDPhi\n")
#      txt.write("# corrWEFJxLyHzDu ... correlation W: MB/lowDPhi with MB/highDPhi\n")
#      txt.write("# corrTTDFJxLyHzDu .. correlation tt: SB/highDPhi with MB/highDPhi\n")
#      txt.write("# corrTTEFJxLyHzDu .. correlation tt: MB/lowDPhi with MB/highDPhi\n")
#      txt.write("# yWttJxLyHzDuC ..... anti-correlated W/tt fraction fit systematics in MB CR\n")
#      txt.write("# yQCDJxLyHzDuC ..... uncertainty QCD estimate in MB CR\n")
#      txt.write("# statJ[34]LyHzDuC .. stat. uncertainty from yield in SB lowDPhi \n")
#      txt.write("# yWttJ[34]LyHzDuS .. anti-correlated W/tt fraction fit systematics in W SB highDPhi\n")
#      txt.write("# yWttJ[34]LyHzDuC ?? anti-correlated W/tt fraction fit systematics in W SB lowDPhi\n")
#      txt.write("# lumi .............. luminosity\n")
#      txt.write("# sigSyst ........... approximated total signal systematics\n")

      for n in self.yWtts:
          print n,self.yWtts[n]

      if self.runLimit:
          stdout = sys.stdout
          sys.stdout = open(logname,"w")
          opts = ""
          if self.runBlind:
              opts = "--run blind"
          res = self.c.calcLimit(options=opts,logfile=outname)
          if xsecFactor!=1:
              for k in res:
                  res[k] *= xsecFactor
          print 'Result ',mbBinNames[0]," , ",self.signal["name"],self.signal["mglu"],self.signal["mlsp"]," : ",res
          sys.stdout.close()
          sys.stdout = stdout
          return res

