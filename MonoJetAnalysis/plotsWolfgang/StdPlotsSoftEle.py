from StdPlotsBase import StdPlotsBase

class StdPlotsSoftEle(StdPlotsBase):

    def __init__(self,name,preselection=None,elist=None,elistBase="./elists",rebin=None):
        StdPlotsBase.__init__(self,name,preselection=preselection,elist=elist,elistBase=elistBase, \
                                  rebin=rebin,leptonPdg=11,hardLepton=False)
