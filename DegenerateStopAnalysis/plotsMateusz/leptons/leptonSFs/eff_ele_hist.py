from ROOT import *
from math import *
import sys

binning = [5., 10., 20., 30., 45., 60.]
etabins = {
"barrel": "probe_sc_abseta<1.442",
"endcap": "probe_sc_abseta>1.566",
"all": "(probe_sc_abseta<1.442||probe_sc_abseta>1.566)"
}

mode = "Data"
if len(sys.argv)>1: mode = sys.argv[1]
if mode != "Data" and mode != "MC":
    print "wrong mode"
    sys.exit()
    
stage = "IdSpec"
#stage = "IpIso"
if len(sys.argv)>2: stage = sys.argv[2]
if stage != "IpIso" and stage != "Id" and stage != "IdSpec":
    print "wrong stage"
    sys.exit()


def gethist(t,cut,lowedge,highedge,tag,etabin):
    histname = "h_{0:.1f}_{1:.1f}_{3}_{2}".format(lowedge,highedge,tag,etabin)
    histname = histname.replace(".","p")
    hz = TH1F(histname,"",60,60,120)
    t.Draw("mass>>"+histname,cut,"goff")
    return hz

EAval = [0.1752,0.1862,0.1411,0.1534,0.1903,0.2243,0.2687]
EAeta = [0.,1.,1.479,2.,2.2,2.3,2.4,2.5]

EAlist = []
for i in xrange(len(EAval)):
    EAlist.append("((probe_Ele_abseta>={0:5.3f}&&probe_Ele_abseta<{1:5.3f})*{2:6.4f})".format(EAeta[i],EAeta[i+1],EAval[i]))
EA = "+".join(EAlist)
relISO = "(probe_Ele_chIso+max(0.0,(probe_Ele_neuIso+probe_Ele_phoIso-PU)))/probe_Ele_pt"
relISO = relISO.replace("PU","event_rho*"+EA)
HISO = relISO+"*min(probe_Ele_pt,25.)"

if stage == "Id":
    ID = "probe_Ele_abseta<2.5&&(tag_Ele_q*probe_Ele_q)==-1"
    PASS = "passingVeto"
elif stage == "IpIso":
    ID = "probe_Ele_abseta<2.5&&passingVeto"
    PASS = "abs(probe_Ele_dxy)<0.02&&abs(probe_Ele_dz)<0.1&&"+HISO+"<5."
elif stage == "IdSpec":
    ID = "probe_Ele_abseta<2.5&&(tag_Ele_q*probe_Ele_q)==-1&&probe_Ele_dr03TkSumPt<4"
    PASS = "passingVeto"

FAIL = "!("+PASS+")"

TRIGZ = "1"
EXTRZ = "tag_Ele_abseta<2.1&&tag_Ele_pt>30&&abs(tag_Ele_dxy)<0.02&&abs(tag_Ele_dz)<0.2"

t = TChain("GsfElectronToEleID/fitter_tree")

if mode =="Data":
    t.Add("/data/run2/tnp/electrons/TnPTree_SingleElectron_2016rereco_RunB.root")
    t.Add("/data/run2/tnp/electrons/TnPTree_SingleElectron_2016rereco_RunC.root")
    t.Add("/data/run2/tnp/electrons/TnPTree_SingleElectron_2016rereco_RunD.root")
    t.Add("/data/run2/tnp/electrons/TnPTree_SingleElectron_2016rereco_RunE.root")
    t.Add("/data/run2/tnp/electrons/TnPTree_SingleElectron_2016rereco_RunF.root")
    t.Add("/data/run2/tnp/electrons/TnPTree_SingleElectron_2016rereco_RunG.root")
    t.Add("/data/run2/tnp/electrons/TnPTree_SingleElectron_2016prompt_RunH.root")
else:
    t.Add("/data/run2/tnp/electrons/TnPTree_DYToEE_NNPDF30_13TeV-powheg-pythia8_DYToEE_powheg_Moriond17.root")
    
fout = TFile("ele_histos"+mode+stage+".root","recreate")

hlist = []

for ipt in range(len(binning)-1):
    ptlow = binning[ipt]
    pthigh = binning[ipt+1]
    PTCUT = "probe_Ele_pt>{0:f}&&probe_Ele_pt<={1:f}".format(ptlow,pthigh)
    print ptlow,pthigh

    for etabin,etacut in etabins.items():

        cut = "&&".join([TRIGZ,ID,EXTRZ,PTCUT,etacut])
        hlist.append(gethist(t,"&&".join([cut,PASS]),ptlow,pthigh,"pass",etabin))
        hlist.append(gethist(t,"&&".join([cut,FAIL]),ptlow,pthigh,"fail",etabin))
    

fout.Write()
fout.Close()


