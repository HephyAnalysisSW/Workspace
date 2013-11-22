import array, types

#set Sumw2
allVars=[]
for stack in allStacks:
  for var in stack:
    if allVars.count(var)==0:
      allVars.append(var)
    if var.style=="e":
      var.data_histo.Sumw2()

#default is log
for var in allVars:
  var.logy=True
#search files
for sample in allSamples:
  sample["filenames"]={}
  for bin in sample["bins"]:
    if type(sample["dirname"])==type([]):
      dirnames = sample["dirname"]
    else:
      dirnames = [sample["dirname"]]
    for dirname in dirnames:
      subdirname = dirname+"/"+bin+"/"
      if sample["bins"]==[""]:
        subdirname = sample["dirname"]+"/"
      if not sample["filenames"].has_key(bin):
        sample["filenames"][bin]=[]
      if small:
        filelist=os.listdir(subdirname)
        counter = 1   #Joining n files
        for thisfile in filelist:
          if os.path.isfile(subdirname+thisfile) and thisfile[-5:]==".root" and thisfile.count("histo")==1: 
            sample["filenames"][bin].append(subdirname+thisfile)
            if counter==0:
              break
            counter=counter-1
      else:
        sample["filenames"][bin] .append(subdirname+"/h*.root")
peng=0
#calculate weights for each sample
for sample in allSamples:
  if sample.has_key("hasWeight"):
    if sample["hasWeight"]:
      if not sample.has_key('weight'):
        sample['weight']="weight"
      print "Sample has stored weight!", sample["dirname"] , sample["name"], "using weight:",sample['weight']
      continue
#  print "peng", sample["name"]
  sample["weight"]={}
  for bin in sample["bins"]:
#    c = ROOT.TChain(sample["Chain"])
    d = ROOT.TChain("Runs")
    for thisfile in sample["filenames"][bin]:
      d.Add(thisfile)
#    print "peng2", sample["name"]
    nevents = 0
    nruns = d.GetEntries()
    for i in range(0, nruns):
      d.GetEntry(i)
  #    print "Counts = ",getValue(d,"uint_EventCounter_runCounts_PAT.obj")
      nevents += getValue(d,"uint_EventCounter_runCounts_PAT.obj")

    weight = 1.
    lumi = 1.
    normToLumi = False
    if globals().has_key("targetLumi"):
      lumi = targetLumi
#    print "peng3", sample["name"]
    if xsec.xsec.has_key(bin):
      normToLumi = True
      if nevents>0:
        weight = xsec.xsec[bin]*lumi/float(nevents)
      else:
        weight = 0.
    if normToLumi:
      print "Normalizing to lumi", lumi, sample["dirname"] , sample["name"], bin, nevents,"weight",weight
    else:
      print "Do NOT normalize to lumi;", sample["dirname"] , sample["name"], bin, nevents,"weight",weight
    sample["weight"][bin]=weight
    del d


#do the eventloop
rwHisto = ""
if globals().has_key("reweightingHistoFile"):
  if reweightingHistoFile!="":
    rf = ROOT.TFile(reweightingHistoFile)
    htmp = rf.Get("ngoodVertices_Data")
    ROOT.gDirectory.cd("PyROOT:/")    
    rwHisto = htmp.Clone()
    rf.Close()
    print "Using reweightingHisto", reweightingHistoFile, rwHisto
for var in allVars:
  var.data_histo.Reset()
for sample in allSamples:
  for bin in sample["bins"]:
    c = ROOT.TChain(sample["Chain"])
    for thisfile in sample["filenames"][bin]:
      c.Add(thisfile)
    ntot = c.GetEntries()
