import ROOT
import pickle
from commons import label, categories
from Workspace.HEPHYCommonTools.helpers import getVarValue
from math import pi, cos, sin, sqrt, atan2
ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()
niceName = {'HF_m':"HF, minus side", 'HF_p':"HF, plus side", 'pE':"Endcap, plus side", 'mE':"Endcap, minus side", 'pB':"Barrel, plus side", 'mB':"Barrel, minus side", '':'inclusive'}
shortName ={'HF_m':"HF-", 'HF_p':"HF+", 'pE':"E+", 'mE':"E-"}

ver = 'v3'
c = ROOT.TChain('Events')
#c.Add('/data/schoef/convertedMETTuples_v1/Mu-DYJetsToLL-M50/histo_'+ver+'.root')
c.Add('/afs/hephy.at/newscratch/s/schoefbeck/histo_'+ver+'.root')

#binning={
#  'egamma_HF_m':[25,0,400],
#  'egamma_HF_p':[25,0,400],
#  'h_HF_m':[25,0,400],
#  'h_HF_p':[25,0,400],
#  'h_pE':[25,0,700],
#  'h_mE':[25,0,700],
#  'h_pB':[25,0,700],
#  'h_mB':[25,0,700],
#  'h0_pE':[20,0,60],
#  'h0_mE':[20,0,60],
#  'h0_pB':[25,0,50],
#  'h0_mB':[25,0,50],
#  'gamma_pE':[25,0,300],
#  'gamma_mE':[25,0,300],
#  'gamma_pB':[25,0,300],
#  'gamma_mB':[25,0,300],
#}
#fitrange={
#  'egamma_HF_m':[50,150],
#  'egamma_HF_p':[50,150],
#  'h_HF_m':[25,300],
#  'h_HF_p':[25,300],
#  'h_pE':[0,500],
#  'h_mE':[0,500],
#  'h_pB':[0,500],
#  'h_mB':[0,500],
#  'h0_pE':[0,40],
#  'h0_mE':[0,40],
#  'h0_pB':[0,25],
#  'h0_mB':[0,25],
#  'gamma_pE':[0,200],
#  'gamma_mE':[0,200],
#  'gamma_pB':[0,200],
#  'gamma_mB':[0,200],
#}
#zoomRange = {'gamma_pE':[-5,5], 'gamma_mE':[-5,5], 'gamma_pB':[-5,5], 'gamma_mB':[-5,5], 'h_HF_p':[-15,15], 'h_HF_m':[-15,15], 'egamma_HF_p':[-5,5], 'egamma_HF_m':[-5,5], 'h0_mB':[-5,5], 'h0_pB':[-5,5], \
#             'h0_mE':[-15,15], 'h0_pE':[-15,15], 'h_mB':[-15,15], 'h_pB':[-15,15], 'h_mE':[-15,15], 'h_pE':[-15,15]}
#shifts = {}
#for cat in categories.values():
#  for etab in cat:
#    px=ROOT.TProfile("p_MEx","p_MEx",*(binning[etab[0]]+[-200,200,'i']))
#    py=ROOT.TProfile("p_MEy","p_MEy",*(binning[etab[0]]+[-200,200,'i']))
#    linx = ROOT.TF1('linx', '[0]*x+[1]',*(fitrange[etab[0]]))
#    c.Draw('MEx_'+etab[0]+':nCand_'+etab[0]+'>>p_MEx','','goff')
#    px.Fit(linx, 'R')
#    shifts['MEx_'+etab[0]]=linx.Clone()
#
#    c.Draw('MEy_'+etab[0]+':nCand_'+etab[0]+'>>p_MEy','','goff')
#    liny = ROOT.TF1('liny', 'pol1', *(fitrange[etab[0]]))
#    py.Fit(liny,'R')
#    shifts['MEy_'+etab[0]]=liny.Clone()
#
#
#    c1 = ROOT.TCanvas()  
#    ROOT.gStyle.SetOptStat(0)
#    ROOT.gStyle.SetOptFit(0)
#    px.Draw('h')
#    px.GetXaxis().SetTitle("multiplicity of '"+etab[0].split('_')[0]+"' in "+niceName['_'.join(etab[0].split('_')[1:])])
#    px.GetYaxis().SetTitle("<#slash{E}_{x,y}> (GeV)")
##    px.GetXaxis().SetLabelSize(0.04)
#    px.GetXaxis().SetTitleSize(0.05)
#    px.GetXaxis().SetTitleOffset(1.1)
#    px.GetYaxis().SetRangeUser(*(zoomRange[etab[0]]))
#    px.SetLineColor(ROOT.kBlue)
#    px.SetLineStyle(0)
#    px.SetLineWidth(2)
#    px.SetMarkerStyle(0)
#    px.SetMarkerSize(0)
##    py.GetYaxis().SetRangeUser(-20,20)
#    py.SetLineColor(ROOT.kRed)
#    py.SetLineStyle(0)
#    py.SetLineWidth(2)
#    py.SetMarkerStyle(0)
#    py.SetMarkerSize(0)
#    py.Draw('hsame')
#
#    if linx.GetParameter(1)>0:
#      sign = "+"
#    else:
#      sign = "-"
#    lines = [ [0.45, 0.78,  "<#slash{E}_{x}> = "+str(round(linx.GetParameter(0),4))+" "+sign+" "+str(round(abs(linx.GetParameter(1)),4))+"*n"],
#              [0.45, 0.73, "<#slash{E}_{y}> = "+str(round(liny.GetParameter(0),4))+" "+sign+" "+str(round(abs(liny.GetParameter(1)),4))+"*n"]]
#
#    latex = ROOT.TLatex();
#    latex.SetNDC();
#    latex.SetTextSize(0.04);
#    latex.SetTextAlign(11); # align right
#    for line in lines:
#        latex.SetTextSize(0.04)
#        latex.DrawLatex(line[0],line[1],line[2])
#    l = ROOT.TLegend(0.55,0.83,.95,.95)
#    l.AddEntry(px, "< #slash{E}_{x} >")#+etab[0].split('_')[0]+", "+shortName[etab[0].split('_')[1]])
#    l.AddEntry(py, "< #slash{E}_{y} >")
#    l.SetFillColor(0)
#    l.SetShadowColor(ROOT.kWhite)
#    l.SetBorderSize(1)
#    l.Draw()
#    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+ver+'_MExy_'+etab[0]+'.png')
#    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+ver+'_MExy_'+etab[0]+'.root')
#    del px, py, l, c1
#
#pickle.dump(shifts, file('/data/schoef/tools/metPhiShifts/shifts_'+ver+'.pkl', 'w'))
#
shifts = pickle.load(file('/data/schoef/tools/metPhiShifts/shifts_'+ver+'.pkl'))
mphi = {}
mphi_corr={}
m = {}
m_corr={}
mx = {}
mx_corr={}
my = {}
my_corr={}
mphi['all']      = ROOT.TH1F('metphi','metphi', 30,-pi,pi)
mphi_corr['all'] = ROOT.TH1F('metphi','metphi', 30,-pi,pi)
mphi_corr['all'].SetLineColor(ROOT.kRed)
m['all']      = ROOT.TH1F('met','met', 200,0,100)
m_corr['all'] = ROOT.TH1F('met','met', 200,0,100)
m_corr['all'].SetLineColor(ROOT.kRed)
mx['all']      = ROOT.TH1F('metx','metx', 200,-100,100)
mx_corr['all'] = ROOT.TH1F('metx','metx', 200,-100,100)
mx_corr['all'].SetLineColor(ROOT.kRed)
my['all']      = ROOT.TH1F('mety','mety', 200,-100,100)
my_corr['all'] = ROOT.TH1F('mety','mety', 200,-100,100)
my_corr['all'].SetLineColor(ROOT.kRed)
for s in [k[4:] for k in shifts.keys()]:
  mphi[s]      = ROOT.TH1F('metphi_'+s,'metphi_'+s, 30,-pi,pi)
  mphi_corr[s] = ROOT.TH1F('metphi_'+s,'metphi_'+s, 30,-pi,pi)
  mphi_corr[s].SetLineColor(ROOT.kRed)
  m[s]      = ROOT.TH1F('met_'+s,'met_'+s, 200,0,100)
  m_corr[s] = ROOT.TH1F('met_'+s,'met_'+s, 200,0,100)
  m_corr[s].SetLineColor(ROOT.kRed)
  mx[s]      = ROOT.TH1F('metx_'+s,'metx_'+s,200,-100,100)
  mx_corr[s] = ROOT.TH1F('metx_'+s,'metx_'+s,200,-100,100)
  mx_corr[s].SetLineColor(ROOT.kRed)
  my[s]      = ROOT.TH1F('mety_'+s,'mety_'+s,200,-100,100)
  my_corr[s] = ROOT.TH1F('mety_'+s,'mety_'+s,200,-100,100)
  my_corr[s].SetLineColor(ROOT.kRed)
