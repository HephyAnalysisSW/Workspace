from Workspace.DegenerateStopAnalysis.navidTools.NavidTools import Plots
from Workspace.DegenerateStopAnalysis.cuts import *
from Workspace.DegenerateStopAnalysis.cuts import *
import ROOT
import math



plots =Plots(**
      {
        "Q80":         {'var':"Q80"                            ,"bins":[20,-2,1]          ,"decor":{"title":"Q80"           ,"x":"Q80"          ,"y":"nEvents"    ,'log':[0,1,0] }},
        "CosLMet":     {'var':"CosLMet"                        ,"bins":[20,-1,1]          ,"decor":{"title":"CosLMet"       ,"x":"CosLMet"      ,"y":"nEvents"    ,'log':[0,1,0] }},
        "DMT":         {'var':"Q80:CosLMet"                    ,"bins":[20,-1,1,20,-2,1] ,"decor":{"title":"{SAMP} Decons. MT"    ,"x":"CosLMet"      ,"y":"Q80"  ,'log':[0,0,1] }},
         "MT":         {'var':"mt"                             ,"bins":[20,0,300]        ,"decor":{"title":"MT"    ,"x":"M_{T}"      ,"y":"nEvents"  ,'log':[0,1,0] }},
      }
        )









xvar="CosLMet"
yvar="Q80"

r1= ROOT.TCutG("r1",3) ##high mt region
r1.SetVarX(xvar)
r1.SetVarY(yvar)
r1.SetPoint(0,-1,1)
r1.SetPoint(1,1,1)
r1.SetPoint(2,-1,-1)

r2= ROOT.TCutG("r2",5) ## lower mt region
r2.SetVarX(xvar)
r2.SetVarY(yvar)
r2.SetPoint(0,-1,-1)
r2.SetPoint(1,0.8,0.8)
r2.SetPoint(2,0.8,0.8)
r2.SetPoint(3,0.8,-10)
r2.SetPoint(4,-1,-10)
r2.SetPoint(5,-1,-1)


r3= ROOT.TCutG("r3",4) ## cos=1 
r3.SetVarX(xvar)
r3.SetVarY(yvar)
r3.SetPoint(0,1,1)
r3.SetPoint(1,1,-10)
r3.SetPoint(2,0.8,-10)
r3.SetPoint(3,0.8,0.8)
r3.SetPoint(4,1,1)


def fy (fx,m,yinterc):
  return m*fx+yinterc
def fx (fy,m,yinterc):
  return (fy-yinterc)/float(m)



class R1():
  def __init__(self,name,m,b,x="CosLMet",y="Q80"):
    self.name=name
    if hasattr(ROOT,name):
      print name , "already exists as a root TCutG! It will be deleted otherwise ROOT freaks out!"
      #getattr(ROOT,name).Delete()
    r1= ROOT.TCutG(name,3) ##high mt region
    r1.SetVarX(xvar)
    r1.SetVarY(yvar)
    yinterc = m+b
    r1.SetPoint(0,-1,1)
    r1.SetPoint(1,fx(1,m,yinterc),1)
    r1.SetPoint(2,-1,b)
    r1.SetPoint(3,-1,1)
    r1.SetLineColor(ROOT.kRed)
    r1.SetLineWidth(2)
    self.r = r1

