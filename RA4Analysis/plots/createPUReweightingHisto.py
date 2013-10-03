import ROOT
#PU S10 scenario
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/Pileup_MC_Gen_Scenarios#2012_Pileup_Scenario_s
ROOT.gROOT.ProcessLine("Double_t Summer2012_S10[60] = {2.560E-06,5.239E-06,1.420E-05,5.005E-05,1.001E-04,2.705E-04,1.999E-03,6.097E-03,1.046E-02,1.383E-02,1.685E-02,2.055E-02,2.572E-02,3.262E-02,4.121E-02,4.977E-02,5.539E-02,5.725E-02,5.607E-02,5.312E-02,5.008E-02,4.763E-02,4.558E-02,4.363E-02,4.159E-02,3.933E-02,3.681E-02,3.406E-02,3.116E-02,2.818E-02,2.519E-02,2.226E-02,1.946E-02,1.682E-02,1.437E-02,1.215E-02,1.016E-02,8.400E-03,6.873E-03,5.564E-03,4.457E-03,3.533E-03,2.772E-03,2.154E-03,1.656E-03,1.261E-03,9.513E-04,7.107E-04,5.259E-04,3.856E-04,2.801E-04,2.017E-04,1.439E-04,1.017E-04,7.126E-05,4.948E-05,3.405E-05,2.322E-05,1.570E-05,5.005E-06}")

ROOT.gROOT.ProcessLine("Double_t Summer2012_S7[60] = {2.344E-05,2.344E-05,2.344E-05,2.344E-05,4.687E-04,4.687E-04,7.032E-04,9.414E-04,1.234E-03,1.603E-03,2.464E-03,3.250E-03,5.021E-03,6.644E-03,8.502E-03,1.121E-02,1.518E-02,2.033E-02,2.608E-02,3.171E-02,3.667E-02,4.060E-02,4.338E-02,4.520E-02,4.641E-02,4.735E-02,4.816E-02,4.881E-02,4.917E-02,4.909E-02,4.842E-02,4.707E-02,4.501E-02,4.228E-02,3.896E-02,3.521E-02,3.118E-02,2.702E-02,2.287E-02,1.885E-02,1.508E-02,1.166E-02,8.673E-03,6.190E-03,4.222E-03,2.746E-03,1.698E-03,9.971E-04,5.549E-04,2.924E-04,1.457E-04,6.864E-05,3.054E-05,1.282E-05,5.081E-06,1.898E-06,6.688E-07,2.221E-07,6.947E-08,2.047E-08}")


S10 = ROOT.TH1F("S10", "S10", 60,0,60)
for i in range(60):
  S10.SetBinContent(i+1, ROOT.Summer2012_S10[i])

S10.Scale(1./S10.Integral())

S7 = ROOT.TH1F("S7", "S7", 60,0,60)
for i in range(60):
  S7.SetBinContent(i+1, ROOT.Summer2012_S7[i])

S7.Scale(1./S7.Integral())

#pileupCalc.py -i Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON.txt --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/pileup_JSON_DCSONLY_190389-203002_corr.txt --calcMode true --minBiasXsec 72870 --maxPileupBin 60 --numPileupBins 60 MyDataPileupHistogram_Run2012AB_13Jul2012ReReco_60max_true_pixelcorr_SysPlus5.root
#pileupCalc.py -i Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON.txt --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/pileup_JSON_DCSONLY_190389-203002_corr.txt --calcMode true --minBiasXsec 65930 --maxPileupBin 60 --numPileupBins 60 MyDataPileupHistogram_Run2012AB_13Jul2012ReReco_60max_true_pixelcorr_SysMinus5.root
#pileupCalc.py -i Cert_190456-203002_8TeV_PromptReco_Collisions12_JSON.txt --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/pileup_JSON_DCSONLY_190389-203002_corr.txt --calcMode true --minBiasXsec 69400 --maxPileupBin 60 --numPileupBins 60 MyDataPileupHistogram_Run2012AB_13Jul2012ReReco_60max_true_pixelcorr_Sys0.root

