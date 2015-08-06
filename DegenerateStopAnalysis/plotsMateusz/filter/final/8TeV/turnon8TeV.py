#turnon.py for 8TeV

#def main(gMETcut, gISRcut):

import ROOT
import os, sys
import math
import copy
import subprocess
from optparse import OptionParser
from DataFormats.FWLite import Events, Handle

#from Workspace.HEPHYPythonTools.helpers import getChain#, getPlotFromChain, getYieldFromChain, getChunks

#ROOT Options
ROOT.gROOT.Reset() #re-initialises ROOT
#ROOT.gROOT.SetStyle("Plain")

ROOT.gStyle.SetOptStat(1111) #0 removes histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis
ROOT.gStyle.SetOptFit(1111) #1111 prints fits results on plot
#ROOT.gStyle.SetTitleX(0.15)
#ROOT.gStyle.SetFuncWidth(1)
#ROOT.gStyle.SetFuncColor(9)
#ROOT.gStyle.SetLineWidth(2)
#ROOT.gStyle.SetOptTitle(0) #suppresses title box

ROOT.gStyle.SetPaintTextFormat("4.2f")
#ROOT.gStyle->SetTitleX(0.1)
#ROOT.gStyle->SetTitleW(0.8)

ROOT.gStyle.SetStatX(0.75)
ROOT.gStyle.SetStatY(0.65)
ROOT.gStyle.SetStatW(0.1)
ROOT.gStyle.SetStatH(0.15)


#dir = "/afs/hephy.at/work/n/nrad/cmgTuples/RunII/T2DegStop_300_270_RunII_withMotherRef"
#dir = "/afs/cern.ch/work/n/nrad/cmgTuples/RunII/RunII_T2DegStop_300_270_prunedGenParticles/T2DegStop_300_270_RunII_genParticles"
#dir = "/afs/cern.ch/work/m/mzarucki/data"

def makeLine():
   line = "\n**********************************************************************************************************************************\n"
   return line

def makeDoubleLine():
   line = "\n**********************************************************************************************************************************\n\
**********************************************************************************************************************************\n"
   return line

def newLine():
   print ""
   return 

#signal=({\
#"name" : "treeProducerSusySingleLepton", #"T2DegStop_300_270_RunII"
#"bins" : ["treeProducerSusySingleLepton"], #["T2DegStop_300_270_RunII"]
#'dir' : dir
#})

#print makeLine()

#T2DegSample = getChain(signal, histname='',treeName="tree")

#print 'Sample: ', signal['name']

print makeLine()

#T2DegSample.Print() #Shows the tree structure of entire chain (entries, branches, leaves)

#T2DegSample.Scan() #Shows all the values of the list of leaves separated by a colon

def drawhist(sample, varname, sel, nbins = 100, min = 0, max = 1000):
   hist = ROOT.TH1F("hist", "Histogram", nbins, min, max)
   sample.Draw(varname + ">>hist", sel, "goff") #">>hname(100, 0, 1000)", sel, "goff")
   #hist = ROOT.gDirectory.Get("hname")
   hist.SetTitle(varname + " Plot")
   hist.GetXaxis().SetTitle(varname + "/ GeV")
   hist.GetYaxis().SetTitle("Counts")
   hist.GetXaxis().CenterTitle()
   hist.GetYaxis().CenterTitle()
   #hist.SetAxisRange(0, 1000, "X")
   #hist.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
   #hist.GetXaxis().SetRangeUser(0, 1000)
   #hist.SetMinimum(0)
   #hist.SetMaximum(2E7)
   return hist 

#Selection function
def select(varname, cut, option): #option = {>, =, <}
   sel = "abs(" + varname + option + str(cut) + ")"
   return sel

#Creates Legend
def makeLegend():
   leg = ROOT.TLegend(0.60,0.70,0.75,0.85)
   leg.SetHeader("#bf{Legend}")
   header = leg.GetListOfPrimitives().First()
   header.SetTextAlign(22)
   return leg 

#Creates Box 
def makeBox():
   box = ROOT.TPaveText(0.775,0.40,0.875,0.65, "NDC") #NB & ARC
   #box.SetHeader("Cuts")
   #header = box.GetListOfPrimitives().First()
   #header.SetTextAlign(22)
   return box 

def alignStats(hist):
   st = hist.FindObject("stats")
   st.SetX1NDC(0.775)
   st.SetX2NDC(0.875)
   st.SetY1NDC(0.7)
   st.SetY2NDC(0.85)

#def getJetPt(jets) #getJets(), #getLeadingJetPt() == Jet_pt[0]
#   for jet in jets:
#         return jet.pt()
#   return 0
 
#
# small class holding MET pt and phi
#

class MyMET:
  def __init__(self,metx,mety):
    self.met_ = math.sqrt(metx**2+mety**2)
    self.phi_ = math.atan2(mety,metx)
 
  def pt(self):
    return self.met_
 
  def phi(self):
    return self.phi_

class MyEvent:
  """event class for easier access to event products"""
  def __init__(self):
    """init with empty list of products"""
    self.products = { }
  
  def defineProduct(self,labels,stype):
    """add a product with (single or tuple of) labels and a type string"""
    if type(labels)==type(""):
      labels_ = ( labels )
    else:
      assert type(labels)==type( () )
      labels_ = labels
    if not labels_ in self.products:
      self.products[labels_] = { }
    assert not stype in self.products[labels_]
    self.products[labels_][stype] = [ Handle(stype), None ]

  def load(self,event):
    """get all predefined products from the event"""
    for labels in self.products:
      for stype in self.products[labels]:
        handle = self.products[labels][stype][0]
        event.getByLabel(labels,handle)
        self.products[labels][stype][1] = handle.product()

  def getProduct(self,labels,stype=None):
    """access to a product by label (and stype, if ambiguous) labels have to be identical to the ones given in defineProduct()"""
    if type(labels)==type(""):
      labels_ = ( labels )
    else:
      assert type(labels)==type( () )
      labels_ = labels
    if stype==None:
      assert len(self.products[labels_].keys())==1
      stype_ = self.products[labels_].keys()[0]
    else:
      stype_ = stype
    return self.products[labels_][stype_][1]

class MyGenParticle:
  """Wrapper for GenParticle in order to have access to indices in event history"""
  def __init__(self,index,genParticle):
    #store index and the GenParticle
    self.index = index
    self.particle = genParticle
    self.mothers = None
    self.daughters = None

  def motherIndices(self):
    if self.mothers==None or self.mothers[0]<0:
      return None
    if self.mothers[1]<0:
      return [ self.mothers[0] ]
    return range(self.mothers[0],self.mothers[1]+1)

  def daughterIndices(self):
    if self.daughters==None or self.daughters[0]<0:
      return None
    if self.daughters[1]<0:
      return [ self.daughters[0] ]
    return range(self.daughters[0],self.daughters[1]+1)

  def xid(self,particle=None):
    """return tuple with key quantities"""
    if particle:
      p = particle
    else:
      p = self.particle
    return ( p.pdgId(), p.status(), p.pt(), p.eta(), p.phi() )

  def __str__(self):
    gp = self.particle
    line = "{0:4d}".format(self.index)
    line += "  pt={0:6.1f} eta={1:9.2f} phi={2:5.2f} m={3:6.1f} id={4:8d} stat={5:3d}".format( \
      gp.pt(),gp.eta(),gp.phi(),gp.mass(),gp.pdgId(),gp.status())
    line += "  mo {0:5d} {1:5d}  da {2:5d} {3:5d}".format(self.mothers[0],self.mothers[1], \
                                                            self.daughters[0],self.daughters[1])
    return line

