import ROOT
import pickle
from Workspace.HEPHYPythonTools.user import username
from Workspace.HEPHYPythonTools.helpers import *
#from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getCutYieldFromChain, getYieldFromChain
from Workspace.RA4Analysis.cmgTuples_Data25ns_PromtV2_mine import *

def allUnique(x):
  seen = list()
  return not any(i in seen or seen.append(i) for i in x)

#jsn = {"273158": [[1, 1279]], "273302": [[1, 459]], "273402": [[100, 292]], "273403": [[1, 53]], "273404": [[1, 18]], "273405": [[2, 25]], "273406": [[1, 112]], "273408": [[1, 6]], "273409": [[1, 309]], "273410": [[1, 90]], "273411": [[1, 29]], "273425": [[62, 352], [354, 733]], "273446": [[1, 33]], "273447": [[1, 113], [115, 412]], "273448": [[1, 391]], "273449": [[1, 214]], "273450": [[1, 214], [219, 647]], "273492": [[71, 71], [73, 282], [284, 325], [327, 338]], "273493": [[1, 233]], "273494": [[1, 192]], "273502": [[73, 256], [258, 318], [320, 813], [815, 1064]], "273503": [[1, 598]], "273554": [[77, 437]], "273555": [[1, 173]], "273725": [[83, 252], [254, 2545]], "273728": [[1, 100]], "273730": [[1, 1814], [1820, 2126]], "274094": [[105, 332]], "274146": [[1, 67]], "274159": [[1, 43]], "274160": [[1, 207]], "274161": [[1, 516]], "274172": [[31, 95]], "274198": [[81, 191]], "274199": [[1, 623]], "274200": [[1, 678]], "274240": [[1, 40], [42, 82]]}
jsn = {"273158": [[1, 1279]], "273302": [[1, 459]], "273402": [[100, 292]], "273403": [[1, 53]], "273404": [[1, 18]], "273405": [[2, 25]], "273406": [[1, 112]], "273408": [[1, 6]], "273409": [[1, 309]], "273410": [[1, 90]], "273411": [[1, 29]], "273425": [[62, 352], [354, 733]], "273446": [[1, 33]], "273447": [[1, 113], [115, 412]], "273448": [[1, 391]], "273449": [[1, 214]], "273450": [[1, 214], [219, 647]], "273492": [[71, 71], [73, 282], [284, 325], [327, 338]], "273493": [[1, 233]], "273494": [[1, 192]], "273502": [[73, 256], [258, 318], [320, 813], [815, 1064]], "273503": [[1, 598]], "273554": [[77, 437]], "273555": [[1, 173]], "273725": [[83, 252], [254, 2545]], "273728": [[1, 100]], "273730": [[1, 1814], [1820, 2126]], "274094": [[105, 332]], "274146": [[1, 67]], "274159": [[1, 43]], "274160": [[1, 207]], "274161": [[1, 516]], "274172": [[31, 95]], "274198": [[81, 191]], "274199": [[1, 623]], "274200": [[1, 678]], "274240": [[1, 40], [42, 82]], "274241": [[1, 296], [298, 1152], [1161, 1176]], "274244": [[1, 607]], "274250": [[1, 701]], "274251": [[1, 546]], "274283": [[2, 19]], "274284": [[1, 210]], "274286": [[1, 154]], "274314": [[97, 97], [99, 158]], "274315": [[1, 375], [377, 424]], "274316": [[1, 959]], "274317": [[1, 3]], "274319": [[1, 225]], "274335": [[60, 1003]], "274336": [[1, 14]], "274337": [[3, 17]], "274338": [[1, 698]], "274339": [[1, 29], [31, 31], [33, 33], [35, 93]], "274344": [[1, 632]], "274345": [[1, 170]], "274382": [[94, 144]], "274387": [[88, 439]], "274388": [[1, 1730], [1732, 1820]], "274420": [[94, 268]], "274421": [[1, 342]], "274422": [[1, 2207]], "274440": [[92, 493]], "274441": [[1, 431]], "274442": [[1, 256], [258, 752]]}
list_run_lumi = []
runs = jsn.keys()
for run in runs:
  for lumi in jsn[run]:
     list_run_lumi.append("(run=="+str(run)+"&&"+"lumi>="+str(lumi[0])+"&&"+"lumi<="+str(lumi[1])+")")

str_run_lumi = "||".join(list_run_lumi)

print str_run_lumi

chunks = getChunks(SingleElectron_Run2016B_PromptReco_v2)
#
chain = getChain(chunks[0],treeName='tree')
print "hey" , chain.GetEntries(str_run_lumi)
##chain = getTreeFromChunk(chunks[0], "nJet>8&&nLepGood==1&&htJet40>1000")
#chain.Draw("nJet", "nJet>8&&nLepGood==1&&htJet40>1000")
#chain.Draw(">>eList", "nJet>8&&nLepGood==1&&htJet40>1000")
#eList = ROOT.gDirectory.Get("eList")
#number_events = eList.GetN()
##chain.Scan("run:lumi:evt", "!("+str_run_lumi+")")
#
#
##nEvents = chain.GetEntries()
#
#ultimate_events = []
#
#for i in range(number_events):
#  chain.GetEntry(eList.GetEntry(i))
#  run_branch = chain.GetLeaf('run').GetValue()
#  lumi_branch = chain.GetLeaf('lumi').GetValue()
#  evt_branch = chain.GetLeaf('evt').GetValue()
#  print run_branch , lumi_branch , evt_branch
#  str_evt = "_".join([str(run_branch),str(lumi_branch),str(evt_branch)]) 
#  #print str_evt
#  ultimate_events.append(list(str_evt)) 
#  
#if not allUnique(ultimate_events):
#  print "HEYY You have double counting in your events!!!!"
