

import ROOT
import sys

xsec_dir = "/afs/cern.ch/user/a/amete/public/EWKGauginoCrossSections_13TeV/"

multiplier = 1.e-3
model_template="{grid}_{comp}_13TeV.root"


def getGauginoXSec( grid, comp, *input_mass ):
    input_mass = input_mass[0] #if len(input_mass)>1 else input_mass

    tfile_path = xsec_dir + model_template.format( grid=grid , comp=comp )
    
    tfile = ROOT.TFile( tfile_path ) 
    
    nFits = tfile.Get("nFits").GetVal()
    
    for i in range(nFits):
        fit_nom = tfile.Get("fit_nom_%s"%i)
        fit_up  = tfile.Get("fit_up_%s"%i)
        fit_dn  = tfile.Get("fit_dn_%s"%i)
    
    
        min_mass, max_mass = map( float, fit_nom.GetTitle().rsplit("_")[2:] )
    
        if input_mass >= min_mass and input_mass < max_mass:
            xsec_nom = fit_nom.Eval( input_mass )
            xsec_up = fit_up.Eval( input_mass ) 
            xsec_dn = fit_dn.Eval( input_mass )
    
            #xsec_unc = xsec_up - xsec_nom if xsec_up-xsec_nom > xsec_nom - xsec_dn else xsec_nom-xsec_dn
            xsec_unc = max( xsec_up-xsec_nom, xsec_nom - xsec_dn )
            break
        else:
            continue
        raise Exception( "Mass %s was not found in any of the fits!" )
    
    output = [xsec_nom*multiplier , xsec_unc/xsec_nom]
    output = [round(x,7) for x in output]
    print "Cross-section for mass %s [GeV] is %s [pb] +/- %s [rel.]"%(input_mass, output[0], output[1])

    return output


higgsino_tfile = ROOT.TFile("/afs/hephy.at/work/n/nrad/CMSSW/CMSSW_8_0_20/src/Workspace/DegenerateStopAnalysis/data/xsecs/higgsino_pMSSM.root")
higgsino_xsecs_incl = higgsino_tfile.Get("output80_higgsino").Get("final-try09").Get("xs13_incl")

def getHiggsinoXSec( mu,m1 ):
    xsec = higgsino_xsecs_incl.GetBinContent(higgsino_xsecs_incl.FindBin(mu,m1))
    print "Cross-section for mu %s [GeV] and M1 %s [GeV] is %s [pb] "%( mu, m1, xsec*multiplier)
    return (xsec*multiplier,)

if __name__ == "__main__":
    grid, comp, mass = sys.argv[-3:]
    getGauginoXSec( grid, comp, mass ) 