tf = ROOT.TFile("PU/MyDataPileupHistogram_Run2012ABC_60max_true_pixelcorr_Sys0.root")
ROOT.gDirectory.cd("PyROOT:/")
reweightingHisto = tf.Get("pileup").Clone("ngoodVertices_Data")
tf.Close()
reweightingHisto.Scale(1./reweightingHisto.Integral())
reweightingHisto.Divide(S10)
tf = ROOT.TFile("PU/reweightingHisto_Summer2012-S10-Run2012ABC_60max_true_pixelcorr_Sys0.root", "recreate")
reweightingHisto.Write()
tf.Close()

tf = ROOT.TFile("PU/MyDataPileupHistogram_Run2012ABC_60max_true_pixelcorr_SysMinus5.root")
ROOT.gDirectory.cd("PyROOT:/")
reweightingHisto = tf.Get("pileup").Clone("ngoodVertices_Data")
tf.Close()
reweightingHisto.Scale(1./reweightingHisto.Integral())
reweightingHisto.Divide(S10)
tf = ROOT.TFile("PU/reweightingHisto_Summer2012-S10-Run2012ABC_60max_true_pixelcorr_SysPlus5.root", "recreate")
reweightingHisto.Write()
tf.Close()

tf = ROOT.TFile("PU/MyDataPileupHistogram_Run2012ABC_60max_true_pixelcorr_SysPlus5.root")
ROOT.gDirectory.cd("PyROOT:/")
reweightingHisto = tf.Get("pileup").Clone("ngoodVertices_Data")
tf.Close()
reweightingHisto.Scale(1./reweightingHisto.Integral())
reweightingHisto.Divide(S10)
tf = ROOT.TFile("PU/reweightingHisto_Summer2012-S10-Run2012ABC_60max_true_pixelcorr_SysMinus5.root", "recreate")
reweightingHisto.Write()
tf.Close()

tf = ROOT.TFile("PU/MyDataPileupHistogram_Run2012ABC_60max_true_pixelcorr_Sys0.root")
ROOT.gDirectory.cd("PyROOT:/")
reweightingHisto = tf.Get("pileup").Clone("ngoodVertices_Data")
tf.Close()
reweightingHisto.Scale(1./reweightingHisto.Integral())
reweightingHisto.Divide(S7)
tf = ROOT.TFile("PU/reweightingHisto_Summer2012-S7-Run2012ABC_60max_true_pixelcorr_Sys0.root", "recreate")
reweightingHisto.Write()
tf.Close()

tf = ROOT.TFile("PU/MyDataPileupHistogram_Run2012ABC_60max_true_pixelcorr_SysMinus5.root")
ROOT.gDirectory.cd("PyROOT:/")
reweightingHisto = tf.Get("pileup").Clone("ngoodVertices_Data")
tf.Close()
reweightingHisto.Scale(1./reweightingHisto.Integral())
reweightingHisto.Divide(S7)
tf = ROOT.TFile("PU/reweightingHisto_Summer2012-S7-Run2012ABC_60max_true_pixelcorr_SysPlus5.root", "recreate")
reweightingHisto.Write()
tf.Close()

tf = ROOT.TFile("PU/MyDataPileupHistogram_Run2012ABC_60max_true_pixelcorr_SysPlus5.root")
ROOT.gDirectory.cd("PyROOT:/")
reweightingHisto = tf.Get("pileup").Clone("ngoodVertices_Data")
tf.Close()
reweightingHisto.Scale(1./reweightingHisto.Integral())
reweightingHisto.Divide(S7)
tf = ROOT.TFile("PU/reweightingHisto_Summer2012-S7-Run2012ABC_60max_true_pixelcorr_SysMinus5.root", "recreate")
reweightingHisto.Write()
tf.Close()














tf = ROOT.TFile("PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_Sys0.root")
ROOT.gDirectory.cd("PyROOT:/")
reweightingHisto = tf.Get("pileup").Clone("ngoodVertices_Data")
tf.Close()
reweightingHisto.Scale(1./reweightingHisto.Integral())
reweightingHisto.Divide(S10)
tf = ROOT.TFile("PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_Sys0.root", "recreate")
reweightingHisto.Write()
tf.Close()

