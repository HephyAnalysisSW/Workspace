from array import *

class sms():

    def __init__(self, modelname):
        if modelname.find("T1tttt") != -1: self.T1tttt()
        if modelname.find("T1bbbb") != -1: self.T1bbbb()
        if modelname == "T2DegStop"  : self.T2DegStop()
        if modelname == "T2bW" : self.T2bW()
        if modelname == "T2DegStop_dm"  : self.T2DegStop_dm()
        if modelname == "T2bW_dm" : self.T2bW_dm()
        if modelname == "T2DegStop_signif"  : self.T2DegStop_signif()
        if modelname == "T2bW_signif" : self.T2bW_signif()


    def T1tttt(self):
        # model name
        self.modelname = "T1tttt"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow t #bar{t} #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 600
        self.Xmax = 1400
        self.Ymin = 0
        self.Ymax = 800
        # produce sparticle
        self.sParticle = "m_{gluino} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"        
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 80
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        
        
    def T1bbbb(self):
        # model name
        self.modelname = "T1bbbb"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow b #bar{b} #tilde{#chi}^{0}_{1}";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 400
        self.Xmax = 1600
        self.Ymin = 0
        self.Ymax = 1200
        # produce sparticle
        self.sParticle = "m_{gluino} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[0, 20000])

    def T2DegStop(self):
        # model name
        self.modelname = "T2DegStop"
        # decay chain
        self.label= "pp #rightarrow #tilde{t} #tilde{t}, #tilde{t} #rightarrow b f f' #tilde{#chi}^{0}_{1}"
        # scan range to plot
#        self.Xmin = 87.5
#        self.Xmax = 412.5
#        self.Ymin = 17.5
#        self.Ymax = 392.5
        self.Xmin = 250
        self.Xmax = 800
        self.Ymin = 100
        self.Ymax = 900
        # produce sparticle
        self.sParticle = "m(#tilde{t}) [GeV]"
        # LSP
        self.LSP = "m(#tilde{#chi}^{0}_{1}) [GeV]"        
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 80
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        

    def T2bW(self):
        # model name
        self.modelname = "T2bW"
        # decay chain
        self.label= "pp #rightarrow #tilde{t} #tilde{t}, #tilde{t} #rightarrow #tilde{#chi}^{#pm}_{1} b,#tilde{#chi}^{#pm}_{1} #rightarrow b f f' #tilde{#chi}^{0}_{1}"
        #self.extraText = "#Deltam(#tilde{#chi}^{#pm}_{1}, #tilde{#chi}^{0}_{1})=5 GeV"
        self.extraText = "m(#tilde{#chi}^{#pm}_{1})=0.5*(m(#tilde{t})+m(#tilde{#chi}^{0}_{1}))"
        # scan range to plot
        self.Xmin = 250
        self.Xmax = 800
        self.Ymin = 100
        self.Ymax = 900
        # produce sparticle
        self.sParticle = "m(#tilde{t}) [GeV]"
        # LSP
        self.LSP = "m(#tilde{#chi}^{0}_{1}) [GeV]"        
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 80
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        


    def T2DegStop_dm(self):
        self.T2DegStop()
        self.modelname = "T2DegStop_dm"
        self.dmplot    = True
        self.Xmin = 250
        self.Xmax = 800
        self.Ymin = 10
        self.Ymax = 100
        # LSP
        self.LSP = "#Deltam(#tilde{t},#tilde{#chi}^{0}_{1}) [GeV]"        
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 80
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        

    def T2bW_dm(self):
        self.T2bW()
        self.modelname = "T2bW_dm"
        self.dmplot    = True
        self.Xmin = 250
        self.Xmax = 800
        self.Ymin = 10
        self.Ymax = 100
        self.LSP = "#Deltam(#tilde{t},#tilde{#chi}^{0}_{1}) [GeV]"        
        mW = 80
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        

    def T2bW_signif(self):
        self.T2bW_dm()
        self.Ymin = 10
        self.Ymax = 90
        self.signifPlot=True

    def T2DegStop_signif(self):
        self.T2DegStop_dm()
        self.Ymin = 10
        self.Ymax = 90
        self.signifPlot=True


