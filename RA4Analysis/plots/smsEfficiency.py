import ROOT, pickle, os
from math import sqrt

ROOT.gROOT.ProcessLine(".L ../../Scripts/aclic/tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.ProcessLine(".L ../../Scripts/aclic/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)
#ROOT.tdrStyle.SetPadRightMargin(0.16)
ROOT.gStyle.SetPadRightMargin(0.18)

ROOT.gROOT.ProcessLine(".L ../limits/TriangularInterpolation.C+")
ROOT.gROOT.ProcessLine(".L ../limits/SmoothingUtils.C+")


from optparse import OptionParser

parser = OptionParser()
parser.add_option("--htl", dest="htl", default=0, type="int", action="store", help="lower HT border")
parser.add_option("--hth", dest="hth", default=2500, type="int", action="store", help="higher HT border")
parser.add_option("--metl", dest="metl", default=0, type="int", action="store", help="lower met border")
parser.add_option("--meth", dest="meth", default=2500, type="int", action="store", help="higher met border")
#parser.add_option("--pdft", dest="pdft", default='cteq', type="string", action="store", help="pdf type ('cteq', 'mstw',  or 'nnpdf')")
parser.add_option("--btb", dest="btb", default='none', type="string", action="store", help="btag bin")
parser.add_option("--njetMin", dest="njetMin", default=6, type="int", action="store", help="min njet")
parser.add_option("--njetMax", dest="njetMax", default=99, type="int", action="store", help="max njet")
parser.add_option("--small", action="store_true", dest="small")
parser.add_option("--sms", dest="sms", default='T1tttt-madgraph', type="string", action="store", help="simplified model: T1tttt, T1tttt-madgraph, T1t1t or T5tttt")
parser.set_defaults(small=False)

(options, args) = parser.parse_args()

c = ROOT.TChain("Events")

from smsInfo import nfsDirectories, th2Binning, th2VarString, xAxisTitle, yAxisTitle
for d in nfsDirectories[options.sms]:
  if options.small:
    c.Add(d+"/histo_10_*.root")
  else:
    c.Add(d+"/histo_*.root")

htBins = [(options.htl, options.hth)]
metBins = [(options.metl, options.meth)]

btbCut={'2':"nbtags==2", '1':'nbtags==1', '0':'nbtags==0', 2:"nbtags==2",'2p':'nbtags>=2', 1:'nbtags==1', 0:'nbtags==0', 'ex2':"nbtags==2", '3p':"nbtags>=3", 3:"nbtags>=3", 'none':"(1)"}

lcut = '((singleMuonic && nvetoMuons==1 && nvetoElectrons==0) || (singleElectronic && nvetoElectrons == 1 && nvetoMuons == 0))'

for htb in htBins:
  for metb in metBins:
    for btb in [options.btb]:
          iname = "h_"+options.sms+"_btb"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])+"_njets_"+str(options.njetMin)+"_"+str(options.njetMax)
          os.system('mkdir -p /afs/hephy.at/user/s/schoefbeck/www/pngEff/'+options.sms+'/')
          filename = '/afs/hephy.at/user/s/schoefbeck/www/pngEff/'+options.sms+'/'+iname
          binning = th2Binning[options.sms]
      
          hYield = ROOT.TH2D(iname+"_yield", iname+"_Yield", *binning)
          hRefYield = ROOT.TH2D(iname+"_RefYield", iname+"_RefYield", *binning)

          cut = lcut+'&&ht>'+str(htb[0])+'&&ht<'+str(htb[1])+'&&type1phiMet>'+str(metb[0])+'&&type1phiMet<'+str(metb[1])+"&&njets>="+str(options.njetMin)+"&&njets<="+str(options.njetMax)
          print "Calculating", htb, metb, btb, "using cut:\n",cut,"\n"


          gluinoSystemPt = "sqrt( (gluino0Pt*cos(gluino0Phi) + gluino1Pt*cos(gluino1Phi))**2 + (gluino0Pt*sin(gluino0Phi) + gluino1Pt*sin(gluino1Phi))**2)"
          ISRRefWeight  = "(1.*("+gluinoSystemPt+"<120) + "+".95*( "+gluinoSystemPt+">120&&"+gluinoSystemPt+"<150) + "+".90*( "+gluinoSystemPt+">150&&"+gluinoSystemPt+"<250) + "+".80*( "+gluinoSystemPt+">250))"

          leptonAndHadWeight = "(0.98*(0.95*singleMuonic + singleElectronic*(0.86*(abs(leptonEta)>1.552) + 0.98*(abs(leptonEta)<=1.552) )))"
          leptonTriggerEff = "(0.96*singleElectronic + singleMuonic*( (abs(leptonEta)<0.9)*0.98 + (abs(leptonEta)>0.9)*0.84) )"
   
          
          c.Draw(th2VarString[options.sms]+' >> '+iname+'_yield', leptonAndHadWeight+"*"+ISRRefWeight+"*"+leptonTriggerEff+"*("+cut+'&&'+btbCut[btb]+")", 'goff')
          c.Draw(th2VarString[options.sms]+' >> '+iname+'_RefYield', "(1)", 'goff')
          hYield.Divide(hRefYield)
          c1 = ROOT.TCanvas()
          hYield.Draw("COLZ")
          hYield.GetXaxis().SetTitle(xAxisTitle[options.sms])
          hYield.GetYaxis().SetTitle(yAxisTitle[options.sms])
          c1.Update()
          palette = hYield.GetListOfFunctions().FindObject("palette");
          palette.SetX1NDC(0.83);
          palette.SetX2NDC(0.87);
#          palette.SetY1NDC(0.2);
#          palette.SetY2NDC(0.8);
          c1.Modified();
          c1.Update();
          c1.Print(filename+".png") 
          c1.Print(filename+".pdf")
          c1.Print(filename+".root")
          del c1 


