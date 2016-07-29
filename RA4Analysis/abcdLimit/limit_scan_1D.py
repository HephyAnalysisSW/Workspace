import ROOT
import sys
import pickle
from xsecSMS import gluino13TeV_NLONLL,gluino13TeV_NLONLL_Up,gluino13TeV_NLONLL_Down
from array import array
from optparse import OptionParser

filename = ""

def toGraph1D(name,title,length,x,y):
    result = ROOT.TGraph(length)
    result.SetName(name)
    result.SetTitle(title)
    for i in range(length):
        result.SetPoint(i,x[i],y[i])
    return result

def toGraph2D(name,title,length,x,y,z):
    result = ROOT.TGraph2D(length)
    result.SetName(name)
    result.SetTitle(title)
    for i in range(length):
        result.SetPoint(i,x[i],y[i],z[i])
    h = result.GetHistogram()
    h.SetMinimum(min(z))
    h.SetMaximum(max(z))
    c = ROOT.TCanvas()
    result.Draw()
    del c
    return result

def toGraph(name,title,length,x,y):
    result = ROOT.TGraph(length)
    result.SetName(name)
    result.SetTitle(title)
    for i in range(length):
        result.SetPoint(i,x[i],y[i])
    return result

def SetupColors():
    num = 5
    bands = 255
    colors = [ ]
    stops = [0.00, 0.34, 0.61, 0.84, 1.00]
    red = [0.50, 0.50, 1.00, 1.00, 1.00]
    green = [0.50, 1.00, 1.00, 0.60, 0.50]
    blue = [1.00, 1.00, 0.50, 0.40, 0.50]
    arr_stops = array('d', stops)
    arr_red = array('d', red)
    arr_green = array('d', green)
    arr_blue = array('d', blue)
    # num = 6
    # red[num] =   {1.,0.,0.,0.,1.,1.}
    # green[num] = {0.,0.,1.,1.,1.,0.}
    # blue[num] =  {1.,1.,1.,0.,0.,0.}
    # stops[num] = {0.,0.2,0.4,0.6,0.8,1.}*/
    fi = ROOT.TColor.CreateGradientColorTable(num,arr_stops,arr_red,arr_green,arr_blue,bands)
    for i in range(bands):
        colors.append(fi+i)
    arr_colors = array('i', colors)
    ROOT.gStyle.SetNumberContours(bands)
    ROOT.gStyle.SetPalette(bands, arr_colors)


def DrawContours (g2, color, style, leg=None, name=None):
    
#    g2.Draw()
#    ROOT.gPad.Update()
    out = ROOT.TGraph()
    h = g2.GetHistogram()
    l = g2.GetContourList(1.)
    print g2.GetName(),l
    print g2.GetName(),l,l.GetSize()
    if not l:
        return out
    added = False
    max_points = -1
    for i in range(l.GetSize()):
        g = l.At(i)
        if not g:
            continue
        n_points = g.GetN()
        #if name=="Observed":
        #    print name,", graph ",i
        #    for j in range(n_points):
        #        print j,g.GetX()[j],g.GetY()[j]
        if n_points > max_points:
            out = g
            max_points = n_points
        g.SetLineColor(color)
        g.SetLineStyle(style)
        g.SetLineWidth(5)
#        g.Draw("L same")
        if ( not added ) and ( leg != None ) and ( name != None ):
            leg.AddEntry(g, name, "l")
            added = True
    return out


parser = OptionParser()
parser.add_option("-b", dest="batch", default=False, action="store_true")
parser.add_option("--mlsp", dest="mlsp", default=None, type="int")
parser.add_option("--mgluino", dest="mgluino", default=None, type="int")
(options, args) = parser.parse_args()

assert options.mlsp!=None or options.mgluino!=None
assert not ( options.mlsp!=None and options.mgluino!=None )

#SetupColors()

vmx = [ ]
vxsec = [ ]
vxsecup = [ ]
vxsecdown = [ ]
vobs = [ ]
vobsup = [ ]
vobsdown = [ ]
vexp = [ ]
vup = [ ]
vdown = [ ]