class MyGenParticles:
  """class holding the list of MyGenParticles for one event including access functions"""
  def __init__(self,genParticles):
    """create list and set mother and daughter indices"""
    self.genParts = [ ]
    
    self.addresses = [ ]
    for ip,p in enumerate(genParticles):
#      self.addresses.append(id(p))
      # create and add MyGenParticle
      mp = MyGenParticle(ip,p)
      self.genParts.append(mp)
      # create a unique object identifying the particle
      #   (for some reason the use of the ROOT address does not work)
      self.addresses.append(mp.xid())

    for mp in self.genParts:
      # now look for indices of mother particles and set the corresponding fields in MyGenParticle
      nm = mp.particle.numberOfMothers()
      if nm:
        mp.mothers = ( self.index(mp.particle.mother(0)), self.index(mp.particle.mother(nm-1)) )
      else:
        mp.mothers = ( -1, -1 )

      # same for daughters
      nd = mp.particle.numberOfDaughters()
      if nd:
        mp.daughters = ( self.index(mp.particle.daughter(0)), self.index(mp.particle.daughter(nd-1)) )
      else:
        mp.daughters = ( -1, -1 )

  def __getitem__(self,index):
    """allow access via [] operator"""
    return self.genParts[index]

  def motherIndices(self,index):
    """get range of indices of mother particles for particle at position <index>"""
    mp = self.genParts[index]
    if mp.mothers==None:
      gp = mp.particle
      nm = gp.numberOfMothers()
      if nm:
        mp.mothers = ( self.index(gp.mother(0)), self.index(gp.mother(nm-1)) )
      else:
        mp.mothers = ( -1, -1 )
    return mp.motherIndices()

  def daughterIndices(self,index):
    """get range of indices of daughter particles for particle at position <index>"""
    mp = self.genParts[index]
    if mp.daughters==None:
      gp = mp.particle
      nd = gp.numberOfDaughters()
      if nd:
        mp.daughters = ( self.index(gp.daughter(0)), self.index(gp.daughter(nd-1)) )
      else:
        mp.daughters = ( -1, -1 )
    return mp.daughterIndices()

  def indexFromAddress(self,address):
    result = self.addresses.index(address)
    assert result>=0
    return result

  def index(self,particle):
#    return self.indexFromAddress(id(particle))
    return self.indexFromAddress(self.genParts[0].xid(particle))

  def indicesByPdgId(self,pdgIds,useAbs=True,indices=None):
    """Get all indices for particles with pdg (or pdg in) pdgIds by default the absolute value is used. Optionally restrict search to a list of indices."""
    result  = [ ]
    if type(pdgIds)==type(0):
      pdgIds_ = [ pdgIds ]
    else:
      pdgIds_ = pdgIds
    parts = self.genParts
    if indices!=None:
      parts = [ self.genParts[i] for i in indices ]
    for mp in parts:
      id = mp.particle.pdgId()
      if useAbs:
        id = abs(id)
      if id in pdgIds_:
        result.append(mp.index)
    return result

  def lastInChain(self,index):
    """Follow mother-daughter chain for a particle as long as the daughter==mother (or the difference is only the radiation of a photon or gluon"""
    result = index
    mp = self.genParts[index]
    pdgId = mp.particle.pdgId()
    while True:
      idas = self.genParts[result].daughterIndices()
      if not idas:
        return result
      daIds = { }
      for ida in idas:
        pdgIdDa = self.genParts[ida].particle.pdgId()
        if not pdgIdDa in daIds:
          daIds[pdgIdDa] = [ ]
        daIds[pdgIdDa].append(ida)
      if len(daIds.keys())>2 or ( not pdgId in daIds ) or len(daIds[pdgId])>1:
        break
      if len(daIds.keys())==1:
        if len(daIds[pdgId])!=1:
          break
      else:
        otherIds = [ x for x in daIds.keys() if x != pdgId ]
        if otherIds[0]!=21 and otherIds[0] != 22:
          break
      if daIds[pdgId][0]==result:
        print "Daughters point back to same line???"
        break
      result = daIds[pdgId][0]
        
    return result

  def genMET(self):
    """Calculate MET from the sum of neutrinos or neutralino_1s"""
    metx = 0.
    mety = 0.
    for mp in self.genParts:
      if mp.particle.status()==1:
        pdgId = abs(mp.particle.pdgId())
        if pdgId==1000022 or pdgId==12 or pdgId==14 or pdgId==16:
          pt = mp.particle.pt()
          phi = mp.particle.phi()
          metx += pt*math.cos(phi)
          mety += pt*math.sin(phi)
    return MyMET(metx,mety)

  def __str__(self):
    result = ""
    for mp in self.genParts:
      result += str(mp) + "\n"
    return result
#
# arguments and options
#

parser = OptionParser()
parser.add_option("--first", dest="first",  help="index of first file", type="int", default=0)
parser.add_option("--maxFiles", dest="number",  help="number of files", type="int", default=None)
parser.add_option("-b", dest="batch",  help="batch", action="store_true", default=False)
(options, args) = parser.parse_args()
if len(args)==0:
    args = [ "//dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_240614/T2DegenerateStop_2J_mStop-100to150-2/" ]
assert len(args)==1
dpmDir = args[0]
if not dpmDir.endswith("/"):
  dpmDir += "/"