prefix = 'ptZ100' 
c.Draw(">>eList", 'ptZ>100')
eList = ROOT.gDirectory.Get('eList')
n = eList.GetN()
#n=20000
for i in range(n):
  if i%1000==0:
    print i,'/',n
  c.GetEntry(eList.GetEntry(i))
  tot_shift_x = 0.
  tot_shift_y = 0.
  tot_MEx = 0. 
  tot_MEy = 0. 
  for cat in categories.values():
    for etab in cat:
#      if not etab[0]=='gamma_mB':continue
      nCand = eval('c.nCand_'+etab[0])
      shift_x = -shifts['MEx_'+etab[0]].Eval(nCand)  
      shift_y = -shifts['MEy_'+etab[0]].Eval(nCand)  
      tot_shift_x += shift_x 
      tot_shift_y += shift_y 
      MEx = eval('c.MEx_'+etab[0]) 
      MEy = eval('c.MEy_'+etab[0])
      mx[etab[0]].Fill(MEx) 
      my[etab[0]].Fill(MEy)
      m[etab[0]].Fill(sqrt(MEx**2+MEy**2)) 
      mphi[etab[0]].Fill(atan2(MEy, MEx))
      MEx_corr=MEx+shift_x
      MEy_corr=MEy+shift_y 
      mphi_corr[etab[0]].Fill(atan2(MEy_corr, MEx_corr))
      mx_corr[etab[0]].Fill(MEx_corr)
      my_corr[etab[0]].Fill(MEy_corr)
      m_corr[etab[0]].Fill(sqrt(MEx_corr**2+MEy_corr**2))

      tot_MEx+=MEx 
      tot_MEy+=MEy 
