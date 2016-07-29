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
        self.corrSystSize = 100.0
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

        self.totalUncertainties = { }
        self.totalPredictions = { }


    def specifyExpectation(self,bin,proc,value):
        self.c.specifyExpectation(bin,proc,value)
        if proc=="signal":
            return
        if not bin in self.totalPredictions:
            self.totalPredictions[bin] = { }
        if not proc in self.totalPredictions[bin]:
            self.totalPredictions[bin][proc] = 0.
        self.totalPredictions[bin][proc] += value
            
    def specifyUncertainty(self,name,bin,proc,value):
        self.c.specifyUncertainty(name,bin,proc,value)
        if proc=="signal":
            return
        if not bin in self.totalUncertainties:
            self.totalUncertainties[bin] = { }
        if not proc in self.totalUncertainties[bin]:
            self.totalUncertainties[bin][proc] = 0.
        rate = self.c.expectation[(bin,proc)]
        if self.c.uncertaintyString[name].startswith("gmN"):
            fields = self.c.uncertaintyString[name].split()
            assert len(fields)==2
            n = int(fields[1])
            unc = 1./sqrt(n)
        else:
            unc = value - 1.
        tot = self.totalUncertainties[bin][proc]**2 + unc**2
        self.totalUncertainties[bin][proc] = sqrt(tot)
                
        
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
        sbnameS = sbname + "S"
        sbres = self.subDict(self.bkgres,self.sbBins[sbname])
        r = "S"
        rDPhi = "low" if r=="C" else "high"
        rDPhi += "DPhi"
        # calculate missing numbers for both low and high dPhi
        # yield (W) = observed - estimated tt # others are neglected in yield
        wYield = sbres["y_crNJet_0b_lowDPhi"] - sbres["yTT_crNJet_0b_lowDPhi"] - \
            sbres["yRest_crNJet_0b_lowDPhi_truth"]
        sbres["yW_crNJet_0b_lowDPhi"] = wYield
        wYield = sbres["y_crNJet_0b_highDPhi"] - sbres["yTT_crNJet_0b_highDPhi"] - \
            sbres["yRest_crNJet_0b_highDPhi_truth"]
        sbres["yW_crNJet_0b_highDPhi"] = wYield
        # error on wYield
        # yield (W) = observed - estimated tt # others are neglected in yield
        wVar = sbres["y_Var_crNJet_0b_lowDPhi"] + sbres["yTT_Var_crNJet_0b_lowDPhi"] + sbres["yRest_Var_crNJet_0b_lowDPhi_truth"]
        sbres["yW_Var_crNJet_0b_lowDPhi"] = wVar
        wVar = sbres["y_Var_crNJet_0b_highDPhi"] + sbres["yTT_Var_crNJet_0b_highDPhi"] + sbres["yRest_Var_crNJet_0b_highDPhi_truth"]
        sbres["yW_Var_crNJet_0b_highDPhi"] = wVar

      for mbname in mbBinNames:
        mbres = self.subDict(self.bkgres,self.mbBins[mbname])
        self.mbsigres = self.subDict(self.sigres,self.mbBins[mbname])
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
        self.specifyExpectation(mbnameS,"signal",self.sigSubDict(self.mbsigres)['yield_MB_SR']*xsecFactor)
        self.specifyExpectation(mbnameS,"tt",mbres["TT_pred_final"])
        self.specifyExpectation(mbnameS,"W",mbres["W_pred_final"])
        self.specifyExpectation(mbnameS,"other",mbres["Rest_truth"])
        self.specifyExpectation(mbnameS,"QCD",0.001)

      #
      # global uncertainties
      #
      # self.c.addUncertainty("worst","lnN")
      self.c.addUncertainty("btag","lnN")
      self.c.addUncertainty("lumi","lnN")
      self.c.addUncertainty("sigSyst","lnN")
      self.c.addUncertainty("xsecOther","lnN")
      for bname in mbBinNames:
        for r in [ "S" ]:
          mbname = bname + r
          self.specifyUncertainty("lumi",mbname,"signal",1.046)
          self.specifyUncertainty("sigSyst",mbname,"signal",1.20) # to be corrected!
          self.specifyUncertainty("lumi",mbname,"other",1.046)
          self.specifyUncertainty("xsecOther",mbname,"other",1.50)
      #
      # correlations between MB/SR and MB/CR or SB/SR
      #
      for sbname in sbBinNames:
          bname = sbname[2:]
          sbnameS = sbname + "S"
          sbres = self.subDict(self.bkgres,self.sbBins[sbname])

          if sbname.startswith("J3"):
              uncName = "corrW"+sbnameS
              pName = "W"
              ysb = sbres["yW_crNJet_0b_highDPhi"]
              eysb = sqrt(sbres["yW_Var_crNJet_0b_highDPhi"])/sbres["yW_crNJet_0b_highDPhi"]
          elif sbname.startswith("J4"):
              uncName = "corrTT"+sbnameS
              pName = "tt"
              ysb = sbres["y_crNJet_1b_highDPhi"] - sbres["yQCD_crNJet_1b_highDPhi"]
              eysb = sqrt(sbres["y_Var_crNJet_1b_highDPhi"])/ysb
          xequ = 1./eysb**2
          nequ = int(1./eysb**2+0.5)
          nequ = max(nequ,1)
          self.c.addUncertainty(uncName,"gmN",nequ)

          for mbname in mbBinNames:
              if not mbname[2:]==bname:
                  continue
              mbnameS = mbname + "S"
              mbres = self.subDict(self.bkgres,self.mbBins[mbname])
              try:
                  self.specifyUncertainty(uncName,mbnameS,pName, \
                                              self.c.expectation[(mbnameS,pName)]/xequ)
              except:
                  print uncName,mbnameS,pName,self.c.expectation[(mbnameS,pName)],nequ,eysb
                  raise

      for mbname in mbBinNames:
          bname = mbname[2:]
          mbnameC = mbname + "C"
          mbnameS = mbname + "S"
          mbres = self.subDict(self.bkgres,self.mbBins[mbname])

          uncName = "corrW" + mbnameS
          yW = mbres["yW_srNJet_0b_lowDPhi"]
          eyW = sqrt(mbres["yW_Var_srNJet_0b_lowDPhi"])/yW
          self.c.addUncertainty(uncName,"lnN")
          self.specifyUncertainty(uncName,mbnameS,"W",1+eyW)