files = [ ]
p = subprocess.Popen(["dpns-ls",dpmDir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
  fn = line[:-1]
  if fn.endswith(".root"):
    files.append("root://hephyse.oeaw.ac.at"+dpmDir+fn)
files.sort()
files = files[options.first:]
if options.number!=None:
  files = files[:options.number]

events = Events(files)
print "Total number of events is ",events.size()

#
# wrapper for events and product definitions
#
myEvent = MyEvent()
myEvent.defineProduct("genParticles","std::vector<reco::GenParticle>")
myEvent.defineProduct(("SUSYTupelizer","met"), "float")
myEvent.defineProduct(("SUSYTupelizer","metphi"), "float")
myEvent.defineProduct(("SUSYTupelizer","osetMC"), "float")
myEvent.defineProduct(("SUSYTupelizer","osetMsq"), "float")
myEvent.defineProduct(("SUSYTupelizer","njets"), "int")
myEvent.defineProduct(("SUSYTupelizer","jetsPt"), "vector<float>")
myEvent.defineProduct(("SUSYTupelizer","jetsEta"), "vector<float>")
#myEvent.defineProduct(("SUSYTupelizer","jetsPhi"), "vector<float>")

#Fit Function
fitFunc = ROOT.TF1("f1", "[0]*TMath::Erf((x-[1])/[2]) + [3]", 0, 1000) #Error function scaled to [0,1]
fitFunc.SetParNames("Normalisation", "Edge", "Resolution", "Y-Offset")
#fitFunc.SetParameter(0, 0.5)
#fitFunc.SetParameter(1, 150)
#fitFunc.SetParameter(2, 50)  
#fitFunc.SetParLimits(0, 0.4, 0.65) #keep fixed?
fitFunc.SetParLimits(1, 0, 200) #init: [0,200]
fitFunc.SetParLimits(2, 0, 60) #init: [0,60]
fitFunc.SetParLimits(3, 0.45, 0.8) #init: [0.45,0.8]

#Selection
#weight = 1
#str(weight) + "*(" && ")" 

#gMETcut = input("Enter Generated MET cut value: ")
#gISRcut = input("Enter Generated ISR Jet pT cut value: ")

cuts=({\
'MET' : 200, #MET cut (fixed)
'ISR' : 110, #ISR/Leading Jet cut (fixed)
'Eta' : 2.4, #eta cut (fixed)

'gMET' : 130, #generated quantity cuts
'gISR' : 90,
'gEta' : 2.5
})

recoBinMET = int(cuts['MET']*nbins/(max - min)) + 1 #cuts['MET']/(h1.GetXaxis().GetBinWidth(0)) # + 1 to get correct bin
recoBinISR = int(cuts['ISR']*nbins/(max - min)) + 1 #cuts['ISR']/(h1.GetXaxis().GetBinWidth(0))

cutString = \
"Preselection cuts: \n\n" + \
"MET cut: " + str(cuts['MET']) + "\n" \
"ISR Jet pT cut: " + str(cuts['ISR']) + "\n" \
"ISR Jet Eta cut: " + str(cuts['Eta']) + "\n\n" + \
"Generator cuts:" + "\n" + \
"Generated MET cut: " + str(cuts['gMET']) + "\n" \
"Generated ISR Jet pT cut: " + str(cuts['gISR']) + "\n" \
"Generated ISR Jet Eta cut: " + str(cuts['gEta']) 

print makeLine()
print cutString
 
#Preselection and Generated Particles Filter Selection

#Variables: met_pt, met_genPt, Jet_pt, GenJet_pt, Jet_eta, GenJet_eta

#MET Selection
#preSel1 = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['Eta']) + "))" + ">" + str(cuts['ISR']) #normally would be with preSel2
#MaxIf$("Jet_pt", select("Jet_eta", cuts['Eta'], "<")) + ">" + cuts['ISR'], #Jet_pt[0] is one with max Pt

#genSel1 = select("met_genPt", cuts['gMET'], ">")

#ISR Jet Pt Selection
#preSel2 = select("met_pt", cuts['MET'], ">") #normally would be with preSel1

#genSel2 = "Max$(GenJet_pt*(abs(GenJet_eta)<" + str(cuts['gEta']) + "))" + ">" + str(cuts['gISR'])
#maxIf$("GenJet_pt", select("GenJet_eta", cuts['gEta'], "<")) + ">" + cuts['gISR'] + ")" #GenJet_pt[0] is one with max Pt

nbins = 100
min = 0 #GeV
max = 1000 #GeV

stopMs = [x for x in range (100,401,25)] 
LSPMs = [20, 30, 45, 55, 60, 65, 70, 80, 90, 100, 130]
massPoints = [str(stop) +"_"+str(LSP) for stop in stopMs for LSP in LSPMs]

hists = {}
for massPoint in massPoints:
   hists[massPoint]={}
   for iHist in range(12):
      hists[massPoint][iHist] = ROOT.TH1F(massPoint + "_h%s"%iHist, massPoint +"_h%s"%iHist, nbins, min, max)

#inspect specific events
#for iev,event in enumerate(events):
#   myEvent.load(event)
#   genParts = myEvent.getProduct("genParticles")
#   myGenParts = MyGenParticles(genParts)
#
#   if iev == 1: #event number
#      print myGenParts
#      break
   
#event loop
for iev,event in enumerate(events):
   if iev == 30000: break
   if iev%1000==0:
     print "At event ",iev," ; file index is ",event.fileIndex()

   myEvent.load(event)
   
   genParts = myEvent.getProduct("genParticles")
   myGenParts = MyGenParticles(genParts)
  
   #MET
   MET = myEvent.getProduct(("SUSYTupelizer","met"))[0]
   #metPhi = myEvent.getProduct(("SUSYTupelizer","metphi"))[0]
   
   #genMET
   genMET = myGenParts.genMET().pt()
   
   #ISR   
   #njets = myEvent.getProduct(("SUSYTupelizer","njets"))[0]
   leadJetPt = myEvent.getProduct(("SUSYTupelizer","jetsPt"))[0] #first = jet with highest pt = leading jet
   leadJetEta = myEvent.getProduct(("SUSYTupelizer","jetsEta"))[0] #first = jet with highest pt = leading jet
   #leadJetPhi = myEvent.getProduct(("SUSYTupelizer","jetsPhi"))[0]
   
   if abs(leadJetEta) < 2.4:
      ISRpt = leadJetPt   
 
   #genISR 
   #get indices of stops (should be 6 and 7)
   istops = myGenParts.indicesByPdgId(1000006)
   assert len(istops)==2
   assert istops==[6,7]
   # get index of first stop daughter
   isdmin = None
   for istop in istops:
     stopds = myGenParts[istop].daughterIndices()
     if isdmin==None or isdmin>stopds[0]:
        isdmin = stopds[0]
   # range of particles (additional radiation) between stops and stop daughters
   print "range of particles between stops and stop daughters",range(8,isdmin)
   
   radiation = []
   
   for myGenPart in myGenParts:
      if myGenPart.index > 7 and myGenPart.index < isdmin: #ISR
         print "rad.: ", myGenPart
         #print "eta: ", myGenPart.particle.eta()
         #print "pt: ", myGenPart.particle.pt()
         radiation.append(myGenPart)
   
   maxPt = 0.0 #None 
   for myGenPart in radiation:
      if abs(myGenPart.particle.eta()) < 2.5: #eta cut
         #print myGenPart
         if myGenPart.particle.pt() > maxPt:
            maxPt = myGenPart.particle.pt()
            genISR = myGenPart
   
   genISRpt = maxPt
   
   print "ISR pt: ", ISRpt
   print "genISR pt: ", genISRpt
            
   #genISRpt = genISR.particle.pt()
   #genISReta = genISR.particle.eta()
   
   #Histogram filling

   stopMass = myEvent.getProduct(("SUSYTupelizer","osetMsq"))[0]
   LSPMass = myEvent.getProduct(("SUSYTupelizer", "osetMC"))[0]
   
   massPoint = str(int(stopMass)) + "_" + str(int(LSPMass)) 
   print massPoint
   
   #MET
   if ISRpt > cuts['ISR']: #presel ISR cut
      hists[massPoint][0].Fill(MET)
 
   if ISRpt > cuts['ISR'] and genMET > cuts['gMET']: # +genMET cut
      hists[massPoint][1].Fill(MET)
   
   hists[massPoint][2].Fill(MET) #no cuts
   
   if genMET > cuts['gMET']: # +genMET cut
      hists[massPoint][3].Fill(MET)
   
   if ISRpt > cuts['ISR'] and genMET > cuts['gMET'] and  genISRpt > cuts['gISR']: #presel + both gCuts
      hists[massPoint][4].Fill(MET)
   
   if genMET > cuts['gMET'] and genISRpt > cuts['gISR']: #both gCuts
      hists[massPoint][5].Fill(MET)
   
   #ISR
   if  MET > cuts['MET']: #presel MET cut
      hists[massPoint][6].Fill(ISRpt)
 
   if MET > cuts['MET'] and genISRpt > cuts['gISR']: #+genISR cut
      hists[massPoint][7].Fill(ISRpt)
   
   hists[massPoint][8].Fill(ISRpt) #no cuts
   
   if genISRpt > cuts['gISR']: #+genISR cut
      hists[massPoint][9].Fill(ISRpt)
   
   if MET > cuts['MET'] and genISRpt > cuts['gISR'] and genMET() > cuts['gMET']: #presel + both gCuts
      hists[massPoint][10].Fill(ISRpt)
   
   if genISRpt > cuts['gISR'] and genMET > cuts['gMET']: #both gCuts
      hists[massPoint][11].Fill(ISRpt)
   
   #print "Masses :", \
   #    myEvent.getProduct(("SUSYTupelizer","osetMC"))[0], \
   #    myEvent.getProduct(("SUSYTupelizer","osetMsq"))[0]
   
   #px = 0.
   #py = 0.
   #for i in istops:
   #    gp = myGenParts[i].particle
   #    px += gp.pt()*math.cos(gp.phi())
   #    py += gp.pt()*math.sin(gp.phi())

   #ptStops = math.sqrt(px**2+py**2)
   #print "Pt = ",ptStops

############################################################################Canvas 1: MET 1 (single gen cut)
print makeDoubleLine()
print "                                                     MET (single generator cut):"
print makeDoubleLine()

c1 = ROOT.TCanvas("c1", "MET 1", 1800, 1500)
c1.Divide(1,2)

#var = "met_pt"

#nbins = 100
#min = 0
#max = 1000

c1.cd(1)
#hists["100_20"][0].SetName("MET 1")
hists["100_20"][0].SetTitle("Generated MET Filter Effect on Reconstructed MET" + massPoint)
hists["100_20"][0].GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
hists["100_20"][0].Draw()
hists["100_20"][0].SetFillColor(ROOT.kRed+1)
hists["100_20"][0].SetLineColor(ROOT.kBlack)
hists["100_20"][0].SetLineWidth(4)

l1 = makeLegend()
l1.AddEntry("MET 1", "MET (no generator cuts)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(hists["100_20"][0])

#hists["100_20"][1].SetName("h2" + massPoint)
hists["100_20"][1].Draw("same")
hists["100_20"][1].SetFillColor(0)
#hists["100_20"][1].SetFillStyle(3001)
hists["100_20"][1].SetLineColor(ROOT.kAzure+7)
hists["100_20"][1].SetLineWidth(4)

#l1.AddEntry("h2" + massPoint, "MET (generator cut)", "F")
#l1.Draw()

#Efficiency and Reduction Factor Calculation 

eff1 = hists["100_20"][3].GetEntries()/hists[massPoint][2].GetEntries()
ineff1 = (hists["100_20"][2].GetEntries()-hists["100_20"][3].GetEntries())/hists["100_20"][2].GetEntries() # = 1 - eff1
red1 = hists["100_20"][2].GetEntries()/hists["100_20"][3].GetEntries() # = 1/eff

#Number of Inefficiencies
#recoCutBin = int(cuts['MET']/(h1.GetXaxis().GetBinWidth(0)))
#numIneff1 = h1.Integral(recoCutBin, max) - h2.Integral(recoCutBin, max) #Integral() in min,max range; Integral(x, 1000000) of total

box1 = makeBox()
box1.AddText("Cuts:")
#box1.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
box1.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
box1.AddText("#bf{ISR Jet #eta cut: }" + str(cuts['Eta']))
box1.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['gMET']) + " GeV")
#box1.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['gISR']) + " GeV")
#box1.AddText("#bf{Gen. ISR Jet Eta #eta cut: }" + str(cuts['gEta']))
#box1.AddLine(0, 0.5, 1, 0.5)
#box1.AddText("")
box1.AddText("Filter:")
box1.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff1))
box1.AddText("#bf{Inefficiencies Fraction: }" + str("%0.3f"%ineff1))
box1.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red1))
box1.Draw()

