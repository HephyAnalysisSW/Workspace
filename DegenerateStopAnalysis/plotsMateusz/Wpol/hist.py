from ROOT import *

def h1f(name,nb,x1,x2):
    if x2 == -999:
        hh = TH1F(name,"",nb,x1)
    else:
        hh = TH1F(name,"",nb,x1,x2)
    hh.Sumw2()
    return hh
def h2f(name,nbx,x1,x2,nby,y1,y2):
    hh = TH2F(name,"",nbx,x1,x2,nby,y1,y2)
    return hh
