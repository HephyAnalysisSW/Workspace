import ROOT
import sys
import pickle
from array import array

filename = ""

def toGraph2D(name,title,length,x,y,z):
    """ convert lists of x, y, z values to 2D graph
    """
    result = ROOT.TGraph2D(length)
    result.SetName(name)
    result.SetTitle(title)
    for i in range(length):
        result.SetPoint(i,x[i],y[i],z[i])
    h = result.GetHistogram()
    h.SetMinimum(min(z))
    h.SetMaximum(max(z))
    #c = ROOT.TCanvas()
    #result.Draw()
    #del c
    return result

def SetupColors():
    """ Color scheme inherited from original RA4+MJ limit_scan script
    """
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


#
# read dictionary from pickle file
#   assume first keys are mglu and mlsp
#
results = pickle.load(open(sys.argv[1],"rb"))
#
# fill graph
#
vmx = [ ]
vmy = [ ]
vz = [ ]
for mg in results:
    # x = mgluino
    pmx = float(mg)
    for ml in results[mg]:
        # y = mLSP
        pmy = float(ml)
        # z = ?? (insert key)
        pz = results[mg][ml][key_to_be_entered]
        # fill lists
        vmx.append(pmx)
        vmy.append(pmy)
        vz.append(pz)
#
# check lengths for consistency
#
assert len(vmx) > 2
assert not ( len(vmx) != len(vmy) \
                 or len(vmx) != len(vz)     
# convert to graph
gz = toGraph2D("gz", "values", len(vz), vmx, vmy, vz)
# define histogram bins
xmin = min(vmx)
xmax = max(vmx)
ymin = min(vmy)
ymax = max(vmy)
bin_size = 12.5
nxbins = max(1, min(500, int((xmax-xmin+bin_size/100.)/bin_size)))
nybins = max(1, min(500, int((ymax-ymin+bin_size/100.)/bin_size)))
gz.SetNpx(nxbins)
gz.SetNpy(nybins)
# convert graph to histogram
hz = gz.GetHistogram()
assert hz
hz.SetTitle(";m_{gluino} [GeV];m_{LSP} [GeV]")
# plot graph
c = ROOT.TCanvas("c","c",800,800)
c.SetLogz()
hz.SetMinimum(min(vz))
hz.SetMaximum(max(vz))
gz.Draw("colz")
c.Print("draw_signal_scan.png")

