# mva_2Dplots.py
# Script to calculate the 2D distributions of the mva response 
# Mateusz Zarucki 2017

from fakeInfo import *

ROOT.gStyle.SetOptStat(0)

script = "plotFakeRegions.py" #os.path.basename(__file__) #sys.argv[0]

##Input options
#parser = argparse.ArgumentParser(description="Input options")
#parser.add_argument("--lep", dest = "lep",  help = "Lepton", type = str, default = "el")
#parser.add_argument("--var1", dest="var1",  help="Variable 1", type=str, default="hybIso")
#parser.add_argument("--var2", dest="var2",  help="Variable 2", type=str, default="mvaResponse")
##parser.add_argument("--slice", dest="slice",  help="Pt Slice Bounds (low,up)", type=int, nargs=2, metavar = ('slice_low', 'slice_up'))
#parser.add_argument("--sample", dest="sample",  help="Sample", type=str, default="qcd")
#parser.add_argument("--logy", dest = "logy",  help = "Toggle logy", type = int, default = 1)
#parser.add_argument("--save", dest="save",  help="Toggle Save", type=int, default=1)
#parser.add_argument("--verbose", dest = "verbose",  help = "Verbosity switch", type = int, default = 0)
#parser.add_argument("-b", dest="batch",  help="Batch Mode", action="store_true", default=False)
#args = parser.parse_args()
#if not len(sys.argv) > 1:
#   print makeLine()
#   print "No arguments given. Using default settings."
#   print makeLine()
#   #exit()

##Arguments
#lep = args.lep
#var1 = args.var1
#var2 = args.var2
##slice = args.slice
#sample = args.sample 
#logy = args.logy
#save = args.save
#verbose = args.verbose

#Arguments
args = fakeParser(script)

lep = args.lep
region = args.region
mva = args.mva
WP = args.WP
looseNotTight = args.looseNotTight
doPlots = args.doPlots
doYields = args.doYields
doControlPlots = args.doControlPlots
varBins = args.varBins
logy = args.logy
save = args.save
verbose = args.verbose

sample = 'z'
var1 = 'mvaResponse'
var2 = 'hybIso'
 
if verbose:
   print makeDoubleLine()
   print "Plotting 2D distributions"
   print makeDoubleLine()

fakeInfo = fakeInfo(script, vars(args))

lepton =      fakeInfo['lepton']
samplesList = fakeInfo['samplesList']
samples =     fakeInfo['samples']
dataset =     fakeInfo['dataset']
selection =   fakeInfo['selection']
bins =        fakeInfo['bins']

index = {'probe': selection[WP]['lepIndex1']}

#Save
if save:
   savedir =  fakeInfo['baseDir']
   savedir += "/applicationRegions/%s/2Dmva"%region
   
   suffix = fakeInfo['suffix']
   suffix += '_' + sample
   suffix += '_' + var1
   suffix += '_' + var2

   makeDir(savedir + '/pdf')
   makeDir(savedir + '/root')

variables = {
             'hybIso':"(LepGood_relIso03[{ind}]*min(LepGood_pt[{ind}], 25))".format(ind = index['probe']),
             'mvaResponse':"mva_response[{mvaIdIndex}]".format(mvaIdIndex = selection['mvaIdIndex']),
            }

plotDict = {\
   #"MET":{    'var':"met",                                             'bins':[100,0,500],   'decor':{'title':"MET Plot",             'x':"Missing E_{T} / GeV",             'y':"Events", 'log':[0,logy,0]}},
   #"HT":{     'var':"ht_basJet",                                       'bins':[100,0,500],   'decor':{'title':"HT Plot",              'x':"H_{T} / GeV",                     'y':"Events", 'log':[0,logy,0]}},
   #"delPhi":{ 'var':"vetoJet_dPhi_j1j2",                               'bins':[16, 0, 3.14], 'decor':{'title':"deltaPhi(j1,j2) Plot", 'x':"#Delta#phi(j1,j2)",               'y':"Events", 'log':[0,logy,0]}},
   #"lepPt":{  'var':variables['lepPt'],                                'bins':[20, 0, 50],  'decor':{'title':"Lepton pT Plot" ,      'x':"Muon p_{T} / GeV",                'y':"Events", 'log':[0,logy,0]}},
   #"lepMt":{  'var':variables['lepMt'],                                'bins':[20,0,100],   'decor':{'title':"Lepton mT Plot",       'x':"m_{T} / GeV",                     'y':"Events", 'log':[0,logy,0]}},
   "hybIso2":{'var':"(log(1 + " + variables['hybIso'] + ")/log(1+5))", 'bins':[16, 0, 4],    'decor':{'title':"Lepton hybIso Plot",   'x':"log(1+HI)/log(1+5)",              'y':"Events", 'log':[0,logy,0]}},
   "hybIso":{ 'var':variables['hybIso'],                               'bins':[20, 0, 20],  'decor':{'title':"Lepton hybIso Plot",   'x':"HI = I_{rel}*min(p_{T}, 25 GeV)", 'y':"Events", 'log':[0,logy,0]}},
   "mvaResponse":{'var':variables['mvaResponse'],                      'bins':[48, -0.6, 0.6],  'decor':{'title':"MVA Response",   'x':"MVA Response", 'y':"Events", 'log':[0,logy,0]}},
   #"absIso":{ 'var':variables['absIso'],                               'bins':[8, 0, 20],   'decor':{'title':"Lepton absIso Plot",   'x':"I_{abs} / GeV",                   'y':"Events", 'log':[0,logy,0]}},
   #"relIso":{ 'var':variables['relIso'],                               'bins':[40, 0, 5],   'decor':{'title':"Lepton relIso Plot",   'x':"I_{rel}",                         'y':"Events", 'log':[0,logy,0]}},
   #"absDxy":{ 'var':variables['absDxy'],                               'bins':[8, 0, 0.04], 'decor':{'title':"Lepton |dxy| Plot" ,   'x':"|dxy|",                           'y':"Events", 'log':[0,logy,0]}},
   #"weight":{ 'var':"weight",                                          'bins':[40,0,400],   'decor':{'title':"Weight Plot",          'x':"Event Weight",                    'y':"Events", 'log':[0,1,0]}}
}

c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
c1.Divide(1,2)

cut = selection[WP][region][sample][0]
weight = selection[WP][region][sample][1]

#2D Histograms (wrt. pT)
hist = make2DHist(samples[sample].tree, variables[var1], variables[var2], weight + "*(%s)"%cut, plotDict[var1]['bins'][0], plotDict[var1]['bins'][1], plotDict[var1]['bins'][2], plotDict[var2]['bins'][0], plotDict[var2]['bins'][1], plotDict[var2]['bins'][2])
hist.SetName("2D_" + var1 + "_" + var2)
hist.SetTitle(var1 + " vs " + var2 + " Distribution")
hist.GetXaxis().SetTitle(var1)
hist.GetYaxis().SetTitle(var2)
hist.Draw("COLZ") #CONT1-5 #plots the graph with axes and points
#hist.GetZaxis().SetRangeUser(0, 4)
if logy: ROOT.gPad.SetLogz() 
#alignStats(hist)
   
c1.Modified()
c1.Update()
   
#Save to Web
if save: #web address: http://www.hephy.at/user/mzarucki/plots/electronID
   c1.SaveAs("%s/2D_%s_%s%s.png"%(savedir, var1, var2, suffix))
   c1.SaveAs("%s/root/2D_%s_%s%s.root"%(savedir, var1, var2, suffix))
   c1.SaveAs("%s/pdf/2D_%s_%s%s.pdf"%(savedir, var1, var2, suffix))
