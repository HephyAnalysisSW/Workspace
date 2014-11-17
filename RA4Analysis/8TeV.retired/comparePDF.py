import pickle
from analysisHelpers import getObjFromFile
import ROOT
from smsInfo import *
from math import sqrt
sms = "T1tttt-madgraph"
sms = "T1tttt"

c = ROOT.TChain("Events")
print "Chaining",sms,"for 1300, 800"
#model point: 1300/800
if sms=="T1tttt":
  for d in ['/data/mhickel/pat_130426/8TeV-T1tttt//histo_2085_1_ce9.root',\
            '/data/mhickel/pat_130426/8TeV-T1tttt//histo_2120_1_71J.root',
            '/data/mhickel/pat_130426/8TeV-T1tttt//histo_2407_1_6Aq.root',
            '/data/mhickel/pat_130426/8TeV-T1tttt//histo_2952_1_y1m.root',
            '/data/mhickel/pat_130426/8TeV-T1tttt//histo_326_3_TFl.root',
            '/data/mhickel/pat_130426/8TeV-T1tttt//histo_327_2_Qcy.root',
            '/data/mhickel/pat_130426/8TeV-T1tttt//histo_410_2_c7Z.root',
            '/data/mhickel/pat_130426/8TeV-T1tttt//histo_414_1_YEd.root',
            '/data/mhickel/pat_130426/8TeV-T1tttt//histo_415_2_Uuy.root',
            '/data/mhickel/pat_130426/8TeV-T1tttt//histo_432_3_0O0.root',
            '/data/mhickel/pat_130426/8TeV-T1tttt//histo_479_1_dBH.root',
            '/data/mhickel/pat_130426/8TeV-T1tttt//histo_480_2_OmV.root']:
    c.Add(d)

if sms=="T1tttt-madgraph":
  for d in [ '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_103_1_GBY.root',\
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_104_1_bRd.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_124_1_0ac.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_1842_1_1Ub.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2281_1_fHw.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_23_1_QYq.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_259_1_TSz.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_260_1_OFP.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_26_1_bUP.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_282_1_iKz.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2860_1_0VN.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2901_1_13O.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2902_1_tHw.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2906_1_2IP.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2907_1_N0L.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2919_1_h3V.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2920_1_zh8.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2921_1_uMn.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2948_1_NdW.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2949_1_NNN.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2950_1_NXY.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2951_1_v0c.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2952_1_6TW.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2966_1_NIV.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2983_1_s7L.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2984_1_Irv.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2985_1_kQu.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2986_1_5cm.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2989_1_6OL.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2990_1_2LF.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_2991_1_AzW.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_300_1_Pw2.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3028_1_z3M.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3040_1_Iwt.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3051_1_cTR.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3057_1_2TM.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_307_1_ZyO.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3082_1_zDC.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3101_1_kTb.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3102_1_sCT.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3130_1_vVe.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3186_2_Jlh.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3209_1_6eR.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3211_1_rYa.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3222_1_5PH.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_325_1_X9f.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3277_1_znO.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3285_1_0V2.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3520_1_Pcf.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3521_1_Z4x.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3543_1_L4g.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3581_1_rzU.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_359_1_z8p.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3603_1_8uF.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3645_1_7r7.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3652_1_IEr.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3664_1_XkH.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_3673_1_rMT.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_374_1_mRH.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_62_1_Dmt.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_66_1_Xpc.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_7_1_dMb.root',
             '/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2//histo_83_1_Hx0.root']:
    c.Add(d)
#
#c.Draw(">>eList","osetMgl==1300&&osetMN==800")
#print "Got eList..."
#eList = ROOT.gDirectory.Get("eList")
#fileNames=[]
#for i in range(eList.GetN()):
#  if i%10000==0:
#    print i
#  c.GetEntry(eList.GetEntry(i))
#  f=c.GetFile().GetName()
#  if not fileNames.count(f):
#    fileNames.append(f)

