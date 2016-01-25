import ROOT



def getRatio(hist1, hist2,normalize=False,min=False,max=False):
  ret = hist1.Clone("Ratio")
  h2  = hist2.Clone()
  if normalize:
    ret.Scale(1./ret.Integral())
    h2.Scale(1./h2.Integral())
  ret.SetLineColor(ROOT.kBlack)
  ret.SetMarkerStyle(21)
  ret.SetTitle("")
  if min:   ret.SetMinimum(min)
  if max:   ret.SetMaximum(max)
  # Set up plot for markers and errors
  ret.Sumw2()
  ret.SetStats(0)
  ret.Divide(h2)
  # Adjust y-axis settings
  y = ret.GetYaxis()
  y.SetTitle("Ratio")
  y.SetNdivisions(505)
  y.SetTitleSize(20)
  y.SetTitleFont(43)
  y.SetTitleOffset(1.55)
  y.SetLabelFont(43)
  y.SetLabelSize(15)
  # Adjust x-axis settings
  x = ret.GetXaxis()
  x.SetTitleSize(20)
  x.SetTitleFont(43)
  x.SetTitleOffset(4.0)
  x.SetLabelFont(43)
  x.SetLabelSize(15)
  return ret





def makeCanvasPads(     c1Name="canvas",  c1ww=600, c1wh=600, 
                       p1Name="pad1", p1M=[0, 0.3, 1, 1.0], p1Gridx=False, p1Gridy=False, 
                       p2Name="pad2", p2M=[0, 0.05, 1, 0.3], p2Gridx=False, p2Gridy=False,
                       joinPads=True,
                       func=None
                    ):
  c = ROOT.TCanvas(c1Name,c1Name,c1ww,c1wh)
  # Upper histogram plot is pad1
  pad1 = ROOT.TPad(p1Name, p1Name, *p1M)
  pad1.SetBottomMargin(0)  # joins upper and lower plot
  if p1Gridx: pad1.SetGridx()
  if p1Gridy: pad1.SetGridy()
  
  # Lower ratio plot is pad2
  c.cd()  # returns to main canvas before defining pad2
  pad2 = ROOT.TPad(p2Name, p2Name, *p2M)

  if joinPads: pad2.SetTopMargin(0)  # joins upper and lower plot
  pad2.SetBottomMargin(0.2)
  if p2Gridx: pad2.SetGridx()
  if p2Gridy: pad2.SetGridy()
  if func:
    func(pad1,pad2)
  pad1.Draw()
  pad2.Draw()
  return c, pad1, pad2


def makeRatioPlot(h1,h2): 
  # create required parts 
  h3 = createRatio(h1, h2) 
  c, pad1, pad2 = createCanvasPads() 
 
  # draw everything 
  pad1.cd() 
  h1.Draw() 
  h2.Draw("same") 
  # to avoid clipping the bottom zero, redraw a small axis 
  h1.GetYaxis().SetLabelSize(0.0) 
  axis = ROOT.TGaxis(-5, 20, -5, 220, 20, 220, 510, "") 
  axis.SetLabelFont(43) 
  axis.SetLabelSize(15) 
  axis.Draw() 
  pad2.cd() 
  h3.Draw("ep") 




