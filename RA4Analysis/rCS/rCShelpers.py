import ROOT
import pickle
from Workspace.HEPHYPythonTools.helpers import *# getChain, getPlotFromChain, getYieldFromChain
from Workspace.RA4Analysis.helpers import *#nameAndCut, nJetBinName, nBTagBinName, varBinName
from math import sqrt, pi, cosh
from array import array

def makeWeight(lumi=4., sampleLumi=3.,debug=False):
  reWeight = 'lepton_muSF_mediumID*lepton_muSF_miniIso02*lepton_muSF_sip3d*lepton_eleSF_cutbasedID*lepton_eleSF_miniIso01'
  if debug:
    print 'No lumi-reweighting done!!'
    return 'weight', 'weight*weight'
  else:
    weight_str = '((weight/'+str(sampleLumi)+')*'+str(lumi)+'*'+reWeight+')'
    weight_err_str = '('+weight_str+'*'+weight_str+')'
  return weight_str, weight_err_str

def getTemplate(cutName, path, sampleName):
  temp = ROOT.TH1F()
  tempFile = ROOT.TFile(path+cutName+'_'+sampleName+'.root')
  if tempFile.IsOpen():
    print 'Found existing template at:',path,'and will use this one'
    temp = tempFile.Get('h_tmp')
    print temp
    return {'hist':temp, 'loadTemp':True, 'file':tempFile}
  else:
    print 'Could NOT find template at:',path,', creating new template now!'
    return {'hist':temp, 'loadTemp':False}
 
def getRandomHistOfTemplate(hist, color=ROOT.kOrange):
  h = ROOT.TH1F()
  hist.Copy(h)
  h.Reset()
  h.Sumw2()
  h.SetLineColor(color)
  h.FillRandom(hist, int(hist.GetEntries()))
  h.Scale(1./h.Integral()*hist.Integral())
  res = h.Clone()
  del h
  return res
 
#combine different Rcs values, where samples should look sth like this: [{'chain':c, 'cut':c, 'weight':w},...]
def combineRCS(samples, dPhiCut):
  totalCRYield = 0.
  totalCRYieldVar = 0.
  for s in samples:
    s['rcs'] = getRCS(s['chain'],s['cut'],dPhiCut, weight=s['weight'])
    s['CRyield'] = getYieldFromChain(s['chain'], cutString=s['cut']+'&&deltaPhi_Wl<'+str(dPhiCut),weight=s['weight'])
    #print s['rcs']['rCS'],s['rcs']['rCSE_sim'], s['CRyield']
    s['CRyieldVar'] = getYieldFromChain(s['chain'], cutString=s['cut']+'&&deltaPhi_Wl<'+str(dPhiCut),weight='('+s['weight']+')**2')
    totalCRYield += s['CRyield']
    totalCRYieldVar += s['CRyieldVar']
  totalRcs = 0.
  totalRcsVar = 0.
  for s in samples:
    if s['rcs']['rCS']>0:
      totalRcs += s['rcs']['rCS']*(s['CRyield']/totalCRYield)
      totalRcsVar += (s['rcs']['rCS']*(s['CRyield']/totalCRYield))**2*(s['rcs']['rCSE_sim']**2/s['rcs']['rCS']**2 + s['CRyieldVar']/s['CRyield']**2 + totalCRYieldVar/totalCRYield**2)
  return {'rCS':totalRcs, 'rCSE_sim':sqrt(totalRcsVar), 'rCSE_pred':1.}

#ROOT.TH1F().SetDefaultSumw2()

