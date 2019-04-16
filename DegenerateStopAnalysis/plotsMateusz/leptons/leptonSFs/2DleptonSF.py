import ROOT
import os, sys
import array

ROOT.gStyle.SetOptStat(0) #1111 adds histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis

inputFileName = "hephy_scale_factors"
if len(sys.argv)>1: inputFileName = sys.argv[1]
inputFile = "results/final/%s.root"%inputFileName
if not os.path.isfile(inputFile):
    print "input file %s does not exist"%inputFile
    sys.exit()

flavor = "ele"
if len(sys.argv)>2: flavor = sys.argv[2]
if flavor != "muon" and flavor != "ele":
    print "wrong flavor"
    sys.exit()

stage = "Id"
if len(sys.argv)>3: stage = sys.argv[3]
if stage != "IpIso" and stage != "Id" and stage != "IdSpec":
    print "wrong stage"
    sys.exit()

suffix = "_%s_%s_%s"%(inputFileName, flavor, stage)

f = ROOT.TFile(inputFile, "update")

h = {}
for etabin in ['barrel', 'endcap']:
    h[etabin] = f.Get("%s_SF_%s_%s"%(flavor,stage,etabin))

def makeDir(path):
    if "." in path[-5:]:
        path = path.replace(os.path.basename(path),"")
    if os.path.isdir(path):
        return
    else:
        os.makedirs(path)

# get binning
nx = h['barrel'].GetNbinsX()
ptbins = h['barrel'].GetXaxis().GetXbins().GetArray()
etabins = array.array("d", [0., 1.442, 1.566, 2.5])

# 2D SF plot
histName = "%s_SF_%s_2D"%(flavor,stage)
SF = ROOT.TH2F(histName, histName, nx, ptbins, len(etabins)-1, etabins)
SF.SetTitle(histName)
SF.GetXaxis().SetTitle("p_{T} (GeV)")
SF.GetYaxis().SetTitle("|#eta|")
SF.GetZaxis().SetTitle("SF")
SF.GetXaxis().SetTitleOffset(1.2)
SF.GetYaxis().SetTitleOffset(1.2)
SF.GetZaxis().SetTitleOffset(1.2)
SF.GetZaxis().SetRangeUser(0.8,1)
SF.SetMarkerSize(1.5)

for i in range(nx):
    i+=1   

    SF.SetBinContent(i, 1, h['barrel'].GetBinContent(i))
    SF.SetBinError(i,   1, h['barrel'].GetBinError(i))
    
    SF.SetBinContent(i, 3, h['endcap'].GetBinContent(i))
    SF.SetBinError(i,   3, h['endcap'].GetBinError(i))

c = ROOT.TCanvas("c", "Canvas", 1800, 1500)
ROOT.gStyle.SetPalette(1)
SF.Draw("COLZ TEXT89E") #CONT1-5 #plots the graph with axes and points

#if logy: ROOT.gPad.SetLogz()
c.Modified()
c.Update()

#Save canvas
savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/TnP/final/2016_80X_v5/2DleptonSF"
makeDir(savedir + '/root')
makeDir(savedir + '/pdf')

c.SaveAs("%s/2DleptonSF%s.png"      %(savedir, suffix))
c.SaveAs("%s/pdf/2DleptonSF%s.pdf"  %(savedir, suffix))
c.SaveAs("%s/root/2DleptonSF%s.root"%(savedir, suffix))

# adds histogram to original file
f.Write(histName, ROOT.TObject.kOverwrite)
f.Close()
