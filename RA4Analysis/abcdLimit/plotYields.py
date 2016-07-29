import ROOT
import pickle
import sys,os

ROOT.gStyle.SetOptStat(0)
fncolor = os.path.expandvars("$WORK/susy/CMSSW_7_4_14/src/Workspace/HEPHYPythonTools/scripts/root/useNiceColorPalette.C")
ROOT.gROOT.ProcessLine(".L "+fncolor)
ROOT.useNiceColorPalette()


def rangeToLabel(r):
    label = str(r[0])
    if r[1]==-1:
        label += "p"
    else:
        label += "to"+str(r[1])
    return label

def srToLabel(sr):
    label = "nj" + rangeToLabel(sr[0]) + "_"
    label += "lt" + rangeToLabel(sr[1]) + "_"
    label += "ht" + rangeToLabel(sr[2])
    return label

sigs = pickle.load(file(sys.argv[1]))

useSignalsKey = None

srs = [ ]
mglus = set()
mlsps = set()
for nj in sigs:
    for lt in sigs[nj]:
        for ht in sigs[nj][lt]:
            sr = ( nj, lt, ht )
            assert not sr in srs
            srs.append(sr)
            subdict = sigs[nj][lt][ht]
            if useSignalsKey==None:
                useSignalsKey = "signals" in subdict
                print "Set useSignalsKey to ",useSignalsKey
            if useSignalsKey:
                subdict = subdict["signals"]
            for mg in subdict:
                if not mg in mglus:
                    mglus.add(mg)
                for ml in subdict[mg]:
                    if not ml in mlsps:
                        mlsps.add(ml)

print mglus
print mlsps

mglus = sorted(mglus)
dmgs = [ ]
for i in range(len(mglus)-1):
    dm = mglus[i+1] - mglus[i]
    if not dm in dmgs:
        dmgs.append(dm)
dmgs.sort()

mlsps = sorted(mlsps)
dmls = [ ]
for i in range(len(mlsps)-1):
    dm = mlsps[i+1] - mlsps[i]
    if not dm in dmls:
        dmls.append(dm)
dmls.sort()

dmglu = 25.
#dmglu = 50.
mgluMin = mglus[0]
mgluMax = mglus[-1]
nmglu = int((mgluMax-mgluMin)/dmglu+1.5)

dmlsp = 25.
#dmlsp = 50.
mlspMin = 0.
mlspMax = mlsps[-1]
nmlsp = int((mlspMax-mlspMin)/dmlsp+1.5)


histos = [ ]
for sr in srs:
    label = srToLabel(sr)
    d = sigs[sr[0]][sr[1]][sr[2]]
    if useSignalsKey:
        d = d["signals"]
    for b in [ "MB" ]:
        for r in [ "SR" ]:
            hn = label+"_"+b+"_"+r
            h = ROOT.TH2F(hn,hn, \
                          nmglu,mgluMin-dmglu/2.,mgluMax+dmglu/2., \
                          nmlsp,mlspMin-dmlsp/2.,mlspMax+dmlsp/2.)
            h.SetMinimum(0.001)
            h.SetMaximum(100.)
            histos.append(h)
            xaxis = h.GetXaxis()
            yaxis = h.GetYaxis()
            for mg in d:
                ix = xaxis.FindBin(float(mg))
                for ml in d[mg]:
                    iy = yaxis.FindBin(float(ml))
                    assert h.GetBinContent(ix,iy)<0.000001
                    h.SetBinContent(ix,iy,d[mg][ml]["yield_"+b+"_"+r])

                


cnvs = [ ]
for h in histos:
    n = h.GetName()
    cn = "c_"+n
    cnvs.append(ROOT.TCanvas(cn,cn))
    h.Draw("zcol")
    cnvs[-1].SetLogz(1)
    cnvs[-1].Update()

if len(sys.argv)>2:
    tfout = ROOT.TFile(sys.argv[2],"recreate")
    for h in histos:
        h.Write()
    tfout.Close()