signalRegions = [ \
  {'btb':'2', 'htb':(750,2500), 'metb':(250,350)},
#  {'btb':'2', 'htb':(750,2500), 'metb':(350,450)},
#  {'btb':'2', 'htb':(750,2500), 'metb':(450,2500)},
#  {'btb':'3p', 'htb':(750,2500), 'metb':(150,250)},
#  {'btb':'3p', 'htb':(750,2500), 'metb':(250,350)},
#  {'btb':'3p', 'htb':(750,2500), 'metb':(350,450)},
#  {'btb':'3p', 'htb':(750,2500), 'metb':(450,2500)},
#  {'btb':'3p', 'htb':(400,750), 'metb':(150,250)},
#  {'btb':'3p', 'htb':(400,750), 'metb':(250,2500)},
]

l={"cteq":44, "mstw":40, "nnpdf":100}

for sr in signalRegions:
  htb = sr['htb'];metb = sr['metb'];btb = sr['btb']
  pdfUncert = {}
  relErr={}
  for pdft in ["cteq", "mstw","nnpdf"]:
    print pdft, sr
    iname = "h_"+sms+'_'+pdft+"_btb"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])
    filename = '/data/schoef/results2012/pdfUncertainty/'+sms+'/'+iname+'.pkl'
    h = pickle.load(file(filename))
    inameRef = "h_"+sms+'_'+pdft+"_btbnone_ht_0_2500_met_0_2500"
    filenameRef = '/data/schoef/results2012/pdfUncertainty/'+sms+'/'+inameRef+'.pkl'
    hRef = pickle.load(file(filenameRef))
#    print "Loaded",filename,filenameRef
    h.Divide(hRef)
#    pdfUncert[pdft]  = ROOT.TH2D("Uncertainty_"+pdft, "Uncertainty_"+pdft, h.GetNbinsX(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax(),  h.GetNbinsY(), h.GetYaxis().GetXmin(), h.GetYaxis().GetXmax())
#    pdfUncert[pdft].GetXaxis().SetTitle(xAxisTitle[sms])
#    pdfUncert[pdft].GetYaxis().SetTitle(xAxisTitle[sms])
##    for ix in range(1, h.GetNbinsX() + 1):
##      for iy in range(1, h.GetNbinsY() +1):
#
    ix = h.GetXaxis().FindBin(1300) 
    iy = h.GetYaxis().FindBin(800) 

    varX = h.GetXaxis().GetBinLowEdge(ix)
    varY  = h.GetYaxis().GetBinLowEdge(iy)
    print varX, varY
    x0 = h.GetBinContent(h.FindBin(varX, varY, 0))
    Delta2XMaxPlus  = 0
    Delta2XMaxMinus = 0
    for iUnc in range(l[pdft]/2):
      nPlus =  1 + 2*iUnc
      nMinus = 2 + 2*iUnc
      xip = h.GetBinContent(h.FindBin(varX, varY, nPlus))
      xim = h.GetBinContent(h.FindBin(varX, varY, nMinus))
      Delta2XMaxPlus  += max(xip - x0, xim - x0, 0)**2
      Delta2XMaxMinus += max(x0 - xip, x0 - xim, 0)**2
#        print "Setting", ix, iy, x0, 0.5*(sqrt(Delta2XMaxPlus) - sqrt(Delta2XMaxMinus))
#    if x0>0.:
    print "ref efficiency",x0, sqrt(Delta2XMaxPlus)/x0, sqrt(Delta2XMaxMinus)/x0,'->rel.err.:',abs(0.5*(sqrt(Delta2XMaxPlus) + sqrt(Delta2XMaxMinus)) / x0)
    relErr[pdft] = abs(0.5*(sqrt(Delta2XMaxPlus) + sqrt(Delta2XMaxMinus)) / x0)
  print "sys unc.:",(relErr['cteq'] + relErr['mstw'] + relErr['nnpdf'])/3.
#      pdfUncert[pdft].SetBinContent(pdfUncert[pdft].FindBin(varX, varY),  abs(0.5*(sqrt(Delta2XMaxPlus) + sqrt(Delta2XMaxMinus)) / x0))
  canv = getObjFromFile('/data/schoef/results2012/'+sms+'/PDF/sigPDFSys_'+sms+'_btb'+btb+'_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+'.root', 'c1')
  hInLimit = canv.GetPrimitive('hist2DSFunc').Clone()
  b = hInLimit.FindBin(1300,800)
  print "Used in Limit:",sms,hInLimit.GetBinContent(b)