#          self.c.addUncertainty(uncName,"gmN",int(yW+0.5))
#          self.specifyUncertainty(uncName,mbnameS,"W", \
#                                        self.c.expectation[(mbnameS,"W")]/int(yW+0.5))
          uncName = "corrTT" + mbnameS
          yTT = mbres["yTT_srNJet_0b_lowDPhi"]
          eyTT = sqrt(mbres["yTT_Var_srNJet_0b_lowDPhi"])/yTT
          self.c.addUncertainty(uncName,"lnN")
          self.specifyUncertainty(uncName,mbnameS,"tt",1.+1./sqrt(yTT))
#          self.c.addUncertainty(uncName,"gmN",int(yTT+0.5))
#          self.specifyUncertainty(uncName,mbnameS,"tt", \
#                                        self.c.expectation[(mbnameS,"tt")]/int(yTT+0.5))
              
        
      #
      # other systematics on (total) prediction in MB/SR
      #
      for mbname in mbBinNames:
        bname = mbname[2:]
        mbnameS = mbname + "S"
        mbres = self.subDict(self.bkgres,self.mbBins[mbname])
        self.mbsigres = self.subDict(self.sigres,self.mbBins[mbname])

        # uncertainty on RCS_W (e+mu)/mu
        uncName = "rcsWemu" + mbnameS
        self.c.addUncertainty(uncName,"lnN")
        self.specifyUncertainty(uncName,mbnameS,"W",1.+mbres["systematics"]["ratio_mu_elemu"])
        # uncertainty on b tagging
        if not "btag" in self.c.uncertainties:
            self.c.addUncertainty("btag","lnN")
        self.specifyUncertainty("btag",mbnameS,"W",1.+mbres["systematics"]["btagSF"])
        self.specifyUncertainty("btag",mbnameS,"tt",1.+mbres["systematics"]["btagSF"])
        self.specifyUncertainty("btag",mbnameS,"other",1.+mbres["systematics"]["btagSF"])
        # uncertainty on top pt (!*! should rescale total rel. uncertainty for application on ttbar only)
        if not "topPt" in self.c.uncertainties:
            self.c.addUncertainty("topPt","lnN")
        self.specifyUncertainty("topPt",mbnameS,"W",1.+mbres["systematics"]["topPt"])
        self.specifyUncertainty("topPt",mbnameS,"tt",1.+mbres["systematics"]["topPt"])
        self.specifyUncertainty("topPt",mbnameS,"other",1.+mbres["systematics"]["topPt"])
        # uncertainty on lepton SFs
        if not "leptonSF" in self.c.uncertainties:
            self.c.addUncertainty("leptonSF","lnN")
        self.specifyUncertainty("leptonSF",mbnameS,"signal",1.+mbres["systematics"]["lepSF"])
        self.specifyUncertainty("leptonSF",mbnameS,"W",1.+mbres["systematics"]["lepSF"])
        self.specifyUncertainty("leptonSF",mbnameS,"tt",1.+mbres["systematics"]["lepSF"])
        self.specifyUncertainty("leptonSF",mbnameS,"other",1.+mbres["systematics"]["lepSF"])
        # stat uncertainty on kappaW, kappaTT and kappa_b
        self.c.addUncertainty("kappaW"+mbnameS,"lnN")
        self.specifyUncertainty("kappaW"+mbnameS,mbnameS,"W",1.+mbres["systematics"]["kappa_W"])
        self.c.addUncertainty("kappaTT"+mbnameS,"lnN")
        self.specifyUncertainty("kappaTT"+mbnameS,mbnameS,"tt",1.+mbres["systematics"]["kappa_TT"])
        self.c.addUncertainty("kappab"+mbnameS,"lnN")
        self.specifyUncertainty("kappab"+mbnameS,mbnameS,"tt",1.+mbres["systematics"]["kappa_b"])
        # Rcs systematics W and tt ("linear fit")
        self.c.addUncertainty("rcsW"+mbnameS,"lnN")
        self.specifyUncertainty("rcsW"+mbnameS,mbnameS,"W",1.+mbres["systematics"]["rcs_W"])
        self.c.addUncertainty("rcsTT"+mbnameS,"lnN")
        self.specifyUncertainty("rcsTT"+mbnameS,mbnameS,"tt",1.+mbres["systematics"]["rcs_tt"])
        # QCD systematics
        self.c.addUncertainty("QCD"+mbnameS,"lnN")
        self.specifyUncertainty("QCD"+mbnameS,mbnameS,"W",1.+mbres["systematics"]["QCD"])
        self.specifyUncertainty("QCD"+mbnameS,mbnameS,"tt",1.+mbres["systematics"]["QCD"])
        self.specifyUncertainty("QCD"+mbnameS,mbnameS,"other",1.+mbres["systematics"]["QCD"])
        # dilepton
        self.c.addUncertainty("DiLep"+mbnameS,"lnN")
        self.specifyUncertainty("DiLep"+mbnameS,mbnameS,"W",1.+mbres["systematics"]["dilep"])
        self.specifyUncertainty("DiLep"+mbnameS,mbnameS,"tt",1.+mbres["systematics"]["dilep"])
        self.specifyUncertainty("DiLep"+mbnameS,mbnameS,"other",1.+mbres["systematics"]["dilep"])
        # PU systematics
        if not "PU" in self.c.uncertainties:
            self.c.addUncertainty("PU","lnN")
        self.specifyUncertainty("PU",mbnameS,"W",1.+mbres["systematics"]["pileup"])
        self.specifyUncertainty("PU",mbnameS,"tt",1.+mbres["systematics"]["pileup"])
        self.specifyUncertainty("PU",mbnameS,"other",1.+mbres["systematics"]["pileup"])
        # Cross sections & W polarization
        if not "xsecW" in self.c.uncertainties:
            self.c.addUncertainty("xsecW","lnN")
        self.specifyUncertainty("xsecW",mbnameS,"W",1.+mbres["systematics"]["Wxsec"])
        self.specifyUncertainty("xsecW",mbnameS,"tt",1.+mbres["systematics"]["Wxsec"])
        self.specifyUncertainty("xsecW",mbnameS,"other",1.+mbres["systematics"]["Wxsec"])
        if not "xsecTT" in self.c.uncertainties:
            self.c.addUncertainty("xsecTT","lnN")
        self.specifyUncertainty("xsecTT",mbnameS,"W",1.+mbres["systematics"]["TTxsec"])
        self.specifyUncertainty("xsecTT",mbnameS,"tt",1.+mbres["systematics"]["TTxsec"])
        self.specifyUncertainty("xsecTT",mbnameS,"other",1.+mbres["systematics"]["TTxsec"])
        if not "WPol" in self.c.uncertainties:
            self.c.addUncertainty("WPol","lnN")
        self.specifyUncertainty("WPol",mbnameS,"W",1.+mbres["systematics"]["Wpol"])
        self.specifyUncertainty("WPol",mbnameS,"tt",1.+mbres["systematics"]["Wpol"])
        self.specifyUncertainty("WPol",mbnameS,"other",1.+mbres["systematics"]["Wpol"])
        # stat. uncertainty on signal efficiency
        uncName = "statSeff" + mbnameS
        self.c.addUncertainty(uncName,"lnN")
        self.specifyUncertainty(uncName,mbnameS,"signal",1+self.sigSubDict(self.mbsigres)["stat_err_MB_SR"])

      #
      # SB related systematics propagated to MB
      #
      for sbname in sbBinNames:
        sbres = self.subDict(self.bkgres,self.sbBins[sbname])
        sbnameC = sbname + "C"
        # statistical uncertainty SB CRs
        uncName = "stat" + sbnameC
        self.c.addUncertainty(uncName,"lnN")
        for mbname in mbBinNames:
          bname = mbname[2:]
          mbnameS = mbname + "S"
          if "J3"+bname==sbname:
              wYield = sbres["yW_crNJet_0b_lowDPhi"]
              wVar = sbres["yW_Var_crNJet_0b_lowDPhi"]
              self.specifyUncertainty(uncName,mbnameS,"W",1.+sqrt(wVar)/wYield)
          elif "J4"+bname==sbname:
              ttYield = sbres["y_crNJet_1b_lowDPhi"]
              ttVar = sbres["y_crNJet_1b_lowDPhi"]
              self.specifyUncertainty(uncName,mbnameS,"tt",1.+sqrt(ttVar)/ttYield)

      txtname = os.path.join(self.dir,self.name+".txt")
      logname = os.path.join(self.dir,self.name+".log")
      outname = os.path.join(self.dir,self.name+".out")
      if os.path.exists(txtname) or os.path.exists(logname) or os.path.exists(outname):
          if not self.force:
              print "Output file(s) exist for ",self.name," - skipping"
              return

      self.c.writeToFile(txtname)
      #
      # comments
      #
      txt = open(txtname,"a")
      if xsecFactor!=1:
          txt.write("#\n")
          txt.write("# ************************\n")
          txt.write("# Signal rates have been scaled by "+str(xsecFactor)+" !!!!!!\n")
          txt.write("#\n")
      txt.write("#\n")
      txt.write("# List of uncertainties\n")
      txt.write("#\n")
      txt.write("# corrWBFJxLyHzDu ... correlation W: SB/highDPhi with MB/highDPhi\n")
      txt.write("# corrWEFJxLyHzDu ... correlation W: MB/lowDPhi with MB/highDPhi\n")
      txt.write("# corrTTDFJxLyHzDu .. correlation tt: SB/highDPhi with MB/highDPhi\n")
      txt.write("# corrTTEFJxLyHzDu .. correlation tt: MB/lowDPhi with MB/highDPhi\n")
      txt.write("# yWttJxLyHzDuC ..... anti-correlated W/tt fraction fit systematics in MB CR\n")
      txt.write("# yQCDJxLyHzDuC ..... uncertainty QCD estimate in MB CR\n")
      txt.write("# statJ[34]LyHzDuC .. stat. uncertainty from yield in SB lowDPhi \n")
      txt.write("# yWttJ[34]LyHzDuS .. anti-correlated W/tt fraction fit systematics in W SB highDPhi\n")
      txt.write("# yWttJ[34]LyHzDuC ?? anti-correlated W/tt fraction fit systematics in W SB lowDPhi\n")
      txt.write("# lumi .............. luminosity\n")
      txt.write("# sigSyst ........... approximated total signal systematics\n")
      txt.close()

      print "Total predictions and uncertainties:"
      for mbname in mbBinNames:
          mbnameS = mbname + "S"
          for p in self.totalPredictions[mbnameS]:
              if not p in self.totalUncertainties[mbnameS]:
                  continue
              pred = self.totalPredictions[mbnameS][p]
              unc = self.totalUncertainties[mbnameS][p]
              print "{0:10s} {1:5s} : {2:8.2f} +- {3:7.2f} ( rel.: {4:7.3f} )".format(mbnameS,p,pred,pred*unc,unc)

      if self.runLimit:
          stdout = sys.stdout
          sys.stdout = open(logname,"w")
          opts = ""
          if self.runBlind:
              opts = "--run blind"
          res = self.c.calcLimit(options=opts)
          if xsecFactor!=1:
              for k in res:
                  res[k] *= xsecFactor
          print 'Result ',mbBinNames[0]," , ",self.signal["name"],self.signal["mglu"],self.signal["mlsp"]," : ",res
          sys.stdout.close()
          sys.stdout = stdout
          return res
