import array

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
    subdirname = sample["dirname"]+"/"+bin+"/"
    if sample["bins"]==[""]:
      subdirname = sample["dirname"]+"/"
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
      sample["filenames"][bin] = [subdirname+"/h*.root"]
peng=0
#calculate weights for each sample
for sample in allSamples:
  if sample.has_key("hasWeight"):
    if sample["hasWeight"]:
      for bin in sample["bins"]:
        print "Sample has stored weight! Not calculated!!", sample["dirname"] , sample["name"], bin
      continue
#  print "peng", sample["name"]
  sample["weight"]={}
  for bin in sample["bins"]:
    c = ROOT.TChain(sample["Chain"])
    for thisfile in sample["filenames"][bin]:
      c.Add(thisfile)
#    print "peng2", sample["name"]
    nevents = -1
    if sample.has_key("Counter"):
      nevents = c.GetEntries(sample["Counter"])
    else:
      nevents = c.GetEntries()
    weight = 1.
    lumi = 1.
    normToLumi = False
    if globals().has_key("targetLumi"):
      lumi = targetLumi
#    print "peng3", sample["name"]
    if xsec.xsec.has_key(bin) and sample.has_key("hasWeight"):
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
    del c

for var in allVars:
  var.data_histo.Reset("M")
for sample in allSamples:
  for bin in sample["bins"]:
    chainstring = "Events"
    if sample.has_key("Chain"):
      chainstring = sample["Chain"]
    c = ROOT.TChain(chainstring)
    for thisfile in sample["filenames"][bin]:
      c.Add(thisfile)
    c.GetEntries()
    for var in allVars:
      if var.reweightVar!="":
        print "Waring! reweightVar = ",var.reweightVar, "ignored!"
      if var.sample["name"] == sample["name"] and var.sample["bins"].count(bin)==1:
        htmp=""
        if var.binningIsExplicit:
          htmp=ROOT.TH1F("htmpSPK","htmpSPK", len(var.binning) - 1, var.binning) # if binning is explicit, var.binning stores the array
        else:
          htmp=ROOT.TH1F("htmpSPK","htmpSPK",*(var.binning))
#        if var.style=="e":
        htmp.Sumw2()
        if not sample["hasWeight"]:
          c.Draw(var.name+">>htmpSPK",str(sample["weight"][bin])+"*("+var.commoncf+")")
          print "At variable",var.name, "Sample",sample["name"],"bin",bin, "adding",htmp.Integral(),str(sample["weight"][bin])+"*("+var.commoncf+")"
        else:
          sstring = sample['weight']+"*("+var.commoncf+")"
          c.Draw(var.name+">>htmpSPK",sstring)
          print "At variable",var.name, "Sample",sample["name"],"bin",bin, "adding",htmp.Integral(),sstring
        htmp=ROOT.gDirectory.Get("htmpSPK")
        var.data_histo.Add(htmp.Clone())
        del htmp
    del c

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
      

for stack in allStacks:
  for var in stack:
    if var.scale !=1.:
      print "Scaling ",var.legendText,"by",var.scale
      var.data_histo.Scale(var.scale)
 
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

for stack in allStacks:
  for var in stack:
    if stack[0].addOverFlowBin.lower() == "upper" or stack[0].addOverFlowBin.lower() == "both":
      nbins = var.data_histo.GetNbinsX()
      var.data_histo.SetBinContent(nbins , var.data_histo.GetBinContent(nbins) + var.data_histo.GetBinContent(nbins + 1))
      var.data_histo.SetBinError(nbins , sqrt(var.data_histo.GetBinError(nbins)**2 + var.data_histo.GetBinError(nbins + 1)**2))
    if stack[0].addOverFlowBin.lower() == "lower" or stack[0].addOverFlowBin.lower() == "both":
      var.data_histo.SetBinContent(1 , var.data_histo.GetBinContent(0) + var.data_histo.GetBinContent(1))
      var.data_histo.SetBinError(1 , sqrt(var.data_histo.GetBinError(0)**2 + var.data_histo.GetBinError(1)**2))

