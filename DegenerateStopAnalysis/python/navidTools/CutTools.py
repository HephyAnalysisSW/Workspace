


less = lambda var,val: "(%s < %s)"%(var,val)
more = lambda var,val: "(%s > %s)"%(var,val)
btw = lambda var,minVal,maxVal: "(%s > %s && %s < %s)"%(var, min(minVal,maxVal), var, max(minVal,maxVal))



def makeCutFlowList(cutList):
  cutFlowList=[]
  for cutName,cutString in cutList:
    cutFlowString = joinCutStrings( [cutList[i][1] for i in range(0, 1+cutList.index( [cutName,cutString]))] )
    cutFlowList.append( [cutName, cutFlowString ])
  return cutFlowList

def combineCutList(cutList):
  return joinCutStrings([x[1] for x in cutList if x[1]!="(1)"])

def joinCutStrings(cutStringList):
  return "(" + " && ".join([ "("+c +")" for c in cutStringList])    +")"





class CutClass():
  def __init__(self,name,cutList,baseCut=None):
    self.name         = name
    self.inclList     = cutList
    #self.inclDict     = self._makeDict(self.inclList)
    self.inclFlow     = self._makeFlow(self.inclList)
    self.inclCombined = self._combine(self.inclList) 
    self.inclCombinedList  = (self.name ,self._combine(self.inclList) )
    self.baseCut = baseCut

    if baseCut:
      if isinstance(baseCut,CutClass):
        self.baseCutString      = baseCut.combined
        self.baseCutName        = baseCut.name
      else:
        self.baseCutName, self.baseCutString = baseCut
    else: 
      self.baseCutName, self.baseCutString = (None,None)



    if not self.baseCutString or self.baseCutString == "(1)":
      self.list         = cutList
    else:
      self.list         =[[self.baseCutName, self.baseCutString]]+  [ [cutName,"(%s)"%"&&".join([self.baseCutString,cut])  ] for cutName,cut in self.inclList ]


    #self.list         = [ [name,"(%s)"%"&&".join([baseCutString,cut])  ] for name,cut in self.inclList ]
    #self.dict         = self._makeDict(self.list)
    self.flow         = self._makeFlow(self.list)
    self.combined     = self._combine(self.inclList,self.baseCutString)
    self.combinedList = (self.name, self.combined)
   # if baseCut and baseCut != "(1)":
   #   self.baseCut = baseCut
   #   self.list = [ [name,baseCut+"&&"+cut] for name,cut in cutList ] 
   #   self.flow = self._makeFlow(self.list)
   #   self.incl_list = cutList
   #   self.incl_flow = self._makeFlow(cutList)
   # else:
   #   self.list = cutList
   # self.keys = [x[0] for x in self.list]
   # self.dict= self._makeDict(self.InclusiveCutList)
   # self._combine(cutList)
  def _makeDict(self,cutList):
    Dict={}
    for cutName, cutString in cutList:
      Dict[cutName]=cutString
    return Dict
  def _makeFlow(self,cutList):
    flow=makeCutFlowList(cutList)
    flowDict= self._makeDict(flow)
    return flow
  def _combine(self,cutList,baseCutString=None) :
    if not baseCutString or baseCutString == "(1)":
      return combineCutList(cutList)
    else:
      return "(%s &&"%baseCutString+ combineCutList(cutList)+ ")"
    #if baseCut:
    #  self.combined=combineCutList(self.inclusiveCutList)
    #else: 
    #  self.combined=combineCutList(cutList)
    #if self.name:
    #  self.combinedList=[self.name,self.combined]


if __name__=='__main__':
  test = CutClass ("test", [
                              {"cutName":"MET200"       ,"cutString":"met>200"             ,"LaTex":"" },
                              {"cutName":"ISR110"       ,"cutString":"nJet110>=1"          ,"LaTex":"" },
                              {"cutName":"HT300"        ,"cutString":"htJet30j>300"        ,"LaTex":"" },
                              {"cutName":"2ndJetPt60"   ,"cutString":"nJet60<=2 "          ,"LaTex":"" },
                              {"cutName":"AntiQCD"      ,"cutString":"deltaPhi_j12 < 2.5"  ,"LaTex":"" },
                              {"cutName":"singleLep"    ,"cutString":"nlep==1"             ,"LaTex":"" },
                           ] , 
                baseCut="(1)",
                ) 




