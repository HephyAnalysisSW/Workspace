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
    
class CalcSingleLimit:

    def __init__(self,bkgres,sbBinNames,sbBins,mbBinNames,mbBins,sigres,signal):

        self.name = "calc_single_limit"
        self.runLimit = False
        self.runBlind = False
        self.force = False
        self.dir = "."
        self.useBins = range(len(mbBinNames))
        self.corrSystSize = 1000.0
        self.corrSystPdf = "lnN"
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

    def subDict(self,d,bins):
        return d[bins[0]][bins[1]][bins[2]]

    def sigSubDict(self,d):
        return d["signals"][self.mglu][self.mlsp]

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
      bkgerrs = { }
      bkgerrs['J5L1H3D2'] = 2.74
      bkgerrs[ 'J5L2H3D2'] = 2.13
      bkgerrs[ 'J5L3H3D2'] = 2.03
      bkgerrs[ 'J6L1H1D2'] = 1.25
      bkgerrs[ 'J6L1H4D2'] = 1.47
      bkgerrs[ 'J6L2H1D2'] = 1.12
      bkgerrs[ 'J6L2H4D2'] = 0.72
      bkgerrs[ 'J6L3H2D1'] = 0.90
      bkgerrs[ 'J6L3H5D1'] = 1.03
      bkgerrs[ 'J8L1H1D2'] = 0.20
      bkgerrs[ 'J8L1H4D2'] = 0.50
      bkgerrs[ 'J8L2H3D1'] = 0.24
      bkgerrs[ 'J8L3H3D1'] = 0.23


      #
      # scale signal cross section for low masses
      #
      xsecFactor = 1
      if self.mglu<1000:
          xsecFactor = 0.1
      #
      # bin definition; observed and expected counts
      #
      for mbname in mbBinNames:
        mbres = self.subDict(self.bkgres,self.mbBins[mbname])
        mbsigres = self.subDict(self.sigres,self.mbBins[mbname])["signals"][self.mglu][self.mlsp]
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
        self.c.specifyExpectation(mbnameS,"tt",mbres["TT_pred_final"])
        self.c.specifyExpectation(mbnameS,"W",mbres["W_pred_final"])
        self.c.specifyExpectation(mbnameS,"other",mbres["Rest_truth"])
        self.c.specifyExpectation(mbnameS,"QCD",0.001)
      #
      # global uncertainties
      #
      self.c.addUncertainty("lumi","lnN")
      self.c.addUncertainty("xsecOther","lnN",group="xsec")
      self.c.addUncertainty("trigger","lnN")
      for bname in mbBinNames:
        for r in [ "S" ]:
          mbname = bname + r
          mbsigres = self.subDict(self.sigres,self.mbBins[bname])["signals"][self.mglu][self.mlsp]
          self.c.specifyUncertainty("lumi",mbname,"signal",1.+mbsigres["syst_lumi"])
          self.c.specifyUncertainty("lumi",mbname,"other",1.+mbsigres["syst_lumi"])
          self.c.specifyUncertainty("trigger",mbname,"signal",1.+mbsigres["syst_trigger"])
          self.c.specifyUncertainty("xsecOther",mbname,"other",1.55)
      #
      # other systematics on (total) prediction in MB/SR
      #
      for mbname in mbBinNames:
        bname = mbname[2:]
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
        # uncertainty on b tagging
        if not "btag" in self.c.uncertainties:
            self.c.addUncertainty("btag","lnN")
            self.c.addUncertainty("btagW","lnN")
            self.c.addUncertainty("btagTT","lnN")
            self.c.addUncertainty("btagOth","lnN")
        self.c.specifyUncertainty("btag",mbnameS,"signal",1.+sqrt(mbsigres["syst_B"]**2+mbsigres["syst_light"]**2))
        self.c.specifyUncertainty("btagW",mbnameS,"W",1.+mbres["systematics"]["btagSF"])
        self.c.specifyUncertainty("btagTT",mbnameS,"tt",1.+mbres["systematics"]["btagSF"])
        self.c.specifyUncertainty("btagOth",mbnameS,"other",1.+mbres["systematics"]["btagSF"])
        # uncertainty on top pt (!*! should rescale total rel. uncertainty for application on ttbar only)
        if not "topPt" in self.c.uncertainties:
            self.c.addUncertainty("topPtW","lnN")
            self.c.addUncertainty("topPtTT","lnN")
            self.c.addUncertainty("topPtOth","lnN")
        self.c.specifyUncertainty("topPtW",mbnameS,"W",1.+mbres["systematics"]["topPt"])
        self.c.specifyUncertainty("topPtTT",mbnameS,"tt",1.+mbres["systematics"]["topPt"])
        self.c.specifyUncertainty("topPtOth",mbnameS,"other",1.+mbres["systematics"]["topPt"])
        # uncertainty on lepton SFs
        if not "leptonSF" in self.c.uncertainties:
            self.c.addUncertainty("leptonSF","lnN")
            self.c.addUncertainty("leptonSFW","lnN")
            self.c.addUncertainty("leptonSFTT","lnN")
            self.c.addUncertainty("leptonSFOth","lnN")
        self.c.specifyUncertainty("leptonSF",mbnameS,"signal",1.+mbsigres["syst_lepton"])
        self.c.specifyUncertainty("leptonSFW",mbnameS,"W",1.+mbres["systematics"]["lepSF"])
        self.c.specifyUncertainty("leptonSFTT",mbnameS,"tt",1.+mbres["systematics"]["lepSF"])
        self.c.specifyUncertainty("leptonSFOth",mbnameS,"other",1.+mbres["systematics"]["lepSF"])
        # stat uncertainty on kappaW, kappaTT and kappa_b
        self.c.addUncertainty("kappaW"+mbnameS,"lnN",group="kappa")
        self.c.specifyUncertainty("kappaW"+mbnameS,mbnameS,"W",1.+mbres["systematics"]["kappa_W"])
        self.c.addUncertainty("kappaTT"+mbnameS,"lnN",group="kappa")
        self.c.specifyUncertainty("kappaTT"+mbnameS,mbnameS,"tt",1.+mbres["systematics"]["kappa_TT"])
        self.c.addUncertainty("kappab"+mbnameS,"lnN",group="kappa")
        self.c.specifyUncertainty("kappab"+mbnameS,mbnameS,"tt",1.+mbres["systematics"]["kappa_b"])
        # Rcs systematics W and tt ("linear fit")
        uncName = "rcsW"
        if not uncName in self.c.uncertainties:
            self.c.addUncertainty(uncName,"lnN",group="rcs")
        self.c.specifyUncertainty(uncName,mbnameS,"W",1.+mbres["systematics"]["rcs_W"])
        uncName = "rcsTT"
        if not uncName in self.c.uncertainties:
            self.c.addUncertainty(uncName,"lnN",group="rcs")
        self.c.specifyUncertainty(uncName,mbnameS,"tt",1.+mbres["systematics"]["rcs_tt"])
        # QCD systematics
        self.c.addUncertainty("QCDW"+mbnameS,"lnN")
        self.c.addUncertainty("QCDTT"+mbnameS,"lnN")
        self.c.addUncertainty("QCDOth"+mbnameS,"lnN")
        self.c.specifyUncertainty("QCDW"+mbnameS,mbnameS,"W",1.+mbres["systematics"]["QCD"])
        self.c.specifyUncertainty("QCDTT"+mbnameS,mbnameS,"tt",1.+mbres["systematics"]["QCD"])
        self.c.specifyUncertainty("QCDOth"+mbnameS,mbnameS,"other",1.+mbres["systematics"]["QCD"])
        # dilepton
        uncName = "diLep"
        if not uncName in self.c.uncertainties:
            self.c.addUncertainty(uncName+"W","lnN")
            self.c.addUncertainty(uncName+"TT","lnN")
            self.c.addUncertainty(uncName+"Oth","lnN")
        self.c.specifyUncertainty(uncName+"W",mbnameS,"W",1.+mbres["systematics"]["dilep"])
        self.c.specifyUncertainty(uncName+"TT",mbnameS,"tt",1.+mbres["systematics"]["dilep"])
        self.c.specifyUncertainty(uncName+"Oth",mbnameS,"other",1.+mbres["systematics"]["dilep"])
        # PU systematics
        if not "PU" in self.c.uncertainties:
            self.c.addUncertainty("PU","lnN")
            self.c.addUncertainty("PUW","lnN")
            self.c.addUncertainty("PUTT","lnN")
            self.c.addUncertainty("PUOth","lnN")
        self.c.specifyUncertainty("PU",mbnameS,"signal",1.+mbsigres["syst_PU"])
        self.c.specifyUncertainty("PUW",mbnameS,"W",1.+mbres["systematics"]["pileup"])
        self.c.specifyUncertainty("PUTT",mbnameS,"tt",1.+mbres["systematics"]["pileup"])
        self.c.specifyUncertainty("PUOth",mbnameS,"other",1.+mbres["systematics"]["pileup"])
        # Cross sections & W polarization
        if not "xsecW" in self.c.uncertainties:
            self.c.addUncertainty("xsecWW","lnN",group="xsec")
            self.c.addUncertainty("xsecWTT","lnN",group="xsec")
            self.c.addUncertainty("xsecWOth","lnN",group="xsec")
        self.c.specifyUncertainty("xsecWW",mbnameS,"W",1.+mbres["systematics"]["Wxsec"])
        self.c.specifyUncertainty("xsecWTT",mbnameS,"tt",1.+mbres["systematics"]["Wxsec"])
        self.c.specifyUncertainty("xsecWOth",mbnameS,"other",1.+mbres["systematics"]["Wxsec"])
        if not "xsecTT" in self.c.uncertainties:
            self.c.addUncertainty("xsecTTW","lnN",group="xsec")
            self.c.addUncertainty("xsecTTTT","lnN",group="xsec")
            self.c.addUncertainty("xsecTTOth","lnN",group="xsec")
        self.c.specifyUncertainty("xsecTTW",mbnameS,"W",1.+mbres["systematics"]["TTxsec"])
        self.c.specifyUncertainty("xsecTTTT",mbnameS,"tt",1.+mbres["systematics"]["TTxsec"])
        self.c.specifyUncertainty("xsecTTOth",mbnameS,"other",1.+mbres["systematics"]["TTxsec"])
        if not "WPol" in self.c.uncertainties:
            self.c.addUncertainty("WPolW","lnN")
            self.c.addUncertainty("WPolTT","lnN")
            self.c.addUncertainty("WPolOther","lnN")
        self.c.specifyUncertainty("WPolW",mbnameS,"W",1.+mbres["systematics"]["Wpol"])
        self.c.specifyUncertainty("WPolTT",mbnameS,"tt",1.+mbres["systematics"]["Wpol"])
        self.c.specifyUncertainty("WPolOth",mbnameS,"other",1.+mbres["systematics"]["Wpol"])
        # 
        uncName = "wStat" + mbnameS
        self.c.addUncertainty(uncName,"lnN",group="stat")
        self.c.specifyUncertainty(uncName,mbnameS,"W",
                                  1+mbres["W_pred_final_err"]/mbres["W_pred_final"])
        uncName = "ttStat" + mbnameS
        self.c.addUncertainty(uncName,"lnN",group="stat")
        self.c.specifyUncertainty(uncName,mbnameS,"tt",
                                  1+mbres["TT_pred_final_err"]/mbres["TT_pred_final"])
        # stat. uncertainty on signal efficiency
        uncName = "statSeff" + mbnameS
        self.c.addUncertainty(uncName,"lnN",group="statSeff")
        if mbsigres["yield_MB_SR"]>0.001:
            self.c.specifyUncertainty(uncName,mbnameS,"signal", \
                                          1+mbsigres["stat_err_MB_SR"]/mbsigres["yield_MB_SR"])
        else:
            self.c.specifyUncertainty(uncName,mbnameS,"signal",1.20)
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
            self.c.addUncertainty(uncName+"W","lnN")
            self.c.addUncertainty(uncName+"TT","lnN")
            self.c.addUncertainty(uncName+"Oth","lnN")
        self.c.specifyUncertainty(uncName,mbnameS,"signal",1+mbsigres["syst_JEC"])
        self.c.specifyUncertainty(uncName+"W",mbnameS,"W",1+mbres["systematics"]["JEC"])
        self.c.specifyUncertainty(uncName+"TT",mbnameS,"tt",1+mbres["systematics"]["JEC"])
        self.c.specifyUncertainty(uncName+"Oth",mbnameS,"other",1+mbres["systematics"]["JEC"])
          
      txtname = os.path.join(self.dir,self.name+".txt")
      logname = os.path.join(self.dir,self.name+".log")
      outname = os.path.join(self.dir,self.name+".out")
      if os.path.exists(txtname) or os.path.exists(logname) or os.path.exists(outname):
          if not self.force:
              print "Output file(s) exist for ",self.name," - skipping"
              return
          
      self.c.writeToFile(txtname)

      #
      # sums
      #
      for mbname in mbBinNames:
          mbnameS = mbname + "S"
          totobs = 0.
          totsig = 0.
          totbkg = 0.
          totobs = self.c.observation[mbnameS]
          bkgexps = { }
          for k in self.c.expectation:
              b,p = k
              if b!=mbnameS:
                  continue
              if p=="signal":
                  totsig += self.c.expectation[k]
              else:
                  totbkg += self.c.expectation[k]
                  assert not p in bkgexps
                  bkgexps[p] = self.c.expectation[k]
          bkgnames = sorted(bkgexps.keys())
          nbkg = len(bkgnames)
          vec = ROOT.TVectorD(nbkg)
          vec *= 0
          cov = ROOT.TMatrixDSym(nbkg)
          cov *= 0
          for i,p in enumerate(bkgnames):
              vec[i] = bkgexps[p]