ROOT.gPad.Update()

#MET Turnon Plot
c1.cd(2)
metTurnon1 = ROOT.TEfficiency(hists["100_20"][1], hists["100_20"][0]) #(passed, total)
metTurnon1.SetTitle("MET Turnon Plot (single generator cut) " + massPoint + "; Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
metTurnon1.SetMarkerColor(ROOT.kBlue)
metTurnon1.SetMarkerStyle(33)
metTurnon1.SetMarkerSize(3)
metTurnon1.Draw("AP") 
metTurnon1.SetLineColor(ROOT.kBlack)
metTurnon1.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
metTurnon1.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) #TEfficiency::GetPaintedGraph()
metTurnon1.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
metTurnon1.GetPaintedGraph().GetXaxis().CenterTitle()
metTurnon1.GetPaintedGraph().GetYaxis().CenterTitle()

#Fitting
fitFunc.SetParameters(0.5, 140, 40, 0.5) #init: (0.5, 140, 40, 0.5)
metTurnon1.Fit(fitFunc)

print makeLine()
print "Filter Efficiency: " + str("%0.3f"%eff1)
print "Inefficiencies Fraction: " + str("%0.3f"%ineff1)
print "Reduction Factor: " + str("%0.3f"%red1)

#Efficiency at Reco Cut
recoEff1_bin = metTurnon1.GetEfficiency(recoBinMET)
recoEff1_fit = fitFunc(cuts['MET'])
print "Efficiency at Reco MET cut (bin): ", str("%0.3f"%recoEff1_bin)
print "Efficiency at Reco MET cut (fit): ", str("%0.3f"%recoEff1_fit)
#print "Number Inefficiencies after Reco MET cut: ", numIneff1

#Fit Parameter Extraction
fit1 = []
#fitFunc.GetParameters(fit1)
fit1.append(fitFunc.GetChisquare())
for x in xrange(0, 4):
   fit1.append(fitFunc.GetParameter(x))
   fit1.append(fitFunc.GetParError(x))

fit1.append(fitFunc.GetX(0.5))
fit1.append(fitFunc.GetX(0.75))
fit1.append(fitFunc.GetX(0.80))
fit1.append(fitFunc.GetX(0.85))
fit1.append(fitFunc.GetX(0.90))
fit1.append(fitFunc.GetX(0.95))
fit1.append(fitFunc.GetX(0.99))
fit1.append(fitFunc.GetX(1))

