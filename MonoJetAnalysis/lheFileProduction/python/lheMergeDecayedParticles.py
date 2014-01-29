import sys, os, copy
import math, re, array, gzip
from xml.dom import minidom
import string

#tolerance for energy momentum conservation
toler = 1e-4

#useful class to describe 4 momentum
class Momentum:
    def __init__(self,px,py,pz,E,m):
        self.px=px
        self.py=py
        self.pz=pz
        self.E=E
        self.m=m
    def __add__(self,other):
        t=Momentum(self.px+other.px,self.py+other.py,self.pz+other.pz,self.E+other.E,0)
        t.m=t.calcMass()
        return t
    def __sub__(self,other):
        t=Momentum(self.px-other.px,self.py-other.py,self.pz-other.pz,self.E-other.E,0)
        t.m=t.calcMass()
        return t
    def calcMass(self):
        tempMass2=self.E**2-self.px**2-self.py**2-self.pz**2
        if tempMass2 > 0:
            t=math.sqrt(tempMass2)
            if t>toler:
                return t
            else:
                return 0
        else:
            return 0
    def boost(self,ref,rdir):
        pmag=ref.E
        DBX=ref.px*rdir/pmag
        DBY=ref.py*rdir/pmag
        DBZ=ref.pz*rdir/pmag
        DB=math.sqrt(DBX**2+DBY**2+DBZ**2)
        DGA=1.0/math.sqrt(1.0-DB**2)        
        DBP=DBX*self.px+DBY*self.py+DBZ*self.pz
        DGABP=DGA*(DGA*DBP/(1.0+DGA)+self.E)
        self.px = self.px+DGABP*DBX
        self.py = self.py+DGABP*DBY
        self.pz = self.pz+DGABP*DBZ
        self.E  = DGA*(self.E+DBP)
    def reScale(self,pi,po):
        self.px = self.px/pi*po
        self.py = self.py/pi*po
        self.pz = self.pz/pi*po
    def printMe(self):
        li = [self.px,self.py, self.pz, self.E, self.m]
        print "| %18.10E %18.10E %18.10E %18.10E %18.10E |" % tuple(li)    

#useful class to describe a particle
class Particle:
    def __init__(self,i,l):
        self.no = i
        self.id = l[0]
        self.status = l[1]
        self.mo1 = l[2]
        self.mo2 = l[3]
        self.co1 = l[4]
        self.co2 = l[5]
        self.mom = Momentum(l[6],l[7],l[8],l[9],l[10])
        self.life = l[11]
        self.polar = l[12]
    def printMe(self):
        li = [self.no, self.id, self.status,self.mo1, self.mo2, self.co1, self.co2, self.mom.px,self.mom.py, self.mom.pz, self.mom.E, self.mom.m, self.life, self.polar]
        print "%2i | %9i | %4i | %4i %4i | %4i %4i | %18.10E %18.10E %18.10E %18.10E %18.10E | %1.0f. %2.0f" % tuple(li)
    def writeMe(self):
        li = [self.id, self.status,self.mo1, self.mo2, self.co1, self.co2, self.mom.px,self.mom.py, self.mom.pz, self.mom.E, self.mom.m, self.life, self.polar]
        return "%9i %4i %4i %4i %4i %4i %18.10E %18.10E %18.10E %18.10E %18.10E  %1.0f. %2.0f\n" % tuple(li)        

#useful function for converting a string to variables
def parseStringToVars(input):
    if input.find(".")>-1 :
        return float(input)
    else:
        return int(input)

def extractBlock(lheFile, blockName):
    
    # extract a block blockName from the header of lheFile
    print '\nExtract block ' + blockName + ' from file ' + lheFile
    
    debug = False   
    blockStatus = False
    
    lheFileObj = gzip.open(lheFile)
    block = []
    
    for line in lheFileObj:
        
        if blockName in line:
            blockStatus = True
            block.append(line)
            continue
         
        if (blockStatus == True):
            block.append(line) 
            if ('#' in line) and (len(line) == 2):
                blockStatus = False
                break

        # additional end of header check                 
        if (line.find("<init>")!= -1):
            break
    
    lheFileObj.close()
    blockStr = ''.join(block)
    
    if debug:
        print '\nBlock ' + blockName + '\n'
        print blockStr
           
    return blockStr

    
