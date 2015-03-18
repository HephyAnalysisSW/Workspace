import os,sys,ROOT,pickle
#from localInfo import username
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getVarValue
from commons import *#pfTypes, label, ptBins, allMaps

def getReweightingHistos(mapSample = 'dy53X', reweightToSample='flat'):
  reweightHistos={}
  for map in allMaps:
#  for map in [h_HF_Plus]:
    t=map['type']
    if not reweightHistos.has_key(t):
      reweightHistos[t]={}
    for ptBin in ptBins:
      if not reweightHistos[t].has_key(tuple(ptBin)):
        reweightHistos[t][tuple(ptBin)]={}
      name = map['name']+'_pt_'+str(ptBin[0]) 
      if ptBin[1]>0:
        name+="_"+str(ptBin[1])
      ifile = '/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+mapSample+'_pt_'+name+'.root'
      f = ROOT.TFile(ifile)
      k = f.GetListOfKeys()[0].GetName()
      f.Close()
      canv = getObjFromFile(ifile, k)
      ptb = canv.GetPrimitive('pt_'+map['name']).Clone(mapSample+'_pt_'+name)
      if reweightToSample.lower()!='flat':
        ifile = '/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/'+reweightToSample+'_pt_'+name+'.root'
        f = ROOT.TFile(ifile)
        k = f.GetListOfKeys()[0].GetName()
        f.Close()
        canv = getObjFromFile(ifile, k)
        ptbRWT = canv.GetPrimitive('pt_'+map['name']).Clone(reweightToSample+'_pt_'+name)
      a = ptb.GetXaxis()
      etaBinning = [a.GetNbins(), a.GetXmin(),  a.GetXmax()]
      for i in range(1,1+etaBinning[0]):
        h=ptb.ProjectionY(name+'_etaBin_'+str(i),i,i)
        integr = h.Integral()
        if integr>0:
          h.Scale(h.GetNbinsX()/integr)
#        print i,name+'_etaBin_'+str(i),integr, h.GetNbinsX()/integr, h.GetBinContent(6)
        if reweightToSample.lower()!='flat': 
          hRWT=ptbRWT.ProjectionY(name+'_RWT_etaBin_'+str(i),i,i)
          integr = hRWT.Integral()
          if integr>0:
            hRWT.Scale(hRWT.GetNbinsX()/integr)
        for b in range(0, 1+h.GetNbinsX()):
          if h.GetBinContent(b)>0:
            if reweightToSample.lower()!='flat':
  #            print name+'_etaBin_'+str(i), hRWT.GetBinContent(b), h.GetBinContent(b)
              h.SetBinContent(b, hRWT.GetBinContent(b)/h.GetBinContent(b))
            else:
  #            print name+'_etaBin_'+str(i), hRWT.GetBinContent(b), h.GetBinContent(b)
              h.SetBinContent(b, 1./h.GetBinContent(b))
#        print 'Now',i,name+'_etaBin_'+str(i), h.GetBinContent(6)
        reweightHistos[t][tuple(ptBin)][(a.GetBinLowEdge(i), a.GetBinUpEdge(i))]=h
  return reweightHistos 