#              print i,vec[i]
          for c in self.c.uncertainties:
              covc = ROOT.TMatrixDSym(nbkg)
              covc *= 0
              for i,p in enumerate(bkgnames):
                  key = (c,mbnameS,p)
                  if key in self.c.uncertaintyVal:
                      covc[i][i] += (1-self.c.uncertaintyVal[key])**2
#                      print "{0:15s} {1:10s} {2:5s} {3:5.3f}".format(c,mbnameS,p,(1-self.c.uncertaintyVal[key]))
#                  else:
#                      print "No such key {0:15s} {1:10s} {2:5s}".format(c,mbnameS,p)
              cov += covc
#          for i in range(nbkg):
#              for j in range(nbkg):
#                  if i!=j:
#                      vi = cov[i][i]
#                      vj = cov[j][j]
#                      cov[i][j] = sqrt(vi*vj)
#          for i in range(nbkg):
#              print i,bkgnames[i],sqrt(cov[i][i])
          toterr = sqrt(cov.Similarity(vec))
          line = "Bin {0:10s}:".format(mbnameS)
          line += "  obs, sig, bkg = {0:5d} {1:6.2f} {2:6.2f} +- {3:5.2f}".format(totobs,totsig,totbkg,toterr)
          print line
                  
                      
      #
      # comments
      #
