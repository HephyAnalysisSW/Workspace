#
# create canvases from UCSB PDF uncertainties
#
#sms = "T1tttt-madgraph"
#sms = "T5tttt"
sms = "T1t1t"
model = sms
if model.find("-")>=0:
    model = model[:model.find("-")]
print model

smsPrefix={}
#smsPrefix["T1tttt"] = ""
smsPrefix["T1tttt-madgraph"] = "T1tttt-madgraph_"
smsPrefix["T1t1t"] = "T1t1t_"
smsPrefix["T5tttt"] = "T5tttt_"

smoothingPostFixPDF = {}
#smoothingPostFixPDF["T1tttt"] = "_smoothed"
smoothingPostFixPDF["T1tttt-madgraph"] = ""
smoothingPostFixPDF["T1t1t"] = ""
smoothingPostFixPDF["T5tttt"] = ""

import os,sys
path = os.path.abspath('../plots')
if not path in sys.path:
    sys.path.insert(1, path)
del path

from smsInfo import th2Binning
thisBinning = th2Binning[sms]
nbx = thisBinning[0]
xmin = float(thisBinning[1])
xmax = float(thisBinning[2])
nby = thisBinning[3]
ymin = float(thisBinning[4])
ymax = float(thisBinning[5])

htb = ( 750, 2500 )
metbins = [(250,350),(350,450),(450,2500)]
metbins3b = [(150,250),(250,350),(350,450),(450,2500)]
lowHTBin = (400, 750)
lowHTmetbins = [(150,250),(250,2500)]

import ROOT
if sms=="T1tttt-madgraph" or sms=="T1t1t":
    ROOT.gROOT.ProcessLine(".L pdf"+model+".C+")

pdfMETbin1 = ROOT.Double(0.)
pdfMETbin2 = ROOT.Double(0.)
pdfMETbin3 = ROOT.Double(0.)
h_2b_sys = { }
h_3b_sys = { }
h_3b_lowHT_sys = { }
for metb in metbins:
    h_2b_sys[metb] = ROOT.TH2D("h_2b_sys_"+str(metb[0])+"_"+str(metb[1]),
                               "h_2b_sys_"+str(metb[0])+"_"+str(metb[1]),
                               nbx,xmin,xmax,nby,ymin,ymax)
for metb in metbins3b:
    h_3b_sys[metb] = ROOT.TH2D("h_3b_sys_"+str(metb[0])+"_"+str(metb[1]),
                               "h_3b_sys_"+str(metb[0])+"_"+str(metb[1]),
                               nbx,xmin,xmax,nby,ymin,ymax)
for metb in lowHTmetbins:
    h_3b_lowHT_sys[metb] = ROOT.TH2D("h_3b_lowHT_sys_"+str(metb[0])+"_"+str(metb[1]),
                                     "h_3b_lowHT_sys_"+str(metb[0])+"_"+str(metb[1]),
                                     nbx,xmin,xmax,nby,ymin,ymax)

