#! /usr/bin/env python

#import ROOT
#import sys
#from DataFormats.FWLite import Events, Handle
#import subprocess
#import cPickle
#import gzip

def isGluino (pdgId):
    if pdgId == 1000021:  return True
    return False

def isNeutralino (pdgId):
    if pdgId == 1000022 or pdgId == 1000023 or pdgId == 1000025 or pdgId == 1000035:  return True
    return False

def isChargino (pdgId):
    absPdgId = abs(pdgId)
    if absPdgId == 1000024 or absPdgId == 1000037:  return True
    return False

def isCharginoOrNeutralino (pdgId):
    return isChargino(pdgId) or isNeutralino(pdgId)

def isStop (pdgId):
    absPdgId = abs(pdgId)
    if absPdgId == 1000006 or absPdgId == 2000006:  return True
    return False
    
def isSbottom (pdgId):
    absPdgId = abs(pdgId)
    if absPdgId == 1000005 or absPdgId == 2000005:  return True
    return False

def isSquark (pdgId):
    absPdgId = abs(pdgId)
    redPdgId = absPdgId % 1000000
    if (absPdgId-redPdgId) != 1000000 and (absPdgId-redPdgId) != 2000000: return False
    if redPdgId == 0 or redPdgId > 6:  return False
    return True

def isSlepton (pdgId):
    absPdgId = abs(pdgId)
    redPdgId = absPdgId % 1000000
    if (absPdgId-redPdgId) != 1000000 and (absPdgId-redPdgId) != 2000000: return False
    if redPdgId < 11 or redPdgId > 16:  return False
    return True

    
def productionCode (pdgIds):
    if len(pdgIds) == 2:
        if ( isCharginoOrNeutralino(pdgIds[0]) and isGluino(pdgIds[1]) ) or \
           ( isCharginoOrNeutralino(pdgIds[1]) and isGluino(pdgIds[0]) ): return "ng"
        if ( isCharginoOrNeutralino(pdgIds[0]) and isSquark(pdgIds[1]) ) or \
           ( isCharginoOrNeutralino(pdgIds[1]) and isSquark(pdgIds[0]) ): return "ns"
        if isCharginoOrNeutralino(pdgIds[0]) and isCharginoOrNeutralino(pdgIds[1]):  return "nn"
        if isSlepton(pdgIds[0]) and isSlepton(pdgIds[1]):  return "ll"
        if isStop(pdgIds[0]) and isStop(pdgIds[1]) and pdgIds[0]*pdgIds[1] < 0:  return "tb"
        if isSbottom(pdgIds[0]) and isSbottom(pdgIds[1]) and pdgIds[0]*pdgIds[1] < 0:  return "bb"
        if isSquark(pdgIds[0]) and isSquark(pdgIds[1]):
            if pdgIds[0]*pdgIds[1] < 0:  return "sb"
            else: return "ss"
        if isGluino(pdgIds[0]) and isGluino(pdgIds[1]):  return "gg"
        if ( isSquark(pdgIds[0]) and isGluino(pdgIds[1]) ) or \
           ( isSquark(pdgIds[1]) and isGluino(pdgIds[0]) ): return "sg"
    return "--"

## Make VarParsing object
## https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example
#from FWCore.ParameterSet.VarParsing import VarParsing
#options = VarParsing ('python')
#options.parseArguments()

# Events takes either
# - single file name
# - list of file names
# - VarParsing options