class R2():
  #def __init__(self,m,m2,cx,cy,x="CosLMet",y="Q80"):
  def __init__(self,name,m1,m2,cx,cy,r3l,x="CosLMet",y="Q80"):
    """ c is the x comp of the intersection point  """
    self.name=name
    yinterc1         = cy - m1*cx
    #b2_check  = (m-m2)*cx+yinterc
    yinterc2        = cy - m2*cx
    #self.line1   = "({m}*{x}+{b})".format(x=x,m=m,b=b)
    ##if not round(b2,3) == round(b2_check,3): 
    ##  print "SOMETHING WORNG MY WITH GEOMETRY", b2,b2_check
    #self.b2_check = b2_check
    #self.b2   = b2
    r2= ROOT.TCutG(name,5) ## lower mt region
    r2.SetVarX(xvar)
    r2.SetVarY(yvar)
    r2.SetPoint(0,-1,fy(-1,m1,yinterc1) )
    r2.SetPoint(1,cx,cy)
    r2.SetPoint(2,r3l, fy(r3l,m2,yinterc2))
    r2.SetPoint(3,r3l, -50 )
    r2.SetPoint(4,-1,-50)
    r2.SetPoint(5,-1,fy(-1,m1,yinterc1))
    r2.SetLineWidth(2)
    self.r=r2


class R3():
  def __init__(self,name,left,top,topright,x="CosLMet",y="Q80"):
    self.name=name
    r3=ROOT.TCutG(name,4) ## cos=1 
    r3.SetVarX(xvar)
    r3.SetVarY(yvar)
    r3.SetPoint(0,left,top)
    r3.SetPoint(1,1,topright)
    r3.SetPoint(2,1,-10)
    r3.SetPoint(3,left,-10)
    r3.SetPoint(4,left,top)
    r3.SetLineColor(ROOT.kMagenta)
    r3.SetLineWidth(2)
    self.r=r3