def writeHead(decname, inname, outname, lspGenMassValue, lspMassValue):
    f = gzip.open(inname)
    g = open(outname,'w')
    
    lspID = '1000022'
    lspName = '~chi_10'
    lspGenMassString = ' ' + str(lspGenMassValue) + ' '
    lspMassString =  ' ' + str(lspMassValue) + '. '

    blockNmix = 'BLOCK NMIX'
    blockStopmix = 'BLOCK STOPMIX'
    blockMass = 'BLOCK MASS'
    
    blockMassStatus = False
    blockNmixStatus = False
    blockStopmixStatus = False
 
    # extract the NMIX and STOPMIX blocks from the decayed files
    blockNmixObj = extractBlock(decname, blockNmix)
    blockStopmixObj = extractBlock(decname, blockStopmix)
   
    while 1:
        try:
            line=f.readline()
        except IOError:
            print "Problem reading from file ",f.name
            sys.exit(0)
        
        # change the mass of LSP to the value used in the decay files    
        if line.find(blockMass):
            blockMassStatus = True
        if (blockMassStatus == True):
            if ((line.find(lspID) > 0) and (line.find(lspGenMassString) > 0) and (line.find(lspName) > 0)):
                lspMassLine = string.replace(line, lspGenMassString, lspMassString)
                blockMassStatus = False
                g.write(lspMassLine)
                continue
        
        # replace BLOCK NMIX and BLOCK STOPMIX with the corresponding block from
        # the decayed sample      
        if blockNmix in line:
            blockNmixStatus = True
            # write new block
            g.write(blockNmixObj)
            
        if (blockNmixStatus == True):   
            # skip the rest of the block lines
            if ('#' in line) and (len(line) == 2):
                blockNmixStatus = False
                continue
            else:
                continue

        if blockStopmix in line:
            blockStopmixStatus = True
            # write new block
            g.write(blockStopmixObj)
            
        if (blockStopmixStatus == True):   
            # skip the rest of the block lines
            if ('#' in line) and (len(line) == 2):
                blockStopmixStatus = False
                continue
            else:
                continue
        
        # otherwise copy the line from the input file header                 
        if line.find("<init>")==-1:
            g.write(line)
        else:
            break
        
    f.close()
    g.close()
    
def writeTrail(outname):
    g = open(outname,'a')
    g.write("</LesHouchesEvents>\n")
    g.close()

def writeInit(inname,outname):
    f = gzip.open(inname)
    g = open(outname,'a')
    try:
        xmldoc = minidom.parse(f)
    except IOError:
        print " could not open file for xml parsing ",f.name
        sys.exit(0)
    f.close()
    xxx = xmldoc.getElementsByTagName('init')
    g.write(xxx[0].toxml()+"\n")
    f.close()
    g.close()

def getEventList(inname):
    f = gzip.open(inname)
    try:
        xmldoc = minidom.parse(f)
    except IOError:
        print " could not open file for xml parsing ",f.name
        sys.exit(0)
    f.close()
    return xmldoc.getElementsByTagName('event')
    
def getEvent(lines):
    slines = lines.split("\n")
    next = 0
    nup = 0
    nlines = len(slines)
    counter = 0
    event = []
    event_description=""
    event_poundSign=""

    while counter<nlines:
        s=slines[counter]
        if s.find("<event>")>-1:
            next=1
        elif s.find("</event>")>-1:
            pass
        elif s.find("#")>-1:
            event_poundSign=s
        elif next==1:
            event_description=s
            next=0
        else:
            t=[]
            for l in s.split(): t.append(parseStringToVars(l))
            nup = nup+1
            event.append(Particle(nup,t))
#            event[nup-1].printMe()
        counter=counter+1
    return [event, event_description, event_poundSign]
    
def getIndex(ev, pid):
    for ip, p in enumerate(ev):
        if(p.id == pid):
            return ip
#    print "did not find", pid, "in event"
    return -1
    