#print sys.argv
#castor_dir = "/castor/cern.ch/user/a/adamwo/CrabOutput/SusyProc"
#if len(sys.argv)>1:  castor_dir = sys.argv[1]
#
#p1 = subprocess.Popen(["nsls",castor_dir],stdout=subprocess.PIPE)
#lines = p1.communicate()[0].splitlines()
#files = []
#for line in lines:
#    files.append('rfio:'+castor_dir+'/'+line)
#print "#files = ",len(files)
##exit
#
## use Varparsing object
##files = [
##    'rfio:/castor/cern.ch/user/a/adamwo/CrabOutput/SusyProc/mSUGRA_tanb-10andA0-0_Summer11_10_0_xPw.root',
##'rfio:/castor/cern.ch/user/a/adamwo/CrabOutput/SusyProc/mSUGRA_tanb-10andA0-0_Summer11_14_0_Mea.root',
##'rfio:/castor/cern.ch/user/a/adamwo/CrabOutput/SusyProc/mSUGRA_tanb-10andA0-0_Summer11_18_0_RYE.root',
##'rfio:/castor/cern.ch/user/a/adamwo/CrabOutput/SusyProc/mSUGRA_tanb-10andA0-0_Summer11_19_0_rNu.root',
##'rfio:/castor/cern.ch/user/a/adamwo/CrabOutput/SusyProc/mSUGRA_tanb-10andA0-0_Summer11_1_1_xqq.root',
##'rfio:/castor/cern.ch/user/a/adamwo/CrabOutput/SusyProc/mSUGRA_tanb-10andA0-0_Summer11_28_0_PoH.root',
##'rfio:/castor/cern.ch/user/a/adamwo/CrabOutput/SusyProc/mSUGRA_tanb-10andA0-0_Summer11_2_1_zgX.root',
##'rfio:/castor/cern.ch/user/a/adamwo/CrabOutput/SusyProc/mSUGRA_tanb-10andA0-0_Summer11_32_0_6CC.root',
##'rfio:/castor/cern.ch/user/a/adamwo/CrabOutput/SusyProc/mSUGRA_tanb-10andA0-0_Summer11_3_1_x2V.root',
##'rfio:/castor/cern.ch/user/a/adamwo/CrabOutput/SusyProc/mSUGRA_tanb-10andA0-0_Summer11_7_1_Cby.root'
##]
##events = Events (files)
##events = Events (files[0])
#events = Events ("/tmp/adamwo/mSUGRA_tanb-10andA0-0_Summer11.root")
#
## create handle outside of loop
#handleIds  = Handle("std::vector<int>")
#labelIds = ("susyProc","sparticles")
#
#handleM0 = Handle("float")
#labelM0 = ("susyProc","msugraM0")
#
#handleM12 = Handle("float")
#labelM12 = ("susyProc","msugraM12")
#
## Create histograms, etc.
#ROOT.gROOT.SetBatch()        # don't pop up canvases
#ROOT.gROOT.SetStyle('Plain') # white background
##zmassHist = ROOT.TH1F ("zmass", "Z Candidate Mass", 50, 20, 220)
#
#processCounts = {}
#msugra = ()
## loop over events
#nev = 0
#nunknown = 0
#ndup = 0
#
#for event in events:
#    nev = nev + 1
#    if ( nev % 100000 ) == 0:  print "nev = ",nev
#    if ( nev % 100000 ) == 0:  break
#
#    event.getByLabel (labelIds, handleIds)
#    pdgIds = handleIds.product()
#    prodCode = productionCode(pdgIds)
#    if prodCode == "--":
#        nunknown = nunknown + 1
# #       out = "Unknown production process:"
# #       for pdgId in pdgIds:
# #           out = out + " "
# #           out = out + str(pdgId)
# #       print out
#
##    numPdgIds = len (pdgIds)
##    print "Number of sparticles = ",numPdgIds
##    for pdgId in pdgIds:
##        print "  ",pdgId
#
#    event.getByLabel (labelM0,handleM0)
#    m0 = handleM0.product()
#    event.getByLabel (labelM12,handleM12)
#    m12 = handleM12.product()
#    msugra = ( m0[0], m12[0], 10, 0, 1 )
#    if not msugra in processCounts:  processCounts[msugra] = {}
#    if not prodCode in processCounts[msugra]: processCounts[msugra][prodCode] = 0
#    processCounts[msugra][prodCode] = processCounts[msugra][prodCode] + 1
##    print "m0, m12 = ",m0[0]," ",m12[0]
#
##    run = event.eventAuxiliary().run()
##    evt = event.eventAuxiliary().event()
##    eventId = ( run, evt )
##    if eventId in eventIds:
##        print "*** Duplicate event id ",eventId
##        ndup = ndup + 1
##    else:
##        eventIds[eventId] = prodCode
#
#
#print "Total number of events = ",nev
#print "Fraction of unknown events = ",nunknown/float(nev)
#print "Fraction of duplicate events = ",ndup/float(nev)
#
#print " "
#for msugra in processCounts:
#    l = str(msugra)+" - :"
#    for prodCode in processCounts[musgra]:
#        l = l+" "+prodCode+":"+str(processCounts[msugra][prodCode])
#    print l

## make a canvas, draw, and save it
#c1 = ROOT.TCanvas()
#zmassHist.Draw()
#c1.Print ("zmass_py.png")

#if len(sys.argv)>2:
#    fname = str(sys.argv[2]) + ".pkl" + ".gz"
#    fout = open(fname,'wb')
##    fout = gzip.open(fname,'wb')
#    cPickle.dump(eventIds,fout,2)
#    fout.close()
