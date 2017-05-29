import sys
from inputFile import *
from smsPlotXSEC import *
from smsPlotCONT import *
from smsPlotBrazil import *

if __name__ == '__main__':
    # read input arguments
    filename = sys.argv[1]
#    modelname = sys.argv[1].split("/")[-1].split("_")[0]
#    analysisLabel = sys.argv[1].split("/")[-1].split("_")[1]
    analysisLabel = "1L"
    outputname = sys.argv[2]

    try:
        modelname = sys.argv[3]
    except:
        modelname = "T2DegStop"

    # read the config file
    fileIN = inputFile(filename)
    
    # classic temperature histogra
    xsecPlot = smsPlotXSEC(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "", fileIN.ANALYSIS)
    xsecPlot.Draw()
    xsecPlot.Save("%sXSEC" %outputname)
#    sys.exit(0)

    # only lines
    contPlot = smsPlotCONT(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "", fileIN.ANALYSIS)
    contPlot.Draw()
    contPlot.Save("%sCONT" %outputname)

    # brazilian flag (show only 1 sigma)
    brazilPlot = smsPlotBrazil(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "", fileIN.ANALYSIS)
    brazilPlot.Draw()
    brazilPlot.Save("%sBAND" %outputname)