###
def lheMergeDecayedParticles(filenameD1, filenameD2, filenameP, filenameO, lspGenMass, lspMass, modelComment):
        
    writeHead(filenameD1, filenameP, filenameO, lspGenMass, lspMass)
    writeInit(filenameP,filenameO)
    
    reflistP = getEventList(filenameP)
    reflistD1 = getEventList(filenameD1)
    reflistD2 = getEventList(filenameD2)
        
    n = min(len(reflistP), len(reflistD1), len(reflistD2))
    
    g = open(filenameO,'a')
    for i in range(0,n):
    
        if(i>0 and (i%10000)==0): print i
        
        [eventP, eventDS, eventPS] = getEvent(reflistP[i].toxml())
        [eventD1, dummy, dummy] = getEvent(reflistD1[i].toxml())
        [eventD2, dummy, dummy] = getEvent(reflistD2[i].toxml())
        
        ist = getIndex(eventP, 1000006)
        ias = getIndex(eventP, -1000006)
        imaxco = 0
        for parton in eventP:
            imaxco = max(imaxco, parton.co1, parton.co2)
        iaddco = 0
        if(ist == -1 or ias == -1):
            print "did not find stops in production event no", i
            print "skipping"
            continue
        eventP[ist].status = 2
        eventP[ias].status = 2
        ientry = max(ist,ias) + 1
        for parton in eventD1:
            if(parton.id != 1000006):
    #            pold = parton.mom
                parton.mom.boost(eventP[ist].mom,1)
    #            pnew = parton.mom
    #            print "dot product",(pold.px*pnew.px+pold.py*pnew.py+pold.pz*pnew.pz)
                if(parton.mo1==1):
                    parton.mo1 = eventP[ist].no
                    parton.mo2 = eventP[ist].no
                else:
                    parton.mo1 += ientry + 1 - parton.no
                    parton.mo2 = parton.mo1
                if(abs(parton.id) == 5):
                    parton.co1 = eventP[ist].co1
                    parton.co2 = eventP[ist].co2
                if(abs(parton.id) < 5):
                    if(parton.co1>0): 
                        parton.co1 = imaxco+1
                        iaddco = 1
                    if(parton.co2>0): 
                        parton.co2 = imaxco+1
                        iaddco = 1
                eventP.insert(ientry, parton)
                ientry += 1
        for parton in eventD2:
            if(parton.id != -1000006):
    #            pold = parton.mom
                parton.mom.boost(eventP[ias].mom,1)
    #            pnew = parton.mom
    #            print "dot product",(pold.px*pnew.px+pold.py*pnew.py+pold.pz*pnew.pz)
                if(parton.mo1==1):
                    parton.mo1 = eventP[ias].no
                    parton.mo2 = eventP[ias].no
                else:
                    parton.mo1 += ientry + 1 - parton.no
                    parton.mo2 = parton.mo1
                if(abs(parton.id) == 5):
                    parton.co1 = eventP[ias].co1
                    parton.co2 = eventP[ias].co2
                if(abs(parton.id) < 5):
                    if(parton.co1>0): parton.co1 = imaxco+1+iaddco
                    if(parton.co2>0): parton.co2 = imaxco+1+iaddco
                eventP.insert(ientry, parton)
                ientry += 1
        
        eventDS = str(int(eventDS[0:2])+8) + eventDS[2:]
        
        pSum = Momentum(0,0,0,0,0)
        for p in eventP:
            if p.status== 2 :
                pass
            elif p.status==-1:
                pSum = pSum - p.mom
            elif p.status==1:
                pSum = pSum + p.mom
    
        if abs(pSum.px)>toler or abs(pSum.py)>toler or abs(pSum.pz)>toler or abs(pSum.E)>toler:
            print "Event does not pass tolerance ",toler
            pSum.printMe()
        else:
            g.write("<event>\n")
            
            nrParticles = len(eventP)
            firstSpacePos = eventDS.find(' ')
            if firstSpacePos > 0:
                g.write(str(nrParticles) + eventDS[firstSpacePos:] + "\n")
            else: 
                print "\nNo space found in event description line - write unmodified event description"
                g.write(eventDS + "\n")
                
            for p in eventP:
                g.write(p.writeMe())
                
            g.write(eventPS+"\n")
            g.write('# model ' + modelComment + '\n')
            g.write("</event>\n")
    
    g.close()
    writeTrail(filenameO)
    