#    print "Sample",sample, "Total number of Events",ntot
    if ntot>0:
      for var in allVars:
        if var.sample["name"] == sample["name"] and var.sample["bins"].count(bin)==1:
          c.Draw(">>eList",var.commoncf)
          elist = ROOT.gDirectory.Get("eList")
          number_events = elist.GetN()
          if var.varfunc!="":
            print "var: Func:", var.varfunc.func_name,"Reading: ", sample["name"], bin, "with",number_events,"Events using cut", var.commoncf
          else:
            print "var:", var.name,"Reading: ", sample["name"], bin, "with",number_events,"Events using cut", var.commoncf
          if var.additionalCutFunc!="":
            print "Using additional Cut requirement:",var.additionalCutFunc
          if small:
            if number_events>200:
              number_events=200
          for i in range(0, number_events):
            if (i%10000 == 0) and i>0 :
              print i
      #      # Update all the Tuples
            if elist.GetN()>0 and ntot>0:
              c.GetEntry(elist.GetEntry(i))
              if var.additionalCutFunc!="" and not var.additionalCutFunc(c):
                continue
              nvtxWeight = 1.
              if rwHisto!="" and xsec.xsec.has_key(bin):
                nvtxWeight = rwHisto.GetBinContent(rwHisto.FindBin(getValue(c, "ngoodVertices" )))
                if sample.has_key("hasWeight"):
                  if sample["hasWeight"]:
                    print "WARNING! Using weights from tuple but also nvtx-reweighting File" , reweightingHistoFile
#                print "nvtx:", c.GetLeaf( "ngoodVertices" ).GetValue(), "bin", rwHisto.FindBin(c.GetLeaf( "ngoodVertices" ).GetValue()),"weight",nvtxWeight
              reweightFac = 1.
              if type(var.reweightVar) == types.FunctionType:
                  reweightFac = var.reweightVar(c)
#                  print "Using function", var.reweightVar, "->",reweightFac
              else:
                if var.reweightVar!="":
                  reweightFac = var.reweightHisto.GetBinContent(var.reweightHisto.FindBin(getValue(c, var.reweightVar)))
#                  print "reweightVar = ",var.reweightVar, c.GetLeaf(var.reweightVar).GetValue(), "->", reweightFac
              nvtxWeight=reweightFac*nvtxWeight 
              scaleFac = 1
              if sample.has_key('scaleFac'):
                scaleFac = sample['scaleFac']
              weight = 1
              if sample.has_key("hasWeight"):
                if sample["hasWeight"]:
                  weight = getValue(c, sample["weight"])
                else:
                  weight = sample["weight"][bin]
              else:
                weight = sample["weight"][bin]
              if var.varfunc!="":
                var.data_histo.Fill(var.varfunc(c), weight*nvtxWeight*scaleFac)
#                print "var",var,"name",var.name,"Using ", var.varfunc(c),"instead of", var.name 
              else:
                var.data_histo.Fill(getValue(c, var.name), weight*nvtxWeight*scaleFac)
#                print "var",var,"name",var.name,"weight",weight,"nvtxWeight",nvtxWeight, "Using ", getValue(c, var.name) 
          del elist
    else:
      print "Zero entries in", bin, sample["name"]
    del c
################################

#do the scalings, or do a chi2 fit
for stack in allStacks:
  zerohisto = stack[0].data_histo.Clone()
  zerohisto.Reset()
  floatingVars = []
  scaledVar = "None"
  myf=0
  for var in stack[:-1]:
    if var.floating == True: #could also be "scaleByNEvents"!
      floatingVars.append(var)
    if var.floating == "scaleByNEvents": #if there's a variable to be scaled by  N-Events(Data) instead, don't do a chi2-Fit
      floatingVars=[]
      scaledVar = var
      break
  if len(floatingVars)>0:
    sstring=""
    for var in floatingVars:
      sstring += var.legendText + " "
    print "Samples floating: "+sstring
    ROOT.gROOT.ProcessLine(".L ../../EarlyMETAnalysis/aclic/FitFraction.C")
    if len(floatingVars)>10:
      print "More than 10 Vars floating, not implemented! (", len(floatingVars),")"
    else:
  #    stuff.append(myf)
      for ivar in range(len(stack) - 1):
  #      myf.SetParameter(ivar, 1.)
        print "Var",ivar, stack[ivar].floating, stack[ivar].legendText
        ROOT.setFitTemplate(ivar, stack[ivar].data_histo.Clone(), int(stack[ivar].floating))
  #      if not stack[ivar].floating:
  #        myf.FixParameter(ivar,1.)
      for ivar in range(len(stack)-1, 10):
  #      myf.SetParameter(0, 0.)
  #      myf.FixParameter(ivar,0)
        print "Var",ivar
        ROOT.setFitTemplate(ivar, zerohisto.Clone(), -1)
  #    myf = ROOT.TF1("myf",ROOT.FitFraction,stack[0].data_histo.GetXaxis().GetXmin(),stack[0].data_histo.GetXaxis().GetXmax(),10)
  #    stack[-1].data_histo.Fit(myf)
      ROOT.Fit.doFit(stack[-1].data_histo)
      for ivar in range(len(stack) - 1):
         stack[ivar].scale = ROOT.getFitCoeff(ivar)
  if scaledVar!="None":
    print "Scaling",scaledVar.legendText
    ndata = stack[-1].data_histo.Integral()
    nmc = 0.
    for var in stack[:-1]:
      if var!=scaledVar:
        nmc+=var.data_histo.Integral()
        print "Summing", var.legendText, var.data_histo.Integral()
