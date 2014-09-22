import array
import xsec
import math
import time, cPickle, os, copy
import ROOT
from array import array
import random
#import MCPfSSVHEMb_snapshot, MCPfSSVHEMc_snapshot,MCPfSSVHEMl_snapshot
#import MCPfSSVHEMbcalc_snapshot, MCPfSSVHEMccalc_snapshot,MCPfSSVHEMlcalc_snapshot
#import BTAGSSVHEM_snapshot, MISTAGSSVHEM_snapshot
from ConvertTupels_fcn import *
bold  = "\033[1m"
reset = "\033[0;0m"

ROOT.gROOT.Reset
ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 3000;")
ROOT.gROOT.SetBatch(True)

def getValue(c, varname):
  alias = c.GetAlias(varname)
  if alias!="":
    #print varname, alias, c.GetLeaf(alias).GetValue()
    return c.GetLeaf(alias).GetValue()
  else:
    #print "No Alias for", varname
    if c.GetLeaf(varname):
      #print "leaf", c.GetLeaf(varname).GetValue()
      return c.GetLeaf(varname).GetValue()
    else:
      #print varname,"nan"
      return float('nan')


commoncf=''
generalCut="True" #"Event['mTbare']>50"

commonstr='description'
reweightingHisto="reweightingHisto_Summer2011.root"
outputDir="/data/trauner/conv_pat120203_pfRA4Tupelizer_htGT350_JetsArr_test/"
small=False
loadArrays=True 
lepton_mode="Mu"
targetLumi = 4700

chain = 'Events'
analyzer_type='pfRA4Tupelizer'
isDefaultType=True
btagWP=1.74
#btagWP=3.3

#modes=["copy"]
#modes=["btagEff3_Norm_sf1", "btagEff3_Up_b_sf1", "btagEff3_Down_b_sf1"]
#modes=["btagEff3_Up_l_sf1", "btagEff3_Down_l_sf1"]
#modes+=["btagEff3_Up_l_sf0", "btagEff3_Down_l_sf0"]
modes=["btagEff3_Norm_sf0", "btagEff3_Up_b_sf0", "btagEff3_Down_b_sf0"]


#if lepton_mode=="Mu":
  #commoncf+='leptonPt>20 && singleMuonic && nvetoElectrons==0 && nvetoMuons==1 && ht>350 && barepfmet>100 && jet2pt>40'
  #commoncf_string='leptonptGT20_singleMuonic_noVetoLeptons_htGT300_jet2ptGT40_metgt100'
#else:
  #commoncf+='leptonPt>20 && singleElectronic && nvetoElectrons==1 && nvetoMuons==0 && ht>300 jet2pt>40'
  #commoncf_string='leptonptGT20_singleElectronic_noVetoLeptons_htGT300_jet2ptGT40'

if lepton_mode=="Mu":
  commoncf+='leptonPt>20 && ngoodMuons>0 && ht>350 && jet2pt>40 '
  commoncf_string='leptonptGT20_ngoodMuonsGT0_htGT350_jet2ptGT40'
else:
  commoncf+='leptonPt>20 && ngoodElectrons>0 && ht>350 && jet2pt>40'
  commoncf_string='leptonptGT20_ngoodElectronsGT0_htGT350_jet2ptGT40'

allSamples = []
data = {}
data['type'] = 'data'
data['bins'] = {'Run2010':['Run2010'],'Run2011':['Run2011A-Aug5ReReco-v1','Run2011A-May10ReReco', 'Run2011A-Prompt-v4', 'Run2011A-Prompt-v6', 'Run2011B-Prompt-v1']}


lm={}
lm['type']="signal"
#lm['bins']={'LM8':["LM8"],'LM9': ["LM9"]}
lm['bins']={'LM0':["LM0"],'LM1': ["LM1"],'LM2':["LM2"],'LM3': ["LM3"],'LM4':["LM4"],'LM5': ["LM5"],'LM6':["LM6"],'LM7': ["LM7"],'LM8':["LM8"],'LM9': ["LM9"],'LM10':["LM10"],'LM11': ["LM11"], 'LM12':["LM12"],'LM13': ["LM13"]}
#lm['bins']={'LM10':["LM10"],'LM11': ["LM11"], 'LM12':["LM12"],'LM13': ["LM13"]}

