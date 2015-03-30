import ROOT

c = ROOT.TChain('Events')
c.Add('/data/schoef/convertedMETTuples_v2//inc/dy53X_dy53X_rwTo_flat/histo_dy53X_from*.root')
#c.Add('/data/schoef/convertedMETTuples_v2//inc/dy53X_dy53X_rwTo_flat/histo_dy53X_from10To11.root')

c1 = ROOT.TCanvas()
c.Draw('log10(candW)>>hLow(100,-6,6)', 'sqrt(Sum$(candPt*candW*cos(candPhi))**2 + Sum$(candPt*candW*cos(candPhi))**2)<90')
c.Draw('log10(candW)>>h',    'sqrt(Sum$(candPt*candW*cos(candPhi))**2 + Sum$(candPt*candW*cos(candPhi))**2)>90','same')
c1.SetLogy()
h = ROOT.gDirectory.Get('h')
hLow = ROOT.gDirectory.Get('hLow')
h.SetLineColor(ROOT.kRed)
#h.Scale(hLow.Integral()/h.Integral())
hLow.Draw()
h.Draw('same')
c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/weight.png')
del h, hLow

#cut = '(candId==1||candId==4||candId==5)'
#prefix = 'only_h_h0_gamma_'
#cut = '(1)'
#prefix = ''

for cut, prefix in [['(candId==1||candId==4||candId==5)', 'only_h_h0_gamma_'], ['(1)', '']]:

  c1 = ROOT.TCanvas()
  c.Draw('sqrt(Sum$('+cut+'*candPt*cos(candPhi))**2 + Sum$('+cut+'*candPt*sin(candPhi))**2)>>hMet(100,0,400)')
  c.Draw('sqrt(Sum$('+cut+'*candW*candPt*cos(candPhi))**2 + Sum$('+cut+'*candW*candPt*sin(candPhi))**2)>>hMetRW','', 'same')
  c.Draw('sqrt(Sum$('+cut+'*max(min(2,candW),0.5)*candPt*cos(candPhi))**2 + Sum$('+cut+'*max(min(2,candW),0.5)*candPt*sin(candPhi))**2)>>hMetRW2','', 'same')
  c1.SetLogy()
  hMet = ROOT.gDirectory.Get('hMet')
  hMetRW = ROOT.gDirectory.Get('hMetRW')
  hMetRW2 = ROOT.gDirectory.Get('hMetRW2')
  hMet.SetLineColor(ROOT.kBlue)
  hMetRW.SetLineColor(ROOT.kRed)
  hMetRW2.SetLineColor(ROOT.kGreen)
  #h.Scale(hLow.Integral()/h.Integral())
  hMet.Draw()
  hMetRW.Draw('same')
  hMetRW2.Draw('same')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/weight_'+prefix+'Met.png')
  del hMet, hMetRW, hMetRW2


  c1 = ROOT.TCanvas()
  c.Draw('atan2(-Sum$('+cut+'*candPt*sin(candPhi)),  -Sum$('+cut+'*candPt*cos(candPhi)))>>hMetPhi(18,-pi,pi)')
  c.Draw('atan2(-Sum$('+cut+'*candW*candPt*sin(candPhi)),- Sum$('+cut+'*candW*candPt*cos(candPhi)))>>hMetPhiRW','', 'same')
  c.Draw('atan2(-Sum$('+cut+'*max(min(2,candW),0.5)*candPt*sin(candPhi)), -Sum$('+cut+'*max(min(2,candW),0.5)*candPt*cos(candPhi)))>>hMetPhiRW2','', 'same')
  c1.SetLogy(0)
  hMetPhi = ROOT.gDirectory.Get('hMetPhi')
  hMetPhiRW = ROOT.gDirectory.Get('hMetPhiRW')
  hMetPhiRW2 = ROOT.gDirectory.Get('hMetPhiRW2')
  hMetPhi.SetLineColor(ROOT.kBlue)
  hMetPhiRW.SetLineColor(ROOT.kRed)
  hMetPhiRW2.SetLineColor(ROOT.kGreen)
  #h.Scale(hLow.Integral()/h.Integral())
  hMetPhi.Draw()
  hMetPhiRW.Draw('same')
  hMetPhiRW2.Draw('same')
  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/weight_'+prefix+'MetPhi.png')
  del hMetPhi, hMetPhiRW, hMetPhiRW2