#box2.Copy(box1)
box2 = ROOT.TPaveText(box1)
box2.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff1_bin))
box2.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff1_fit))
#box2.AddText("Inefficiencies after Reco Cut: " + str(numIneff1))
#box2.AddText("              #bf{Plot:}")
#box2.AddEntry(metTurnon1, "MET Turnon Fit (single cut)", "LP")
box2.Draw()

#c1.SetGridx()
c1.Modified()
c1.Update()

    #c1.SaveAs(savedir + "/MET/MET1_%s_%s.root"%( str(cuts['gMET']), str(cuts['gISR'])))
#########################################################################################Canvas 2: MET 2 (both gen cuts)
#print makeDoubleLine()
#print "                                                       MET (both generator cuts):"
#print makeDoubleLine()
#
#c2 = ROOT.TCanvas("c2", "MET 2", 1800, 1500)
#c2.Divide(1,2)
#
##var = "met_pt"
#
##nbins = 100
##min = 0
##max = 1000
#
#c2.cd(1)
#h5 = h1.Clone()
#h5.SetName("MET 2")
#h5.SetTitle("Generated MET & ISR Jet p_{T} Filter Effect on Reconstructed MET")
##h5.GetXaxis().SetTitle("Missing Transverse Energy #slash{E}_{T} / GeV")
#h5.Draw() 
#h5.SetFillColor(ROOT.kRed+1)
#h5.SetLineColor(ROOT.kBlack)
#h5.SetLineWidth(4)
#
#l2 = makeLegend()
#l2.AddEntry("MET 2", "MET (no generator cuts)", "F")
#
#ROOT.gPad.SetLogy()
##ROOT.gPad.Update()
##alignStats(h5)
#
#h6 = drawhist(T2DegSample, var, preSel1 + "&&" + genSel1 + "&&" + genSel2) # + ISR generator cuts
#h6.SetName("h6")
#h6.Draw("same")
#h6.SetFillColor(0)
##h6.SetFillStyle(3001)
#h6.SetLineColor(ROOT.kAzure+7)
#h6.SetLineWidth(4)
#
#l2.AddEntry("h6", "MET (both generator cuts)", "F")
#l2.Draw()
#
##Efficiency and Reduction Factor Calculation 
#h7 = drawhist(T2DegSample, var, "") #no cuts 
#h8 = drawhist(T2DegSample, var, genSel1 + "&&" + genSel2) #both gen cuts
#
#eff2 = h8.GetEntries()/h7.GetEntries()
#ineff2 = (h7.GetEntries()-h8.GetEntries())/h7.GetEntries()
#red2 = h7.GetEntries()/h8.GetEntries() # = 1/eff
#
##Number of Inefficiencies
##recoCutBin = int(cuts['MET']/(h7.GetXaxis().GetBinWidth(0)))
##numIneff2 = h7.Integral(recoCutBin, max) - h8.Integral(recoCutBin, max) #Integral() in min,max range; Integral(x, 1000000) of total
#
#box3 = makeBox()
#box3.AddText("Cuts:")
##box3.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
#box3.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
#box3.AddText("#bf{ISR Jet #eta cut: }" + str(cuts['Eta']))
#box3.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['gMET']) + " GeV")
#box3.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['gISR']) + " GeV")
#box3.AddText("#bf{Gen. ISR Jet #eta cut: }" + str(cuts['gEta']))
#box3.AddText("Filter:")
#box3.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff2))
#box3.AddText("#bf{Inefficiencies Fraction: }" + str("%0.3f"%ineff2))
#box3.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red2))
#box3.Draw()
#
##MET Turnon Plot
#c2.cd(2)
#metTurnon2 = ROOT.TEfficiency(h6, h5) #(passed, total)
#metTurnon2.SetTitle("MET Turnon Plot (both generator cuts) ; Missing Transverse Energy #slash{E}_{T} / GeV ; Counts")
#metTurnon2.SetMarkerColor(ROOT.kBlue)
#metTurnon2.SetMarkerStyle(33)
#metTurnon2.SetMarkerSize(3)
#metTurnon2.Draw("AP") 
#metTurnon2.SetLineColor(ROOT.kBlack)
#metTurnon2.SetLineWidth(2)
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
#ROOT.gPad.Update()
#metTurnon2.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) #TEfficiency::GetPaintedGraph()
#metTurnon2.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
#metTurnon2.GetPaintedGraph().GetXaxis().CenterTitle()
#metTurnon2.GetPaintedGraph().GetYaxis().CenterTitle()
#
##Fitting
#metTurnon2.Fit(fitFunc)
#
#print makeLine()
#print "Filter Efficiency: " + str("%0.3f"%eff2)
#print "Inefficiencies Fraction: " + str("%0.3f"%ineff2)
#print "Reduction Factor: " + str("%0.3f"%red2)
#
##Efficiency at Reco Cut
#recoEff2_fit = fitFunc(cuts['MET'])
#recoEff2_bin = metTurnon2.GetEfficiency(recoBinMET)
#print "Efficiency at Reco MET cut (bin): ", str("%0.3f"%recoEff2_bin) 
#print "Efficiency at Reco MET cut (fit): ", str("%0.3f"%recoEff2_fit)
##print "Number of Inefficiencies after Reco MET cut: ", numIneff2
#
##Fit Parameter Extraction
#fit2 = []
##fitFunc.GetParameters(fit3)
#fit2.append(fitFunc.GetChisquare())
#for x in xrange(0, 4):
#   fit2.append(fitFunc.GetParameter(x))
#   fit2.append(fitFunc.GetParError(x))
#
#fit2.append(fitFunc.GetX(0.5))
#fit2.append(fitFunc.GetX(0.75))
#fit2.append(fitFunc.GetX(0.80))
#fit2.append(fitFunc.GetX(0.85))
#fit2.append(fitFunc.GetX(0.90))
#fit2.append(fitFunc.GetX(0.95))
#fit2.append(fitFunc.GetX(0.99))
#fit2.append(fitFunc.GetX(1))
#
##box4.Copy(box3)
#box4 = ROOT.TPaveText(box3)
#box4.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff2_bin))
#box4.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff2_fit))
##box4.AddText("Inefficiencies after Reco Cut: " + str(numIneff2))
##box4.AddText("              #bf{Plot:}")
##box4.AddEntry(metTurnon1, "MET Turnon Fit (both cuts)", "LP")
#box4.Draw()
#
##c2.SetGridx()
#c2.Modified()
#c2.Update()
#
#######################################################################################################################################################################################################################################

#################################################################Canvas 3: ISR 1 (single gen cut)
print makeDoubleLine()
print "                                              ISR Jet pT (single generator cut):"
print makeDoubleLine()

c3 = ROOT.TCanvas("c3", "ISR 1", 1800, 1500)
c3.Divide(1,2)

#var = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['Eta']) + "))" #Leading JET pt with eta < 2.4

#nbins = 100
#min = 0
#max = 1000

c3.cd(1)
#hists["100_20"][6].SetName("ISR 1")
hists["100_20"][6].SetTitle("Generated ISR Jet p_{T} Filter Effect on Reconstructed ISR Jet p_{T}")
hists["100_20"][6].GetXaxis().SetTitle("ISR Jet p_{T} / GeV")
hists["100_20"][6].Draw()
hists["100_20"][6].SetFillColor(ROOT.kRed+1)
hists["100_20"][6].SetLineColor(ROOT.kBlack)
hists["100_20"][6].SetLineWidth(4)