bg = {}
bg['type'] = 'mc'
bg['bins'] = {}
TTJets    = ['TTJets']
DYJets    = ['DYtoEE-M20', 'DYtoMuMu-M20', 'DYtoTauTau-M20'] #, "DYtoLL-M50"]
#DYJets    = ['DYtoLL']
if lepton_mode=="Mu":
	QCD       = ["QCD_Pt-15to20_MuPt5Enriched", "QCD_Pt-20to30_MuPt5Enriched", "QCD_Pt-30to50_MuPt5Enriched", "QCD_Pt-50to80_MuPt5Enriched", "QCD_Pt-80to120_MuPt5Enriched", "QCD_Pt-120to150_MuPt5Enriched", "QCD_Pt-150_MuPt5Enriched"]
else:
	QCD =  ["QCD_BCtoE_Pt20to30", "QCD_BCtoE_Pt30to80", "QCD_BCtoE_Pt80to170", "QCD_EMEnriched_Pt20to30", "QCD_EMEnriched_Pt30to80", "QCD_EMEnriched_Pt80to170", "QCD_Pt1000to1400", "QCD_Pt1400to1800", "QCD_Pt170to300", "QCD_Pt1800", "QCD_Pt300to470", "QCD_Pt470to600", "QCD_Pt600to800","QCD_Pt800to1000"]

singleTop = ['single-Top', "T-t", "T-s", "T-tW", "Tbar-t", "Tbar-s", "Tbar-tW"]
WJets     = ['WJets-HT300'] #, "WJetsToLNu"]
Wbb     = ['WbbToLNu']
bg['bins']["TTJets"]=TTJets
bg['bins']["WJets"]=WJets
##bg['bins']["Wbb"]=Wbb
bg['bins']["QCD"]=QCD
bg['bins']["DYJets"]=DYJets
bg['bins']["single-Top"]=singleTop
 

#allSamples.append(data)
allSamples.append(bg)
allSamples.append(lm)
#data['path'] = '/data/schoef/pat_111201/'+lepton_mode+"/"
#bg['path'] = '/data/schoef/pat_111201/'+lepton_mode+"/" 
bg['path'] = '/data/trauner/pat_120125/'+lepton_mode+"/" 
lm['path'] = '/data/trauner/pat_120125/'+lepton_mode+"/" 
#lm['path']='/data/schoef/pat_111201/'+lepton_mode+"/"
    


additionalInfo=[{"small": small, "commoncf":commoncf, "generalCut": generalCut, "commoncf_string":commoncf_string, "commonstr":commonstr, "targetLumi":targetLumi, "btagWP": btagWP, "chain": chain}]

variables = ["weight", "met", "mT", "barepfmet" ,"ht", "genmet", "genmetpx","genmetpy", "metpxUncorr", 
	"metpyUncorr", "m3", "singleMuonic", "singleElectronic", "btag0", "btag1", "btag2", "btag3", \
  "leptonPt", "leptonEta", "leptonPhi", "leptonPdg", "jet0pt", "jet1pt", "jet2pt", "jet3pt", "nvetoMuons", 
  "nvetoElectrons", "ngoodMuons", "ngoodElectrons", "ngoodVertices", "btag0pt", "btag1pt", "btag2pt", "btag3pt", "btag0eta", 
  "btag1eta", "btag2eta", "btag3eta", "nbtags", "nbjets", "ht2", "njets", "jet0eta", "jet1eta", "jet2eta", "jet3eta", "jet0btag",
   "jet1btag", "jet2btag", "jet3btag", "jet0parton", "jet1parton", "jet2parton", "jet3parton", "jet0btagMass", "jet1btagMass", 
   "jet2btagMass", "jet3btagMass", "btag0parton", "btag1parton", "btag2parton", "btag3parton", "btag0Mass", "btag1Mass", 
   "btag2Mass", "btag3Mass", "antinuMu", "antinuE", "antinuTau", "nuMu", "nuE", "nuTau", "nuMuFromTausFromWs", "nuEFromTausFromWs", "nuTauFromTausFromWs",
    "run", "event"]
