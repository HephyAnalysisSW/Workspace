# LheFile

class LheFile:
    def __init__(self, fullName, name, stopMass, lspGeneratedMass, runNumber, lspMass, processPrefix, nrEvents):
        self.fullName = fullName
        self.name = name
        self.stopMass = stopMass
        self.lspGeneratedMass = lspGeneratedMass        
        self.runNumber = runNumber        
        self.lspMass = lspMass 
        self.processPrefix = processPrefix 
        self.nrEvents = nrEvents           
  
    def __repr__(self):
        return '\n' + self.fullName + \
               '\n' + self.name + \
               '\n' + str(self.stopMass) + \
               '\n' + str(self.lspGeneratedMass) + \
               '\n' + str(self.runNumber) + \
               '\n' + str(self.lspMass) + \
               '\n' + str(self.nrEvents)
  
    def __str__(self):
        if (self.nrEvents > 0):
            nrEventsString = str(self.nrEvents)
        else:
            nrEventsString = 'N/A'
        
        if (self.lspMass > 0):
            lspMassString = str(self.lspMass)
        else:
            lspMassString = 'N/A'

        return '\nFull name:          ' + self.fullName + \
               '\nName:               ' + self.name + \
               '\nStop mass:          ' + str(self.stopMass) + \
               '\nGenerated LSP mass: ' + str(self.lspGeneratedMass) + \
               '\nRun number:         ' + str(self.runNumber) + \
               '\nDecay LSP mass:     ' + lspMassString + \
               '\nNumber of events:   ' + nrEventsString + \
               '\n'
        
