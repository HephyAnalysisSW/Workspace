#redMassScanDPM.py for 8TeV
#Use: 'python 2DredMassScanDPM.py --first=## -b //dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_240614/T2DegenerateStop_2J_mStop-100to150-4/'

import ROOT
import os, sys
import math
import copy
import subprocess
import pickle

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

#def makeDoubleLine():
#   line = "\n**********************************************************************************************************************************\n\
#**********************************************************************************************************************************\n"
#   return line
#
#def newLine():
#   print ""
#   return 
#

##Selection function
#def select(varname, cut, option): #option = {>, =, <}
#   sel = "abs(" + varname + option + str(cut) + ")"
#   return sel

##Creates Legend
#def makeLegend():
#   leg = ROOT.TLegend(0.60,0.70,0.75,0.85)
#   leg.SetHeader("#bf{Legend}")
#   header = leg.GetListOfPrimitives().First()
#   header.SetTextAlign(22)
#   return leg 

##Creates Box 
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

#def getJetPt(jets) #getJets(), #getLeadingJetPt() == Jet_pt[0]
#   for jet in jets:
#         return jet.pt()
#   return 0
 
#
# small class holding MET pt and phi
#

#class MyMET:
#  def __init__(self,metx,mety):
#    self.met_ = math.sqrt(metx**2+mety**2)
#    self.phi_ = math.atan2(mety,metx)
# 
#  def pt(self):
#    return self.met_
# 
#  def phi(self):
#    return self.phi_

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
dir = "//dpm/oeaw.ac.at/home/cms/store/user/schoef/pat_240614/T2DegenerateStop_2J_mStop-100to150-4/" #"/afs/hephy.at/work/w/wadam/CMSSW_5_3_20/src/T2DegenerateStop_2J_mStop-100to150-4/"

parser = OptionParser()
parser.add_option("--first", dest="first",  help="index of first file", type="int", default=1)
parser.add_option("--maxFiles", dest="number",  help="number of files", type="int", default=None)
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
   exit()