arrays=["jetsPt", "jetsEta", "jetsPhi", "jetsParton", "jetsBtag"]
#MISSING  flavorHistory,

	
btags=["btag0", "btag1", "btag2", "btag3"]	
	     
print "Creating Tupel" #ONLY WORKS ONCE IN IPYTHON!!! DO NOT CHANGE VARIABLES AND IPYTHON AGAIN!!
struct_str = "struct ra4_tupel{"
for var in variables:
  struct_str +="Float_t "+var+";"
if loadArrays:
  for arr in arrays:
    struct_str += "Float_t "+arr+"[20];"  
struct_str   +="};"
ROOT.gROOT.ProcessLine(struct_str)
struct = ROOT.ra4_tupel()
print "Loaded tupel!"

nVertex={"allData":{}}
#PUweights=reweight(allSamples, targetLumi, commoncf, commoncf_string, chain) #FIXME Get Reweighting Histogram!
rwHisto = ""
if reweightingHisto is not "":
   rf = ROOT.TFile(reweightingHisto)
   htmp = rf.Get("ngoodVertices_Data")
   ROOT.gDirectory.cd("PyROOT:/")
   rwHisto = htmp.Clone()
   rf.Close()
   print "Loaded reweightingHisto", reweightingHisto, rwHisto   
print 'Loading Data...'
if small: print "...only testing, small is true!"
print "PRESELECTION: ", commoncf
for datatype in allSamples:
  print '============================================================================='
  print "Loading datatype: ", datatype["type"]  
  datatype['weights'] = {}
  datatype['loadedbins']={}
  for sample in datatype['bins']:
    print '---------------------------------------------------------------------------'
    print "Loading entry: ", bold+sample+reset
    nVertex[sample]={}
    loadBins = []
    path = datatype['path']
    if datatype.has_key(sample): 
       path=datatype[sample]["path"]
    folderList=os.listdir(path)
    for bin in datatype['bins'][sample]:
       for folder in folderList:
	 if bin == folder: 
	    loadBins.append(folder)
	    print "...selected", folder, "for", bin
    loadBins=list(set(loadBins))
    loadBins.sort()
    print 'Loading for ', sample, ' from path ', path, 'the bins', loadBins
    datatype["loadedbins"][bin]=copy.deepcopy(loadBins)
    for bin in loadBins:
      print 'Adding ', bin, "...."
      c = ROOT.TChain(chain)
      d = ROOT.TChain('Runs')
      fileList=os.listdir(path+bin+'/')
      for file in fileList:
	if 'root' in file: 	
            c.Add(path+bin+'/'+file)
	    d.Add(path+bin+'/'+file)
	else:
	  print 'This file:', file, ' shouldn\'t be here!!'
	  continue
      
      countEvents=0
      #binEvents = d.GetEntries('bool_EventCounter_passed_PAT.obj')
      nruns = d.GetEntries()
      print nruns
      for i in range(0, nruns):
        d.GetEntry(i)
        countEvents += getValue(d,"uint_EventCounter_runCounts_PAT.obj")
    
      if countEvents == 0:
	print bold+'No Events in this bin, check your code or path!'+reset
	continue
      if not xsec.xsec.has_key(bin):
	print bold+'\t WARNING: Bin '+bold+ bin +reset+' not in xsec setting weight to 1!'+reset 
	weight = 1
      else:
	weight = targetLumi * xsec.xsec[str(bin)] / countEvents
	print targetLumi, xsec.xsec[str(bin)], countEvents 
      print '\t Eventcount in bin '+bold+ bin +reset+ ' is', countEvents, ' weight: ', weight 
      
      datatype['weights'][bin]=weight
      
      c.Draw('>>eList',commoncf)
      elist = ROOT.gDirectory.Get('eList')#GetList.FindObject('eList')
      number_events = elist.GetN()
	      
      print '\t Number of events passing preselection:', number_events
      
