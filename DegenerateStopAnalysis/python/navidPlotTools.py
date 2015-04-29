import ROOT



def saveCanvas(canv,name,plotDir="./",format=".gif"):
  canv.SaveAs(plotDir+"/"+name+format)



def decorate(hist,color='',width='',histTitle='',fillColor=''):
  if color: hist.SetLineColor(color)
  if width: hist.SetLineWidth(width)
  if histTitle: hist.SetTitle(histTitle)
  if fillColor: hist.SetFillColor(fillColor)
  return

def decorateAxis(hist,xAxisTitle='x title',yAxisTitle='y title',title=''):
  axis = hist.GetXaxis()
  axis.SetTitle(xAxisTitle)
#  axis.SetTitleOffSet(1)
  axis = hist.GetYaxis()
  axis.SetTitle(yAxisTitle)
#  axis.SetTitleOffSet(1)
#  axis.SetTitleFont(62) 
  if title:  hist.SetTitle(title)
  return 


def addToLeg(legend,hist,RMS=1,Mean=1,RMSError=0,MeanError=0,pName=''):
  if RMS:
    rmsString='  RMS={RMS:.2f}'.format(RMS=hist.GetRMS())
    if RMSError: rmsString += ' #pm {0:.2f}'.format(hist.GetRMSError())
  else: rmsString=''
  if Mean:
    meanString='  Mean={MEAN:.2f}'.format(MEAN=hist.GetMean())
    if MeanError: meanString += ' #pm {0:.2f}'.format(hist.GetMeanError())
  else: meanString=''
  if pName: nameString=pName

  else: nameString=hist.GetName()
  legString= nameString + rmsString + meanString
  legend.AddEntry(hist,legString)
  return legend
