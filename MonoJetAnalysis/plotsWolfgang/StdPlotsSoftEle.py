from StdElePlotsBase import StdElePlotsBase

class StdPlotsSoftEle(StdElePlotsBase):

    def __init__(self,name,preselection=None,elist=None,elistBase="./elists",rebin=None):
        StdElePlotsBase.__init__(self,name,preselection=preselection,elist=elist,elistBase=elistBase, \
                                     rebin=rebin,hardElectron=False)
