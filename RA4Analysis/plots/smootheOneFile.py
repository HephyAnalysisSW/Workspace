import os, sys, ROOT
ROOT.gROOT.ProcessLine(".L ../scripts/tdrstyle.C")
ROOT.setTDRStyle()
ROOT.tdrStyle.SetPadRightMargin(0.20)

ROOT.gROOT.ProcessLine(".L ../scripts/useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)
ROOT.gROOT.ProcessLine(".L ../limits/TriangularInterpolation.C+")
ROOT.gROOT.ProcessLine(".L ../limits/SmoothingUtils.C+")
ROOT.gROOT.ProcessLine(".L ../limits/interpolate.h+")
#path = os.path.abspath('../plots')
#if not path in sys.path:
#    sys.path.insert(1, path)
#del path

from analysisHelpers import getObjFromFile

if len(sys.argv)>=4:
  try:
      minz = float(sys.argv[1])
      maxz = float(sys.argv[2])
      filenames = sys.argv[3:]
  except ValueError:
      print "Don't change z-Axis"
      filenames = sys.argv[1:]

  print "Smoothing",filenames

  for filename in filenames:
    if filename[-5:]==".root" and not filename.count("smoothed"):
      direction = "SW"
      if filename.count('T1t1t'):direction = "EW"
      ifile = filename[:-5]
      canv = getObjFromFile(filename, 'c1') 
      if not canv:canv = getObjFromFile(filename, 'c1_n2')
      if not canv:canv = getObjFromFile(filename, 'c1_n3')
      hist2DSFunc = canv.GetPrimitive("hist2DSFunc")

      res = hist2DSFunc.Clone()
      c1 = ROOT.TCanvas()
    #  hist2DSFunc.Draw("colz")
    #  c1.Print(ifile+".png")
      #res = smooth2DHisto(hist2DSFunc, 1,1, False, 0)
      if minz<0:
        for ix in range(1, res.GetNbinsX()+1):
          for iy in range(1, res.GetNbinsY()+1):
            if res.GetBinContent(ix,iy) ==0:
              res.SetBinContent(ix,iy,2*minz)

      if globals().has_key("minz"):
        res.GetZaxis().SetRangeUser(minz, maxz)
      res.Draw("colz")
      c1.Print(ifile+"_orig.png")
      c1.Print(ifile+"_orig.pdf")
      c1.Print(ifile+"_orig.root")

      res = hist2DSFunc.Clone()
      res = ROOT.interpolate(res,direction)

      if globals().has_key("minz"):
        res.GetZaxis().SetRangeUser(minz, maxz)

      res.Draw("colz")
      c1.Print(ifile+"_interpolated.png")
      c1.Print(ifile+"_interpolated.pdf")
      c1.Print(ifile+"_interpolated.root")

      res = ROOT.doSmooth(res, "ka3",2,0) 
      res.Draw("colz")
      c1.Print(ifile+"_interpolated_smoothed.png")
      c1.Print(ifile+"_interpolated_smoothed.pdf")
      c1.Print(ifile+"_interpolated_smoothed.root")