#CREATE FILES AND DIRS=======================================================================	      
      #tree=copy.deepcopy(c);
      #tree.MakeClass("RA4v3")
      #ROOT.gROOT.ProcessLine(".L RA4v3.C++") 
      #ra4=ROOT.RA4v3(c)
      if lepton_mode=="EG":
	lepton_mode="Ele"
      workingDir=""
      print "\t checking output directory...",
      if not os.path.isdir(outputDir):
         os.system("mkdir "+outputDir)
      for mode in modes:
	print "\t\t",bold, mode, reset
	if not os.path.isdir(outputDir+mode):
         os.system("mkdir "+outputDir+mode)	 
	if not os.path.isdir(outputDir+mode+"/"+lepton_mode):
	   os.system("mkdir "+outputDir+mode+"/"+lepton_mode) 	 	 
	if not os.path.isdir(outputDir+mode+"/"+lepton_mode+"/"+bin+"/"):
	   os.system("mkdir "+outputDir+mode+"/"+lepton_mode+"/"+bin+"/")
	   workingDir=outputDir+mode+"/"+lepton_mode+"/"+bin+"/"
	   print "..created directory ", outputDir+mode+"/"+lepton_mode+"/"+bin+"/"
	else:
	  timestr=time.localtime()
	  date=str(timestr[0])+"_"+str(timestr[1])+"_"+str(timestr[2])+"_"+str(timestr[3])+"_"+str(timestr[4])
	  os.system("mkdir "+outputDir+mode+"/"+lepton_mode+"/"+bin+"_"+date+"/")
	  workingDir=outputDir+mode+"/"+lepton_mode+"/"+bin+"_"+date+"/"
	  print "\n", bold, "ERROR directory", outputDir+mode+"/"+lepton_mode+"/"+bin+"/", "already existing",
	  print "created directory", outputDir+mode+"/"+lepton_mode+"/"+bin+"_"+date+"/", "instead!", reset      
	    
      
      
	tree = ROOT.TTree( "Events", "Events", 1 ) #Construct the Events TTreefor the target file
	for var in variables:
	  tree.Branch(var,   ROOT.AddressOf(struct,var),var+'/F')
	if loadArrays:
	  for arr in arrays:
	    tree.Branch(arr,   ROOT.AddressOf(struct,arr),arr+'[20]/F')
	root_file = workingDir+"histo_"+sample+"_"+analyzer_type+"_"+commoncf_string+".root"
	
	if os.path.isfile(root_file):
	  print bold, "ERROR", root_file, "already there! Adding Time!!!", reset
	  timestr=time.localtime()
	  root_file = workingDir+timestr[4]+timestr[5]+"histo_"+sample+"_"+analyzer_type+"_"+commoncf_string+".root" 
  #=======================================================================CREATED FILES AND DIRS	
	if small:
	  if number_events>200:
	   number_events=2
	   print '\t Only loading 2000 Events from this bin! - Missing ', number_events-2000, " events"
	for i in range(0, number_events):
	  if (i%10000 == 0) and i>0 :
	    print "\t\t Processing event number: ", i
	    
	  if elist.GetN()>0 and c.GetEntries()>0:
	    c.GetEntry(elist.GetEntry(i))
	    if datatype["type"] is "data":
	      rewVertex=1
	    else:
	      rewVertex=rwHisto.GetBinContent(rwHisto.FindBin(getValue(c, "ngoodVertices")))
	    struct.weight  = weight*rewVertex 
	    
	    for var in variables[1:]: #exclude weight
	      varname=var
	      if not isDefaultType:
		varname=analyzer_type+"_"+var
	      exec("struct."+var+"="+str(getValue(c, varname)).replace("nan","float('nan')"))
	      
	    if loadArrays:  
	      for arr in arrays: #exclude weight
		varname=arr
		if not isDefaultType:
		  varname=analyzer_type+"_"+arr
		for i in range(0,20):
		  exec("struct."+arr+"["+str(i)+"]="+str(getArrValue(c, varname, i)).replace("nan","float('nan')")) 
            #print "Nbtags davor", struct.nbtags
	    #if "btagEff" in mode and datatype["type"] is not "data":
	      #print bold,"IN EFF MODE: ", mode, reset
	      #print datatype["type"]
	      #btagArr=[]
	      #nbtags=0
	      #for btag in btags:
		#jetpt=0; jeteta=0; jetParton=0;
		#jetpt=eval("struct."+btag+"pt")
		#jeteta=eval("struct."+btag+"eta")
		#jetParton=eval("struct."+btag+"parton")
		##print "vorher", eval("struct."+btag), jetpt, jeteta, jetParton
		#err=0
		#if jetpt>0:
		  #if abs(jetParton)==5:
		    #sf=loadSF("BTAGSSVHEM", jetpt, jeteta)
		    #effPair=loadEff("bcalc", jetpt, jeteta)
		    #if mode.split("_")[1]=="b":
		      #err=sf[1] 
		  #elif abs(jetParton)==4:
		    #sf=loadSF("BTAGSSVHEM", jetpt, jeteta)
		    #effPair=loadEff("ccalc", jetpt, jeteta)
		    #if mode.split("_")[1]=="b":
		      #err=sf[1]
		  #else:
		    #sf=loadSF("MISTAGSSVHEM", jetpt, jeteta)
		    #effPair=loadEff("lcalc", jetpt, jeteta)
		    #if mode.split("_")[1]=="l":
		      #err=sf[1]
		  #if mode.split("_")[-1]=="sf0":
		    #sf[0]=1;
		  #if "Up" in mode:
		    #eff=effPair[0]*sf[0]*(1+err)
		  #elif "Down" in mode:
		    #eff=effPair[0]*sf[0]*(1-err)
		  #else:     		  
		    #eff=effPair[0]*sf[0]
		  #rnd=random.uniform(0,1)
		  ##print "random", rnd, "eff", eff, "sf", sf, "error", err, "effBefore", effPair[0]  
		  #if rnd<eff:
		    #btagArr.append([10, jetpt, jeteta, jetParton])
		    #nbtags+=1
		  #else:
		    #btagArr.append([-2,jetpt, jeteta, jetParton])
		##print btagArr[-1][0]
		#btagArr.sort()
		#btagArr.reverse()
		
	      #for i in range(0, len(btagArr)):
	         #exec("struct.btag"+str(i)+"="+str(btagArr[i][0]))
	         #exec("struct.btag"+str(i)+"pt="+str(btagArr[i][1]))
	         #exec("struct.btag"+str(i)+"eta="+str(btagArr[i][2]))
	         #exec("struct.btag"+str(i)+"parton="+str(btagArr[i][3]))
	         ##print "i", btagArr[i]
	      #exec("struct.nbtags="+str(nbtags))
	      ##print "nbtags", nbtags
		
		 
	    if mode.split("_")[0]== "btagEff3" and datatype["type"] is not "data":
	      #print bold,"IN EFF MODE: ", mode, reset
              full_weight = struct.weight

	      
              btagArr=[]
	      JetsArr=[]
              nbtags=0
	      njets=0
                
              #for btag in btags: 
                  #jetpt=0; jeteta=0; jetParton=0;
                  #jetpt=eval("struct."+btag+"pt")
                  #jeteta=eval("struct."+btag+"eta")
                  #jetParton=eval("struct."+btag+"parton")
                  #print "vorher", eval("struct."+btag), jetpt, jeteta, jetParton
	      for j in range(0, 20):
		  #print "jet", j, eval("struct.jetsPt["+str(j)+"]")
                  jetpt=0; jeteta=0; jetParton=0;
                  jetpt=eval("struct.jetsPt["+str(j)+"]")
                  jeteta=eval("struct.jetsEta["+str(j)+"]")
                  jetParton=eval("struct.jetsParton["+str(j)+"]")
                  #print "vorher", eval("struct."+btag), jetpt, jeteta, jetParton	  
                  err=0
                  if jetpt>0:
		    njets+=1
                    if abs(jetParton)==5:
                      sf=loadSF("BTAGSSVHEM", jetpt, jeteta)
                      effPair=loadEff("bcalcJets", jetpt, jeteta)
                      if mode.split("_")[2]=="b":
                        err=sf[1] 
                    elif abs(jetParton)==4:
                      sf=loadSF("CBTAGSSVHEM", jetpt, jeteta)
                      effPair=loadEff("ccalcJets", jetpt, jeteta)
                      if mode.split("_")[2]=="b":
                        err=sf[1]
                    else:
                      sf=loadSF("MISTAGSSVHEM", jetpt, jeteta)
                      effPair=loadEff("lcalcJets", jetpt, jeteta)
                      if mode.split("_")[2]=="l":
                        err=sf[1]
                    if mode.split("_")[-1]=="sf0":
                      sf[0]=1;
                    if "Up" in mode:
                      eff=effPair[0]*sf[0]*(1+err)
                    elif "Down" in mode:
                      eff=effPair[0]*sf[0]*(1-err)
                    else:           
                      eff=effPair[0]*sf[0]
		    
		    JetsArr.append([eff, 1-eff,jetpt])
	            #print "pt:", jetpt, "parton:", jetParton, "effBefore", effPair[0], "sf", sf, 
		    #print "\tused eff", eff, "used error", err
		    #print "----------------------------------"
                    #rnd=random.uniform(0,1)