l4 = makeLegend()
l4.AddEntry("ISR 1", "ISR Jet p_{T} (MET preselection cut)", "F")

ROOT.gPad.SetLogy()
ROOT.gPad.Update()

alignStats(hists["100_20"][6])

hists["100_20"][7].SetName(massPoint + "_h8")
hists["100_20"][7].Draw("same")
hists["100_20"][7].SetFillColor(0)
#hists["100_20"][7].SetFillStyle(3001)
hists["100_20"][7].SetLineColor(ROOT.kAzure+7)
hists["100_20"][7].SetLineWidth(4)

l4.AddEntry(massPoint + "_h8", "ISR Jet p_{T} (generator cut)", "F")
l4.Draw()

#Efficiency and Reduction Factor Calculation 

eff3 = hists["100_20"][9].GetEntries()/hists["100_20"][8].GetEntries()
ineff3 = (hists["100_20"][8].GetEntries()-hists["100_20"][9].GetEntries())/hists["100_20"][8].GetEntries()
red3 = hists["100_20"][8].GetEntries()/hists["100_20"][9].GetEntries() # = 1/eff

#Number of Inefficiencies
#recoCutBin = int(cuts['MET']/(h3.GetXaxis().GetBinWidth(0)))
#numIneff3 = h9.Integral(recoCutBin, max) - h10.Integral(recoCutBin, max) #Integral() in min,max range; Integral(x, 1000000) of total

box7 = makeBox()
box7.AddText("Cuts:")
box7.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
#box7.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
#box7.AddText("#bf{ISR Jet #eta cut: }" + str(cuts['Eta']))
#box7.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['gMET']) + " GeV")
box7.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['gISR']) + " GeV")
box7.AddText("#bf{Gen. ISR Jet #eta cut: }" + str(cuts['gEta']))
box7.AddText("Filter:")
box7.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff3))
box7.AddText("#bf{Inefficiencies Fraction: }" + str("%0.3f"%ineff3))
box7.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red3))
box7.Draw()

#Jet Turnon Plot
c3.cd(2)
isrTurnon1 = ROOT.TEfficiency(hists["100_20"][7], hists["100_20"][6]) #(passed, total)
isrTurnon1.SetTitle("ISR Jet p_{T} Turnon Plot (single generator cut)" + massPoint + "; ISR Jet p_{T} / GeV ; Counts")
isrTurnon1.SetMarkerColor(ROOT.kBlue)
isrTurnon1.SetMarkerStyle(33)
isrTurnon1.SetMarkerSize(3)
isrTurnon1.Draw("AP") 
isrTurnon1.SetLineColor(ROOT.kBlack)
isrTurnon1.SetLineWidth(2)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
ROOT.gPad.Update()
isrTurnon1.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) #TEfficiency::GetPaintedGraph()
isrTurnon1.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
isrTurnon1.GetPaintedGraph().GetXaxis().CenterTitle()
isrTurnon1.GetPaintedGraph().GetYaxis().CenterTitle()

#Fitting
fitFunc.SetParameters(0.45, 70, 20, 0.6) #init: (0.45,60,20,0.6)
#fitFunc.SetParLimits(1, 0, 120) #init: [0,120]
isrTurnon1.Fit(fitFunc)

print makeLine()
print "Filter Efficiency: " + str("%0.3f"%eff3)
print "Reduction Factor: " + str("%0.3f"%red3)
print "Inefficiencies Fraction: " + str("%0.3f"%ineff3)

#Efficiency at Reco Cut
recoEff3_bin = isrTurnon1.GetEfficiency(recoBinISR)
recoEff3_fit = fitFunc(cuts['ISR'])
print "Efficiency at Reco ISR Jet pT cut (bin): ", str("%0.3f"%recoEff3_bin) 
print "Efficiency at Reco ISR Jet pT cut (fit): ", str("%0.3f"%recoEff3_fit)
#print "Number of Inefficiencies after Reco ISR Jet pT cut: ", numIneff4

#Fit Parameter Extraction
fit3 = []
#fitFunc.GetParameters(fit4)
fit3.append(fitFunc.GetChisquare())
for x in xrange(0, 4):
   fit3.append(fitFunc.GetParameter(x))
   fit3.append(fitFunc.GetParError(x))

fit3.append(fitFunc.GetX(0.5))
fit3.append(fitFunc.GetX(0.75))
fit3.append(fitFunc.GetX(0.80))
fit3.append(fitFunc.GetX(0.85))
fit3.append(fitFunc.GetX(0.90))
fit3.append(fitFunc.GetX(0.95))
fit3.append(fitFunc.GetX(0.99))
fit3.append(fitFunc.GetX(1))

box8 = ROOT.TPaveText(box7)
box8.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff3_bin))
box8.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff3_fit))
#box8.AddText("Inefficiencies after Reco Cut: " + str(numIneff4))
#box8.AddText("              #bf{Plot:}")
#box8.AddEntry(jetTurnon1, "ISR Turnon Fit (single cut)", "LP")
box8.Draw()

#c3.SetGridx()
c3.Modified()
c3.Update() 