class QCosRegion():
  def __init__(self,name,(r1m,r1b), (r2m1,r2m2,r2cx,r2cy), (r3l,r3t,r3tr), x=xvar, y =yvar , baseCut=sr1Loose):
    self.name = name
    self.r1 = R1("r1"+name, r1m, r1b )
    self.r2 = R2("r2"+name, r2m1,r2m2,r2cx,r2cy , r3l )
    self.r3 = R3("r3"+name, r3l, r3t, r3tr   )
    self.r1cut = "({r1} )".format(r1=self.r1.name)
    self.r2cut = "({r2} && ! ( {r1} ))".format(r1=self.r1.name,r2=self.r2.name)
    self.r3cut = "({r3} && ! ( {r1} || {r2}) )".format(r1=self.r1.name,r2=self.r2.name,r3=self.r3.name)
    self.rej   = "(!({r1} ||  {r2} || {r3} ) )".format(r1=self.r1.name,r2=self.r2.name,r3=self.r3.name)
    self.all   = "({r1} ||  {r2} || {r3} )".format(r1=self.r1.name,r2=self.r2.name,r3=self.r3.name)
    self.cut = CutClass(name,  [
                            ["r1",self.r1cut],
                            ["r2",self.r2cut],
                            ["r3",self.r3cut],
                            ["rejected",self.rej],
                             ],
                          baseCut= baseCut     
                        )
    self.cut1 = CutClass(name+"_R1",  [
                            ["r1",self.r1cut],
                             ],
                          baseCut= baseCut     
                        )
    self.cut2 = CutClass(name+"_R2",  [
                            ["r2",self.r2cut],
                             ],
                          baseCut= baseCut     
                        )
    self.cut3 = CutClass(name+"_R3",  [
                            ["r3",self.r3cut],
                             ],
                          baseCut= baseCut     
                        )
    self.cutRej = CutClass(name+"_Rej",  [
                            ["rej",self.rej],
                             ],
                          baseCut= baseCut     
                        )
    self.cut_ptbin = CutClass(name,  [
                            #["r1",self.r1cut],
                                  ["r1_pt1",     "(%s && %s)"%(self.r1cut,  btw("lepPt",5,12)  )],
                                  ["r1_pt2",     "(%s && %s)"%(self.r1cut,  btw("lepPt",12,20)  )],
                                  ["r1_pt3",     "(%s && %s)"%(self.r1cut,  btw("lepPt",20,30)  )],
                            #["r2",self.r2cut],
                                  ["r2_pt1",     "(%s && %s)"%(self.r2cut,  btw("lepPt",5,12)  )],
                                  ["r2_pt2",     "(%s && %s)"%(self.r2cut,  btw("lepPt",12,20)  )],
                                  ["r2_pt3",     "(%s && %s)"%(self.r2cut,  btw("lepPt",20,30)  )],
                            #["r3",self.r3cut],
                                  ["r3_pt1",     "(%s && %s)"%(self.r3cut,  btw("lepPt",5,12)  )],
                                  ["r3_pt2",     "(%s && %s)"%(self.r3cut,  btw("lepPt",12,20)  )],
                                  ["r3_pt3",     "(%s && %s)"%(self.r3cut,  btw("lepPt",20,30)  )],
                            #["rejected",self.rej],
                                  ["rej_pt1",     "(%s && %s)"%(self.rej,  btw("lepPt",5,12)  )],
                                  ["rej_pt2",     "(%s && %s)"%(self.rej,  btw("lepPt",12,20)  )],
                                  ["rej_pt3",     "(%s && %s)"%(self.rej,  btw("lepPt",20,30)  )],
                             ],
                          baseCut= baseCut     
                        )

    self.cut1_ptbin = CutClass(name,  [
                            #["r1",self.r1cut],
                                  ["r1_pt1",     "(%s && %s)"%(self.r1cut,  btw("lepPt",5,12)  )],
                                  ["r1_pt2",     "(%s && %s)"%(self.r1cut,  btw("lepPt",12,20)  )],
                                  ["r1_pt3",     "(%s && %s)"%(self.r1cut,  btw("lepPt",20,30)  )],
                             ],
                          baseCut= baseCut     
                        )
    self.cut2_ptbin = CutClass(name,  [
                            #["r2",self.r2cut],
                                  ["r2_pt1",     "(%s && %s)"%(self.r2cut,  btw("lepPt",5,12)  )],
                                  ["r2_pt2",     "(%s && %s)"%(self.r2cut,  btw("lepPt",12,20)  )],
                                  ["r2_pt3",     "(%s && %s)"%(self.r2cut,  btw("lepPt",20,30)  )],
                             ],
                          baseCut= baseCut     
                        )
    self.cut3_ptbin = CutClass(name,  [
                            #["r3",self.r3cut],
                                  ["r3_pt1",     "(%s && %s)"%(self.r3cut,  btw("lepPt",5,12)  )],
                                  ["r3_pt2",     "(%s && %s)"%(self.r3cut,  btw("lepPt",12,20)  )],
                                  ["r3_pt3",     "(%s && %s)"%(self.r3cut,  btw("lepPt",20,30)  )],
                             ],
                          baseCut= baseCut     
                        )



