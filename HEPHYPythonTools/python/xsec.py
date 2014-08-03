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
xsec['TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola_Spring14miniaod-PU20bx25_POSTLS170_V5-v1'] = 689.1 

##------------------------------------------------------------
##SUMMER 12
##https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat8TeV
#xsec["8TeV-DYJetsToLL-M50"]                     =       3503.71
#xsec["8TeV-DYJetsToLL-M10to50"]                 =       877.
#xsec["8TeV-DYToEE-M20"]                         =       1915.08333
#xsec["8TeV-DYToMuMu-M20"]                       =       1915.08333
#xsec["8TeV-DYToTauTau-M20"]                     =       1915.08333
#
#xsec["8TeV-T-s"]                                =       3.79
#xsec["8TeV-T-t"]                                =       56.4
#xsec["8TeV-T-tW"]                               =       11.1
#
#xsec["8TeV-Tbar-s"]                             =       1.76
#xsec["8TeV-Tbar-t"]                             =       30.7
#xsec["8TeV-Tbar-tW"]                            =       11.1
#
#xsec["8TeV-TTJets"]                             =       225.197
#xsec["8TeV-TTWJets"]                            =       0.232 
#xsec["8TeV-TTZJets"]                            =       0.2057 
#
#xsec["8TeV-WJetsToLNu"]                         =       36257.2
#
##https://twiki.cern.ch/twiki/bin/view/CMS/TTbarHiggs
#xsec["8TeV-W1JetsToLNu"] =  6440.4  
#xsec["8TeV-W2JetsToLNu"] =  2087.2  
#xsec["8TeV-W3JetsToLNu"] =  619.0 
#xsec["8TeV-W4JetsToLNu"] =  255.2 
#
###http://cms.cern.ch/iCMS/prep/requestmanagement?campid=Summer12_DR52X
##xsec["8TeV-WJets-HT400"]                   =       25.22 #* 27965.3/18656.04 #including match to NLO WJetstoLNu (corr-factor obtained from normalizing MET-shape HT>450)
##xsec["8TeV-WJets-HT250to300"]              =       48.01 #* 27965.3/18656.04 #including match to NLO WJetstoLNu (corr-factor obtained from normalizing MET-shape HT>450)
##xsec["8TeV-WJets-HT300to400"]              =       38.3  #* 27965.3/18656.04 #including match to NLO WJetstoLNu (corr-factor obtained from normalizing MET-shape HT>450)
#xsec["8TeV-WbbJetsToLNu"]                  =       3*0.108*377.4 #https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat8TeV times lep. BR from PDG
#
##http://cms.cern.ch/iCMS/jsp/mcprod/admin/requestmanagement.jsp?campid=Summer12_DR53X
#xsec["8TeV-WJetsToLNu_HT-150To200"] = 235.6  #/WJetsToLNu_HT-150To200_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM
#xsec["8TeV-WJetsToLNu_HT-200To250"] =  90.27#/WJetsToLNu_HT-200To250_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM
#xsec["8TeV-WJetsToLNu_HT-250To300"] =  48.01#/WJetsToLNu_HT-250To300_8TeV-madgraph_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-WJetsToLNu_HT-300To400"] =  38.3#/WJetsToLNu_HT-300To400_8TeV-madgraph_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-WJetsToLNu_HT-400ToInf"] =  25.22 #/WJetsToLNu_HT-400ToInf_8TeV-madgraph_v2/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#
##http://cms.cern.ch/iCMS/jsp/mcprod/admin/requestmanagement.jsp?campid=Summer12_DR53X
##xsec["8TeV-WJetsToLNu_PtW-100_8TeV-herwigpp"] =  #/WJetsToLNu_PtW-100_8TeV-herwigpp/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM #https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsMCProductionSummer12
#xsec["8TeV-WJetsToLNu_PtW-100_TuneZ2star_8TeV_ext-madgraph-tarball"] = 221.3  #/WJetsToLNu_PtW-100_TuneZ2star_8TeV_ext-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM
#xsec["8TeV-WJetsToLNu_PtW-180_TuneZ2star_8TeV-madgraph-tarball"] = 23.5 #/WJetsToLNu_PtW-180_TuneZ2star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM
#
#xsec["8TeV-WJetsToLNu_PtW-50To70_TuneZ2star_8TeV-madgraph"] = 811.2 #/WJetsToLNu_PtW-50To70_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-WJetsToLNu_PtW-70To100_TuneZ2star_8TeV-madgraph"] =  428.9 #/WJetsToLNu_PtW-70To100_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-WJetsToLNu_PtW-100_TuneZ2star_8TeV-madgraph"] = 228.9  #/WJetsToLNu_PtW-100_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#
#xsec["8TeV-WminusToENu"] = 4697.0  #/WminusToENu_CT10_TuneZ2star_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-WminusToMuNu"] =4697.0  #/WminusToMuNu_CT10_TuneZ2star_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-WminusToTauNu"] =4697.0  #/WminusToTauNu_CT10_TuneZ2star_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-WminusToTauNu-tauola"] =4697.0  #/WminusToTauNu_CT10_TuneZ2star_8TeV-powheg-tauola-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-WplusToENu"] = 6702.0 #/WplusToENu_CT10_TuneZ2star_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-WplusToMuNu"] = 6702.0 #/WplusToMuNu_CT10_TuneZ2star_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-WplusToTauNu"] = 6702.0 #/WplusToTauNu_CT10_TuneZ2star_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-WplusToTauNu-tauola"] = 6702.0 #/WplusToTauNu_CT10_TuneZ2star_8TeV-powheg-tauola-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#
##http://cms.cern.ch/iCMS/jsp/mcprod/admin/requestmanagement.jsp?campid=Summer12_DR53X
##xsec["8TeV-DYJetsToLL_M10-50_PtZ-100_TuneZ2star_8TeV-madgraph"] =  #/DYJetsToLL_M10-50_PtZ-100_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM
##xsec["8TeV-DYJetsToLL_M10-50_PtZ70-100_TuneZ2star_8TeV-madgraph"] =  #/DYJetsToLL_M10-50_PtZ70-100_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM
#xsec["8TeV-DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball"] = 4.56 #/DYJetsToLL_PtZ-180_TuneZ2star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM
#
#xsec["8TeV-DYJetsToLL_PtZ-50To70_TuneZ2star_8TeV-madgraph-tarball"] = 93.8 #/DYJetsToLL_PtZ-50To70_TuneZ2star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-DYJetsToLL_PtZ-70To100_TuneZ2star_8TeV-madgraph-tarball"] = 52.31 #/DYJetsToLL_PtZ-70To100_TuneZ2star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM
#xsec["8TeV-DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph"] = 34.1 #/DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v2/AODSIM
#
#xsec["8TeV-DYJetsToLL_PtZ-50To70_TuneZ2star_8TeV_ext-madgraph-tarball"] = 89.0 #/DYJetsToLL_PtZ-50To70_TuneZ2star_8TeV_ext-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM
#xsec["8TeV-DYJetsToLL_PtZ-70To100_TuneZ2star_8TeV_ext-madgraph-tarball"] = 53.0 #/DYJetsToLL_PtZ-70To100_TuneZ2star_8TeV_ext-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM
#xsec["8TeV-DYJetsToLL_PtZ-100_TuneZ2star_8TeV_ext-madgraph-tarball"] = 32.9 #/DYJetsToLL_PtZ-100_TuneZ2star_8TeV_ext-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM
#
#
#xsec["8TeV-ZJetsToNuNu_50_HT_100_TuneZ2Star_8TeV_madgraph"] = 381.2  #/ZJetsToNuNu_50_HT_100_TuneZ2Star_8TeV_madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-ZJetsToNuNu_50_HT_100_TuneZ2Star_8TeV_madgraph_ext"] = 381.2 #/ZJetsToNuNu_50_HT_100_TuneZ2Star_8TeV_madgraph_ext/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-ZJetsToNuNu_100_HT_200_TuneZ2Star_8TeV_madgraph"] = 160.3 #/ZJetsToNuNu_100_HT_200_TuneZ2Star_8TeV_madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-ZJetsToNuNu_100_HT_200_TuneZ2Star_8TeV_madgraph_ext"] = 160.3 #/ZJetsToNuNu_100_HT_200_TuneZ2Star_8TeV_madgraph_ext/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM
#xsec["8TeV-ZJetsToNuNu_200_HT_400_TuneZ2Star_8TeV_madgraph"] = 41.49 #/ZJetsToNuNu_200_HT_400_TuneZ2Star_8TeV_madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-ZJetsToNuNu_200_HT_400_TuneZ2Star_8TeV_madgraph_ext"] = 41.49  #/ZJetsToNuNu_200_HT_400_TuneZ2Star_8TeV_madgraph_ext/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-ZJetsToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph"] = 5.274  #/ZJetsToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-ZJetsToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph_ext"] = 5.274  #/ZJetsToNuNu_400_HT_inf_TuneZ2Star_8TeV_madgraph_ext/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#
##xsec["8TeV-ZJetsToLL_Pt-100_8TeV-herwigpp"] =  #/ZJetsToLL_Pt-100_8TeV-herwigpp/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
##xsec["8TeV-ZJetsToNuNu_Pt-100_8TeV-herwigpp"] =  #/ZJetsToNuNu_Pt-100_8TeV-herwigpp/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#xsec["8TeV-ZJetsToNuNu_PtZ-70To100_8TeV"] = 32.9  #/ZJetsToNuNu_PtZ-70To100_8TeV/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM
#xsec["8TeV-ZJetsToNuNu_PtZ-100_8TeV-madgraph"] = 21.44 #/ZJetsToNuNu_PtZ-100_8TeV-madgraph/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM
#
##http://cms.cern.ch/iCMS/prep/requestmanagement?campid=Summer12_DR52X
#xsec["8TeV-LM6"]                                =       0.5047
#xsec["8TeV-LM9"]                                =       9.287
#xsec["8TeV-QCD-Pt1000-MuEnrichedPt5"]           =       0.774*0.1097
#xsec["8TeV-QCD-Pt120to170-MuEnrichedPt5"]       =       157800.0*0.0473
#xsec["8TeV-QCD-Pt170to300-MuEnrichedPt5"]       =       34020.0*0.0676
#xsec["8TeV-QCD-Pt20to30-MuEnrichedPt5"]         =       2.87*(10**8)*0.0065
#xsec["8TeV-QCD-Pt300to470-MuEnrichedPt5"]       =       1757.0*0.0864
#xsec["8TeV-QCD-Pt30to50-MuEnrichedPt5"]         =       6.609*(10**7)*0.0122
#xsec["8TeV-QCD-Pt50to80-MuEnrichedPt5"]         =       8.082*(10**6)*0.0218
#xsec["8TeV-QCD-Pt470to600-MuEnrichedPt5"]       =       115.2*0.1024
#xsec["8TeV-QCD-Pt600to800-MuEnrichedPt5"]       =       27.01*0.0996
#xsec["8TeV-QCD-Pt800to1000-MuEnrichedPt5"]      =       3.57*0.1033
#xsec["8TeV-QCD-Pt80to120-MuEnrichedPt5"]        =       1024000.0*0.0395
#xsec["8TeV-ZJetsToNuNu-HT50to100"] =  452.75 #NNLO https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSYJetsMETTausAnalysis2012 
#xsec["8TeV-ZJetsToNuNu-HT100to200"] = 190.39
#xsec["8TeV-ZJetsToNuNu-HT200to400"] = 49.28
#xsec["8TeV-ZJetsToNuNu-HT200-400"] = 49.28
#xsec["8TeV-ZJetsToNuNu-HT400"] = 6.26
#
#xsec["8TeV-QCD_Pt-5to15"]                       =       4.2639499*(10**10)
##fehlt
#xsec["8TeV-QCD_Pt-30to50"]                      =       6.6285328*(10**7)
#xsec["8TeV-QCD_Pt-50to80"]                      =       8148778.0
#xsec["8TeV-QCD_Pt-80to120"]                     =       1033680.0
#xsec["8TeV-QCD_Pt-120to170"]                    =       156293.3
#xsec["8TeV-QCD_Pt-170to300"]                    =       34138.15
#xsec["8TeV-QCD_Pt-300to470"]                    =       1759.549
#xsec["8TeV-QCD_Pt-470to600"]                    =       113.8791
#xsec["8TeV-QCD_Pt-600to800"]                    =       26.9921
#xsec["8TeV-QCD_Pt-800to1000"]                   =       3.550036
#xsec["8TeV-QCD_Pt-1000to1400"]                  =       0.737844
#xsec["8TeV-QCD_Pt-1400to1800"]                  =       0.03352235
#xsec["8TeV-QCD_Pt-1800"]                        =       0.001829005
#
#xsec["8TeV-QCD_EMEnriched_Pt_20_30"]           =        2.886*(10**8)*0.0101 	
#xsec["8TeV-QCD_EMEnriched_Pt_30_80"]           =        7.433*(10**7)*0.0621 	
#xsec["8TeV-QCD_EMEnriched_Pt_80_170"]          = 	    1191000.0*0.1539
#xsec["8TeV-QCD_EMEnriched_Pt_170_250"]         =        30990.0*0.148
#xsec["8TeV-QCD_EMEnriched_Pt_250_350"]         =        4250.0*0.131
#xsec["8TeV-QCD_EMEnriched_Pt_350"]             = 	    810.0*0.11
#xsec["8TeV-QCD_BCtoE_Pt_20_30"]                =        2.886*(10**8)*5.8*(10**(-4))
#xsec["8TeV-QCD_BCtoE_Pt_30_80"]                =        7.424*(10**7)*0.00225
#xsec["8TeV-QCD_BCtoE_Pt_80_170"]               =        1191000.0*0.0109
#xsec["8TeV-QCD_BCtoE_Pt_170_250"]              =        30980.0*0.0204
#xsec["8TeV-QCD_BCtoE_Pt_250_350"]              =        4250.0*0.0243
#xsec["8TeV-QCD_BCtoE_Pt_350"]                  =        811.0*0.0295
#
##xsec["8TeV-ZJetsToNuNu-HT50to100"] = 381.2
##xsec["8TeV-ZJetsToNuNu-HT100to200"] = 160.3
##xsec["8TeV-ZJetsToNuNu-HT200to400"] = 41.49
##xsec["8TeV-ZJetsToNuNu-HT200-400"] = 41.49
##xsec["8TeV-ZJetsToNuNu-HT400"] = 5.274
#xsec["8TeV-WW"] = 54.838
#xsec["8TeV-WZ"] = 32.3 
#xsec["8TeV-ZZ"] = 7.7 
#
##MonoJet Signals
##https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SUSYCrossSections8TeVstopsbottom
#xsec["8TeV-stop300-LSP270"] = 1.99608
#xsec["8TeV-stop300-LSP270-FullSim"] = 1.99608
#xsec["8TeV-stop200lsp170g100"] = 18.5245  
#xsec["8TeV-stop300lsp240g150"] = 1.99608
#xsec["8TeV-stop300lsp270g175"] = 1.99608
#xsec["8TeV-stop300lsp270"] = 1.99608
#xsec["8TeV-stop300lsp270g200"] = 1.99608
#
#xsec["T5Full_1100_200_100-4"] = 0.0101744
#xsec["T5Full_1100_800_600-4"] = 0.0101744
