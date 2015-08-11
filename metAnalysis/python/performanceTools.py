import ROOT
from array import array
from math import sqrt, cosh, cos, sin
import os, copy, sys
from Workspace.HEPHYPythonTools.helpers import getObjFromFile, getChain, getChunks, getObjDict, getVarValue


def findBin(v, varValue):
  for bin in v['bins']:
    if varValue>=bin[0] and varValue<bin[1]:
      return bin

def makeMETPerformanceHistos(setup):
  small = True if setup.has_key('small') and setup['small'] else False
  for name, v in setup["variables"].iteritems():
    v['bins']=[(v["binning"][i],v["binning"][i+1]) for i in range(len(v["binning"])-1)]
    v['uperp']={}
    v['upara']={}
    v['qt']={}
    v['histo']={}
    for mname, mv in setup["metVariables"].iteritems():
      hname = '_'.join([name,mname])
      v['histo'][mname]=ROOT.TH1D('histo_'+hname, 'histo_'+hname, len(v['binning'])-1, array('d',v['binning']))
      v['upara'][mname]={}
      v['uperp'][mname]={}
      v['qt'][mname]={}
      v['upara'][mname]["scale"] = ROOT.TH1D(hname+'_upara_scale', hname+'_upara_scale',len(v['binning'])-1, array('d',v['binning']))
  #    v['upara'][mname]["scale"] = ROOT.TH1D(hname+'_upara_scale', hname+'_upara_scale',len(v['binning'])-1, array('d',v['binning']))
      v['upara'][mname]["RMS"] = ROOT.TH1D(hname+'_upara_RMS', hname+'_upara_RMS',len(v['binning'])-1, array('d',v['binning']))
      v['uperp'][mname]["RMS"] = ROOT.TH1D(hname+'_uperp_RMS', hname+'_uperp_RMS',len(v['binning'])-1, array('d',v['binning']))
      v['upara'][mname]["RMScorr"] = ROOT.TH1D(hname+'_upara_RMScorr', hname+'_upara_RMScorr',len(v['binning'])-1, array('d',v['binning']))
      v['uperp'][mname]["RMScorr"] = ROOT.TH1D(hname+'_uperp_RMScorr', hname+'_uperp_RMScorr',len(v['binning'])-1, array('d',v['binning']))
      for b in v['bins']:
        hname = name+'_'.join([str(x) for x in b])
        v['uperp'][mname][b] = ROOT.TH1D(hname+'_'+mname+'_uperp', hname+'_'+mname+'_uperp', 400,-200,200) 
        v['upara'][mname][b] = ROOT.TH1D(hname+'_'+mname+'_upara', hname+'_'+mname+'_upara', 500,-400,100) 
        v['qt'][mname][b] = ROOT.TH1D(hname+'_'+mname+'_qt', hname+'_'+mname+'_qt', 500,-400,100) 

  for s in setup["samples"]:
    for b in s['bins']:
      b['chain'].Draw('>>eList', setup['preselection'])
      eList = ROOT.gDirectory.Get('eList')
      nEvents = eList.GetN() if not small else 10000
      for nev in range(nEvents):
        if nev%1000==0:print "At %i / %i"%(nev, nEvents)
        b['chain'].GetEntry(eList.GetEntry(nev))
        muons = setup['leptons'](b['chain'])
        if len(muons)!=2:continue
        l0, l1 = muons
        if not setup['massWindow'](l0,l1):continue
        qx = l0['pt']*cos(l0['phi']) + l1['pt']*cos(l1['phi'])  
        qy = l0['pt']*sin(l0['phi']) + l1['pt']*cos(l1['phi']) 
  #      qphi = atan2(qy, qx)
        qt = sqrt(qx**2+qy**2)
  #      print l0, l1

        for mname, mv in setup["metVariables"].iteritems():
          mv['pt'] = mv['ptFunc'](b['chain']) 
          mv['phi'] = mv['phiFunc'](b['chain'])
          ux = -mv['pt']*cos(mv['phi']) - qx 
          uy = -mv['pt']*sin(mv['phi']) - qy
          upara = (ux*qx+uy*qy)/qt
          uperp = (ux*qy-uy*qx)/qt
          weight = getVarValue(b['chain'], 'genWeight')*b['lumiScale']
          for name, v in setup["variables"].iteritems():
            if v['func']=='qt':varValue=qt
            else:
              varValue = v['func'](b['chain'])
            v['histo'][mname].Fill(varValue, weight)         #Filling distribution of binning variable
            varBin = findBin(v, varValue)
            if varBin: 
              v['uperp'][mname][varBin].Fill(uperp, weight) 
              v['upara'][mname][varBin].Fill(upara, weight) 
              v['qt'][mname][varBin].Fill(qt, weight) 
    del eList

  for name, v in setup["variables"].iteritems():
    for mname, mv in setup["metVariables"].iteritems():
      for bin in v['bins']:
        upara_mean      = v['upara'][mname][bin].GetMean()
        upara_mean_err  = v['upara'][mname][bin].GetMeanError()
        uperp_mean      = v['uperp'][mname][bin].GetMean()
        uperp_mean_err  = v['uperp'][mname][bin].GetMeanError()
        upara_RMS      = v['upara'][mname][bin].GetRMS()
        upara_RMS_err  = v['upara'][mname][bin].GetRMSError()
        uperp_RMS      = v['uperp'][mname][bin].GetRMS()
        uperp_RMS_err  = v['uperp'][mname][bin].GetRMSError()
        qt_mean       = v['qt'][mname][bin].GetMean()
        qt_mean_err   = v['qt'][mname][bin].GetMeanError()
        if (not qt_mean>0) or (not upara_RMS>0) or (not uperp_RMS>0):continue
        scale         =  - upara_mean / qt_mean 
        scale_err     =  upara_mean / qt_mean * sqrt(upara_mean_err**2/upara_mean**2 + qt_mean_err**2/qt_mean**2)
        upara_RMS_scaleCorr       =  upara_RMS/scale
        upara_RMS_scaleCorr_err   =  upara_RMS/scale*sqrt(upara_RMS_err**2/upara_RMS**2 + scale_err**2/scale**2)
        uperp_RMS_scaleCorr       =  uperp_RMS/scale
        uperp_RMS_scaleCorr_err   =  uperp_RMS/scale*sqrt(uperp_RMS_err**2/uperp_RMS**2 + scale_err**2/scale**2)
        val = 0.5*(bin[0]+bin[1])
        nbin = v['upara'][mname]["scale"].FindBin(val)
        v['upara'][mname]["scale"].SetBinContent(nbin, scale)
        v['upara'][mname]["scale"].SetBinError(nbin, scale_err)
        v['upara'][mname]["RMS"].SetBinContent(nbin, upara_RMS)
        v['upara'][mname]["RMS"].SetBinError(nbin, upara_RMS_err)
        v['upara'][mname]["RMScorr"].SetBinContent(nbin, upara_RMS_scaleCorr)
        v['upara'][mname]["RMScorr"].SetBinError(nbin, upara_RMS_scaleCorr_err)
        v['uperp'][mname]["RMS"].SetBinContent(nbin, uperp_RMS)
        v['uperp'][mname]["RMS"].SetBinError(nbin, uperp_RMS_err)
        v['uperp'][mname]["RMScorr"].SetBinContent(nbin, uperp_RMS_scaleCorr)
        v['uperp'][mname]["RMScorr"].SetBinError(nbin, uperp_RMS_scaleCorr_err)
  return setup

