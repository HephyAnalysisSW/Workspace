#redMassScanDPM.py for 8TeV
#Use: 'python 2DredMassScanDPM.py --first=## -b //dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_240614/T2DegenerateStop_2J_mStop-100to150-4/'

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

def makeLine():
   line = "\n**********************************************************************************************************************************\n"
   return line

#def makeBox():
#   box = ROOT.TPaveText(0.775,0.40,0.875,0.65, "NDC") #NB & ARC
#   #box.SetHeader("Cuts")
#   #header = box.GetListOfPrimitives().First()
#   #header.SetTextAlign(22)
#   return box 

def alignStats(hist):
   st = hist.FindObject("stats")
   st.SetX1NDC(0.775)
   st.SetX2NDC(0.875)
   st.SetY1NDC(0.7)
   st.SetY2NDC(0.85)

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
   def __init__(self,genParticles,nGenParts=30):
     """create list and set mother and daughter indices"""
    
     self.genParts = []
     
     self.addresses = []
     for ip,p in enumerate(genParticles):
        if ip > nGenParts: break
        #print "ip: ", ip
        #self.addresses.append(id(p))
        # create and add MyGenParticle
        mp = MyGenParticle(ip,p)
        self.genParts.append(mp)
        # create a unique object identifying the particle
        #   (for some reason the use of the ROOT address does not work)
        self.addresses.append(mp.xid())
 
     for i,mp in enumerate(self.genParts):
       # now look for indices of mother particles and set the corresponding fields in MyGenParticle
       if i > nGenParts: break
       #print "i", i
       nm = mp.particle.numberOfMothers()
       if nm:
          try:
            firstMotherIndex = self.index(mp.particle.mother(0))
          except ValueError:
            firstMotherIndex = -1
       
          try:
            lastMotherIndex = self.index(mp.particle.mother(nm-1))
          except ValueError:
            lastMotherIndex = -1
          
          mp.mothers = (firstMotherIndex,lastMotherIndex)
       
       else:
          mp.mothers = (-1, -1)
       
       #same for daughters
       nd = mp.particle.numberOfDaughters()
       
       if nd: #if has daughters
          #print "Number of Daughters: ", nd
       
          try:
            firstDaughterIndex = self.index(mp.particle.daughter(0))
          except ValueError:
            firstDaughterIndex = -1

          try:
            lastDaughterIndex = self.index(mp.particle.daughter(nd-1))
          except ValueError:
            lastDaughterIndex = -1
 
          mp.daughters = (firstDaughterIndex,lastDaughterIndex)
       
       else:
          mp.daughters = (-1, -1)

       #lastDaughterIndex = self.index(mp.particle.daughter(nd-1))
       #   if firstDaughterIndex > nGenParts:
       #      print "> 30"
       #      firstDaughterIndex = -1
       #   else:
       #      firstDaughter
       #   if lastDaughterIndex > nGenParts:
       #      print "> 30"
       #      lastDaughterIndex = -1
       #   mp.daughters = (firstDaughterIndex, lastDaughterIndex)
       #print "Daughter indices: ", firstDaughterIndex, " ", lastDaughterIndex 
 
   def __getitem__(self,index):
     """allow access via [] operator"""
     return self.genParts[index]
 
   #def motherIndices(self,index):
   #  """get range of indices of mother particles for particle at position <index>"""
   #  mp = self.genParts[index]
   #  if mp.mothers==None:
   #     gp = mp.particle
   #     nm = gp.numberOfMothers()
   #     if nm:
   #        mp.mothers = (self.index(gp.mother(0)), self.index(gp.mother(nm-1)))
   #     else:
   #        mp.mothers = (-1, -1)
   #  return mp.motherIndices()
 
   #def daughterIndices(self,index):
   #   """get range of indices of daughter particles for particle at position <index>"""
   #   mp = self.genParts[index]
   #   if mp.daughters==None:
   #      gp = mp.particle
   #      nd = gp.numberOfDaughters()
   #      if nd:
   #         mp.daughters = (self.index(gp.daughter(0)), self.index(gp.daughter(nd-1)))
   #      else:
   #         mp.daughters = (-1, -1)
   #   return mp.daughterIndices()
 
   def indexFromAddress(self,address):
      result = self.addresses.index(address)
      assert result>=0
      return result
 
   def index(self,particle):
     #return self.indexFromAddress(id(particle))
      return self.indexFromAddress(self.genParts[0].xid(particle))
 
   def indicesByPdgId(self,pdgIds,useAbs=True,indices=None):
      """Get all indices for particles with pdg (or pdg in) pdgIds by default the absolute value is used. Optionally restrict search to a list of indices."""
      result  = []
      if type(pdgIds)==type(0):
         pdgIds_ =  [pdgIds]
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
 
   #def lastInChain(self,index):
   #  """Follow mother-daughter chain for a particle as long as the daughter==mother (or the difference is only the radiation of a photon or gluon"""
   #  result = index
   #  mp = self.genParts[index]
   #  pdgId = mp.particle.pdgId()
   #  while True:
   #    idas = self.genParts[result].daughterIndices()
   #    if not idas:
   #      return result
   #    daIds = { }
   #    for ida in idas:
   #      pdgIdDa = self.genParts[ida].particle.pdgId()
   #      if not pdgIdDa in daIds:
   #        daIds[pdgIdDa] = [ ]
   #      daIds[pdgIdDa].append(ida)
   #    if len(daIds.keys())>2 or ( not pdgId in daIds ) or len(daIds[pdgId])>1:
   #      break
   #    if len(daIds.keys())==1:
   #      if len(daIds[pdgId])!=1:
   #        break
   #    else:
   #      otherIds = [ x for x in daIds.keys() if x != pdgId ]
   #      if otherIds[0]!=21 and otherIds[0] != 22:
   #        break
   #    if daIds[pdgId][0]==result:
   #      print "Daughters point back to same line???"
   #      break
   #    result = daIds[pdgId][0]
   #      
   #  return result

   #def genMET(self):
   #  """Calculate MET from the sum of neutrinos or neutralino_1s"""
   #  metx = 0.
   #  mety = 0.
   #  for mp in self.genParts:
   #    if mp.particle.status()==1:
   #      pdgId = abs(mp.particle.pdgId())
   #      if pdgId==1000022 or pdgId==12 or pdgId==14 or pdgId==16:
   #        pt = mp.particle.pt()
   #        phi = mp.particle.phi()
   #        metx += pt*math.cos(phi)
   #        mety += pt*math.sin(phi)
   #  return MyMET(metx,mety)

   def __str__(self):
      result = ""
      for mp in self.genParts:
         result += str(mp) + "\n"
      return result