#print reweightHistos
#
#  metPhi = ROOT.TH1F('metPhi','metPhi',30,-pi,pi)
#  metPhiCorr = ROOT.TH1F('metPhiCorr','metPhiCorr',30,-pi,pi)
#  metPhiCorrPt = ROOT.TH1F('metPhiCorrPt','metPhiCorrPt',30,-pi,pi)
#  met = ROOT.TH1F('met','met',100,0,100)
#  metCorr = ROOT.TH1F('metCorr','metCorr',100,0,100)
#  metCorrPt = ROOT.TH1F('metCorrPt','metCorrPt',100,0,100)
#  metx = ROOT.TH1F('metx','metx',100,-100,100)
#  metxCorr = ROOT.TH1F('metxCorr','metxCorr',100,-100,100)
#  metxCorrPt = ROOT.TH1F('metxCorrPt','metxCorrPt',100,-100,100)
#  mety = ROOT.TH1F('mety','mety',100,-100,100)
#  metyCorr = ROOT.TH1F('metyCorr','metyCorr',100,-100,100)
#  metyCorrPt = ROOT.TH1F('metyCorrPt','metyCorrPt',100,-100,100)
#
#  nEvents = min([30000, c.GetEntries()])
#  for i in range(nEvents):
#    if i%100==0:print "At",i,"/",nEvents
#    mexUncorr = 0.
#    meyUncorr = 0.
#    mexCorr = 0.
#    meyCorr = 0.
#    mexCorrPt = 0.
#    meyCorrPt = 0.
#    c.GetEntry(i)
#    nCand = getVarValue (c, 'nCand')
#    counter=0
#    for j in range(int(nCand)):
#      if label[getVarValue(c, 'candId', j)] == t:
#        pt = getVarValue (c, 'candPt', j)
#        if pt>=ptBin[0] and pt<ptBin[1]:
#          counter+=1
#          eta = getVarValue (c, 'candEta', j)
#          etaBin =  a.FindBin(eta)
#          phi = getVarValue (c, 'candPhi', j)
#          phiBin = projOcc[etaBin].FindBin(phi)
#          resOcc = projOcc[etaBin].GetBinContent(phiBin)
#          weightOcc=1.
#          if resOcc>0:
#            weightOcc=1./resOcc
#          resPt = projPt[etaBin].GetBinContent(phiBin)
#          weightPt=1.
#          if resPt>0:
#            weightPt=1./resPt
#  #        print i,j,weight,'pt',pt,'eta',eta,'phi',phi
#          cp = cos(phi)
#          sp = sin(phi)
#          dmx=cp*pt
#          dmy=sp*pt
#          mexUncorr-=dmx
#          meyUncorr-=dmy
#          mexCorr-=dmx*weightOcc
#          meyCorr-=dmy*weightOcc
#          mexCorrPt-=dmx*weightPt
#          meyCorrPt-=dmy*weightPt
#    if counter>0:
#      metPhi.Fill(atan2(meyUncorr, mexUncorr))
#      metPhiCorr.Fill(atan2(meyCorr, mexCorr))
#      metPhiCorrPt.Fill(atan2(meyCorrPt, mexCorrPt))
#      met.Fill(sqrt(mexUncorr**2+meyUncorr**2))
#      metCorr.Fill(sqrt(mexCorr**2+meyCorr**2))
#      metCorrPt.Fill(sqrt(mexCorrPt**2+meyCorrPt**2))
#      metx.Fill(mexUncorr)
#      metxCorr.Fill(mexCorr)
#      metxCorrPt.Fill(mexCorrPt)
#      mety.Fill(meyUncorr)
#      metyCorr.Fill(meyCorr)
#      metyCorrPt.Fill(meyCorrPt)
#
#  c1 = ROOT.TCanvas()
#  metPhi.SetLineColor(ROOT.kBlue)
#  metPhi.Draw()
#  metPhiCorr.SetLineColor(ROOT.kRed)
#  metPhiCorr.Draw('same')
#  metPhiCorrPt.SetLineColor(ROOT.kGreen)
#  metPhiCorrPt.Draw('same')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/metPhi_comparison_'+sample+'_'+t+'_pt_'+str(ptBin[0])+'_'+str(ptBin[1])+'.png')
#
#  c1 = ROOT.TCanvas()
#  met.SetLineColor(ROOT.kBlue)
#  met.Draw()
#  metCorr.SetLineColor(ROOT.kRed)
#  metCorr.Draw('same')
#  metCorrPt.SetLineColor(ROOT.kGreen)
#  metCorrPt.Draw('same')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/met_comparison_'+sample+'_'+t+'_pt_'+str(ptBin[0])+'_'+str(ptBin[1])+'.png')
#
#  c1 = ROOT.TCanvas()
#  metx.SetLineColor(ROOT.kBlue)
#  metx.Draw()
#  metxCorr.SetLineColor(ROOT.kRed)
#  metxCorr.Draw('same')
#  metxCorrPt.SetLineColor(ROOT.kGreen)
#  metxCorrPt.Draw('same')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/metx_comparison_'+sample+'_'+t+'_pt_'+str(ptBin[0])+'_'+str(ptBin[1])+'.png')
#
#  c1 = ROOT.TCanvas()
#  mety.SetLineColor(ROOT.kBlue)
#  mety.Draw()
#  metyCorrPt.SetLineColor(ROOT.kGreen)
#  metyCorrPt.Draw('same')
#  c1.Print('/afs/hephy.at/user/s/schoefbeck/www/pngMetPhi/mety_comparison_'+sample+'_'+t+'_pt_'+str(ptBin[0])+'_'+str(ptBin[1])+'.png')
