from StdElePlotsBase import StdElePlotsBase

class StdPlotsHardEle(StdElePlotsBase):

    def __init__(self,name,preselection=None,elist=None,elistBase="./elists",rebin=None):
        StdElePlotsBase.__init__(self,name,preselection=preselection,elist=elist,elistBase=elistBase, \
                                     rebin=rebin,hardElectron=True)