#       txt = open(txtname,"a")
#       if xsecFactor!=1:
#           txt.write("#\n")
#           txt.write("# ************************\n")
#           txt.write("# Signal rates have been scaled by "+str(xsecFactor)+" !!!!!!\n")
#           txt.write("#\n")
#       txt.write("#\n")
#       txt.write("# List of uncertainties\n")
#       txt.write("#\n")
#       txt.write("# corrWBFJxLyHzDu ... correlation W: SB/highDPhi with MB/highDPhi\n")
#       txt.write("# corrWEFJxLyHzDu ... correlation W: MB/lowDPhi with MB/highDPhi\n")
#       txt.write("# corrTTDFJxLyHzDu .. correlation tt: SB/highDPhi with MB/highDPhi\n")
#       txt.write("# corrTTEFJxLyHzDu .. correlation tt: MB/lowDPhi with MB/highDPhi\n")
#       txt.write("# yWttJxLyHzDuC ..... anti-correlated W/tt fraction fit systematics in MB CR\n")
#       txt.write("# yQCDJxLyHzDuC ..... uncertainty QCD estimate in MB CR\n")
#       txt.write("# statJ[34]LyHzDuC .. stat. uncertainty from yield in SB lowDPhi \n")
#       txt.write("# yWttJ[34]LyHzDuS .. anti-correlated W/tt fraction fit systematics in W SB highDPhi\n")
#       txt.write("# yWttJ[34]LyHzDuC ?? anti-correlated W/tt fraction fit systematics in W SB lowDPhi\n")
#       txt.write("# lumi .............. luminosity\n")
#       txt.write("# sigSyst ........... approximated total signal systematics\n")
#       txt.close()

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