tf = ROOT.TFile("PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysMinus5.root")
ROOT.gDirectory.cd("PyROOT:/")
reweightingHisto = tf.Get("pileup").Clone("ngoodVertices_Data")
tf.Close()
reweightingHisto.Scale(1./reweightingHisto.Integral())
reweightingHisto.Divide(S10)
tf = ROOT.TFile("PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_SysPlus5.root", "recreate")
reweightingHisto.Write()
tf.Close()

tf = ROOT.TFile("PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysPlus5.root")
ROOT.gDirectory.cd("PyROOT:/")
reweightingHisto = tf.Get("pileup").Clone("ngoodVertices_Data")
tf.Close()
reweightingHisto.Scale(1./reweightingHisto.Integral())
reweightingHisto.Divide(S10)
tf = ROOT.TFile("PU/reweightingHisto_Summer2012-S10-Run2012ABCD_60max_true_pixelcorr_SysMinus5.root", "recreate")
reweightingHisto.Write()
tf.Close()

tf = ROOT.TFile("PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_Sys0.root")
ROOT.gDirectory.cd("PyROOT:/")
reweightingHisto = tf.Get("pileup").Clone("ngoodVertices_Data")
tf.Close()
reweightingHisto.Scale(1./reweightingHisto.Integral())
reweightingHisto.Divide(S7)
tf = ROOT.TFile("PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_Sys0.root", "recreate")
reweightingHisto.Write()
tf.Close()

tf = ROOT.TFile("PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysMinus5.root")
ROOT.gDirectory.cd("PyROOT:/")
reweightingHisto = tf.Get("pileup").Clone("ngoodVertices_Data")
tf.Close()
reweightingHisto.Scale(1./reweightingHisto.Integral())
reweightingHisto.Divide(S7)
tf = ROOT.TFile("PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_SysPlus5.root", "recreate")
reweightingHisto.Write()
tf.Close()

tf = ROOT.TFile("PU/MyDataPileupHistogram_Run2012ABCD_60max_true_pixelcorr_SysPlus5.root")
ROOT.gDirectory.cd("PyROOT:/")
reweightingHisto = tf.Get("pileup").Clone("ngoodVertices_Data")
tf.Close()
reweightingHisto.Scale(1./reweightingHisto.Integral())
reweightingHisto.Divide(S7)
tf = ROOT.TFile("PU/reweightingHisto_Summer2012-S7-Run2012ABCD_60max_true_pixelcorr_SysMinus5.root", "recreate")
reweightingHisto.Write()
tf.Close()

##Calculate T1tttt reweighting histo for reweighting wrt. reco nvtx
#cT1tttt = ROOT.TChain("Events")
#cT1tttt.Add("/data/mhickel/pat_121012/sms//8-TeV-T1tttt/h*.root")
#cT1tttt.Draw("ngoodVertices>>hMC(60,0,60)","ht>400&&met>100&&singleMuonic")
#hMC = ROOT.gDirectory.Get("hMC")
#hMC.Scale(1./hMC.Integral())
#
#cData = ROOT.TChain("Events")
#for b in  ['MuHad-Run2012A-13Jul2012', 'MuHad-Run2012B-13Jul2012', 'MuHad-Run2012C-PromptReco-v2', 'MuHad-Run2012C-PromptReco']:
#  cData.Add("/data/mhickel/pat_120927/data8TeV/"+b+"/h*.root")
#
#cData.Draw("ngoodVertices>>hData(60,0,60)","ht>400&&met>100&&singleMuonic")
#hData = ROOT.gDirectory.Get("hData")
#hData.Scale(1./hData.Integral())
#
#hData.Divide(hMC)
#hData.SetName("ngoodVertices_Data")
#hData.SetTitle("ngoodVertices_Data")
#
#tf = ROOT.TFile("PU/reweightingHisto_T1tttt-Run2012ABC-PromptReco_RecoNvtx.root", "recreate")
#hData.Write()
#tf.Close()

