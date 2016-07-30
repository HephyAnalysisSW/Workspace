import ROOT




def btw(var,minVal,maxVal, rangeLimit=[0,1] ):
    greaterOpp = ">"
    lessOpp = "<"
    vals = [minVal, maxVal]
    minVal = min(vals)
    maxVal = max(vals)
    if rangeLimit[0]:
        greaterOpp += "="
    if rangeLimit[1]:
        lessOpp += "="
    return "(%s)"%" ".join(["%s"%x for x in [var,greaterOpp,minVal, "&&", var, lessOpp, maxVal ]])


pu_hist_file = "PU_ratio_central.root"

pu_hist     = ROOT.TFile(pu_hist_file)
puweights   = [ [pu_hist.h_ratio.GetBinLowEdge(i), pu_hist.h_ratio.GetBinLowEdge(i+1), x] for i,x in enumerate(pu_hist.h_ratio) if x]

vtxPUweight = lambda l,h,w : "(%s * %s )"%(w, btw("nTrueInt",l,h))
print ' + '.join( [ vtxPUweight(l,h,w) for l,h,w in puweights] )







