import ROOT
import pickle
import sys




def findRange(values):
    vmin = None
    vmax = None
    dvmin = None
    vprev = None
    for v in sorted(list(values)):
        if vmin==None or v<vmin:
            vmin = v
        if vmax==None or v>vmax:
            vmax = v
        if vprev!=None:
            dv = abs(v-vprev)
            if dv>0 and ( dvmin==None or dv<dvmin ):
                dvmin = dv
        vprev = v
    return vmin,vmax,dvmin


def pklToHistos( input_pkl, output_file = "test.root"):
    labels = { '0.500' : 'exp', '-1.000' : 'obs', \
                   '0.840' : 'expM1', '0.160' : 'expP1', \
                   '0.975' : 'expM2', '0.025' : 'expP2' }
    
    #d = pickle.load(file("/afs/hephy.at/user/n/nrad/public/CRSystFix_v0/Limits/Full_Limits.pkl"))
    #d = pickle.load(file("/afs/hephy.at/work/m/mzarucki/results/cards_and_limits/8012_mAODv2_v3/80X_postProcessing_v10/13TeV/HT/ApprovalSys_Mt95_Inccharge_LepAll_lep_pu_SF/AdjustedSys/presel/BinsSummary/CRSystFix_v0/Full_Limits.pkl"))
    d = pickle.load(file( input_pkl ) )
    xs = set()
    ys = set()
    ds = set()
    for x in d:
        if x>801:
            continue
        xs.add(x)
        for y in d[x]:
            ys.add(y)
            ds.add(y-x)
            print x,y
    
    xmin,xmax,dxmin = findRange(xs)
    ymin,ymax,dymin = findRange(ys)
    dmin,dmax,ddmin = findRange(ds)
    print xmin,xmax,dxmin
    print dmin,dmax,ddmin
     
    xmin = xmin - dxmin/2.
    xmax = xmax + dxmin/2.
    nbx = int((xmax-xmin+dxmin/2.)/dxmin)
    ymin = ymin - dymin/2.
    ymax = ymax + dymin/2.
    nby = int((ymax-ymin+dymin/2.)/dymin)
    
    fout = ROOT.TFile( output_file,"recreate")
    histos = { }
    xaxis = None
    yaxis = None
    for v,l in labels.iteritems():
        histos[l] = ROOT.TH2F(l,l,nbx,xmin,xmax,nby,ymin,ymax)
        if xaxis==None:
            xaxis = histos[l].GetXaxis()
            yaxis = histos[l].GetYaxis()
    
    
    for x in d:
        if x>xmax:
            continue
        ix = xaxis.FindBin(x)
        for y in d[x]:
            iy = yaxis.FindBin(y)
            for k in d[x][y]:
                if k in labels:
                    histos[labels[k]].SetBinContent(ix,iy,d[x][y][k])
    fout.Write()
    print "Histogram read from: \n %s and written to: \n %s"%( input_pkl, output_file) 
    return histos 


if __name__ == '__main__':

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--input", dest="input_pkl",
                  help="path to the input pickle file containing the limit results" )
    parser.add_option("--output", dest="output_file", default="test.root",
                  help="path to the output root file" )
    (options,args) = parser.parse_args()
    output_script_name = options.output_script_name

    histos = pklToHistos( options.input_pkl, options.output_file) 
    
    #print d[775][705].keys()
    
    #print xmin,xmax,dxmin
    #print ymin,ymax,dymin       
    #print d.keys()
    #print d[d.keys()[0]].keys()