results = pickle.load(open(args[0],"rb"))
for mg in sorted(results.keys()):
    if options.mgluino!=None:
        if mg!=options.mgluino:
            continue
    else:
        pmx = float(mg)
    for ml in sorted(results[mg].keys()):
        if options.mlsp!=None:
            if ml!=options.mlsp:
                continue
        else:
            pmx = float(ml)
        pxsec = gluino13TeV_NLONLL[mg]
        pxsecup = gluino13TeV_NLONLL_Up[mg]
        pxsecdown = gluino13TeV_NLONLL_Down[mg]
        kobs = '-1.000'
        if not '-1.000' in results[mg][ml]:
            kobs = '0.500'
        pobs = results[mg][ml][kobs]
        pexp = results[mg][ml]['0.500']
        pup = results[mg][ml]['0.840']
        pdown = results[mg][ml]['0.160']
        vmx.append(pmx)
        vxsec.append(pxsec)
        vxsecup.append(pxsecup)
        vxsecdown.append(pxsecdown)
        vobs.append(pxsec*pobs)
        vexp.append(pxsec*pexp)
        vup.append(pxsec*pup)
        vdown.append(pxsec*pdown)

print len(vmx)
print vmx
assert len(vmx) > 2
assert not ( len(vmx) != len(vxsec) \
                 or len(vmx) != len(vobs) \
                 or len(vmx) != len(vexp) \
                 or len(vmx) != len(vup) \
                 or len(vmx) != len(vdown) ) 
  
  
vlim = [ ]
for i in range(len(vxsec)):
    vlim.append(vxsec[i]*vobs[i])

gxsec = toGraph1D("gxsec", "Cross section", len(vlim), vmx, vxsec)
gxsecup = toGraph1D("gxsecup", "Cross section", len(vlim), vmx, vxsecup)
gxsecdown = toGraph1D("gxsecdown", "Cross section", len(vlim), vmx, vxsecdown)
glim = toGraph1D("glim", "Cross-Section Limit", len(vlim), vmx, vlim)
gobs = toGraph1D("gobs", "Observed Limit", len(vobs), vmx, vobs)
gexp = toGraph1D("gexp", "Expected Limit", len(vexp), vmx, vexp)
gup = toGraph1D("gup", "Expected +1#sigma Limit", len(vup), vmx, vup)
gdown = toGraph1D("gdown", "Expected -1#sigma Limit", len(vdown), vmx, vdown)

xmin = min(vmx)
xmax = max(vmx)
ymax = max(vlim+vobs+vobsup+vobsdown+vexp+vup+vdown)
bin_size = 12.5
nxbins = max(1, min(500, int((xmax-xmin+bin_size/100.)/bin_size)))
cnv = ROOT.TCanvas()
frame = cnv.DrawFrame(xmin-12.5,2*ymax/1000.,xmax+12.5,2*ymax)
if options.mgluino!=None:
    frame.SetTitle(";m_{gluino} [GeV];95% CL uppder limit [pb]")
else:
    frame.SetTitle(";m_{LSP} [GeV];95% CL uppder limit [pb]")
cnv.SetLogy(1)


l = ROOT.TLegend(ROOT.gStyle.GetPadLeftMargin(), 1.-ROOT.gStyle.GetPadTopMargin(), \
                     1.-ROOT.gStyle.GetPadRightMargin(), 1.)
gup.SetLineColor(2)
gup.SetLineStyle(2)
gup.Draw("PL")
gdown.SetLineColor(2)
gdown.SetLineStyle(2)
gdown.Draw("PL")
gexp.SetLineColor(2)
gexp.SetLineStyle(1)
gexp.Draw("PL")

gxsecup.SetLineColor(4)
gxsecup.SetLineStyle(2)
gxsecup.Draw("PL")
gxsecdown.SetLineColor(4)
gxsecdown.SetLineStyle(2)
gxsecdown.Draw("PL")
gxsec.SetLineColor(4)
gxsec.SetLineStyle(1)
gxsec.Draw("PL")

gobs.SetLineWidth(3)
gobs.SetLineStyle(1)
gobs.Draw("PL")

cnv.Update()
if not options.batch:
    raw_input("Enter")
l.SetNColumns(2)
l.SetBorderSize(0)
l.Draw("same")
#c.Print("limit_scan.pdf")
#if len(args)>1:
#    c.Print(args[1]+".png")

#if len(args)>1:
#    tfile = ROOT.TFile(args[1]+".root","recreate")
#    hlim.Write("hXsec_exp_corr")
#    cobs.Write("graph_smoothed_Obs")
#    cobsup.Write("graph_smoothed_ObsP")
#    cobsdown.Write("graph_smoothed_ObsM")
#    cexp.Write("graph_smoothed_Exp")
#    cup.Write("graph_smoothed_ExpP")
#    cdown.Write("graph_smoothed_ExpM")
#    tfile.Close()

  
