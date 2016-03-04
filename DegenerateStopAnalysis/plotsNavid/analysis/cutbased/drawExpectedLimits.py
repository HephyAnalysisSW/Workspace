


import pickle
import os


limit_pickle = "./pkl/RunII_Reload_Scan_Limits_2260.pkl"

limits = pickle.load(open(limit_pickle, "r"))

xyz = []

for point in limits:
    if point in ['s30','s30FS','s10FS','s60FS','t2tt30FS']:
        continue
    masses = point.replace("Reload_Inc_T2_4bd","").replace("s","")
    mstop, mlsp = masses.rsplit("_")[:2]
    #xyz.append( [ float(mstop),float(mlsp),float( limits[point][1]['0.500'] ) ]  )
    #xyz.append( [ float(mstop),float(mlsp),float( limits[point]['0.500'] ) ]  )
    if limits[point]:
        xyz.append( [ int(mstop),int(mlsp),float( limits[point]['50.0'] ) ]  )
    #else:
    #    xyz.append( [ int(mstop),int(mlsp),float( -1 ) ]  )

import ROOT
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("0.2f")


plot = ROOT.TH2F("explim","expected limit", 24,100,700, 70,0,700 )





for x,y,z in xyz:
    plot.Fill(x,y,z)



plot.SetContour(2 )
plot.SetContourLevel(0,0 )
plot.SetContourLevel(1,1 )
plot.SetContourLevel(2,10 )



output_name = os.path.splitext(os.path.basename(limit_pickle))[0]+".png"

c1 = ROOT.TCanvas("c1","c1",1920,1080)
plot.Draw("COL TEXT")
c1.SaveAs("/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/mAODv2_7412pass2/reload_scan/%s"%output_name)

