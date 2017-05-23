import ROOT
import sys
import pickle
from xsecSMS import gluino13TeV_NLONLL,gluino13TeV_NLONLL_Up,gluino13TeV_NLONLL_Down
from array import array
from optparse import OptionParser

filename = ""

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
(options, args) = parser.parse_args()

#SetupColors()

vmx = [ ]
vmy = [ ]
vxsec = [ ]
vobs = [ ]
vobsup = [ ]
vobsdown = [ ]
vexp = [ ]
vup = [ ]
vdown = [ ]

results = pickle.load(open(args[0],"rb"))
for mg in results:
    pmx = float(mg)
    for ml in results[mg]:
        print mg , ml
        pmy = float(ml)

        pxsec = gluino13TeV_NLONLL[mg]
        kobs = '-1.000'
        if not '-1.000' in results[mg][ml]:
            kobs = '0.500'
        if len(results[mg][ml].keys())<3: continue
        pobs = results[mg][ml][kobs]
        pobsup = pobs * pxsec/gluino13TeV_NLONLL_Up[mg]
        pobsdown = pobs * pxsec/gluino13TeV_NLONLL_Down[mg]
        pexp = results[mg][ml]['0.500']
        pup = results[mg][ml]['0.840']
        pdown = results[mg][ml]['0.160']
        ## **** temporary !!! ***
        #if mg<=900 and ml<=400:
        #    print "*** removing point"
        #    pxsec = 1.
        #    pobs = 0.000001
        #    pobsup = 0.000001
        #    pobsdown = 0.000001
        #    pexp = 0.000001
        #    pup = 0.000001
        #    pdown = 0.000001
        vmx.append(pmx)
        vmy.append(pmy)
        vxsec.append(pxsec)
        vobs.append(pobs)
        vobsup.append(pobsup)
        vobsdown.append(pobsdown)
        vexp.append(pexp)
        vup.append(pup)
        vdown.append(pdown)
#print "vmx" , vmx
print len(vmx)
assert len(vmx) > 2
assert not ( len(vmx) != len(vmy) \
                 or len(vmx) != len(vxsec) \
                 or len(vmx) != len(vobs) \
                 or len(vmx) != len(vobsup) \
                 or len(vmx) != len(vobsdown) \
                 or len(vmx) != len(vexp) \
                 or len(vmx) != len(vup) \
                 or len(vmx) != len(vdown) ) 
  
vlim = [ ]
for i in range(len(vxsec)):
    vlim.append(vxsec[i]*vobs[i])

glim = toGraph2D("glim", "Cross-Section Limit", len(vlim), vmx, vmy, vlim)
gobs = toGraph2D("gobs", "Observed Limit", len(vobs), vmx, vmy, vobs)
gobsup = toGraph2D("gobsup", "Observed +1#sigma Limit", len(vobsup), vmx, vmy, vobsup)
gobsdown = toGraph2D("gobsdown", "Observed -1#sigma Limit", len(vobsdown), vmx, vmy, vobsdown)
gexp = toGraph2D("gexp", "Expected Limit", len(vexp), vmx, vmy, vexp)
gup = toGraph2D("gup", "Expected +1#sigma Limit", len(vup), vmx, vmy, vup)
gdown = toGraph2D("gdown", "Expected -1#sigma Limit", len(vdown), vmx, vmy, vdown)
dots = toGraph("dots","dots",len(vmx), vmx, vmy)



#can = ROOT.TCanvas("c","c",800,800)
contor = DrawContours(gexp, 2, 1, "Expected")
tfilem = ROOT.TFile(args[1]+".root","recreate")
contor.Write("graph_smoothed_Exp")
tfilem.Close()
#contor.Draw()
#if len(args)>1:
#    can.Print(args[1]+"expected.png")
#    can.Print(args[1]+"expected.pdf")
#    can.Print(args[1]+"expected.root")


xmin = min(vmx)
xmax = max(vmx)
ymin = min(vmy)
ymax = max(vmy)
bin_size = 12.5
nxbins = max(1, min(500, int((xmax-xmin+bin_size/100.)/bin_size)))
nybins = max(1, min(500, int((ymax-ymin+bin_size/100.)/bin_size)))
glim.SetNpx(nxbins)
glim.SetNpy(nybins)

#hobs = gobs.GetHistogram()
hlim = glim.GetHistogram()
assert hlim
hlim.SetTitle(";m_{gluino} [GeV];m_{LSP} [GeV]")

l = ROOT.TLegend(ROOT.gStyle.GetPadLeftMargin(), 1.-ROOT.gStyle.GetPadTopMargin(), \
                     1.-ROOT.gStyle.GetPadRightMargin(), 1.)
cup = DrawContours(gup, 2, 2)
cdown = DrawContours(gdown, 2, 2)
cexp = DrawContours(gexp, 2, 1, l, "Expected")
cobsup = DrawContours(gobsup, 1, 2)
cobsdown = DrawContours(gobsdown, 1, 2)
cobs = DrawContours(gobs, 1, 1, l, "Observed")
print "contours are drawn"
c = ROOT.TCanvas("c","c",800,800)
c.SetLogz()
#hobs.SetMinimum(min(vlim))
#hobs.SetMaximum(max(vlim))
hlim.SetMinimum(min(vlim))
hlim.SetMaximum(max(vlim))
# *** temporary
hlim.SetMaximum(1000*min(vlim))
#hlim.Draw()
#c.Update()
#raw_input(" ")
glim.Draw("colz")
#gobs.Draw("colz")
cobs.Draw("L same")
cobsup.Draw("L same")
cobsdown.Draw("L same")
cexp.Draw("L same")
cup.Draw("L same")
cdown.Draw("L same")
c.Update()
if not options.batch:
    raw_input("Enter")
l.SetNColumns(2)
l.SetBorderSize(0)
l.Draw("same")
dots.Draw("p same")
#c.Print("limit_scan.pdf")
print args[1]
if len(args)>1:
    c.Print(args[1]+".png")
    c.Print(args[1]+".pdf")
    c.Print(args[1]+".root")

if len(args)>1:
    tfile = ROOT.TFile(args[1]+".root","recreate")
    hlim1 = ROOT.TH2F("hlim1","hlim1", \
                          hlim.GetNbinsX(),hlim.GetXaxis().GetXmin(),hlim.GetXaxis().GetXmax(),
                          hlim.GetNbinsY(),hlim.GetYaxis().GetXmin(),hlim.GetYaxis().GetXmax())
    for ix in range(hlim.GetNbinsX()):
        for iy in range(hlim.GetNbinsY()):
            v = hlim.GetBinContent(ix+1,iy+1)
            print "v" , v
            if v>1.e-10:
                hlim1.SetBinContent(ix+1,iy+1,v)
    hlim1.Write("hXsec_exp_corr")
    cobs.Write("graph_smoothed_Obs")
    cobsup.Write("graph_smoothed_ObsP")
    cobsdown.Write("graph_smoothed_ObsM")
    cexp.Write("graph_smoothed_Exp")
    cup.Write("graph_smoothed_ExpP")
    cdown.Write("graph_smoothed_ExpM")
    tfile.Close()

  
