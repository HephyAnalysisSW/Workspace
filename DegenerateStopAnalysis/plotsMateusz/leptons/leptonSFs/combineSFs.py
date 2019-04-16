import ROOT
import os, sys
import array
import pprint

ROOT.gStyle.SetOptStat(0) #1111 adds histogram statistics box #Name, Entries, Mean, RMS, Underflow, Overflow, Integral, Skewness, Kurtosis


def makeDir(path):
    if "." in path[-5:]:
        path = path.replace(os.path.basename(path),"")
    if os.path.isdir(path):
        return
    else:
        os.makedirs(path)

def combineSFs(baseHistName, updateHistName, updatePtRange, file_dir = './', savedir = './', drawOriginalSFs = False, verbose = False):

    leptonSFsDict = {
        # muons
        "mu_LooseWP_2D_cent":{"tag":'LooseWP_cent', "hist_name":'SF',                             "file_name":'TnP_NUM_LooseID_DENOM_generalTracks_VAR_map_pt_eta.root', "lep":'mu', 'dim':'2D'},
        "mu_LooseWP_1D_priv":{"tag":'LooseWP_priv', "hist_name":'muon_SF_Id_all',                 "file_name":'hephy_scale_factors.root',                                "lep":'mu', 'dim':'1D'},
        "mu_IpIso_1D_priv":  {"tag":'IpIso_priv',   "hist_name":'muon_SF_IpIsoSpec_all',          "file_name":'hephy_scale_factors.root',                                "lep":'mu', 'dim':'1D'},
        
        # electrons
        "el_VetoWP_2D_cent": {"tag":'VetoWP_cent',  "hist_name":'GsfElectronToCutBasedSpring15V', "file_name":'scaleFactors.root',                                       "lep":'el', 'dim':'2D'},
        "el_VetoWP_2D_priv": {"tag":'VetoWP_priv',  "hist_name":'ele_SF_IdSpec_2D',               "file_name":'hephy_scale_factors.root',                                "lep":'el', 'dim':'2D'},
        "el_IpIso_2D_priv":  {"tag":'IpIso_priv',   "hist_name":'ele_SF_IpIso_2D',                "file_name":'hephy_scale_factors.root',                                "lep":'el', 'dim':'2D'},
    }
    
    for histName in [baseHistName, updateHistName]:
        if histName not in leptonSFsDict:
            print "%s not in leptonSFsDict. Fix name or update dictionary. Exiting."%histName
            sys.exit()
    
    baseHistDict   = leptonSFsDict[baseHistName]
    updateHistDict = leptonSFsDict[updateHistName]
    
    if baseHistDict['lep'] != updateHistDict['lep']:
        print "Trying to combine SFs between %s and %s. Exiting."%(baseHistDict['lep'], updateHistDict['lep'])
        sys.exit() 
    
    selectedHistDict = {
        baseHistName:baseHistDict,
        updateHistName:updateHistDict
    }
    
    for hist in selectedHistDict:
        selectedHistDict[hist]['file'] = ROOT.TFile(file_dir + selectedHistDict[hist]['file_name'])

        if selectedHistDict[hist]['hist_name'] not in [x.GetName() for x in selectedHistDict[hist]['file'].GetListOfKeys()]:
            print "Histogram %s not found in file %s. Exiting."%(selectedHistDict[hist]['hist_name'], selectedHistDict[hist]['file_name'])
            sys.exit()

        selectedHistDict[hist]['hist'] = selectedHistDict[hist]['file'].Get(selectedHistDict[hist]['hist_name'])
    
        selectedHistDict[hist]['binning'] = {'nx':selectedHistDict[hist]['hist'].GetNbinsX(), 'xbins':list(selectedHistDict[hist]['hist'].GetXaxis().GetXbins())}
        if selectedHistDict[hist]['dim'] == '2D': 
            selectedHistDict[hist]['binning'].update({'ny':selectedHistDict[hist]['hist'].GetNbinsY(), 'ybins':list(selectedHistDict[hist]['hist'].GetYaxis().GetXbins())})
    
    # updating bins
    
    if not (type(updatePtRange) == type([]) and len(updatePtRange) == 2):
        print "updatePtRange needs to be a list with length of 2. Exiting"
        sys.exit()
    
    if not updatePtRange[0] < updatePtRange[1]:
        print "updatePtRange needs to be from a lower to a higher number. Exiting"
        sys.exit()
    
    if not all(x in selectedHistDict[updateHistName]['binning']['xbins'] for x in updatePtRange):
        print "updatePtRange %s must coincide with binning %s of histogram that updates the SFs. Exiting."%(updatePtRange, selectedHistDict[updateHistName]['binning']['xbins'])
        sys.exit() 
    
    updatePtBinsAll = selectedHistDict[updateHistName]['binning']['xbins']
    basePtBinsAll   = selectedHistDict[baseHistName]['binning']['xbins']
    
    updatePtBins = updatePtBinsAll[updatePtBinsAll.index(updatePtRange[0]):updatePtBinsAll.index(updatePtRange[1])+1] # bins to update the base histogram
    
    if updatePtBins[0] < basePtBinsAll[0]: # lower edge less than lowest existing bin
        basePtBinsLower = []
    else:
        basePtBinsLower = basePtBinsAll[:basePtBinsAll.index(updatePtBins[0])]
    
    if updatePtBins[-1] > basePtBinsAll[-1]: # higher edge more than highest existing bin
        basePtBinsUpper = []
    else:
        basePtBinsUpper = basePtBinsAll[basePtBinsAll.index(updatePtBins[-1])+1:]
    
    combinedPtBins = basePtBinsLower + updatePtBins + basePtBinsUpper 
    
    # deltas
    basePtBinsLowerDelta = len(basePtBinsLower) - 1 if len(basePtBinsLower) > 0 else 0
    updatePtBinsDelta    = len(updatePtBins)    - 1 if len(updatePtBins)    > 0 else 0
    
    # combined histogram
    combinedHistDict = {
        "tag": '{}_{}_{}-{}'.format(selectedHistDict[baseHistName]['tag'], selectedHistDict[updateHistName]['tag'], updatePtRange[0], updatePtRange[1]).replace('.','p'), 
        "dim":selectedHistDict[baseHistName]['dim'],
        "lep":selectedHistDict[baseHistName]['lep'],
        "binning":{}
    }
    
    combinedHistName = "%s_SF_%s_%s"%(selectedHistDict[baseHistName]['lep'], selectedHistDict[baseHistName]['dim'], combinedHistDict['tag'])
    combinedHistDict['hist_name'] = combinedHistName
    
    nx = len(combinedPtBins)-1
    combinedPtBinsArray = array.array("d", combinedPtBins)
    combinedHistDict['binning']['xbins'] = combinedPtBins
    combinedHistDict['binning']['nx'] = nx
    
    # filling combined histogram
    if combinedHistDict['dim'] == '2D': # 2D SF plot
        baseEtaBins = selectedHistDict[baseHistName]['binning']['ybins'] # currently keeping base eta binning #NOTE: equivalent to selectedHistDict[baseHistName]['hist'].GetYaxis().GetXbins()).GetArray()
        combinedEtaBins = [x for x in baseEtaBins if x >= 0] # only positive values for absEta
        positiveEtaBinsDelta = len(baseEtaBins) - len(combinedEtaBins)
 
        ny = len(combinedEtaBins)-1
        combinedEtaBinsArray = array.array("d", combinedEtaBins) 
        combinedHistDict['binning']['ybins'] = combinedEtaBins
        combinedHistDict['binning']['ny'] = ny
    
        SF = ROOT.TH2F(combinedHistName, combinedHistName, nx, combinedPtBinsArray, ny, combinedEtaBinsArray)
        SF.SetTitle(combinedHistName)
        SF.GetXaxis().SetTitle("p_{T} (GeV)")
        SF.GetYaxis().SetTitle("|#eta|")
        SF.GetZaxis().SetTitle("SF")
        SF.GetXaxis().SetTitleOffset(1.2)
        SF.GetYaxis().SetTitleOffset(1.2)
        SF.GetZaxis().SetTitleOffset(1.2)
        #SF.GetZaxis().SetLabelSize(0.1)
        SF.GetZaxis().SetRangeUser(0.8,1)
        SF.SetMarkerSize(1.5)
        
        for xbin in range(1, nx+1):
            # lower range base values
            for ybin in range(1, ny+1):
                if combinedPtBins[xbin-1] < updatePtRange[0]:
                    binContent = selectedHistDict[baseHistName]['hist'].GetBinContent(xbin, ybin+positiveEtaBinsDelta)
                    binError   = selectedHistDict[baseHistName]['hist'].GetBinError(xbin, ybin+positiveEtaBinsDelta)
                # updated values
                elif combinedPtBins[xbin-1] >= updatePtRange[0] and combinedPtBins[xbin-1] < updatePtRange[1]: # NOTE: does not include the bin starting from the upper edge
                    if selectedHistDict[updateHistName]['dim'] == "2D":
                        ybinFix    = selectedHistDict[updateHistName]['hist'].GetYaxis().FindBin(selectedHistDict[baseHistName]['hist'].GetYaxis().GetBinCenter(ybin+positiveEtaBinsDelta)) # NOTE: if eta bins are not identical
                        binContent = selectedHistDict[updateHistName]['hist'].GetBinContent(xbin-basePtBinsLowerDelta, ybinFix)
                        binError   = selectedHistDict[updateHistName]['hist'].GetBinError(xbin-basePtBinsLowerDelta, ybinFix)
                    elif selectedHistDict[updateHistName]['dim'] == "1D":
                        binContent = selectedHistDict[updateHistName]['hist'].GetBinContent(xbin-basePtBinsLowerDelta)
                        binError   = selectedHistDict[updateHistName]['hist'].GetBinError(xbin-basePtBinsLowerDelta)
                # fill upper range base values
                elif combinedPtBins[xbin-1] >= updatePtRange[1]:
                    binContent = selectedHistDict[baseHistName]['hist'].GetBinContent(xbin-updatePtBinsDelta, ybin+positiveEtaBinsDelta)
                    binError   = selectedHistDict[baseHistName]['hist'].GetBinError(xbin-updatePtBinsDelta, ybin+positiveEtaBinsDelta)
                else:
                    print "Issue with filling bins. Exiting."
                    sys.exit()
   
                SF.SetBinContent(xbin, ybin, binContent)
                SF.SetBinError(xbin,   ybin, binError) 
    
    elif combinedHistDict['dim'] == '1D':
        SF = ROOT.TH1F(combinedHistName, combinedHistName, nx, combinedPtBinsArray)
        SF.SetTitle(combinedHistName)
        SF.GetXaxis().SetTitle("p_{T} (GeV)")
        SF.GetYaxis().SetTitle("SF")
        SF.GetXaxis().SetTitleOffset(1.2)
        SF.GetYaxis().SetTitleOffset(1.2)
        SF.GetYaxis().SetRangeUser(0.8,1)
        
        for xbin in range(nx+1):
            # fill base values
            if combinedPtBins[xbin] < updatePtRange[0] or combinedPtBins[xbin] > updatePtRange[1]:
                SF.SetBinContent(xbin, selectedHistDict[baseHistName]['hist'].GetBinContent(xbin))
                SF.SetBinError(xbin,   selectedHistDict[baseHistName]['hist'].GetBinError(xbin))
            # fill updated values
            elif combinedPtBins[xbin] >= updatePtRange[0] and combinedPtBins[xbin] <= updatePtRange[1]:
                SF.SetBinContent(xbin, selectedHistDict[updateHistName]['hist'].GetBinContent(xbin))
                SF.SetBinError(xbin,   selectedHistDict[updateHistName]['hist'].GetBinError(xbin))
            else:
                print "Issue with filling bins. Exiting."
                sys.exit()
        
    combinedHistDict['hist'] = SF
    
    # Save histogram in separate root file locally
    fout = ROOT.TFile(combinedHistDict['hist_name'] + '.root', "recreate")
    fout.cd()
    SF.Write() #combinedHistDict['hist_name'])
    fout.Close()
    
    if verbose:
        print "Details of combined histogram:"
        print pprint.pprint(combinedHistDict)
   
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetPaintTextFormat("5.3f") 
    
    c1 = ROOT.TCanvas("c1", "Canvas 1", 1800, 1500)
    
    if combinedHistDict['dim'] == '2D':
        SF.Draw("COLZ TEXT89E") #CONT1-5 #plots the graph with axes and points
        SF.SetMarkerSize(1) # text size
    elif combinedHistDict['dim'] == '1D': 
        SF.Draw("EP")
        
    c1.Modified()
    c1.Update()
    
    if drawOriginalSFs:
        c2 = ROOT.TCanvas("c2", "Canvas 2", 1800, 1500)
            
        selectedHistDict[baseHistName]['hist'].GetZaxis().SetRangeUser(0.8,1)
        
        if selectedHistDict[baseHistName]['dim'] == '2D':
            selectedHistDict[baseHistName]['hist'].Draw("COLZ TEXT89E")
        elif selectedHistDict[baseHistName]['dim'] == '1D':
            selectedHistDict[baseHistName]['hist'].Draw("EP")
    
        c2.Modified()
        c2.Update()
        
        c3 = ROOT.TCanvas("c3", "Canvas 3", 1800, 1500)
            
        selectedHistDict[updateHistName]['hist'].GetZaxis().SetRangeUser(0.8,1)
        
        if selectedHistDict[updateHistName]['dim'] == '2D':
            selectedHistDict[updateHistName]['hist'].Draw("COLZ TEXT89E")
        elif selectedHistDict[updateHistName]['dim'] == '1D':
            selectedHistDict[updateHistName]['hist'].Draw("EP")
        
        c3.Modified()
        c3.Update()
    
    # Save canvas
    savedir += '/' + combinedHistDict['hist_name']
    makeDir(savedir + '/root')
    makeDir(savedir + '/pdf')
    
    c1.SaveAs("%s/combinedSF_%s.png"      %(savedir, combinedHistDict['hist_name']))
    c1.SaveAs("%s/pdf/combinedSF_%s.pdf"  %(savedir, combinedHistDict['hist_name']))
    c1.SaveAs("%s/root/combinedSF_%s.root"%(savedir, combinedHistDict['hist_name']))
    
    if drawOriginalSFs:
    
        c2.SaveAs("%s/%s.png"      %(savedir, selectedHistDict[baseHistName]['hist_name']))
        c2.SaveAs("%s/pdf/%s.pdf"  %(savedir, selectedHistDict[baseHistName]['hist_name']))
        c2.SaveAs("%s/root/%s.root"%(savedir, selectedHistDict[baseHistName]['hist_name']))
        
        c3.SaveAs("%s/%s.png"      %(savedir, selectedHistDict[updateHistName]['hist_name']))
        c3.SaveAs("%s/pdf/%s.pdf"  %(savedir, selectedHistDict[updateHistName]['hist_name']))
        c3.SaveAs("%s/root/%s.root"%(savedir, selectedHistDict[updateHistName]['hist_name']))
   
if __name__ == '__main__':
    savedir = "/afs/hephy.at/user/m/mzarucki/www/plots/leptonSFs/combinedSFs"
    combineSFs(baseHistName = 'mu_LooseWP_2D_cent', updateHistName = 'mu_LooseWP_1D_priv', updatePtRange = [3.5, 10], file_dir = './', savedir = savedir, drawOriginalSFs = True, verbose = True)
    combineSFs(baseHistName = 'el_VetoWP_2D_cent',  updateHistName = 'el_VetoWP_2D_priv',  updatePtRange = [3.5, 10], file_dir = './', savedir = savedir, drawOriginalSFs = True, verbose = True)
