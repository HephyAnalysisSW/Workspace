import ROOT
import math
from DataFormats.FWLite import Events, Handle
from navidPlotTools import *


def plot(chains,var,cut,prefix,suffix,bin=(),logX=0,logY=0,logZ=0,plotDir="./",format=".gif"):
  varName= ''.join(e for e in var if e.isalnum())
  canv=[ROOT.TCanvas("c1","c1",800,800)]
  chains[0].Draw(var+">>%s"%str(bin),cut,"")
  for chain in chains[1:]:
    chain.Draw(var,cut,"same")
  canv[0].SetLogx(logX)
  canv[0].SetLogy(logY)
  canv[0].SetLogz(logZ)
  saveCanvas(canv[0],"%s%s%s"%(prefix, varName ,suffix),plotDir=plotDir,format=format)
  return canv[0]


calcDeltaR = lambda phi1,phi2,eta1,eta2: math.sqrt( (phi1-phi2)**2 + (eta1-eta2)**2 )

def getHandle(iTree,fwEvt,iTyp,iLabel,iEvent=None):
  #events = Events(iTree)
  #events.toBegin()
  if not iEvent == None:
    iTree.GetEntry(iEvent)
    fwEvt.to(iEvent)
  gps = Handle(iTyp)
  lgp = iLabel
  fwEvt.getByLabel(lgp,gps)
  gps = gps.product()
  try:
    lgp = list(gps)
    #return lgp
    #print lgp
  except TypeError:
    lgp=[0]
    lgp[0]=gps

    #return gps
  return lgp









##### FOR CMG Chains:


def getCuts(chain,baseCut):
  cuts={}
  #chain=sc
  #baseCut="(abs(LepOther_pdgId)==11)"
  cuts['nocuts']    = 1.  *  chain.Draw("LepOther_pt","%s"%baseCut)
  cuts['absiso<5']  = 100.*  chain.Draw("LepOther_pt","(LepOther_relIso03*LepOther_pt < 5)&&%s"%baseCut) / cuts['nocuts']
  cuts['|eta|<2.4'] = 100.*  chain.Draw("LepOther_pt","(abs(LepOther_eta)<2.4)&&%s"%baseCut) / cuts['nocuts']
  cuts['|dxy|<0.02']= 100.*  chain.Draw("LepOther_pt","(abs(LepOther_dxy)<0.02)&&%s"%baseCut) / cuts['nocuts']
  cuts['|dz|<0.5']  = 100.*  chain.Draw("LepOther_pt","(abs(LepOther_dz)<0.5)&&%s"%baseCut)/ cuts['nocuts']
  cuts['|dz|<0.5 |dxy|<0.02']  =100.*  chain.Draw("LepOther_pt","(abs(LepOther_dxy)<0.02)&&(abs(LepOther_dz)<0.5)&&%s"%baseCut)/ cuts['nocuts']
  cuts['|dz|<0.5 |dxy|<0.02 absIso<5']  =100.*  chain.Draw("LepOther_pt"," (LepOther_relIso03*LepOther_pt < 5) && (abs(LepOther_dxy)<0.02)&&(abs(LepOther_dz)<0.5)&&%s"%baseCut)/ cuts['nocuts']
  cuts['all']    =100.*  chain.Draw("LepOther_pt","abs(LepOther_eta)<2.4&&abs(LepOther_dxy)<0.02&&abs(LepOther_dz)<0.5&&LepOther_pt>5&&(LepOther_relIso03*LepOther_pt < 5)&&%s"%baseCut)/cuts['nocuts']
  return cuts


def makeTable(cutDictList,outTitle):
  col=['   ']+[cutDict['name'] for cutDict in cutDictList]
  f2=open( './%s.tex'%outTitle,'wb')
  f2.write( '\documentclass{article} \n\usepackage[english]{babel}\n \usepackage[margin=0.5in]{geometry}  \n\usepackage[T1]{fontenc}\n\\begin{document}\
              \n\\begin{center}\n\\begin{tabular}')
  f2.write(' { |c | '+ '|'.join( 'l' for icol in col[1:len(col)]) +'| } \n' )
  f2.write('\\hline \n')
  f2.write( '&'.join(icol for icol in col) + ' \\\ \hline \n' )
  rowList= sorted(cutDictList[1]['cuts'].keys())
  rowList.remove("nocuts")
  rowList.insert(0,"nocuts")
  rowList.remove("all")
  rowList.append("all")
  for row in rowList:
    if row=="nocuts":
      f2.write(row +' & '+ ' & '.join([ format(cutDictList[i]['cuts'][row] ) + cutDictList[i]['lepCutName']  for i in range(len(cutDictList)) ] ))
    else: f2.write(row +' & '+ ' & '.join([ format(cutDictList[i]['cuts'][row],"0.2f") + '\\%'  for i in range(len(cutDictList)) ] ))
    f2.write('\\\ \hline \n')
  f2.write( '\end{tabular}\n\end{center}\n\end{document}')
  f2.close()
  print '%stex file written'%outTitle
  return