#      else:
#        print "Omitting", var.legendText
    expected = ndata - nmc
    nsv = scaledVar.data_histo.Integral()
    print "expected", expected, "data", ndata, "rest-mc", nmc, "sample before scaling", nsv
    if expected <= 0.:
      print "Warning! Scale of", scaledVar.legendText,"non-Positive! Won't scale!"
      continue
    if ndata <= 0:
      print "Warning! Adjusting",scaledVar.legendText,"to non-positive histo! Won't scale!"
      continue
    if nsv<=0:
      print "Warning! Histo to-be-scaled (",scaledVar.legendText," has non-positive Integral! Won't scale"
    scaledVar.scale= (ndata - nmc)/nsv
      
#Print a warning
for stack in allStacks:
  for var in stack:
    if var.scale !=1.:
      print "Scaling ",var.legendText,"by",var.scale
      var.data_histo.Scale(var.scale)
 
#For each var, add all histos in the list var.add (recursively)
sumsToBeDone = True
while sumsToBeDone:
  sumsToBeDone = False
#  print "Adding..."
  for var in allVars:
    if var.add!=[]:
      sumsToBeDone = True
      for addvar in var.add:
        if addvar==var:
          print "Warning! Recursion when adding up vars! --> Omitted", var.name, var
          continue
        if addvar.add==[]:    #if the variable to be added is not a sum itself then add it
          var.data_histo.Add(addvar.data_histo.Clone())
          var.add.remove(addvar)
#          print "    adding",addvar.legendText, "to", var.legendText
#        else:
#          print "NOT adding",addvar.legendText, "to", var.legendText

#rescale maximum (default)
for stack in allStacks:
  rescale=1.
  maximum = stack[0].data_histo.GetMaximum()
  for var in stack[1:]:
    if var.data_histo.GetMaximum()>maximum:
      maximum = var.data_histo.GetMaximum()
  fac=1.
  if var.logy:
    fac = 2.
  else:
    fac = 1.2
  stack[0].data_histo.SetMaximum(fac*maximum)

#do over-flow bins
for stack in allStacks:
  for var in stack:
    if stack[0].addOverFlowBin.lower() == "upper" or stack[0].addOverFlowBin.lower() == "both":
      nbins = var.data_histo.GetNbinsX()
      var.data_histo.SetBinContent(nbins , var.data_histo.GetBinContent(nbins) + var.data_histo.GetBinContent(nbins + 1))
      var.data_histo.SetBinError(nbins , sqrt(var.data_histo.GetBinError(nbins)**2 + var.data_histo.GetBinError(nbins + 1)**2))
    if stack[0].addOverFlowBin.lower() == "lower" or stack[0].addOverFlowBin.lower() == "both":
      var.data_histo.SetBinContent(1 , var.data_histo.GetBinContent(0) + var.data_histo.GetBinContent(1))
      var.data_histo.SetBinError(1 , sqrt(var.data_histo.GetBinError(0)**2 + var.data_histo.GetBinError(1)**2))
