import ROOT, pickle, os
from math import sqrt

ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)
ROOT.tdrStyle.SetPadRightMargin(0.16)

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

l={"cteq":44, "mstw":40, "nnpdf":100}
lcut = 'njets>=6&&((singleMuonic && nvetoMuons==1 && nvetoElectrons==0) || (singleElectronic && nvetoElectrons == 1 && nvetoMuons == 0))'

for htb in htBins:
  for metb in metBins:
    for btb in [options.btb]:
      for pdft in ["cteq", "mstw", "nnpdf"]:
          iname = "h_"+options.sms+"_"+pdft+"_btb"+btb+"_ht_"+str(htb[0])+"_"+str(htb[1])+"_met_"+str(metb[0])+"_"+str(metb[1])
          os.system('mkdir -p /data/schoef/results2012/pdfUncertainty/'+options.sms+'/')
          filename = '/data/schoef/results2012/pdfUncertainty/'+options.sms+'/'+iname+'.pkl'
          if os.path.isfile(filename) and not options.small:
            print "Found",filename,"! -> Skipping!"
            hYield = pickle.load(file(filename))
          else:
            print "Calculating", htb, metb, btb, pdft
            binning = th2Binning[options.sms]+[l[pdft]+1, 0, l[pdft]+1] 
            hYield = ROOT.TH3D(iname+"_yield", iname+"_Yield", *binning)
            cut = lcut+'&&ht>'+str(htb[0])+'&&ht<'+str(htb[1])+'&&type1phiMet>'+str(metb[0])+'&&type1phiMet<'+str(metb[1])
            print 'Iteration$:'+th2VarString[options.sms]+' >> '+iname+'_yield', pdft+'Weights*('+cut+'&&'+btbCut[btb]+')' 
            c.Draw('Iteration$:'+th2VarString[options.sms]+' >> '+iname+'_yield', pdft+'Weights*('+cut+'&&'+btbCut[btb]+')', 'goff')
#            hYield.GetXaxis().SetTitle(xAxisTitle[options.sms])
#            hYield.GetXaxis().SetLabelSize(0.03)
#            hYield.GetXaxis().SetTitleSize(0.03)
#            hYield.GetYaxis().SetTitle(yAxisTitle[options.sms])
#            hYield.GetYaxis().SetLabelSize(0.03)
#            hYield.GetYaxis().SetTitleSize(0.03)
            if not options.small:
              pickle.dump(hYield, file(filename, "w"))
              print "Written",filename
            else:
              print "No writing when small"
          c1 = ROOT.TCanvas()
          hYield.Draw("COLZ")
          c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".png") 
          c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngPDF/"+iname+".pdf")
          del c1 