regions = [
              ["incl0",(1,-1),        (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl1",(1,-.5),       (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl2",(1,-0),        (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl3",(1,0.5),       (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl4",(1,-0.3),      (1,-1000,0.8,0.8), (0.8,0.8,1)],

              ["incl11",(1.2,-.5),    (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl12",(1.2,-0),     (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl13",(1.2,0.5),    (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl14",(1.2,-0.3),   (1,-1000,0.8,0.8), (0.8,0.8,1)],

              ["incl21",(1.5/2,-.5),  (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl22",(1/2.,-0),    (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl23",(1/4.,0.5),   (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl24",(0.3/2,-0.3), (1,-1000,0.8,0.8), (0.8,0.8,1)],

              ["incl31",(1,-.5),      (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl32",(1,-0),       (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl33",(1,0.5),      (1,-1000,0.8,0.8), (0.8,0.8,1)],
              ["incl34",(1,-0.3),     (1,-1000,0.8,0.8), (0.8,0.8,1)],

              ["bench01",(0.9,-0.7),  (1,-1000,0.8,0), (0.8,0.0,1)  ],
              ["bench02",(0.9,-0.7),  (1,-1000,0.8,0.2), (0.8,0.2,1)],
              ["bench03",(0.9,-0.9),  (1,-1000,0.8,0.2), (0.8,0.2,1)],
              ["bench04",(0.9,-0.8),  (1,-1000,0.8,0.2), (0.8,0.2,1)],

          ]


#r1def = (1,-1)
#r2def = (1,-1000,0.8,0.8)
#r3def = (0.8,0.8,1)

r1bm1 = (0.8,-0.5)
r2bm1 = (1.2,-1000,0.8,0.5)
r3bm1 = (0.8,0.8,0.8)

r1def = r1bm1
r2def = r2bm1
r3def = r3bm1

r1_regions = [
              #["r1_1p0_m1p0"  , r1def ,       r2def           , r3def      ],
              ["r1_1p0_m0p8",  (1,-.8),       r2def  , r3def    ],
              ["r1_1p0_m0p7",  (1,-0.7),      r2def  , r3def    ],
              ["r1_1p0_m0p5",  (1,-0.5),      r2def  , r3def    ],
              ["r1_1p0_m1p2",  (1,-1.2),      r2def  , r3def    ],
              ["r1_1p0_m0p3",  (1,-0.3),       r2def  , r3def    ],

              ["r1_1p1_m0p5",  (1.1,-.5 ),   r2def   , r3def   ],
              ["r1_1p2_m0p5",  (1.2,-.5  ),  r2def   , r3def   ],
              ["r1_0p9_m0p5",  (0.9,-0.5 ),  r2def   , r3def   ],
              ["r1_0p8_m0p5",  (0.8,-0.5),   r2def   , r3def   ],

              ["r1_1p1_m0p3",  (1.1,-0.3 ),  r2def   , r3def   ],
              ["r1_1p2_m0p3",  (1.2,-0.3  ), r2def   , r3def   ],
              ["r1_0p9_m0p3",  (0.9,-0.3 ),  r2def   , r3def   ],
              ["r1_0p8_m0p3",  (0.8,-0.3),   r2def   , r3def   ],

              ["r1_1p1_m0p7",  (1.1,-0.7 ),  r2def   , r3def   ],
              ["r1_1p2_m0p7",  (1.2,-0.7  ), r2def   , r3def   ],
              ["r1_0p9_m0p7",  (0.9,-0.7 ),  r2def   , r3def   ],
              ["r1_0p8_m0p7",  (0.8,-0.7),   r2def   , r3def   ],
          ]


r2_regions = [
              ["r2_1p0_0p8_0p8"  , r1bm1 ,  (1,-1000,0.8,0.8)  , r3def      ],
              ["r2_1p0_0p8_0p5"  , r1bm1 ,  (1,-1000,0.8,0.5)  , r3def      ],
              ["r2_1p0_0p8_0p3"  , r1bm1 ,  (1,-1000,0.8,0.3)  , r3def      ],
              ["r2_1p0_0p8_0p0"  , r1bm1 ,  (1,-1000,0.8,0.0)  , r3def      ],

              ["r2_1p2_0p8_0p8"  , r1bm1 ,  (1.2,-1000,0.8,0.8)  , r3def      ],
              ["r2_1p2_0p8_0p5"  , r1bm1 ,  (1.2,-1000,0.8,0.5)  , r3def      ],
              ["r2_1p2_0p8_0p3"  , r1bm1 ,  (1.2,-1000,0.8,0.3)  , r3def      ],
              ["r2_1p2_0p8_0p0"  , r1bm1 ,  (1.2,-1000,0.8,0.0)  , r3def      ],


              ["r2_0p9_0p8_0p8"  , r1bm1 ,  (0.9,-1000,0.8,0.8)  , r3def      ],
              ["r2_0p9_0p8_0p5"  , r1bm1 ,  (0.9,-1000,0.8,0.5)  , r3def      ],
              ["r2_0p9_0p8_0p3"  , r1bm1 ,  (0.9,-1000,0.8,0.3)  , r3def      ],
              ["r2_0p9_0p8_0p0"  , r1bm1 ,  (0.9,-1000,0.8,0.0)  , r3def      ],
             ]


r3_regions = [
              ["r3_0p8_0p8_1p0"  , r1bm1 ,  r2bm1  , (0.8,0.8,1)      ],
              ["r3_0p8_0p5_1p0"  , r1bm1 ,  r2bm1  , (0.8,0.5,1)      ],
              ["r3_0p8_0p3_1p0"  , r1bm1 ,  r2bm1  , (0.8,0.3,1)      ],
              ["r3_0p8_0p0_1p0"  , r1bm1 ,  r2bm1  , (0.8,0.0,1)      ],

              ["r3_0p8_0p8_1p2"  , r1bm1 ,  r2bm1  , (0.8,0.8,1.2)      ],
              ["r3_0p8_0p5_1p2"  , r1bm1 ,  r2bm1  , (0.8,0.5,1.2)      ],
              ["r3_0p8_0p3_1p2"  , r1bm1 ,  r2bm1  , (0.8,0.3,1.2)      ],
              ["r3_0p8_0p0_1p2"  , r1bm1 ,  r2bm1  , (0.8,0.0,1.2)      ],

              ["r3_0p8_0p8_0p8"  , r1bm1 ,  r2bm1  , (0.8,0.8,0.8)      ],
              ["r3_0p8_0p5_0p8"  , r1bm1 ,  r2bm1  , (0.8,0.5,0.8)      ],
              ["r3_0p8_0p3_0p8"  , r1bm1 ,  r2bm1  , (0.8,0.3,0.8)      ],
              ["r3_0p8_0p0_0p8"  , r1bm1 ,  r2bm1  , (0.8,0.0,0.8)      ],


              ["r3_0p8_0p0_0p3"  , r1bm1 ,  r2bm1  , (0.8,0.0,0.3)        ],
              ["r3_0p8_0p0_0p0"  , r1bm1 ,  r2bm1  , (0.8,0.0,0.0)        ],
              ["r3_0p8_0p0_m0p3"  , r1bm1 ,  r2bm1  , (0.8,0.0,-0.3)      ],
              ["r3_0p8_0p0_m0p5"  , r1bm1 ,  r2bm1  , (0.8,0.0,-0.5)      ],

              ["r3_0p9_0p0_0p3"  , r1bm1 ,  r2bm1  ,  (0.9,0.0,0.3)       ],
              ["r3_0p9_0p0_0p0"  , r1bm1 ,  r2bm1  ,  (0.9,0.0,0.0)       ],
              ["r3_0p9_0p0_m0p3"  , r1bm1 ,  r2bm1  , (0.9,0.0,-0.3)      ],
              ["r3_0p9_0p0_m0p5"  , r1bm1 ,  r2bm1  , (0.9,0.0,-0.5)      ],


              ["r3_0p8_m0p3_0p3"  , r1bm1 ,  r2bm1  ,   (0.8,-0.3,0.3)        ],
              ["r3_0p8_m0p3_0p0"  , r1bm1 ,  r2bm1  ,   (0.8,-0.3,0.0)        ],
              ["r3_0p8_m0p3_m0p3"  , r1bm1 ,  r2bm1  ,  (0.8,-0.3,-0.3)      ],
              ["r3_0p8_m0p3_m0p5"  , r1bm1 ,  r2bm1  ,  (0.8,-0.3,-0.5)      ],

              ["r3_0p9_m0p3_0p3"  , r1bm1 ,  r2bm1  ,  (0.9,-0.3,0.3)       ],
              ["r3_0p9_m0p3_0p0"  , r1bm1 ,  r2bm1  ,  (0.9,-0.3,0.0)       ],
              ["r3_0p9_m0p3_m0p3"  , r1bm1 ,  r2bm1  , (0.9,-0.3,-0.3)      ],
              ["r3_0p9_m0p3_m0p5"  , r1bm1 ,  r2bm1  , (0.9,-0.3,-0.5)      ],

             ]


r=QCosRegion("t",(1,-1), (1,-1000,0.8,0.8), (0.8,0.8,1),  x=xvar,y=yvar)


qcosRegionBM1 = QCosRegion("BM1", r1bm1, r2bm1, r3bm1, baseCut=sr1Loose)


dmtBM1R1=qcosRegionBM1.cut1
dmtBM1R2=qcosRegionBM1.cut2
dmtBM1R3=qcosRegionBM1.cut3
dmtBM1Rej=qcosRegionBM1.cutRej





saveDir = '/afs/hephy.at/user/n/nrad/www/T2Deg13TeV/analysis/RunII/cutbased/dmt_regions'

canvas={}



regDict={} 
print "Getting Yields for different regions:" 
allregions = r1_regions + r2_regions + r3_regions

for r in allregions: 
  name=r[0] 
  canv={} 
  regDict[name] = QCosRegion(*r, x=xvar,y=yvar) 
  #print "----------------------------------------------------------------" 
  #print getattr(regDict[name],cut).list 
  #print regDict[name]
  #print "----------------------------------------------------------------" 

  #yDict[name]=  Yields(samples,['w','s'], getattr(regDict[name],cut), cutOpt='list', tableName='{cut}_dmt',pklOpt=True,pklDir=pklDir )    
  #JinjaTexTable(yDict[name]) 
  #canv[name]=ROOT.TCanvas(name,name,800,800) 
  #fomHistW.Draw("COLZ") 
  #regDict[name].r1.r.Draw("same") 
  #regDict[name].r2.r.Draw("same") 
  #regDict[name].r3.r.Draw("same") 
  #canv[name].SaveAs(saveDir+"/%s.png"%name) 


dmtRegions = CutClass( "dmtRegions", 
                        [  [r[0] , regDict[r[0]].r1cut] for r in r1_regions ] +
                        [  [r[0] , regDict[r[0]].r2cut] for r in r2_regions ] +
                        [  [r[0] , regDict[r[0]].r3cut] for r in r3_regions ] 
                     ,
              baseCut=sr1Loose,
            )
dmtR1 = CutClass( "dmtR1", 
                        [  [r[0] , regDict[r[0]].r1cut] for r in r1_regions ] 
                     ,
              baseCut=sr1Loose,
            )
dmtR2 = CutClass( "dmtR2", 
                        [  [r[0] , regDict[r[0]].r2cut] for r in r2_regions ] 
                     ,
              baseCut=sr1Loose,
            )
dmtR3 = CutClass( "dmtR3", 
                        [  [r[0] , regDict[r[0]].r3cut] for r in r3_regions ] 
                     ,
              baseCut=sr1Loose,
            )


dmtRejRegions = CutClass( "dmtRejRegions", 
                        [  [r[0] , regDict[r[0]].rej] for r in r1_regions ] +
                        [  [r[0] , regDict[r[0]].rej] for r in r2_regions ] +
                        [  [r[0] , regDict[r[0]].rej] for r in r3_regions ] 
                     ,
              baseCut=sr1Loose,
            )








plotQCOSregions=False
if plotQCOSregions:
  for region in QCosRegions:
    qcos=QCosR(*QCosRegions[region]);
    canvas[region]=ROOT.TCanvas()
    sample.Draw("Q80:CosLMet",sr1Loose.combined +"*weight","COLZ" );
    sample.Draw(qcos.r2.line2d,"","same");
    sample.Draw(qcos.r3.topLine2d,"","same");
    sample.Draw(qcos.r3.leftLine2d,"","same");
    sample.Draw(qcos.r1.line2d,"","same")
    canvas[region].SaveAs(saveDir+"/%s.png"%region)