files = []
p = subprocess.Popen(["dpns-ls",dpmDir], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
  fn = line[:-1]
  if fn.endswith(".root"):
    files.append("root://hephyse.oeaw.ac.at"+dpmDir+fn)
files.sort()
if options.first < 1:
   print "Choose file index starting from 1."
   exit()

files = files[(options.first-1):]
if options.number != None:
  files = files[:options.number]

print makeLine()
print "Starting with file:", files[0], "corresponding to file index ", options.first
if options.number != None:
   print "Ending with file:", files[options.number-1], "corresponding to file index ", options.first + options.number - 1
print makeLine()

#wrapper for events and product definitions
myEvent = MyEvent()
myEvent.defineProduct("genParticles","std::vector<reco::GenParticle>")
myEvent.defineProduct(("SUSYTupelizer","met"), "float")
#myEvent.defineProduct(("SUSYTupelizer","metphi"), "float")
myEvent.defineProduct(("SUSYTupelizer","osetMC"), "float") #LSP mass
myEvent.defineProduct(("SUSYTupelizer","osetMsq"), "float") #stop mass
#myEvent.defineProduct(("SUSYTupelizer","njets"), "int")
myEvent.defineProduct(("SUSYTupelizer","jetsPt"), "vector<float>")
myEvent.defineProduct(("SUSYTupelizer","jetsEta"), "vector<float>")
#myEvent.defineProduct(("SUSYTupelizer","jetsPhi"), "vector<float>")
myEvent.defineProduct(("SUSYTupelizer","genmet"), "float")

#gMETcut = input("Enter Generated MET cut value: ")
#gISRcut = input("Enter Generated ISR Jet pT cut value: ")

cuts=({\
'MET' : 200, #MET cut (fixed)
'ISR' : 110, #ISR/Leading Jet cut (fixed)
'Eta' : 2.4, #eta cut (fixed)

'gMET' : 135, #generated quantity cuts
'gISR' : 80,
'gEta' : 2.5
})

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
print makeLine()
 
#Preselection and Generated Particles Filter Selection

#Variables: met_pt, met_genPt, Jet_pt, GenJet_pt, Jet_eta, GenJet_eta

#MET Selection
nbins = 100
min = 0 #GeV
max = 1000 #GeV

stopMs = range(100,401,25)
deltaMs = range(10,81,10)
LSPMs = [stop-deltaM for stop in stopMs for deltaM in deltaMs]

massPoints = [str(stop) + "_"+ str(stop-deltaM) for stop in stopMs for deltaM in deltaMs]

hists = {}
for massPoint in massPoints:
   hists[massPoint]={}
   #for iHist in range(4):
   hists[massPoint][0] = ROOT.TH1F("MET_" + massPoint, "MET_" + massPoint , nbins, min, max)
   hists[massPoint][1] = ROOT.TH1F("MET1_" + massPoint, "MET1_" + massPoint , nbins, min, max) #+1 gCut
   hists[massPoint][2] = ROOT.TH1F("MET2_" + massPoint, "MET2_" + massPoint , nbins, min, max) #+2 gCuts
   hists[massPoint][3] = ROOT.TH1F("gMET_" + massPoint, "gMET_" + massPoint , nbins, min, max) #genMET
   hists[massPoint][4] = ROOT.TH1F("gMET2_" + massPoint, "gMET2_" + massPoint , nbins, min, max) #genMET + gCuts
   hists[massPoint][5] = ROOT.TH1F("ISR_" + massPoint, "ISR_" + massPoint ,nbins, min, max)
   hists[massPoint][6] = ROOT.TH1F("ISR1_" + massPoint, "ISR1_" + massPoint , nbins, min, max) #+1 gCut
   hists[massPoint][7] = ROOT.TH1F("ISR2_" + massPoint, "ISR2_" + massPoint , nbins, min, max) #+2 gCuts
   hists[massPoint][8] = ROOT.TH1F("gISR_" + massPoint, "gISR_" + massPoint , nbins, min, max) #genISRpt
   hists[massPoint][9] = ROOT.TH1F("gISR2_" + massPoint, "gISR2_" + massPoint , nbins, min, max) #genISRpt + gCuts

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
   #if iev == 100: break
   if iev%10000==0:
      print "At event",iev,"the file index is", options.first + event.fileIndex()
   myEvent.load(event)
   
   #Masses
   stopMass = myEvent.getProduct(("SUSYTupelizer","osetMsq"))[0]
   LSPMass = myEvent.getProduct(("SUSYTupelizer", "osetMC"))[0]
   
   massPoint = str(int(stopMass)) + "_" + str(int(LSPMass))  
   
   #Generated Particles
   genParts = myEvent.getProduct("genParticles")#[0:30]
   myGenParts = MyGenParticles(genParts)#[0:30]
  
   #MET
   MET = myEvent.getProduct(("SUSYTupelizer","met"))[0]
   
   #genMETpt
   genMET = myEvent.getProduct(("SUSYTupelizer", "genmet"))[0]
  
   #if genMET < cuts['gMET']:
   #   continue #skips iteration, as both cuts need to be applied
   
   #ISR   
   ISRpt = 0.0
   
   if myEvent.getProduct(("SUSYTupelizer","jetsPt")).empty() != True:
      leadJetPt = myEvent.getProduct(("SUSYTupelizer","jetsPt"))[0] #first = jet with highest pt = leading jet
   else: leadJetPt = 0.0

   if myEvent.getProduct(("SUSYTupelizer","jetsEta")).empty() != True:
      leadJetEta = myEvent.getProduct(("SUSYTupelizer","jetsEta"))[0] #first = jet with highest pt = leading jet
   else: leadJetEta = 0.0
   
   if abs(leadJetEta) < 2.4:
      ISRpt = leadJetPt
    
   #genISRpt 
   
   #get indices of stops (should be 6 and 7)
   istops = myGenParts.indicesByPdgId(1000006) #indices = 6,7
   #if len(istops)!=2: print myGenParts
   assert len(istops)==2
   assert istops==[6,7]
   # get index of first stop daughter
   isdmin = None
   for istop in istops:
     stopds = myGenParts[istop].daughterIndices()
     if isdmin==None or isdmin>stopds[0]:
        isdmin = stopds[0]
   # range of particles (additional radiation) between stops and stop daughters
   #print "range of particles between stops and stop daughters",range(8,isdmin)
   
   maxPt = 0.0 #None 
   for myGenPart in myGenParts:
      if myGenPart.index > 7 and myGenPart.index < isdmin: #ISR
         if abs(myGenPart.particle.eta()) < 2.5: #eta cut
            #print myGenPart
            if myGenPart.particle.pt() > maxPt:
               maxPt = myGenPart.particle.pt()
               #genISR = myGenPart
   
   genISRpt = maxPt
   
   #print "Event: ", iev, ", ISR pt: ", ISRpt
   #print "genISR pt: ", genISRpt
            
   #genISRpt = genISR.particle.pt()
   #genISReta = genISR.particle.eta()
   
   #Histogram filling

   #MET
   hists[massPoint][0].Fill(MET) #no preselection 
   
   #if ISRpt > cuts['ISR']: #presel ISR cut 
   #   hists[massPoint][0].Fill(MET)
   if genMET > cuts['gMET']: # +genMET cut
      hists[massPoint][1].Fill(MET)
      if genISRpt > cuts['gISR']: # + genISRpt cut
         hists[massPoint][2].Fill(MET)
 
   hists[massPoint][3].Fill(genMET) #no cuts
   
   if genMET > cuts['gMET'] and genISRpt > cuts['gISR']: #both gCuts
      hists[massPoint][4].Fill(genMET)

   #ISR
   hists[massPoint][5].Fill(ISRpt) #no preselection
   #if MET > cuts['MET']: #presel MET cut
   #   hists[massPoint][5].Fill(ISRpt)
   if genISRpt > cuts['gISR']: # +genISRpt cut
      hists[massPoint][6].Fill(ISRpt)
      if genMET > cuts['gMET']: # +genMET cut
         hists[massPoint][7].Fill(ISRpt)
 
   hists[massPoint][8].Fill(genISRpt) #no cuts
   
   if genISRpt > cuts['gISR'] and genMET > cuts['gMET']:  #both gCuts
      hists[massPoint][9].Fill(genISRpt)

#Write to file
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/filter/8TeV/filter_%s_%s/"%(str(cuts["gMET"]),str(cuts["gISR"])) + str(options.stopMasses) + "/genCutsOnly/hists_%s_%s/"%(str(cuts["gMET"]),str(cuts["gISR"])) #web directory http://www.hephy.at/user/mzarucki/plots/filter/

if not os.path.exists(savedir):
   os.makedirs(savedir)

#outfile = open(savedir + "redFactorScan_%s_%s.txt"%(str(cuts["gMET"]),str(cuts["gISR"])), "w")
#outfile.write(\
#"genMET Cut: " + str(cuts["gMET"]) +  "   " + "genISRpt Cut: " + str(cuts["gISR"]) + "\n\n" + \
#"Mass point" + "   " + "Reduction factor" + "\n"
#)
#
#for massPoint in massPoints:
#   
#   #Efficiency and Reduction Factor Calculation 
#   redFactor = hists[massPoint][3].GetEntries()/hists[massPoint][4].GetEntries() # = 1/eff
#   #redFactor2 = hists[massPoint][8].GetEntries()/hists[massPoint][9].GetEntries() # should be same
#   
#   outfile.write(\
#   " (" + massPoint + ")" + "        " + str(redFactor) + "\n" \
#   )
#outfile.close()

pickle.dump(hists, file(savedir + "hists_%s_%s_"%(str(cuts["gMET"]),str(cuts["gISR"])) + str(options.jobNumber) + ".pkl", "w"))#_%s_%s_pkl"%(str(cuts["gMET"]),str(cuts["gISR"]))), "w")
