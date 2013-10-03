from analysisHelpers import *
from math import *

def mcClosureTable (ht = 750):

  htb = [ ht, 2500 ]
  btbs = [ 0, 1, 2 ]
  mets = [ 250, 350, 450, 550 ]
  table = [ ]
  table.append(r"\begin{table}")
  table.append(r"\begin{center}")
  table.append(r"\caption{")
  table.append(r"Predicted and true event counts in simulation for different $\ETmiss$ signal regions for $"+str(ht)+r" < \HT < 2500 \GeV$.")
  table.append("Uncertainties are statistical.")
  table.append(r"}\label{tab:fitResultsDetails-ht"+str(ht)+"}")
  table.append(r"\begin{tabular}{c"+len(btbs)*r"||c|c"+"}")
  table.append(r"\hline")
  line = r"\multirow{2}{*}{$\HT > "+str(ht)+" \GeV$}"
  for ibtb,btb in enumerate(btbs):
      line += r" & \multicolumn{2}{"
      if ibtb > 0:  line += "||"
      line += "c}{"+str(btb)+"-tag}"
  line += r" \\ \cline{2-"+str(2*len(btbs)+1)+"}"
  table.append(line)
  line = ""
  for btb in btbs:
      line += " & MC pred. & MC truth"
  line += r" \\ \hline"
  table.append(line)
  for met in [ 250, 350, 450, 550 ]:
      metb = [ met, 2500 ]
      line = r"\rule{0pt}{2.5ex} $\ETmiss > "+str()+" \GeV$"
      for btb in btbs:
          res  = getPredictionFromSamplingDirectory(goodDirectories['MC_central'], btb = btb, htb = htb, metb = metb, metvar = "met")
          predval = res['predictedYield']
          prederrplus = res['predictedYield_Uncertainty_CombinedPoissonian_Up'] - predval
          prederrminus = predval - res['predictedYield_Uncertainty_CombinedPoissonian_Down']
          trueval = res['dataYield']['res']
          trueerr = res['dataYield']['sigma']
          minerr = min(abs(prederrplus),abs(prederrminus),abs(trueerr))
          ndig = -int(floor(log10(minerr))) + 1
          if ndig < 0:  ndig = 0
          cfmt = " & $ %"+str(5+ndig)+"."+str(ndig)+"f ^{+ %"+str(4+ndig)+"."+str(ndig)+"f} _{- %"+str(4+ndig)+"."+str(ndig)+"f} $"
          line += cfmt%(predval,prederrplus,prederrminus)
          cfmt = " & $ %"+str(5+ndig)+"."+str(ndig)+"f \pm %"+str(4+ndig)+"."+str(ndig)+"f $"
          line += cfmt%(trueval,trueerr)
      line += r"\\"
      table.append(line)
  table.append(r"\end{tabular}")
  table.append(r"\end{center}")
  table.append(r"\end{table}")

  for line in table:  print line
          
def dataTable (ht = 750):

  htb = [ ht, 2500 ]
  btbs = [ 0, 1, 2 ]
  mets = [ 250, 350, 450, 550 ]
  print r"\begin{table}"
  print r"\begin{center}"
  print r"\begin{tabular}{c"+len(btbs)*r"||c|c"+"}"
  print r"\hline"
  line = r"\multirow{2}{*}{$"+str(ht)+r" < \HT < 2500 \GeV$}"
  for ibtb,btb in enumerate(btbs):
      line += r" & \multicolumn{2}{"
      if ibtb > 0:  line += "||"
      line += "c}{"+str(btb)+"-tag}"
  line += r" \\ \cline{2-"+str(2*len(btbs)+1)+"}"
  print line
  line = ""
  for btb in btbs:
      line += " & pred. & obs. "
  line += r" \\ \hline"
  print line
  for met in [ 250, 350, 450, 550 ]:
      metb = [ met, 2500 ]
      line = "$"+str(met)+r" < \ETmiss < 2500 \GeV$"
      for btb in btbs:
          res  = getPredictionFromSamplingDirectory(goodDirectories['data_central'], btb = btb, htb = htb, metb = metb, metvar = "met")
          predval = res['predictedYield']
          prederrplus = res['predictedYield_Uncertainty_CombinedPoissonian_Up'] - predval
          prederrminus = predval - res['predictedYield_Uncertainty_CombinedPoissonian_Down']
          trueval = res['dataYield']['res']
          trueerr = res['dataYield']['sigma']
          minerr = min(abs(prederrplus),abs(prederrminus),abs(trueerr))
          ndig = -int(floor(log10(minerr)))
          if ndig < 0:  ndig = 0
          cfmt = " & $ %"+str(5+ndig)+"."+str(ndig)+"f ^{+ %"+str(4+ndig)+"."+str(ndig)+"f} _{- %"+str(4+ndig)+"."+str(ndig)+"f} $"
          line += cfmt%(predval,prederrplus,prederrminus)
          line += " & $ "+str(int(trueval+0.5))+" $"
      line += r"\\"
      print line
  print r"\end{tabular}"
  print r"\end{center}"
  print r"\end{table}"
          
def systTable (met=250, btbs = [0,1], hts=[750,1000]):

  metb = [ met, 2500 ]
