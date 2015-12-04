class xsec_(dict):

    def reduceID(self, id):
      s=id.split('__')
      if len(s)>1 and s[-1].isdigit():
        return '__'.join(s[:-1])
      else:
        return id
        
    def __init__(self):
        self._dict = {}

    def __setitem__(self, idl, val):
      assert type(idl)==type(''),"Only strings allowed as keys. You tried "+str(type(idl))
      id = self.reduceID(idl)
      assert (not self._dict.has_key(id) or val==self._dict[id]), "Error: Trying to overwrite key "+str(id)+' with value '+str(val)+' but was previously set to value '+str(self._dict[id]) 
      self._dict[id] = val
    def __getitem__(self, idl):
      id = self.reduceID(idl)
      return self._dict[id]

xsec=xsec_()
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
xsec['/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM'] = 689.1 
xsec['/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM'] = 689.1 
xsec['/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU_S14_POSTLS170_V6-v1/MINIAODSIM'] = 689.1

xsec['/WJetsToLNu_13TeV-madgraph-pythia8-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM'] = 20508.9
xsec['/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'] = 20508.9 
##Obtained from HT fit
xsec['/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/Spring14dr-PU_S14_POSTLS170_V6-v1/AODSIM'] = 20508.9*0.0746149974976  
xsec['/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/Spring14dr-PU_S14_POSTLS170_V6-v1/AODSIM'] = 20508.9*0.00867842338647 
xsec['/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/Spring14dr-PU_S14_POSTLS170_V6-v1/AODSIM'] = 20508.9*0.00151784517782 
xsec['/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Spring14dr-PU_S14_POSTLS170_V6-v1/AODSIM'] = 20508.9*0.000327181070988

#from StopsDilepton.samples.xsecSMS import gluino13TeV_NLONLL
from xsecSMS import gluino13TeV_NLONLL

xsec['T1qqqq_1400_325_300'] = gluino13TeV_NLONLL[1400]
xsec["SMS_T1qqqq_2J_mGl1000_mLSP800_PU_S14_POSTLS170"] =  gluino13TeV_NLONLL[1000]
xsec["SMS_T1qqqq_2J_mGl1400_mLSP100_PU_S14_POSTLS170"] =  gluino13TeV_NLONLL[1400]
xsec["SMS_T1bbbb_2J_mGl1000_mLSP900_PU_S14_POSTLS170"] =  gluino13TeV_NLONLL[1000]
xsec["SMS_T1bbbb_2J_mGl1500_mLSP100_PU_S14_POSTLS170"] =  gluino13TeV_NLONLL[1500]
xsec["T1ttbb_2J_mGo1500_mChi100"] = gluino13TeV_NLONLL[1500] 
xsec['T1ttbb_mGo1500_mChi100'] = gluino13TeV_NLONLL[1500] 

xsec["T1ttbbWW_2J_mGo1000_mCh725_mChi715_3bodydec"] = gluino13TeV_NLONLL[1000] 
xsec["T1ttbbWW_2J_mGo1000_mCh725_mChi720_3bodydec"] = gluino13TeV_NLONLL[1000]
xsec["T1ttbbWW_2J_mGo1300_mCh300_mChi290_3bodydec"] = gluino13TeV_NLONLL[1300]
xsec["T1ttbbWW_2J_mGo1300_mCh300_mChi295_3bodydec"] = gluino13TeV_NLONLL[1300]
xsec['T1ttbbWW_mGo1000_mCh725_mChi715'] = gluino13TeV_NLONLL[1000]
xsec['T1ttbbWW_mGo1000_mCh725_mChi720'] = gluino13TeV_NLONLL[1000]
xsec['T1ttbbWW_mGo1300_mCh300_mChi290'] = gluino13TeV_NLONLL[1300]
xsec['T1ttbbWW_mGo1300_mCh300_mChi295'] = gluino13TeV_NLONLL[1300]