################################################################################Canvas 4: ISR 2 (both gen cuts)
#print makeDoubleLine()
#print "                                                         ISR Jet pT (both generator cuts):"
#print makeDoubleLine()
#
#c5 = ROOT.TCanvas("c5", "ISR 2", 1800, 1500)
#c5.Divide(1,2)
#
##var = "Max$(Jet_pt*(abs(Jet_eta)<" + str(cuts['Eta']) + "))" #Leading JET (highest pT) with eta < 2.4 
#
##nbins = 100
##min = 0
##max = 1000
#
#c5.cd(1)
#h17 = h13.Clone()
#h17.SetName("ISR 2")
#h17.SetTitle("Generated ISR Jet p_{T} & MET Filter Effect on Reconstructed ISR Jet p_{T}")
#h17.GetXaxis().SetTitle("ISR Jet p_{T} / GeV")
#h17.Draw() #MET preselection cut
#h17.SetFillColor(ROOT.kRed+1)
#h17.SetLineColor(ROOT.kBlack)
#h17.SetLineWidth(4)
#
#l5 = makeLegend()
#l5.AddEntry("ISR 2", "ISR Jet p_{T} (no generator cuts)", "F")
#
#ROOT.gPad.SetLogy()
##ROOT.gPad.Update()
##alignStats(h17)
#
#h18 = drawhist(T2DegSample, var, preSel2 + "&&" + genSel2 + "&&" + genSel1) # + MET generator cut
#h18.SetName("h14")
#h18.Draw("same")
#h18.SetFillColor(0)
##h18.SetFillStyle(3001)
#h18.SetLineColor(ROOT.kAzure+7)
#h18.SetLineWidth(4)
#
#l5.AddEntry("h17", "ISR Jet p_{T} (both generator cuts)", "F")
#l5.Draw()
#
##Efficiency and Reduction Factor Calculation 
#h19 = drawhist(T2DegSample, var, "") #no cuts
#h20 = drawhist(T2DegSample, var, genSel2 + "&&" + genSel1) #both gen cuts
#
#eff5 = h20.GetEntries()/h19.GetEntries()
#ineff5 = (h19.GetEntries()-h20.GetEntries())/h19.GetEntries()
#red5 = h19.GetEntries()/h20.GetEntries() # = 1/eff
#
##Number of Inefficiencies
##recoCutBin = int(cuts['MET']/(h17.GetXaxis().GetBinWidth(0)))
##numIneff5 = h17.Integral(recoCutBin, max) - h18.Integral(recoCutBin, max) #Integral() in min,max range; Integral(x, 1000000) of total
#
#box9 = makeBox()
#box9.AddText("Cuts:")
#box9.AddText("#bf{MET p_{T} cut: }" + str(cuts['MET']) + " GeV")
##box9.AddText("#bf{ISR Jet p_{T} cut: }" + str(cuts['ISR']) + " GeV")
##box9.AddText("#bf{ISR Jet Eta #eta cut: }" + str(cuts['Eta']))
#box9.AddText("#bf{Gen. MET p_{T} cut: }" + str(cuts['gMET']) + " GeV")
#box9.AddText("#bf{Gen. ISR Jet p_{T} cut: }" + str(cuts['gISR']) + " GeV")
#box9.AddText("#bf{Gen. ISR Jet #eta cut: }" + str(cuts['gEta']))
#box9.AddText("Filter:")
#box9.AddText("#bf{Filter Efficiency: }" + str("%0.3f"%eff5))
#box9.AddText("#bf{Inefficiencies Fraction }" + str("%0.3f"%ineff5))
#box9.AddText("#bf{Reduction Factor: }" + str("%0.3f"%red5))
#box9.Draw()
#
##Jet Turnon Plot
#c5.cd(2)
#isrTurnon2 = ROOT.TEfficiency(h18, h17) #(passed, total)
#isrTurnon2.SetTitle("ISR Jet p_{T} Turnon Plot (both generator cuts) ; ISR Jet p_{T} / GeV ; Counts")
#isrTurnon2.SetMarkerColor(ROOT.kBlue)
#isrTurnon2.SetMarkerStyle(33)
#isrTurnon2.SetMarkerSize(3)
#isrTurnon2.Draw("AP") #L/C option for curve | * - Star markers #X - no error bars
#isrTurnon2.SetLineColor(ROOT.kBlack)
#isrTurnon2.SetLineWidth(2)
#ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()
#ROOT.gPad.Update()
#isrTurnon2.GetPaintedGraph().GetXaxis().SetRangeUser(0,1000) #TEfficiency::GetPaintedGraph()
#isrTurnon2.GetPaintedGraph().GetXaxis().SetNdivisions(540, 1)
#isrTurnon2.GetPaintedGraph().GetXaxis().CenterTitle()
#isrTurnon2.GetPaintedGraph().GetYaxis().CenterTitle()
#
##Fitting
##fitFunc.SetParameters(0.45, 60, 20, 0.6) #init: (0.45,60,20,0.6)
##fitFunc.SetParLimits(2, 10, 16)
#isrTurnon2.Fit(fitFunc)
#
#print makeLine()
#print "Filter Efficiency: " + str("%0.3f"%eff5)
#print "Reduction Factor: " + str("%0.3f"%red5)
#print "Inefficiencies Fraction: " + str("%0.3f"%ineff5)
#
##Efficiency at Reco Cut
#recoEff5_bin = isrTurnon2.GetEfficiency(recoBinISR)
#recoEff5_fit = fitFunc(cuts['ISR'])
#print "Efficiency at Reco ISR Jet pT cut (bin): ", str("%0.3f"%recoEff5_bin)
#print "Efficiency at Reco ISR Jet pT cut (fit): ", str("%0.3f"%recoEff5_fit)
##print "Number of Inefficiencies after Reco ISR Jet pT cut: ", numIneff4
#print makeLine()
#
##Fit Parameter Extraction
#fit5 = []
##fitFunc.GetParameters(fit4)
#fit5.append(fitFunc.GetChisquare())
#for x in xrange(0, 4):
#   fit5.append(fitFunc.GetParameter(x))
#   fit5.append(fitFunc.GetParError(x))
#
#fit5.append(fitFunc.GetX(0.5))
#fit5.append(fitFunc.GetX(0.75))
#fit5.append(fitFunc.GetX(0.80))
#fit5.append(fitFunc.GetX(0.85))
#fit5.append(fitFunc.GetX(0.90))
#fit5.append(fitFunc.GetX(0.95))
#fit5.append(fitFunc.GetX(0.99))
#fit5.append(fitFunc.GetX(1))
#
##box8.Copy(box1)
#box10 = ROOT.TPaveText(box9)
#box10.AddText("#bf{Efficiency at Reco Cut (bin): }" + str("%0.3f"%recoEff5_bin))
#box10.AddText("#bf{Efficiency at Reco Cut (fit): }" + str("%0.3f"%recoEff5_fit))
##box10.AddText("Inefficiencies after Reco Cut: " + str(numIneff5))
##box10.AddText("              #bf{Plot:}")
##box10.AddEntry(isrTurnon2, "ISR Turnon Fit (both cuts)", "LP")
#box10.Draw()
#
##c5.SetGridx()
#c5.Modified()
#c5.Update()
# 
##Write to file
#savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/8TeV/filter_%s_%s"%(str(cuts["gMET"]),str(cuts["gISR"])) #web directory http://www.hephy.at/user/mzarucki/plots/filter/
#
#if not os.path.exists(savedir):
#   os.makedirs(savedir)
#
#if not os.path.exists(savedir + "/MET"):
#   os.makedirs(savedir + "/MET")
#
#if not os.path.exists(savedir + "/ISR"):
#   os.makedirs(savedir + "/ISR")
#
#outfile1 = open(savedir + "/filterResults_%s_%s.txt"%(str(cuts["gMET"]),str(cuts["gISR"])), "w")
#print >> outfile1, "Generator Filter Results", "\n", makeLine(), "\n", cutString, "\n", makeLine(), "\n", \
#"Variable", "    ", "Filter Efficiency", "   ", "Inefficiencies Fraction", "   ", "Reduction Factor", "  ", "Efficiency at Reco Cut (bin)","   ", "Efficiency at Reco Cut (fit)", "\n\n", \
#"MET1       ", "    ", eff1, "     ", ineff1, "         ", red1, "      ", recoEff1_bin, "                ", recoEff1_fit, "\n\n", \
#"MET2       ", "    ", eff2, "     ", ineff2, "         ", red2, "      ", recoEff2_bin, "                ", recoEff2_fit, "\n\n", \
#"MET3       ", "    ", eff3, "     ", ineff3, "         ", red3, "      ", recoEff3_bin, "                ", recoEff3_fit, "\n\n", \
#"ISR1       ", "    ", eff4, "     ", ineff4, "         ", red4, "      ", recoEff4_bin, "                ", recoEff4_fit, "\n\n", \
#"ISR2       ", "    ", eff5, "     ", ineff5, "         ", red5, "      ", recoEff5_bin, "                ", recoEff5_fit, "\n\n", \
#"ISR3       ", "    ", eff6, "     ", ineff6, "         ", red6, "      ", recoEff6_bin, "                ", recoEff6_fit, "\n", \
#makeLine(), "\n", \
#"Turnon fit results:", "\n\n", \
#" ", "ChiSquared", "   ", fitFunc.GetParName(0), "  ", fitFunc.GetParName(0) + "_Err", "    ", fitFunc.GetParName(1), "        ", \
#fitFunc.GetParName(1) + "_Err", "     ", fitFunc.GetParName(2), "    ", fitFunc.GetParName(2) + "_Err", "   ", \
#fitFunc.GetParName(3), "   ", fitFunc.GetParName(3) + "_Err", "\n\n", \
#fit1[0], " ", fit1[1], " ", fit1[2], " ", fit1[3], " ", fit1[4], " ", fit1[5], " ", fit1[6], " ", fit1[7], " ", fit1[8], "\n\n", \
#fit2[0], " ", fit2[1], " ", fit2[2], " ", fit2[3], " ", fit2[4], " ", fit2[5], " ", fit2[6], " ", fit2[7], " ", fit2[8], "\n\n", \
#fit3[0], " ", fit3[1], " ", fit3[2], " ", fit3[3], " ", fit3[4], " ", fit3[5], " ", fit3[6], " ", fit3[7], " ", fit3[8], "\n\n", \
#fit4[0], " ", fit4[1], " ", fit4[2], " ", fit4[3], " ", fit4[4], " ", fit4[5], " ", fit4[6], " ", fit4[7], " ", fit4[8], "\n\n", \
#fit5[0], " ", fit5[1], " ", fit5[2], " ", fit5[3], " ", fit5[4], " ", fit5[5], " ", fit5[6], " ", fit5[7], " ", fit5[8], "\n\n", \
#fit6[0], " ", fit6[1], " ", fit6[2], " ", fit6[3], " ", fit6[4], " ", fit6[5], " ", fit6[6], " ", fit6[7], " ", fit6[8], "\n", \
#makeLine(), "\n", \
#"Variable values for various efficiecies:", "\n\n", \
#"Efficiency:        50%           75%            80%           85%           90%           95%           99%          100%", "\n\n", \
#"MET1        ", fit1[9], fit1[10], fit1[11], fit1[12], fit1[13], fit1[14], fit1[15], fit1[16], "\n\n", \
#"MET2        ", fit2[9], fit2[10], fit2[11], fit2[12], fit2[13], fit2[14], fit2[15], fit2[16], "\n\n", \
#"MET3        ", fit3[9], fit3[10], fit3[11], fit3[12], fit3[13], fit3[14], fit3[15], fit3[16], "\n\n", \
#"ISR1        ", fit4[9], fit4[10], fit4[11], fit4[12], fit4[13], fit4[14], fit4[15], fit4[16], "\n\n", \
#"ISR2        ", fit5[9], fit5[10], fit5[11], fit5[12], fit5[13], fit5[14], fit5[15], fit5[16], "\n\n", \
#"ISR3        ", fit6[9], fit6[10], fit6[11], fit6[12], fit6[13], fit6[14], fit6[15], fit6[16]
#outfile1.close()
#
#outfile2 = open(savedir + "/reductionEfficiency_%s_%s.txt"%(str(cuts["gMET"]),str(cuts["gISR"])), "w")
#outfile2.write(\
#"gMET Cut" + "   " + "gISR Cut" + "    " + "MET 1 Red. Factor" + "    " + "MET 1 Reco Eff." + "    " + "MET 2 Red. Factor" + "    " + "MET 2 Reco Eff." + "    " + "ISR 1 Red. Factor" + "    " + "ISR 1 Reco Eff." + "    " + "ISR 2 Red. Factor" + "    " + "ISR 2 Reco Eff." + "\n" +\
#"  " + str(cuts["gMET"]) + "         " + str(cuts["gISR"]) + "         " + str(red1) + "      " + str(recoEff1_bin) + "      " + str(red2) + "      " + str(recoEff2_bin) + "      " + str(red4) + "      " + str(recoEff4_bin) + "      " + str(red5) + "      " + str(recoEff5_bin)\
#)
#outfile2.close()

