import sys
import ROOT as rt

class inputFile():

    def __init__(self, fileName):
        self.HISTOGRAM = self.findHISTOGRAM(fileName)
        print self.HISTOGRAM
        self.EXPECTED = self.findEXPECTED(fileName)
        self.OBSERVED = self.findOBSERVED(fileName)
        self.LUMI = self.findATTRIBUTE(fileName, "LUMI")
        self.ENERGY = self.findATTRIBUTE(fileName, "ENERGY")
        print self.ENERGY
        self.PRELIMINARY = self.findATTRIBUTE(fileName, "PRELIMINARY")
        print self.PRELIMINARY
        self.ANALYSIS = self.findATTRIBUTE(fileName, "ANALYSIS")

    def findATTRIBUTE(self, fileName, attribute):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE = line[:-1]
            ind = tmpLINE.find("#")
            if ind==0: continue
            if ind>0:
                tmpLINE = tmpLINE[:ind-1]
            tmpLINE =  tmpLINE.split(" ")
            if tmpLINE[0] != attribute: continue
            fileIN.close()
            return " ".join(tmpLINE[1:])

    def findHISTOGRAM(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "HISTOGRAM": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            rt.gROOT.cd()
            return {'histogram': rootFileIn.Get(tmpLINE[2]).Clone()}
            
    def findEXPECTED(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "EXPECTED": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            rt.gROOT.cd()
            return {'nominal': rootFileIn.Get(tmpLINE[2]).Clone(),
                    'plus': rootFileIn.Get(tmpLINE[3]).Clone(),
                    'minus': rootFileIn.Get(tmpLINE[4]).Clone(),
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}

    def findOBSERVED(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "OBSERVED": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            rt.gROOT.cd()
            return {'nominal': rootFileIn.Get(tmpLINE[2]).Clone(),
                    'plus': rootFileIn.Get(tmpLINE[3]).Clone(),
                    'minus': rootFileIn.Get(tmpLINE[4]).Clone(),
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}