xsec["SMS_T1tttt_2J_mGl1200_mLSP800_PU_S14_POSTLS170"] =  gluino13TeV_NLONLL[1200]
xsec["SMS_T1tttt_2J_mGl1200_mLSP800"] =  gluino13TeV_NLONLL[1200]
xsec["SMS_T1tttt_2J_mGl1500_mLSP100_PU_S14_POSTLS170"] =  gluino13TeV_NLONLL[1500]
xsec["SMS_T1tttt_2J_mGl1500_mLSP100"] =  gluino13TeV_NLONLL[1500]
xsec['SMS_T1tttt_2J_mGl1300_mLSP100'] = gluino13TeV_NLONLL[1300] 
xsec['SMS_T1tttt_2J_mGl800_mLSP450'] = gluino13TeV_NLONLL[800] 
xsec["T1tttt_2J_mGo1300_mStop300_mCh285_mChi280"] = gluino13TeV_NLONLL[1300]
xsec["T1tttt_2J_mGo1300_mStop300_mChi280"] = gluino13TeV_NLONLL[1300]
xsec["T1tttt_2J_mGo800_mStop300_mCh285_mChi280"] = gluino13TeV_NLONLL[800]
xsec["T1tttt_2J_mGo800_mStop300_mChi280"] = gluino13TeV_NLONLL[800]
xsec["T1tttt_gluino_1300_LSP_100"] = gluino13TeV_NLONLL[1300]
xsec["T1tttt_gluino_800_LSP_450"] = gluino13TeV_NLONLL[800]
#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVstopsbottom
xsec["SMS_T2tt_2J_mStop425_mLSP325_PU_S14_POSTLS170"] =  1.31169
xsec["SMS_T2tt_2J_mStop500_mLSP325_PU_S14_POSTLS170"] = 0.51848
xsec["SMS_T2tt_2J_mStop650_mLSP325_PU_S14_POSTLS170"] = 0.107045
xsec["SMS_T2tt_2J_mStop850_mLSP100_PU_S14_POSTLS170"] = 0.0189612
xsec["SMS_T2tt_2J_mStop425_mLSP325"] =  1.31169
xsec["SMS_T2tt_2J_mStop500_mLSP325"] = 0.51848
xsec["SMS_T2tt_2J_mStop650_mLSP325"] = 0.107045
xsec["SMS_T2tt_2J_mStop850_mLSP100"] = 0.0189612
xsec["SMS_T2bb_2J_mStop600_mLSP580_PU_S14_POSTLS170"] = 0.174599
xsec["SMS_T2bb_2J_mStop900_mLSP100_PU_S14_POSTLS170"] = 0.0128895
#CMGTools/TTHAnalysis/python/samples/samples_13TeV_CSA14.py
#and  https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVstopsbottom
xsec["SMS_T2qq_2J_mStop600_mLSP550_PU_S14_POSTLS170"] = 1.76645
xsec["SMS_T2qq_2J_mStop1200_mLSP100_PU_S14_POSTLS170"] = 0.0162846
xsec["T5WW_2J_mGo1200_mCh1000_mChi800"] = gluino13TeV_NLONLL[1200]
xsec["T5WW_2J_mGo1500_mCh800_mChi100"] = gluino13TeV_NLONLL[1500]
xsec["T5WW_2J_mGo1400_mCh315_mChi300"] = gluino13TeV_NLONLL[1400]

xsec["T6ttWW_2J_mSbot600_mCh425_mChi50"] = 0.174599
xsec['T6ttWW_mSbot600_mCh425_mChi50'] = 0.174599 
xsec["T6ttWW_2J_mSbot650_mCh150_mChi50"] = 0.107045
xsec['T6ttWW_mSbot650_mCh150_mChi50'] = 0.107045