def getRCS(c, cut, dPhiCut, useGenMet=False, useAllGen=False, useOnlyGenMetPt=False, useOnlyGenMetPhi=False, useWeight = True, weight='weight', QCD_lowDPhi={'y':0.,'e':0.}, QCD_highDPhi={'y':0.,'e':0.}, cutVar='deltaPhi_Wl', varMax=pi): 
  if useGenMet: dPhiStr = "acos((leptonPt+met_genPt*cos(leptonPhi-met_genPhi))/sqrt(leptonPt**2+met_genPt**2+2*met_genPt*leptonPt*cos(leptonPhi-met_genPhi)))"
  elif useAllGen: dPhiStr = "acos((genLep_pt+met_genPt*cos(genLep_phi-met_genPhi))/sqrt(genLep_pt**2+met_genPt**2+2*met_genPt*genLep_pt*cos(genLep_phi-met_genPhi)))"
  elif useOnlyGenMetPt: dPhiStr = "acos((leptonPt+met_genPt*cos(leptonPhi-met_phi))/sqrt(leptonPt**2+met_genPt**2+2*met_genPt*leptonPt*cos(leptonPhi-met_phi)))"
  elif useOnlyGenMetPhi: dPhiStr = "acos((leptonPt+met_pt*cos(leptonPhi-met_genPhi))/sqrt(leptonPt**2+met_pt**2+2*met_pt*leptonPt*cos(leptonPhi-met_genPhi)))"
  else: dPhiStr = cutVar
  if useWeight:
    h = getPlotFromChain(c, dPhiStr, [0,dPhiCut,varMax], cutString=cut, binningIsExplicit=True, weight=weight)
  else:
    h = getPlotFromChain(c, dPhiStr, [0,dPhiCut,varMax], cutString=cut, binningIsExplicit=True, weight='1')
  h.Sumw2()
  if h.GetBinContent(1)>0:
    rcs = (h.GetBinContent(2) - QCD_highDPhi['y']) / (h.GetBinContent(1) - QCD_lowDPhi['y'])
    if h.GetBinContent(2)>0:
      rCSE_sim = rcs*sqrt((h.GetBinError(2)**2 + QCD_highDPhi['e']**2)/(h.GetBinContent(2) - QCD_highDPhi['y'])**2 + (h.GetBinError(1)**2 + QCD_lowDPhi['e']**2)/(h.GetBinContent(1) -QCD_lowDPhi['y'] )**2)
      rCSE_pred = rcs*sqrt((h.GetBinContent(2) + QCD_highDPhi['y'])/(h.GetBinContent(2) - QCD_highDPhi['y'])**2 + (h.GetBinContent(1) + QCD_lowDPhi['y'])/(h.GetBinContent(1) -QCD_lowDPhi['y'] )**2)
      
      #rCSE_sim = rcs*sqrt(h.GetBinError(2)**2/h.GetBinContent(2)**2 + h.GetBinError(1)**2/h.GetBinContent(1)**2) #errors without QCD consideration
      #rCSE_pred = rcs*sqrt(1./h.GetBinContent(2) + 1./h.GetBinContent(1)) #errors without QCD consideration
      del h
      return {'rCS':rcs, 'rCSE_pred':rCSE_pred, 'rCSE_sim':rCSE_sim}
    else:
      del h
      return {'rCS':rcs, 'rCSE_pred':float('nan'), 'rCSE_sim':float('nan')}
  else:
    del h
    return {'rCS':float('nan'), 'rCSE_pred':float('nan'), 'rCSE_sim':float('nan')}

#get Rcs value with event loop
def getRCSel(c, cut, dPhiCut, dPhiMetJet=0.45):
  dPhiStr = 'deltaPhi_Wl'
  c.Draw('>>eList',cut)
  elist = ROOT.gDirectory.Get("eList")
  number_events = elist.GetN()
  twoBin=[0,dPhiCut,3.2]
  h = ROOT.TH1F('h','h',len(twoBin)-1, array('d', twoBin))
  h.Sumw2()
  for i in range(number_events):
    c.GetEntry(elist.GetEntry(i))
    weight = getVarValue(c,"weight")
    deltaPhi = c.GetLeaf(dPhiStr).GetValue()
    if cmgMinDPhiJet(c, nJets=2)>dPhiMetJet: #optimize this cut value
      h.Fill(deltaPhi, weight)
    else: continue
  if h.GetBinContent(1)>0:
    rcs = h.GetBinContent(2)/h.GetBinContent(1)
    if h.GetBinContent(2)>0:
      rCSE_sim = rcs*sqrt(h.GetBinError(2)**2/h.GetBinContent(2)**2 + h.GetBinError(1)**2/h.GetBinContent(1)**2)
      rCSE_pred = rcs*sqrt(1./h.GetBinContent(2) + 1./h.GetBinContent(1))
      del h
      return {'rCS':rcs, 'rCSE_pred':rCSE_pred, 'rCSE_sim':rCSE_sim}
    else:
      del h
      return {'rCS':rcs, 'rCSE_pred':float('nan'), 'rCSE_sim':float('nan')}
  else:
    del h
    return {'rCS':float('nan'), 'rCSE_pred':float('nan'), 'rCSE_sim':float('nan')}
 
