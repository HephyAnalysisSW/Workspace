import ROOT

"""

    to get the data PU profile:

    
    data_json = "/afs/cern.ch/user/n/nrad/public/bril_res/2016/MET_Run2016_Total.json"
    
    pileupCalc.py -i /afs/cern.ch/user/n/nrad/public/bril_res/2016/MET_Run2016_Total.json  --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 59850 --maxPileupBin 50 --numPileupBins 50  DataPUHisto_12p9_Run2016BCD_59p85mb.root
    pileupCalc.py -i /afs/cern.ch/user/n/nrad/public/bril_res/2016/MET_Run2016_Total.json  --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 60000 --maxPileupBin 50 --numPileupBins 50  DataPUHisto_12p9_Run2016BCD_63mb.root
    pileupCalc.py -i /afs/cern.ch/user/n/nrad/public/bril_res/2016/MET_Run2016_Total.json  --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 66150 --maxPileupBin 50 --numPileupBins 50  DataPUHisto_12p9_Run2016BCD_66p15mb.root


    pileupCalc.py -i /afs/cern.ch/user/n/nrad/public/bril_res/2016/MET_Run2016_BC.json  --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 59850 --maxPileupBin 50 --numPileupBins 50  DataPUHisto_8p5_Run2016BC_59p85mb.root
    pileupCalc.py -i /afs/cern.ch/user/n/nrad/public/bril_res/2016/MET_Run2016_BC.json  --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 60000 --maxPileupBin 50 --numPileupBins 50  DataPUHisto_8p5_Run2016BC_63mb.root
    pileupCalc.py -i /afs/cern.ch/user/n/nrad/public/bril_res/2016/MET_Run2016_BC.json  --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 66150 --maxPileupBin 50 --numPileupBins 50  DataPUHisto_8p5_Run2016BC_66p15mb.root

    pileupCalc.py -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt   --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 59850 --maxPileupBin 50 --numPileupBins 50  DataPUHisto_12p9_Run2016BCD_59p85mb_CentralJSON.root
    pileupCalc.py -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt   --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 60000 --maxPileupBin 50 --numPileupBins 50  DataPUHisto_12p9_Run2016BCD_63mb_CentralJSON.root
    pileupCalc.py -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt   --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 66150 --maxPileupBin 50 --numPileupBins 50  DataPUHisto_12p9_Run2016BCD_66p15mb_CentralJSON.root

"""


PU_var = { \
                "8p5_up"        :   {'xsec': "59p85"  , 'file': 'DataPUHisto_8p5_Run2016BC_%smb.root'} , 
                "8p5_central"   :   {'xsec': "63"     , 'file': 'DataPUHisto_8p5_Run2016BC_%smb.root'} , 
                "8p5_down"      :   {'xsec': "66p15"  , 'file': 'DataPUHisto_8p5_Run2016BC_%smb.root'} ,
                "up"        :   {'xsec': "59p85"  , 'file': 'DataPUHisto_12p9_Run2016BCD_%smb.root'} , 
                "central"   :   {'xsec': "63"     , 'file': 'DataPUHisto_12p9_Run2016BCD_%smb.root'} , 
                "down"      :   {'xsec': "66p15"  , 'file': 'DataPUHisto_12p9_Run2016BCD_%smb.root'} ,
                "up_CJ"        :   {'xsec': "59p85"  , 'file': 'DataPUHisto_12p9_Run2016BCD_%smb_CentralJSON.root'} , 
                "central_CJ"   :   {'xsec': "63"     , 'file': 'DataPUHisto_12p9_Run2016BCD_%smb_CentralJSON.root'} , 
                "down_CJ"      :   {'xsec': "66p15"  , 'file': 'DataPUHisto_12p9_Run2016BCD_%smb_CentralJSON.root'} ,
          }

mc_histo_file = "mcSpring16_25ns_pu.root"
import os
for var, info in PU_var.iteritems():
  xsec = info['xsec']
  fname = info['file']%xsec

  #data_PU_file = os.path.expandvars("$CMSSW_BASE") + "/src/Workspace/DegenerateStopAnalysis/cmgPostprocessing/pileup/DataPilePUHisto_12p9fb_Run2016BCD_%smb.root"%xsec
  PU_dir = os.path.expandvars("$CMSSW_BASE") + "/src/Workspace/DegenerateStopAnalysis/python/cmgPostProcessing/pileup/"
  data_PU_file = PU_dir+"/"+ fname
  data_f = ROOT.TFile(data_PU_file)

  h_data = data_f.Get("pileup")
  h_data.Scale(1/h_data.Integral())

  mc_file = ROOT.TFile(PU_dir +"/"+ mc_histo_file) 
  mc_histo = mc_file.Get("pileup")

  h_ratio = h_data.Clone('h_ratio')
  h_ratio.Divide(mc_histo)
  h_ratio.SetTitle( var )
  h_ratio.SaveAs( PU_dir + "/PU_ratio_"+str(var)+".root")
  cb = ROOT.TCanvas("cb","cb",564,232,600,600)
  cb.cd()
  h_ratio.Draw()
  h_ratio.SetMaximum(4)
  h_ratio.SetMinimum(-4)
  cb.SaveAs( PU_dir + "/PU_ratio_"+str(var)+".png")
  cb.SaveAs( "/afs/hephy.at/user/n/nrad/www/data/2016/PU/" + "/PU_ratio_"+str(var)+".png")
  del h_ratio , data_f , h_data