xsec['/T5Full_T5Full-1200-1000-800-Decay-MGMMatch50/schoef-T5Full_T5Full-1200-1000-800-Decay-MGMMatch50-miniAOD-92bfc1aa0ef8c674e0edabb945b19298/USER'] = gluino13TeV_NLONLL[1200] 
xsec['/T5Full_T5Full-1500-800-100-Decay-MGMMatch50/schoef-T5Full_T5Full-1500-800-100-Decay-MGMMatch50-miniAOD-92bfc1aa0ef8c674e0edabb945b19298/USER'] = gluino13TeV_NLONLL[1500]
xsec["T5Full_1200_1000_800"] = gluino13TeV_NLONLL[1200]
xsec["T5Full_1500_800_100"]  =  gluino13TeV_NLONLL[1500]
xsec["T5qqqqWW_mGo1500_mCh800_mChi100"] = gluino13TeV_NLONLL[1500]

xsec["SMS_T5qqqqWW_Gl1200_Chi1000_LSP800"] = gluino13TeV_NLONLL[1200]       
xsec["SMS_T5qqqqWW_Gl1500_Chi800_LSP100"]  =  gluino13TeV_NLONLL[1500]      
xsec["T5qqqqWW_Gl_1400_LSP_100_Chi_325"] = gluino13TeV_NLONLL[1400]
xsec["T5qqqqWW_Gl_1400_LSP_300_Chi_315"] = gluino13TeV_NLONLL[1400]
xsec['SMS_T5qqqqWW_2J_mGo1400_mCh315_mChi300'] = gluino13TeV_NLONLL[1400] 

xsec['T5ttttDeg_mGo1000_mStop300_mCh285_mChi280'] = gluino13TeV_NLONLL[1000] 
xsec['T5ttttDeg_mGo1000_mStop300_mChi280'] = gluino13TeV_NLONLL[1000]
xsec['T5ttttDeg_mGo1300_mStop300_mCh285_mChi280'] = gluino13TeV_NLONLL[1300]
xsec['T5ttttDeg_mGo1300_mStop300_mChi280'] = gluino13TeV_NLONLL[1300]

xsec['T5qqqqWW_mGo1000_mCh800_mChi700'] = gluino13TeV_NLONLL[1000]
xsec['T5qqqqWW_mGo1000_mCh800_mChi700_dilep'] = gluino13TeV_NLONLL[1000]
xsec['T5qqqqWW_mGo1200_mCh1000_mChi800'] = gluino13TeV_NLONLL[1200]
xsec['T5qqqqWW_mGo1200_mCh1000_mChi800_cmg'] = gluino13TeV_NLONLL[1200]
xsec['T5qqqqWW_mGo1200_mCh1000_mChi800_dilep'] = gluino13TeV_NLONLL[1200]
xsec['T5qqqqWW_mGo1500_mCh800_mChi100'] = gluino13TeV_NLONLL[1500]
xsec['T5qqqqWWDeg_mGo1000_mCh310_mChi300'] = gluino13TeV_NLONLL[1000]
xsec['T5qqqqWWDeg_mGo1000_mCh315_mChi300'] = gluino13TeV_NLONLL[1000]
xsec['T5qqqqWWDeg_mGo1000_mCh325_mChi300'] = gluino13TeV_NLONLL[1000]
xsec['T5qqqqWWDeg_mGo1400_mCh315_mChi300'] = gluino13TeV_NLONLL[1400]
xsec['T5qqqqWWDeg_mGo800_mCh305_mChi300'] = gluino13TeV_NLONLL[800]


xsec['T5ttttDeg_mGo1000_mStop300_mCh285_mChi280_dil'] = gluino13TeV_NLONLL[1000] 
xsec['T5ttttDeg_mGo1300_mStop300_mCh285_mChi280_dil'] = gluino13TeV_NLONLL[1300]

#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVsquarkantisquark
xsec["T6qqWW_Sq_950_LSP_300_Chi_350"] = 0.0898112
xsec['SMS_T6qqWW_mSq950_mChi325_mLSP300'] = 0.0898112 