#outfile.write("")

##Save to Web
#c1.SaveAs(savedir + "/MET/MET1_%s_%s.root"%( str(cuts['gMET']), str(cuts['gISR'])))
#c2.SaveAs(savedir + "/MET/MET2_%s_%s.root"%(str(cuts['gMET']), str(cuts['gISR'])))
#c3.SaveAs(savedir + "/MET/MET3_%s_%s.root"%(str(cuts['gMET']), str(cuts['gISR'])))
#c4.SaveAs(savedir + "/ISR/ISR1_%s_%s.root"%(str(cuts['gMET']), str(cuts['gISR'])))
#c5.SaveAs(savedir + "/ISR/ISR2_%s_%s.root"%(str(cuts['gMET']), str(cuts['gISR'])))
#c6.SaveAs(savedir + "/ISR/ISR3_%s_%s.root"%(str(cuts['gMET']), str(cuts['gISR'])))
#
#c1.SaveAs(savedir + "/MET/MET1_%s_%s.png"%( str(cuts['gMET']), str(cuts['gISR'])))
#c2.SaveAs(savedir + "/MET/MET2_%s_%s.png"%(str(cuts['gMET']), str(cuts['gISR'])))
#c3.SaveAs(savedir + "/MET/MET3_%s_%s.png"%(str(cuts['gMET']), str(cuts['gISR'])))
#c4.SaveAs(savedir + "/ISR/ISR1_%s_%s.png"%(str(cuts['gMET']), str(cuts['gISR'])))
#c5.SaveAs(savedir + "/ISR/ISR2_%s_%s.png"%(str(cuts['gMET']), str(cuts['gISR'])))
#c6.SaveAs(savedir + "/ISR/ISR3_%s_%s.png"%(str(cuts['gMET']), str(cuts['gISR'])))
#
#c1.SaveAs(savedir + "/MET/MET1_%s_%s.pdf"%( str(cuts['gMET']), str(cuts['gISR'])))
#c2.SaveAs(savedir + "/MET/MET2_%s_%s.pdf"%(str(cuts['gMET']), str(cuts['gISR'])))
#c3.SaveAs(savedir + "/MET/MET3_%s_%s.pdf"%(str(cuts['gMET']), str(cuts['gISR'])))
#c4.SaveAs(savedir + "/ISR/ISR1_%s_%s.pdf"%(str(cuts['gMET']), str(cuts['gISR'])))
#c5.SaveAs(savedir + "/ISR/ISR2_%s_%s.pdf"%(str(cuts['gMET']), str(cuts['gISR'])))
#c6.SaveAs(savedir + "/ISR/ISR3_%s_%s.pdf"%(str(cuts['gMET']), str(cuts['gISR'])))

#if __name__ == '__main__':
#   sys.exit(main(sys.argv[1], sys.argv[2]))
