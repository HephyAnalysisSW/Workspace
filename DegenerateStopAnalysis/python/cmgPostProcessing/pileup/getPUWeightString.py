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

vtxPUweight = lambda l,h,w : "(%s * %s )"%(w, btw("nTrueInt",l,h))

pu_hist_file_up      = "PU_ratio_66150.root"
pu_hist_file_central = "PU_ratio_63000.root"
pu_hist_file_down    = "PU_ratio_59850.root"



pu_hist_up     = ROOT.TFile(pu_hist_file_up)
puweights_up   = [ [pu_hist_up.PU_ratio.GetBinLowEdge(i), pu_hist_up.PU_ratio.GetBinLowEdge(i+1), x] for i,x in enumerate(pu_hist_up.PU_ratio) if x]
puW_up =  ' + '.join( [ vtxPUweight(l,h,w) for l,h,w in puweights_up] )


pu_hist_central     = ROOT.TFile(pu_hist_file_central)
puweights_central   = [ [pu_hist_central.PU_ratio.GetBinLowEdge(i), pu_hist_central.PU_ratio.GetBinLowEdge(i+1), x] for i,x in enumerate(pu_hist_central.PU_ratio) if x]
puW_central =  ' + '.join( [ vtxPUweight(l,h,w) for l,h,w in puweights_central] )


pu_hist_down     = ROOT.TFile(pu_hist_file_down)
puweights_down   = [ [pu_hist_down.PU_ratio.GetBinLowEdge(i), pu_hist_down.PU_ratio.GetBinLowEdge(i+1), x] for i,x in enumerate(pu_hist_down.PU_ratio) if x]
puW_down =  ' + '.join( [ vtxPUweight(l,h,w) for l,h,w in puweights_down] )


print "puW_up       =   '%s'"%puW_up
print "puW_down     =   '%s'"%puW_down
print "puW_central  =   '%s'"%puW_central