##                    print "random", rnd, "eff", eff, "sf", sf, "error", err, "effBefore", effPair[0]  
                    #if rnd<eff:
##                      btagArr.append([10, jetpt, jeteta, jetParton])
                      #nbtags+=1
##                    else:
##                      btagArr.append([-2,jetpt, jeteta, jetParton])
                  #print btagArr[-1][0]
#                btagArr.sort()
#                btagArr.reverse()
#                for i in range(0, len(btagArr)):
#                   exec("struct.btag"+str(i)+"="+str(btagArr[i][0]))
#                   exec("struct.btag"+str(i)+"pt="+str(btagArr[i][1]))
#                   exec("struct.btag"+str(i)+"eta="+str(btagArr[i][2]))
#                   exec("struct.btag"+str(i)+"parton="+str(btagArr[i][3]))
#                   #print "i", btagArr[i]
#                exec("struct.nbtags="+str(nbtags))
              
	      weights=[]
	      n=njets
	      #print "used Jets Arr", JetsArr
	      weights.append(calcEff([""], JetsArr))
	      for k in range(1, n+1):
		arr=block(n, k, 0, 1)
		weights.append(calcEff(arr, JetsArr))
			  
	      weightsGT2=0
	      for i in range(2, len(weights)):
		  #print i
		  weightsGT2+=weights[i]       
	      
	      weightsGT3=0
	      for i in range(3, len(weights)):
		  #print i
		  weightsGT3+=weights[i]       	  
	      #print "njets", njets, "nbtags", struct.nbtags, "nbjets", struct.nbjets
	      #print weights[0], weights[1], weights[2], weights[3], "gt2", weightsGT2
	      #print weights
	      #print weightsGT2
	      
              struct.btag0 = -2
              struct.btag1 = -2
              struct.btag2 = -2
              struct.btag3 = -2
	      struct.nbtags=0
              struct.weight = weights[0]*full_weight
              #print "Fill 1", struct.weight 
              tree.Fill()
              struct.btag0 = 10
              struct.btag1 = -2
              struct.btag2 = -2
              struct.btag3 = -2
	      struct.nbtags=1
              struct.weight = weights[1]*full_weight
              #print "Fill 2", struct.weight 
              tree.Fill()
              struct.btag0 = 10
              struct.btag1 = 10
              struct.btag2 = -2
              struct.btag3 = -2
	      struct.nbtags=2
              struct.weight = weightsGT2*full_weight
              #print "Fill 3", struct.weight     
	      #tree.Fill()
	      #struct.btag0 = 10
              #struct.btag1 = 10
              #struct.btag2 = 10
              #struct.btag3 = -2
	      #struct.nbtags=3
              #struct.weight = weightsGT3*full_weight
              #print "Fill 4", struct.weight     ,"(", full_weight,")" 
	    tree.Fill() #Fill output ttree 
	file = ROOT.TFile(root_file, "recreate")   #Write to file
	tree.Write()
	file.Close()
	print "\t Written",root_file
	del tree, file
      del elist, c,d          #End of LOAD BINS
	 
print 'Loading DONE!'
#WRITE PICKLE REPORT!
returnvalue=[allSamples, additionalInfo] #SAVE AS PICKLES!! die allSamples, 
timestr=time.localtime()
date=str(timestr[0])+"_"+str(timestr[1])+"_"+str(timestr[2])+"_"+str(timestr[3])+"_"+str(timestr[4])      
cPickle.dump(returnvalue,open(outputDir+mode+"/"+lepton_mode+"/"+date+"_PickelREPORT_CONVERSION_"+commonstr+"_"+commoncf_string+".pickle", "wb"))


  
