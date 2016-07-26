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




def makeCanvasMultiPads(     c1Name="canvas",  c1ww=600, c1wh=600,  joinPads=True, func=None, 
                             pads = [
                                {"name":"p1" , "m":[0,0.3,1,1.0], "gridX":False, "gridY":False},
                                {"name":"p2" , "m":[0, 0.05, 1, 0.3], "gridX":False, "gridY":False},
                             ], 
                             padRatios=[],
                     ):
    """
        can split create a canvas with multiple pads. use a list for the pads with the following format:
        pads = [
                 {"name":"p1" , "m"=[0,0.3,1,1.0], "gridX":False, "gridY":False},
                 {"name":"p2", .....}
                ]

        you can use func, to do funckier stuff with the funcs. it takes all the pads as input

    """
    c = ROOT.TCanvas(c1Name,c1Name,c1ww,c1wh)
    c.cd()  # returns to main canvas before defining pad2
    # Upper histogram plot is pad1
    ms = [ pad['m'] for pad in  pads]
    nPads = len(pads)
    if not all(ms) or not nPads:
        bottom_marg = 0.05
        left_marg = 0
        right_marg = 0.05
        top_marg = 0
        #if padRatios and len(padRatios)==len(pads):
        if padRatios:
            if not nPads:
                pads=[{"name":"%s_p%s"%(c1Name, ipad+1) , "m":[], "gridX":False, "gridY":False} for ipad in range(len(padRatios))]
            padRatios = [float(x)/(sum(padRatios)) for x in padRatios]
            print "++++++++++++++ pads", padRatios 
            for ipad, pad in enumerate(pads):
                yhigh = sum(padRatios[ipad:])
                ylow  = sum(padRatios[ipad+1:]) 
                pad['m']=[ 0 + left_marg, ylow + (ipad+1==nPads)*bottom_marg , 1-right_marg, yhigh]
                #print ipad, pad, nPads, ipad+1==nPads, bottom_marg, (ipad+1==nPads)*bottom_marg
        else:
            raise Exception("Need a way to distribute the pads, either provide padRatios, or pad['m']=[xlow,ylow,xhigh,yhigh]")
        #print pads

    for pad in pads:
        pad['pad'] = ROOT.TPad(pad['name'], pad['name'], *pad['m']    ) 
        if pad['gridX']: pad['pad'].SetGridx()
        if pad['gridY']: pad['pad'].SetGridy()
        if joinPads: 
            pad['pad'].SetTopMargin(0)  # joins upper and lower plot
            pad['pad'].SetBottomMargin(0)  # joins upper and lower plot
            
    padList = [x['pad'] for x in pads]
    padList[0].SetBottomMargin(0)  # joins upper and lower plot
    padList[0].SetTopMargin(0.1)
    padList[-1].SetBottomMargin(0.25)


    # Lower ratio plot is pad2
    if func:
        func(*padList)
    for pad in padList:
        pad.Draw() 
    ret = [c]+padList
    return ret


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