#  btbs = [ 0, 1, 2 ]
#  btbs = [ 0, 1 ]
#  hts = [ 400, 750, 1000 ]
  
  table = [ ]

  table.append(r"\begin{table}")
  table.append(r"\begin{center}")
  table.append(r"\caption{")
  table.append(r"}\label{tab:BkgSyst_"+str(met)+"}")
  table.append(r"\begin{tabular}{c"+len(hts)*(r"|"+len(btbs)*r"|c")+"}")
  table.append(r"\hline")
  line = "Source "
  for iht,ht in enumerate(hts):
    line += r"& \multicolumn{"+str(len(btbs))+"}{c"
    if iht<(len(hts)-1):  line += r"||"
    line += r"c}{$ \HT > "+str(ht)+r" \GeV$}"
  line += r" \\ \cline{2-"+str(len(hts)*len(btbs)+1)+"}"
  table.append(line)
  line = ""
  for ht in hts:
    for ibtb,btb in enumerate(btbs):
      line += " & "+str(btb)+"-tag"
#  line += r" \\ \cline{2-"+str(2*len(btbs)+1)+"}"
  line += r"\\ \hline"
  table.append(line)

  systNames = [
    ( 'JES' , r"JES and \ETmiss scale" ),
    ( 'WPol1' , r"\PW\ polarization (1)" ),
    ( 'WPol2Minus' , r"\PWm\ polarization (2)" ),
    ( 'WPol2Plus' , r"\PWp\ polarization (2)" ),
    ( 'WPol3' , r"\PW\ polarization (3)" ),
#    ( 'btag_SF_b' , "" ), 
#    ( 'btag_SF_light' , "" ), 
    ( 'DiLep' , "dilep. contr." ),
    ( 'PU' , "pile-up" ),
    ( 'TTPol' , r"\ttbar polarization" ),
    ( 'TTXSec' , r"$\sigma$(\ttbar)" )
    ]

  allres = { }
  for ht in hts:
    allres[ht] = { }
    for btb in btbs:
      allres[ht][btb] = allUncertainties(htb=[ht,2500],metb=metb,btb=btb)

  for syst,systName in systNames:
    line = systName
    for ht in hts:
      for btb in btbs:
#        print "relAbsSys",syst,ht,btb,allres[ht][btb][syst]['relAbsSysSR'],allres[ht][btb][syst]['relAbsSysDR']
#        print "res_sum: +/-", \
#              allres[ht][btb][syst]['predictedYield_Plus'], \
#              allres[ht][btb][syst]['predictedYield_Minus'], \
#              allres[ht][btb][syst]['trueYield_Reference'], \
#              allres[ht][btb][syst]['trueYield_Plus'], \
#              allres[ht][btb][syst]['trueYield_Minus']
        absSR = allres[ht][btb][syst]['relAbsSysSR']
        absDR = allres[ht][btb][syst]['relAbsSysDR']
        line += "& %5.1f%s" % (100*min(absSR,absDR),r"\%")
    line += r" \\"
    table.append(line)
  table.append(r"\end{tabular}")
  table.append(r"\end{center}")
  table.append(r"\end{table}")

  print ""
  for line in table:  print line

def btagTable ():

  btbs = [ 0, 1, 2 ]
  hts = [ 750, 1000 ]
  mets = [ 250, 350, 450, 550 ]
  
  varNames = [
    ( 'btag_SF_b' , "var. b" ), 
    ( 'btag_SF_light' , "var. light" )
    ]


  table = [ ]

  table.append(r"\begin{table}")
  table.append(r"\begin{center}")
  table.append(r"\caption{")
  table.append(r"}\label{tab:btaggingVarBG}")
  table.append(r"\begin{tabular}{c"+len(hts)*(r"|"+len(varNames)*r"|c")+"}")
  table.append(r"\hline")
  line = ""
  for iht,ht in enumerate(hts):
    line += r"& \multicolumn{"+str(len(varNames))+"}{"
    if iht>0:  line += r"||"
    line += "c}{$"+str(ht)+r" < \HT < 2500 \GeV$}"
  line += r" \\ \cline{2-"+str(len(hts)*len(varNames)+1)+"}"
  table.append(line)
  line = ""
  for ht in hts:
    for ivar,var in enumerate(varNames):
#      if ivar>0:  line += r"||"
      line += " & "+var[1]
  line += r"\\ \hline"
  table.append(line)


  allres = { }
  for met in mets:
    allres[met] = { }
    for ht in hts:
      allres[met][ht] = { }
      for btb in btbs:
        allres[met][ht][btb] = allUncertainties(htb=[ht,2500],metb=[met,2500],btb=btb)

  for met in mets:
    table.append("\hline")
    line = r"& \multicolumn{"+str(len(hts)*len(varNames))+"}{c}{$"+str(met)+r" <\ETmiss < 2500 \GeV$} \\ \hline"
    table.append(line)
    for btb in btbs:
      line = str(btb)+"-tags"
      for ht in hts:
        for var in varNames:
          delta = allres[met][ht][btb][var[0]]['trueYield_Plus']/allres[met][ht][btb][var[0]]['trueYield_Reference']-1
          line += "& %5.1f%s" % ( 100*delta, r"\%" )
      line += r"\\"
      table.append(line)
    table.append(r"\hline")
  table.append(r"\end{tabular}")
  table.append(r"\end{center}")
  table.append(r"\end{table}")

  print ""
  for line in table:  print line