#  tot_MEx = eval('c.MEx') 
#  tot_MEy = eval('c.MEy')
#  print tot_MEx, eval('c.MEx'),  tot_MEy, eval('c.MEy') 
  tot_MEx_corr = tot_MEx+tot_shift_x
  tot_MEy_corr = tot_MEy+tot_shift_y
  mphi['all'].Fill(atan2(tot_MEy, tot_MEx)) 
  mphi_corr['all'].Fill(atan2(tot_MEy_corr , tot_MEx_corr)) 
 
  mx_corr['all'].Fill(tot_MEx_corr)
  my_corr['all'].Fill(tot_MEy_corr)
  m_corr['all'].Fill(sqrt(tot_MEx_corr**2+tot_MEy_corr**2))
  mx['all'].Fill(tot_MEx)
  my['all'].Fill(tot_MEy)
  m['all'].Fill(sqrt(tot_MEx**2+tot_MEy**2))

varname = {'metPhi':"#phi(#slash{E})", 'MEt':'#slash{E}_{T}','MEx':'#slash{E}_{x}', 'MEy':'#slash{E}_{y}'}
for d, d_corr, name in [[mphi, mphi_corr,'metPhi'], [m, m_corr, 'MEt'], [mx,mx_corr,'MEx'], [my, my_corr, 'MEy']]:
  for k in d.keys():
#    if k!='gamma_mB':continue
    c1 = ROOT.TCanvas()
    if name!='metPhi':
      c1.SetLogy()
      d[k].GetYaxis().SetRangeUser(1.,10**1.5*d[k].GetBinContent(d[k].GetMaximumBin()))
    else:
      c1.SetLogy(0)
      d[k].GetYaxis().SetRangeUser(1.,1.5*d[k].GetBinContent(d[k].GetMaximumBin()))
    d[k].GetXaxis().SetTitle(varname[name]+" for '"+k.split('_')[0]+"' in "+niceName['_'.join(k.split('_')[1:])])
    d[k].GetYaxis().SetTitle("Number of Events")
    d[k].GetXaxis().SetTitleSize(0.05)
    d[k].GetXaxis().SetTitleOffset(1.1)
  #  d[k].GetYaxis().SetRangeUser(*(zoomRange[k]))
    d[k].SetLineColor(ROOT.kBlue)
    d[k].SetLineStyle(0)
    d[k].SetLineWidth(2)
    d[k].SetMarkerStyle(0)
    d[k].SetMarkerSize(0)
    d_corr[k].SetLineColor(ROOT.kRed)
    d_corr[k].SetLineStyle(0)
    d_corr[k].SetLineWidth(2)
    d_corr[k].SetMarkerStyle(0)
    d_corr[k].SetMarkerSize(0)
    d[k].Draw()
    d_corr[k].Draw('same')
    l = ROOT.TLegend(0.55,0.83,.95,.95)
    l.AddEntry(d[k], "raw")#+etab[0].split('_')[0]+", "+shortName[etab[0].split('_')[1]])
    l.AddEntry(d_corr[k], "corrected")
    l.SetFillColor(0)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    l.Draw()
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+prefix+"_"+ver+'_'+name+'_corr_'+k+'.png')
    c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+prefix+"_"+ver+'_'+name+'_corr_'+k+'.root')
    del c1
#  c1 = ROOT.TCanvas()
#  m[k].Draw()
#  c1.SetLogy()
#  m_corr[k].Draw('same')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+ver+'_met_corr_'+k+'.png')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+ver+'_met_corr_'+k+'.root')
#  del c1
#  c1 = ROOT.TCanvas()
#  c1.SetLogy()
#  mx[k].Draw()
#  mx_corr[k].Draw('same')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+ver+'_metx_corr_'+k+'.png')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+ver+'_metx_corr_'+k+'.root')
#  del c1
#  c1 = ROOT.TCanvas()
#  c1.SetLogy()
#  my[k].Draw()
#  my_corr[k].Draw('same')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+ver+'_mety_corr_'+k+'.png')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngPF/'+ver+'_mety_corr_'+k+'.root')
#  del c1
 