def getFOM(Ysig ,Ysig_Err , Ybkg,  Ybkg_Err):
  if Ybkg>0.0:
    FOM = Ysig/sqrt(Ybkg+(0.2*Ybkg)**2)
    return FOM
  else:
    return 'nan'

def dynDeltaPhi(dPhi=1.0, stb='def', htb='def', njb='def', nbjb='def'):
  if stb[0] >= 450:
    if njb[0] >= 6:
      dPhi = 0.75
  elif stb[0]>=350:
    if njb[0]>=8:
      dPhi = 0.75
  print 'Using deltaPhi value:',dPhi, 'with ST, HT, njet: ',stb, htb, njb 
  #deltaPhis = {'stb':{'htb':{'njb':{'nbjb':1.0}}}, }
  #deltaPhiD = {nan:{nan:{nan:1.0}}, (250,350):{nan:{nan:1.0}}, (350,450):{nan:{nan:0.75}}, (450,-1):{nan:{nan:0.5}}}

  #deltaPhi = {}#(250,350):1.2, (350,450):0.9, (450,-1):0.8, (450,600):0.7, (600,-1):0.6}
  #if stb in deltaPhi: dPhi = deltaPhi[stb]
  #else: print 'Using default deltaPhi value:',dPhi

  return dPhi


#don't use k_factor calculation right now it has to be optimized
#def getTTcorr(stb,htb,filename='hardSingleLeptonic_TTfitnjet_', dir='/afs/hephy.at/user/d/dhandl/www/pngCMG2/rCS/'):
#  binreg = nameAndCut(stb,htb,njetb=None)[0]
#  f0 = ROOT.TFile(dir+filename+binreg+'.root')
#  f1 = ROOT.TFile(dir+'hardSingleLeptonic_fullBkgFitnjet_'+binreg+'.root')
#  can0 = f0.Get('c1_n2')
#  can1 = f1.Get('c1_n2')
#  assert can0, 'Error: could not find TCanvas in '+str(f0)+str(f0.ls())
#  Profile_0b = can0.GetPrimitive('profile_rCS_njet_bTag0')
#  Profile_1b = can1.GetPrimitive('profile_rCS_njet_bTag1')
#  assert Profile_0b and Profile_1b,'Error: could not find TProfile'
#  FitPar0b = Profile_0b.GetFunction('pol0').GetParameter(0)
#  FitPar1b = Profile_1b.GetFunction('pol0').GetParameter(0)
#  FitParError0b = Profile_0b.GetFunction('pol0').GetParError(0)
#  FitParError1b = Profile_1b.GetFunction('pol0').GetParError(0)
#  assert Profile_0b.GetFunction('pol0') and Profile_1b.GetFunction('pol0'), 'Error: could not find Function'
#  k = FitPar0b/FitPar1b
#  k_E = k* sqrt(FitParError0b**2/FitPar0b**2 + FitParError1b**2/FitPar1b**2)
#  del f0
#  del f1
#  return {'k':k, 'k_Error':k_E}

def getNumString(n,ne, acc=2):    ##For printing table 
  if type(n) is float and type(ne) is float:
    return str(round(n,acc))+'&$\pm$&'+str(round(ne,acc))
  #if type(n) is str and type(ne) is str: 
  else:
    return n +'&$\pm$&'+ ne

def getNumStringWithSyst(n,eSys, eStat, acc=2):    ##For printing table 
  if type(n) is float and type(eSys) is float and type(eStat) is float:
    return str(round(n,acc))+'&$\pm$&'+str(round(eSys,acc)) +'&$\pm$&'+str(round(eStat,acc))
  #if type(n) is str and type(ne) is str: 
  else:
    return n +'&$\pm$&'+ eSys +'&$\pm$&'+ eStat