dx = (xmax-xmin)/nbx
dy = (ymax-ymin)/nby
for ix in range(nbx):
    x = xmin + (ix+0.5)*dx
    for iy in range(nby):
        y = ymin + (iy+0.5)*dy
        if (y+1)>x:  continue

        if sms=="T1tttt-madgraph":
            ROOT.pdfT1tttt(htb[0],x,y,pdfMETbin1,pdfMETbin2,pdfMETbin3)
        elif sms=="T1t1t":
            ROOT.pdfT1t1t(htb[0],x,y,pdfMETbin1,pdfMETbin2,pdfMETbin3)
        elif sms=="T5tttt":
            pdfMETbin1 = 0.20
            pdfMETbin2 = 0.20
            pdfMETbin3 = 0.20
        h_2b_sys[(250,350)].SetBinContent(ix+1,iy+1,pdfMETbin1)
        h_2b_sys[(350,450)].SetBinContent(ix+1,iy+1,pdfMETbin2)
        h_2b_sys[(450,2500)].SetBinContent(ix+1,iy+1,pdfMETbin3)

        h_3b_sys[(150,250)].SetBinContent(ix+1,iy+1,pdfMETbin1)
        h_3b_sys[(250,350)].SetBinContent(ix+1,iy+1,pdfMETbin1)
        h_3b_sys[(350,450)].SetBinContent(ix+1,iy+1,pdfMETbin2)
        h_3b_sys[(450,2500)].SetBinContent(ix+1,iy+1,pdfMETbin3)

        if sms=="T1tttt-madgraph":
            ROOT.pdfT1tttt(500,x,y,pdfMETbin1,pdfMETbin2,pdfMETbin3)
        elif sms=="T1t1t":
            ROOT.pdfT1t1t(500,x,y,pdfMETbin1,pdfMETbin2,pdfMETbin3)
        elif sms=="T5tttt":
            pdfMETbin1 = 0.20
            pdfMETbin2 = 0.20
            pdfMETbin3 = 0.20
        h_3b_lowHT_sys[lowHTmetbins[0]].SetBinContent(ix+1,iy+1,pdfMETbin1)
        pdfMET = pdfMETbin1
        if pdfMETbin2>pdfMET:  pdfMET = pdfMETbin2
        if pdfMETbin3>pdfMET:  pdfMET = pdfMETbin3
        h_3b_lowHT_sys[lowHTmetbins[1]].SetBinContent(ix+1,iy+1,pdfMET)

c_2b_sys = { }
c_3b_sys = { }
c_3b_lowHT_sys = { }
for metb in metbins:
    c_2b_sys[metb] = ROOT.TCanvas("c_2b_sys_"+str(metb[0])+"_"+str(metb[1]),
                                  "c_2b_sys_"+str(metb[0])+"_"+str(metb[1]),600,600)
    h_2b_sys[metb].Draw("zcol")
for metb in metbins3b:
    c_3b_sys[metb] = ROOT.TCanvas("c_3b_sys"+str(metb[0])+"_"+str(metb[1]),
                                  "c_3b_sys"+str(metb[0])+"_"+str(metb[1]),600,600)
    h_3b_sys[metb].Draw("zcol")
for metb in lowHTmetbins:
    c_3b_lowHT_sys[metb] = ROOT.TCanvas("c_3b_lowHT_sys"+str(metb[0])+"_"+str(metb[1]),
                                        "c_3b_lowHT_sys"+str(metb[0])+"_"+str(metb[1]),600,600)
    h_3b_lowHT_sys[metb].Draw("zcol")

#    fn_3b_sys = 'sigPDFSys_'+smsPrefix[sms]+'btb3b_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixPDF[sms]+'.root'
#    fn_3b_lowHT_sys = 'sigPDFSys_'+smsPrefix[sms]+'btb3p_ht_'+str(lowHTBin[0])+'_'+str(lowHTBin[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixPDF[sms]+'.root'

raw_input("Press")

outdir = '/data/adamwo/results2012/'+sms+'/PDF/'
for metb in metbins:
    fn = 'sigPDFSys_'+smsPrefix[sms]+'btb2_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixPDF[sms]+'.root'
    c = ROOT.TCanvas("c1","c1",600,600)
    h = h_2b_sys[metb].Clone("hist2DSFunc")
    h.Draw("zcol")
    c.SaveAs(outdir+fn)
    del c

for metb in metbins3b:
    fn = 'sigPDFSys_'+smsPrefix[sms]+'btb3p_ht_'+str(htb[0])+'_'+str(htb[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixPDF[sms]+'.root'
    c = ROOT.TCanvas("c1","c1",600,600)
    h = h_3b_sys[metb].Clone("hist2DSFunc")
    h.Draw("zcol")
    c.SaveAs(outdir+fn)
    del c

for metb in lowHTmetbins:
    fn = 'sigPDFSys_'+smsPrefix[sms]+'btb3p_ht_'+str(lowHTBin[0])+'_'+str(lowHTBin[1])+'_met_'+str(metb[0])+'_'+str(metb[1])+smoothingPostFixPDF[sms]+'.root'
    c = ROOT.TCanvas("c1","c1",600,600)
    h = h_3b_lowHT_sys[metb].Clone("hist2DSFunc")
    h.Draw("zcol")
    c.SaveAs(outdir+fn)
    del c
