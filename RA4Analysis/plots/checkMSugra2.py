import ROOT, pickle
from Workspace.RA4Analysis.simplePlotsCommon import *
ROOT.gStyle.SetOptStat(0)
ROOT.setTDRStyle()
#ROOT.gStyle.SetPadRightMargin(0.10);
if type(ROOT.tdrStyle)!=type(ROOT.gStyle):
  del ROOT.tdrStyle
  ROOT.setTDRStyle()

ROOT.tdrStyle.SetPadRightMargin(0.16)
ROOT.gROOT.ProcessLine(".L ../../HEPHYCommonTools/scripts/root/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)

#load stuff

if not globals().has_key("LO_Mu_efficiency"):
  print "Loading..."

  globals()["countsPP"]   =  pickle.load(file('/data/schoef/efficiencies/msugra/msugra_countsPP.pkl'))

  globals()["LO_Mu_efficiency"] =     pickle.load(open("/data/schoef/efficiencies/msugra/Mu_msugra_LO_efficiency.pkl"))
  globals()["NLO_Mu_efficiency"] =    pickle.load(open("/data/schoef/efficiencies/msugra/Mu_msugra_NLO_efficiency.pkl"))
  globals()["LO_Mu_events"] =     pickle.load(open("/data/schoef/efficiencies/msugra/Mu_msugra_LO_events.pkl"))
  globals()["NLO_Mu_events"] =    pickle.load(open("/data/schoef/efficiencies/msugra/Mu_msugra_NLO_events.pkl"))
  globals()["NLO_Mu_eventsPP"] =    pickle.load(open("/data/schoef/efficiencies/msugra/Mu_msugra_NLO_eventsPP.pkl"))
  globals()["Mu_efficiencyPP"] =   pickle.load(open("/data/schoef/efficiencies/msugra/Mu_msugra_efficiencyPP.pkl"))
  globals()["LO_Mu_countsPP"] =    pickle.load(open("/data/schoef/efficiencies/msugra/Mu_msugra_LO_countsPP.pkl"))
  globals()["NLO_Mu_countsPP"] =    pickle.load(open("/data/schoef/efficiencies/msugra/Mu_msugra_NLO_countsPP.pkl"))

  globals()["LO_Ele_efficiency"] =    pickle.load(open("/data/schoef/efficiencies/msugra/Ele_msugra_LO_efficiency.pkl"))
  globals()["NLO_Ele_efficiency"] =   pickle.load(open("/data/schoef/efficiencies/msugra/Ele_msugra_NLO_efficiency.pkl"))
  globals()["LO_Ele_events"] =    pickle.load(open("/data/schoef/efficiencies/msugra/Ele_msugra_LO_events.pkl"))
  globals()["NLO_Ele_events"] =   pickle.load(open("/data/schoef/efficiencies/msugra/Ele_msugra_NLO_events.pkl"))
  globals()["NLO_Ele_eventsPP"] =    pickle.load(open("/data/schoef/efficiencies/msugra/Ele_msugra_NLO_eventsPP.pkl"))
  globals()["Ele_efficiencyPP"] =   pickle.load(open("/data/schoef/efficiencies/msugra/Ele_msugra_efficiencyPP.pkl"))
  globals()["LO_Ele_countsPP"] =    pickle.load(open("/data/schoef/efficiencies/msugra/Ele_msugra_LO_countsPP.pkl"))
  globals()["NLO_Ele_countsPP"] =    pickle.load(open("/data/schoef/efficiencies/msugra/Ele_msugra_NLO_countsPP.pkl"))
else:
  print "Already loaded."

#specify point

m0 = 760
m12 = 400

btagbin = 'inc'
metcut = 250
htcut = 750
targetLumi = 4700

#load xsec-dicts and define getters
if not globals().has_key("xsecNLODict"):
  xsecNLODict = pickle.load(file('/data/schoef/efficiencies/msugra/tanb10.msugra_xsecs.pc'))
def xsecNLO(m0, m12, pcode):
  if (xsecNLODict.has_key(int(m12))) and not pcode == "--":
    if (xsecNLODict[int(m12)].has_key(int(m0))):
      return xsecNLODict[int(m12)][int(m0)][pcode]
  return float('nan')

if not globals().has_key("xsecLODict"):
  xsecLODict =  pickle.load(file('/data/schoef/efficiencies/msugra/goodModelNames_10_0_1.pkl'))
def xsecLO(m0, m12):
  if xsecLODict.has_key((m0, m12, 10,0,1)):
    return xsecLODict[(m0, m12, 10, 0, 1)]
  else:
    return float('nan')

#load counts PP before any cut i.e. "generated counts"
countsPP   =  pickle.load(file('/data/schoef/efficiencies/msugra/msugra_countsPP.pkl')) #dict. with generated events which should sum to the countsTotal dict (next line) 
countsTotal=  pickle.load(file('/data/schoef/efficiencies/msugra/msugra_counts.pkl')) #a number which should be very close to 10k

#print some stuff
sstring = "msugra_"+str(m0)+"_"+str(m12)+"_10_0_1"
print "Consistency check: "+b("m0")+":",m0,b("m12"),m12
print b("countsPP    "),    countsPP [sstring]
print b("countsTotal "), countsTotal [sstring]
print b("xSecLO      "), xsecLO(m0,m12), b("events LO Total"), xsecLO(m0,m12)*targetLumi,\
         "signal events LO Mu:", LO_Mu_events[btagbin][htcut][metcut][sstring], "signal events LO Ele:", LO_Ele_events[btagbin][htcut][metcut][sstring]
print b("xSecNLO     "), xsecNLO(m0,m12, 'total'), b("events NLO Total"), xsecNLO(m0,m12,'total')*targetLumi,\
         "signal events NLO Mu:", NLO_Mu_events[btagbin][htcut][metcut][sstring], "signal events NLO Ele:", NLO_Ele_events[btagbin][htcut][metcut][sstring]

#make an independent calculation of efficiencies by calculating the weighted avarage of the efficienciesPP which themselves are independent of NLO/LO stuff
mu_lo_num = 0.
ele_lo_num = 0.
lo_den = 0.
mu_nlo_num = 0.
ele_nlo_num = 0.
nlo_den = 0.
for k in countsPP [sstring].keys():
  targetLumi*xsecNLO(m0,m12, 'total')
  lo_cont = countsPP [sstring][k]/10000.
  nlo_cont =  xsecNLO(m0,m12,k)/xsecNLO(m0,m12,'total')
  ele_eff_d = Ele_efficiencyPP[btagbin][htcut][metcut][sstring]
  ele_eff = 0.
  if ele_eff_d.has_key(k):
    ele_eff = ele_eff_d[k]
  mu_eff_d = Mu_efficiencyPP[btagbin][htcut][metcut][sstring]
  mu_eff = 0.
  if mu_eff_d.has_key(k):
    mu_eff = mu_eff_d[k]

  print k, "contr. at LO", lo_cont, "contr. at NLO", nlo_cont, "relative contribution change for this process:", nlo_cont/lo_cont, "(it has eff. Mu:", mu_eff, "Ele", ele_eff,")"
  mu_nlo_num += nlo_cont*mu_eff
  ele_nlo_num += nlo_cont*ele_eff
  nlo_den += nlo_cont 
  mu_lo_num += lo_cont*mu_eff
  ele_lo_num += lo_cont*ele_eff
  lo_den += lo_cont 
#Result: 
print "mu_lo_num/lo_den", mu_lo_num/lo_den, "ele_lo_num/nlo_den", ele_lo_num/nlo_den, "mu_nlo_num/lo_den", mu_nlo_num/lo_den, "ele_nlo_num/nlo_den", ele_nlo_num/nlo_den,

#print some more stuff
print "\n",b("NLO events Mu                "), NLO_Mu_events[btagbin][htcut][metcut][sstring]
print      b("NLO events Ele               "), NLO_Ele_events[btagbin][htcut][metcut][sstring]
print      b("NLO events Ele+Mu            "), NLO_Mu_events[btagbin][htcut][metcut][sstring]+NLO_Ele_events[btagbin][htcut][metcut][sstring]
print "\n"
print "\n",b("LO events Mu                 "), LO_Mu_events[btagbin][htcut][metcut][sstring]
print      b("LO events Ele                "), LO_Ele_events[btagbin][htcut][metcut][sstring]
print      b("LO events Ele+Mu             "), LO_Mu_events[btagbin][htcut][metcut][sstring]+LO_Ele_events[btagbin][htcut][metcut][sstring]
print "\n"
#compare k-factors
print "\n",b("k-factor signal region Mu    "), (NLO_Mu_events[btagbin][htcut][metcut][sstring])/(LO_Mu_events[btagbin][htcut][metcut][sstring])
print      b("k-factor signal region Ele   "), (NLO_Ele_events[btagbin][htcut][metcut][sstring])/(LO_Ele_events[btagbin][htcut][metcut][sstring])
print      b("k-factor signal region Mu+Ele"), (NLO_Mu_events[btagbin][htcut][metcut][sstring]+NLO_Ele_events[btagbin][htcut][metcut][sstring])/(LO_Mu_events[btagbin][htcut][metcut][sstring]+LO_Ele_events[btagbin][htcut][metcut][sstring])
print      b("k-factor inclusive           "), xsecNLO(m0,m12,'total') / xsecLO(m0,m12)
print "\n"
#print some dicts for easy c/p in the terminal
print b("xSecNLO PP  "), xsecNLODict[int(m12)][int(m0)]
print b("efficiencyPP: Mu :"),  Mu_efficiencyPP[btagbin][htcut][metcut][sstring]
print b("efficiencyPP: Ele:"),  Ele_efficiencyPP[btagbin][htcut][metcut][sstring]
print b("LO efficiency: Mu:"),  LO_Mu_efficiency[btagbin][htcut][metcut][sstring]
print b("LO efficiency: Ele:"),  LO_Ele_efficiency[btagbin][htcut][metcut][sstring]
print b("NLO efficiency: Mu:"),  NLO_Mu_efficiency[btagbin][htcut][metcut][sstring]
print b("NLO efficiency: Ele:"),  NLO_Ele_efficiency[btagbin][htcut][metcut][sstring]

#calculating NLO efficiency by hand a third time
Mu_num = 0.
Ele_num = 0.
den = 0.
for k in Mu_efficiencyPP[btagbin][htcut][metcut][sstring].keys(): 
    Mu_num+=Mu_efficiencyPP[btagbin][htcut][metcut][sstring][k]*xsecNLO(m0,m12,k)
    Ele_num+=Ele_efficiencyPP[btagbin][htcut][metcut][sstring][k]*xsecNLO(m0,m12,k)
    den+=xsecNLO(m0,m12,k)
print b("NLO-x-sec-weighted effPP-avg: "),"Mu:",Mu_num/den,"Ele:",Ele_num/den

#The sanity check mentioned in the mail
print "Ele events     sg/ss", NLO_Ele_eventsPP['inc'][750][250][sstring]['sg'] / NLO_Ele_eventsPP['inc'][750][250][sstring]['ss']
print "Ele count*xsec sg/ss", (NLO_Ele_countsPP['inc'][750][250][sstring]['sg']*xsecNLO(m0,m12,'sg') / countsPP[sstring]['sg']) /(NLO_Ele_countsPP['inc'][750][250][sstring]['ss']*xsecNLO(m0,m12,'ss')/ countsPP[sstring]['ss'])
print "Mu events      sg/ss", NLO_Mu_eventsPP['inc'][750][250][sstring]['sg'] / NLO_Mu_eventsPP['inc'][750][250][sstring]['ss']
print "Mu count*xsec  sg/ss", (NLO_Mu_countsPP['inc'][750][250][sstring]['sg']*xsecNLO(m0,m12,'sg')/ countsPP[sstring]['sg']) /(NLO_Mu_countsPP['inc'][750][250][sstring]['ss']*xsecNLO(m0,m12,'ss')/ countsPP[sstring]['ss'])
