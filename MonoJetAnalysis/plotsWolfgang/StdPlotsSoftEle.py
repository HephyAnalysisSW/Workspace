from StdPlotsEleBase import StdPlotsEleBase

class StdPlotsSoftEle(StdPlotsEleBase):

    def __init__(self,name,preselection=None,elist=None,elistBase="./elists",rebin=None):
        StdPlotsEleBase.__init__(self,name,preselection=preselection,elist=elist,elistBase=elistBase, \
                                     rebin=rebin,hardElectron=False)