# arguments and options
dir =  "//dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_240614/T2DegenerateStop_2J_mStop-100to150-4/" #"/afs/hephy.at/work/w/wadam/CMSSW_5_3_20/src/T2DegenerateStop_2J_mStop-100to150-4/"

parser = OptionParser()
parser.add_option("--first", dest="first",  help="index of first file", type="int", default=1)
parser.add_option("--maxFiles", dest="number",  help="number of files", type="int", default=1)
parser.add_option("--job", dest="jobNumber",  help="job number", type="int", default=0)
parser.add_option("--masses", dest="stopMasses",  help="stop mass range", type="str", default="100to150")
parser.add_option("-b", dest="batch",  help="batch", action="store_true", default=False)
(options, args) = parser.parse_args()
if len(args)==0:
   args = [dir]
   print "No input files given."
   #exit()
assert len(args)==1
dpmDir = args[0]
if not dpmDir.endswith("/"):
  dpmDir += "/"

massRanges = ["100to150", "175to225", "250to300", "325to375", "400"]

if options.stopMasses not in massRanges:
   print "Please choose valid stop mass range from: 100to150, 175to225, 250to300, 325to375 or 400."
   #exit()

files = []
p = subprocess.Popen(["dpns-ls",dpmDir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
  fn = line[:-1]
  if fn.endswith(".root"):
    files.append("root://hephyse.oeaw.ac.at"+dpmDir+fn)
files.sort()
if options.first < 1:
   print "Choose file index starting from 1."
   #exit()

files = files[(options.first-1):]
if options.number!=None:
  files = files[:options.number]

print makeLine()
print "Starting with file:", files[0], "corresponding to file index ", options.first
print "Ending with file:", files[options.number-1], "corresponding to file index ", options.first + options.number - 1
print makeLine()

#wrapper for events and product definitions
myEvent = MyEvent()
myEvent.defineProduct("genParticles","std::vector<reco::GenParticle>")
#myEvent.defineProduct(("SUSYTupelizer","met"), "float")
#myEvent.defineProduct(("SUSYTupelizer","metphi"), "float")
myEvent.defineProduct(("SUSYTupelizer","osetMC"), "float") #LSP mass
myEvent.defineProduct(("SUSYTupelizer","osetMsq"), "float") #stop mass
#myEvent.defineProduct(("SUSYTupelizer","njets"), "int")
#myEvent.defineProduct(("SUSYTupelizer","jetsPt"), "vector<float>")
#myEvent.defineProduct(("SUSYTupelizer","jetsEta"), "vector<float>")
#myEvent.defineProduct(("SUSYTupelizer","jetsPhi"), "vector<float>")
myEvent.defineProduct(("SUSYTupelizer","genmet"), "float")

#genMETcut = input("Enter Generated MET cut value: ")
#genHTcut = input("Enter Generated ISR Jet pT cut value: ")

#Cuts 
cuts=({\
'MET' : 120, #MET cut (fixed)
'HT' : 200, #HT cut (fixed)
'HTjetPt' : 40, #Jet pt threshold for HT (fixed)
'HTjetEta' : 3, #Jet eta cut for HT (fixed)

'genMET' : 60, #generated quantity cuts
'genHT' : 160,
'genHTjetPt' : 30, #GenJet pt threshold for HT
'genHTjetEta' : 5 #GenJet eta cut for HT
})

cutString = \
"Preselection cuts: \n\n" + \
"MET cut: " + str(cuts['MET']) + "\n" + \
"HT cut: " + str(cuts['HT']) + "\n" + \
"HT Jets pT cut: " + str(cuts['HTjetPt']) + "\n" + \
"HT Jets eta cut: " + str(cuts['HTjetEta']) + "\n\n" + \
"Generator cuts:" + "\n\n" + \
"Generated MET cut: " + str(cuts['genMET']) + "\n" + \
"Generated HT cut: " + str(cuts['genHT']) + "\n" + \
"Generated HT Jets pT cut: " + str(cuts['genHTjetPt']) + "\n" + \
"Generated HT Jets eta cut: " + str(cuts['genHTjetEta'])

print makeLine()
print cutString
print makeLine()
 
#Preselection and Generated Particles Filter Selection

totalCounts = ROOT.TH2F("h1", "Total Counts", 80, 50, 450, 18, 0, 90)
passedCounts = ROOT.TH2F("h2", "Passed Counts", 80, 50, 450, 18, 0, 90)

#inspect specific events
#for iev,event in enumerate(events):
#   myEvent.load(event)
#   genParts = myEvent.getProduct("genParticles")
#   myGenParts = MyGenParticles(genParts)
#
#   if iev == 1: #event number
#      print myGenParts
#      break

events = Events(files)
#print "Total number of events is ",events.size()
   
#event loop

for iev,event in enumerate(events):
   #if iev == 10: break
   if iev%10000==0:
      print "At event",iev,"the file index is", options.first + event.fileIndex()
   myEvent.load(event)
   
   genParts = myEvent.getProduct("genParticles")#[0:30]
   myGenParts = MyGenParticles(genParts)#[0:30]
  
   #MET
   #MET = myEvent.getProduct(("SUSYTupelizer","met"))[0]
   #metPhi = myEvent.getProduct(("SUSYTupelizer","metphi"))[0]
   
   #genMET
   #genMET = myGenParts.genMET().pt()
   genMET = myEvent.getProduct(("SUSYTupelizer", "genmet"))[0]
   
   #Masses
   stopMass = myEvent.getProduct(("SUSYTupelizer","osetMsq"))[0]
   LSPMass = myEvent.getProduct(("SUSYTupelizer", "osetMC"))[0]
   
   totalCounts.Fill(stopMass, stopMass-LSPMass)
   
   #if genMET < cuts['genMET']:
   #   continue #skips iteration, as both cuts need to be applied
   
   #ISR   
   #njets = myEvent.getProduct(("SUSYTupelizer","njets"))[0]
   #if myEvent.getProduct(("SUSYTupelizer","jetsPt")).empty() != True:
   #   leadJetPt = myEvent.getProduct(("SUSYTupelizer","jetsPt"))[0] #first = jet with highest pt = leading jet
   #else: leadJetPt = 0.0

   #if myEvent.getProduct(("SUSYTupelizer","jetsEta")).empty() != True:
   #   leadJetEta = myEvent.getProduct(("SUSYTupelizer","jetsEta"))[0] #first = jet with highest pt = leading jet
   #else: leadJetEta = 0.0
   #
   ##leadJetPhi = myEvent.getProduct(("SUSYTupelizer","jetsPhi"))[0]
   #
   #if abs(leadJetEta) < 2.4:
   #   ISRpt = leadJetPt
    
   ##genISR 
   ##
   #get indices of stops (should be 6 and 7)
   istops = myGenParts.indicesByPdgId(1000006) #indices = 6,7
   #if len(istops)!=2: print myGenParts
   assert len(istops)==2
   assert istops==[6,7]
   ## get index of first stop daughter
   #isdmin = None
   #for istop in istops:
   #  stopds = myGenParts[istop].daughterIndices()
   #  if isdmin==None or isdmin>stopds[0]:
   #     isdmin = stopds[0]
   ## range of particles (additional radiation) between stops and stop daughters
   ##print "range of particles between stops and stop daughters",range(8,isdmin)
   
   #maxPt = 0.0 #None 
   #for myGenPart in myGenParts:
   #   if myGenPart.index > 7 and myGenPart.index < isdmin: #ISR
   #      if abs(myGenPart.particle.eta()) < 2.5: #eta cut
   #         #print myGenPart
   #         if myGenPart.particle.pt() > maxPt:
   #            maxPt = myGenPart.particle.pt()
   #            #genISR = myGenPart
   #
   #genISRpt = maxPt
   
   quarkPdgIds = [1, 2, 3, 4, 5, 6, 7, 8, 21] # +gluon
   #print myGenParts
   genHT = 0.0
   for myGenPart in myGenParts:
      if myGenPart.index > 7 and myGenPart.particle.status() == 3 and abs(myGenPart.particle.pdgId()) in quarkPdgIds: #hadronic activity after stops
         #print myGenPart
         if myGenPart.particle.pt() > cuts['genHTjetPt'] and abs(myGenPart.particle.eta()) < cuts['genHTjetEta']:
            #print myGenPart
            genHT += myGenPart.particle.pt()
            #print "HT :", genHT

   #print "total HT: ", genHT
   #print "Event: ", iev, ", ISR pt: ", ISRpt
   #print "genISR pt: ", genISRpt
            
   #genISRpt = genISR.particle.pt()
   #genISReta = genISR.particle.eta()
   
   #Histogram filling

   if genMET > cuts['genMET'] and genHT > cuts['genHT']: #both gCuts
      passedCounts.Fill(stopMass, stopMass-LSPMass)

#Drawing 2D Histograms
   
c1 = ROOT.TCanvas("c1", "2D Counts", 1800, 1500)
c1.Divide(1,2)

c1.cd(1)
#totalCounts.SetTitle("MET and ISR Jet p_{T} Histogram (no generator cuts)")
totalCounts.GetXaxis().SetTitle("Stop Mass / GeV")
totalCounts.GetYaxis().SetTitle("#Deltam / GeV")
totalCounts.GetZaxis().SetTitle("Counts")
totalCounts.GetXaxis().SetTitleOffset(1.6)
totalCounts.GetYaxis().SetTitleOffset(1.6)
totalCounts.GetZaxis().SetTitleOffset(1.6)
totalCounts.GetXaxis().CenterTitle()
totalCounts.GetYaxis().CenterTitle()
totalCounts.GetZaxis().CenterTitle()
#totalCounts.GetYaxis().SetRangeUser(0, 500)
#totalCounts.GetXaxis().SetRangeUser(0, 500)
totalCounts.GetZaxis().SetRangeUser(0, 10000)
#totalCounts.SetAxisRange(0, 1000, "X")
#totalCounts.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
#totalCounts.SetMinimum(0)
#totalCounts.SetMaximum(2E7)
totalCounts.Draw("COLZ") #CONT1-5 #plots the graph with axes and points

ROOT.gPad.SetLogz()
ROOT.gPad.Update()

alignStats(totalCounts)

c1.cd(2)
#passedCounts.SetTitle("MET and ISR Jet p_{T} Histogram (no generator cuts)")
passedCounts.GetXaxis().SetTitle("Stop Mass / GeV")
passedCounts.GetYaxis().SetTitle("#Deltam / GeV")
passedCounts.GetZaxis().SetTitle("Counts")
passedCounts.GetXaxis().SetTitleOffset(1.6)
passedCounts.GetYaxis().SetTitleOffset(1.6)
passedCounts.GetZaxis().SetTitleOffset(1.6)
passedCounts.GetXaxis().CenterTitle()
passedCounts.GetYaxis().CenterTitle()
passedCounts.GetZaxis().CenterTitle()
#passedCounts.GetYaxis().SetRangeUser(0, 500)
#passedCounts.GetXaxis().SetRangeUser(0, 500)
passedCounts.GetZaxis().SetRangeUser(0, 10000)
#passedCounts.SetAxisRange(0, 1000, "X")
#passedCounts.SetAxisRange(0, 2E6, "Y") #automatically calls SetMin-/Max-imum()
#passedCounts.SetMinimum(0)
#passedCounts.SetMaximum(2E7)
passedCounts.Draw("COLZ") #CONT1-5 #plots the graph with axes and points

ROOT.gPad.SetLogz()
ROOT.gPad.Update()

alignStats(passedCounts)

#Write to file
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/8TeV/HT/filter_%s_%s/"%(str(cuts["genMET"]),str(cuts["genHT"])) + str(options.stopMasses) #web directory http://www.hephy.at/user/mzarucki/plots/filter/

if not os.path.exists(savedir):
   os.makedirs(savedir)

c1.SaveAs(savedir + "/redMassScanHT_%s_%s_"%(str(cuts['genMET']), str(cuts['genHT'])) + str(options.jobNumber) + ".root")
c1.SaveAs(savedir + "/redMassScanHT_%s_%s_"%(str(cuts['genMET']), str(cuts['genHT'])) + str(options.jobNumber) + ".png")
c1.SaveAs(savedir + "/redMassScanHT_%s_%s_"%(str(cuts['genMET']), str(cuts['genHT'])) + str(options.jobNumber) + ".pdf")