#CMGTools/samples PHYS14
#https://twiki.cern.ch/twiki/bin/view/CMS/ACDSUSYSingleLepton, also used in CMGTools/samples
xsec['/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] = 809.1
xsec['/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM'] = 809.1 
xsec["/WJetsToLNu_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM"] = 1817.0*1.23
xsec["/WJetsToLNu_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM"] = 471.6*1.23
xsec["/WJetsToLNu_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM"] = 55.61*1.23
xsec["/WJetsToLNu_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM"] = 18.81*1.23
xsec["/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM"] = 2008.*3
xsec["/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM"] = 2008.*3

xsec["/DYJetsToLL_M-50_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM"] = 139.4*1.27
xsec["/DYJetsToLL_M-50_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM"] = 42.75*1.27
xsec["/DYJetsToLL_M-50_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM"] = 5.497*1.27
xsec["/DYJetsToLL_M-50_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM"] = 2.21*1.27 
xsec["/DYJetsToLL_M-50_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM"] = 139.4*1.27 
xsec["/DYJetsToLL_M-50_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM"] = 42.75*1.27
xsec["/DYJetsToLL_M-50_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM"] = 5.497*1.27
xsec["/DYJetsToLL_M-50_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/AODSIM"] = 2.21*1.27 

xsec['/QCD_HT_100To250_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] =  28730000.  
xsec['/QCD_HT_250To500_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] =  670500.  
xsec['/QCD_HT_500To1000_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] =  26740.
xsec['/QCD_HT_1000ToInf_13TeV-madgraph/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] =  769.7 
xsec['/TBarToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] =  4.16*0.108*3 
xsec['/TBarToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] = 80.97*0.108*3 
xsec['/TToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] = 7.20*0.108*3 
xsec['/TToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] = 136.05*0.108*3 
xsec['/T_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] =  35.6 
xsec['/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] =  35.6 
xsec['/TTWJets_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] =  0.6647 
xsec['/TTZJets_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'] =  0.8565 
xsec['/TTbarH_M-125_13TeV_amcatnlo-pythia8-tauola/Phys14DR-PU40bx25_PHYS14_25_V1-v1/MINIAODSIM'] =  0.5085 

#CMGTools/samples Spring15 25ns
xsec['/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-AsymptFlat10to50bx25Raw_MCRUN2_74_V9-v1/MINIAODSIM'] = 3.*2008.
xsec['/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM'] = 2008.*3.
xsec["/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 18610
xsec['/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'] = 18610 

xsec["/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =  139.4*1.27 
xsec["/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =  42.75*1.27 
xsec["/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =  5.497*1.27 
xsec["/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =  2.21*1.27 

xsec['/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'] = 1347*1.23
xsec['/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'] = 360*1.23
xsec['/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM'] = 48.9*1.23
xsec['/WJetsToLNu_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'] = 18.77*1.23
xsec['/WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'] = 12.8*1.23
xsec['/WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'] = 5.26*1.23
xsec['/WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'] = 1.33*1.23
xsec['/WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'] = 0.03089*1.23

xsec['/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'] = (7.20+4.16)*0.108*3
xsec['/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'] =     (136.05+80.97)*0.108*3
xsec['/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'] =   35.6
xsec['/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'] =       35.6

xsec['/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM']=831.76

xsec["/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"]= 831.76
xsec["/TTJets_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 1.610*831.76/502.2
xsec["/TTJets_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 0.663*831.76/502.2
xsec["/TTJets_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 0.12*831.76/502.2
xsec["/TTJets_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =  0.001430*831.76/502.2


xsec["/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = (831.76*(3*0.108)*(1-3*0.108))
xsec["/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] = (831.76*(3*0.108)*(1-3*0.108))
xsec["/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] = (831.76*(3*0.108)**2)

xsec["/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 2762530.0
xsec["/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"]=  471100
xsec["/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"]=  117276
xsec["/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"]=  7823
xsec["/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"]=  648.2
xsec["/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM"]=  186.9
xsec["/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =  32.293
xsec["/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"]  = 9.4183
xsec["/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"]  = 0.84265
xsec["/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"]  = 0.114943
xsec["/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"]  = 0.00682981
xsec["/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"]   = 0.000165445

xsec["/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] = 1735000
xsec["/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] = 367000
xsec["/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 29400
xsec["/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 6524
xsec["/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] = 1064
xsec["/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 121.5
xsec["/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 25.42

xsec["/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =     1273190000*0.003  
xsec["/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =     558528000*0.0053
xsec["/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =     139803000*0.01182
xsec["/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =     19222500*0.02276
xsec["/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =    2758420*0.03844
xsec["/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =   469797*0.05362
xsec["/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =   117989*0.07335
xsec["/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =   7820.25*0.10196
xsec["/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =   645.528*0.12242
xsec["/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =   187.109*0.13412
xsec["/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =  32.3486*0.14552
xsec["/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =  10.4305*0.15544

xsec["/QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =    1273000000*0.0002 
xsec["/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =    557600000*0.0096
xsec["/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =    136000000*0.073
xsec["/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =    19800000*0.146
xsec["/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM"] =   2800000*0.125
xsec["/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =  477000*0.132
xsec["/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =  114000*0.165
xsec["/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =  9000*0.15

xsec["/QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =   1272980000*0.0002 
xsec["/QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =   557627000*0.00059
xsec["/QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =   159068000*0.00255
xsec["/QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] =  3221000*0.01183
xsec["/QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 105771*0.02492
xsec["/QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM"] = 21094.1*0.03375

xsec["/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = (40.2+25.9)
xsec["/WWTo2L2Nu_13TeV-powheg/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] =  118.7*((3*0.108)**2)
xsec["/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM"] = 31.8
xsec["/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 78.36*1.27 
xsec["/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 10.94*1.27
xsec["/ZJetsToNuNu_HT-600ToInf_13TeV-madgraph/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM"] = 4.203*1.27

#CMGTools/samples Spring15 50ns
xsec['WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'] = 20508.9*3

xsec['/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'] = 18610
xsec['/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM'] = 2008.*3
xsec['/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'] = 139.4*1.27 
xsec['/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'] = 42.75*1.27
xsec['/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'] = 5.497*1.27
xsec['/DYJetsToLL_M-50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'] = 2.21*1.27 

xsec["/ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"] =      (136.05+80.97)*0.108*3 
xsec["/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"] =    35.6
xsec["/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"] =        35.6

xsec["/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"]=831.76 

xsec["/QCD_Pt_10to15_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"]=5887580000
xsec["/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"]=1837410000
xsec["/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"]=140932000
xsec["/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"]=19204300
xsec["/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"]=2762530
xsec["/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"]=471100
xsec["/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"]=117276
xsec["/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"]=7823
xsec["/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"]=648.2
xsec["/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"]=186.9
xsec["/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"]=32.293
xsec["/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"]=9.4183
xsec["/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"]=0.84265
xsec["/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"]=0.114943
xsec["/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"]=0.00682981
xsec["/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"]=0.000165445

xsec["/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM"] =     1273190000*0.003   
xsec["/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"] =     558528000*0.0053
xsec["/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"] =     139803000*0.01182
xsec["/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"] =     19222500*0.02276
xsec["/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"] =    2758420*0.03844
xsec["/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM"] =   469797*0.05362
xsec["/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"] =   117989*0.07335
xsec["/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM"] =   7820.25*0.10196
xsec["/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM"] =   645.528*0.12242
xsec["/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"] =   187.109*0.13412
xsec["/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"] =  32.3486*0.14552
xsec["/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"] =  10.4305*0.15544

xsec["/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"] = (40.2+25.9) 
xsec["/WWTo2L2Nu_13TeV-powheg/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"] = 118.7*((3*0.108)**2) 
xsec["/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM"] =31.8 

#https://wiki.hephy.at/index.php/CMS_Analyse_LightDegStops/13TeVDegStop
#https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections13TeVstopsbottom 8.51615 +- 13.9223%
xsec['/T2DegStop2j_300_270_GENSIM/nrad-T2DegStop2j_300_270_MINIAOD-a279b5108ada7c3c0926210c2a95f22e/USER'] = 8.51615
xsec['T2DegStop_300_270'] = 8.51615
#xsec['T2DegStop_test'] = 8.51615

