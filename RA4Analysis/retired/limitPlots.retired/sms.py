from array import *

class sms():

    def __init__(self, modelname):
        if modelname.find("T1tttt") != -1: self.T1tttt()
        if modelname.find("T1bbbb") != -1: self.T1bbbb()
        if modelname.find("T1t1t") != -1: self.T1t1t()
        if modelname.find("T5tttt") != -1: self.T5tttt()


    def T1tttt(self):
        # model name
        self.modelname = "T1tttt"
        # decay chain
        #self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow t #bar{t} #tilde{#chi}^{0}_{1}";
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow t #bar{t} #tilde{#chi}^{0}";
        # scan range to plot
        #self.Xmin = 600
        self.Xmin = 500
        self.Xmax = 1400
        self.Ymin = 0
        #self.Ymax = 800
        self.Ymax = 900
        # produce sparticle
        #self.sParticle = "m_{gluino} (GeV)"
        self.sParticle = "m(#tilde{g}) [GeV]"
        # LSP
        #self.LSP = "m_{LSP} (GeV)"        
        self.LSP = "m(#tilde{#chi}^{0}) [GeV]"        
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


    def T5tttt(self):
        # model name
        self.modelname = "T5tttt"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#scale[0.2]{ }#tilde{g}, #tilde{g} #rightarrow #tilde{t}#scale[0.3]{ }t, #tilde{t} #rightarrow t#scale[0.2]{ }#tilde{#chi}^{0}, m(#tilde{#chi}^{0})=50 GeV";
        #self.label= "#splitline{pp #rightarrow #tilde{g}#scale[0.2]{ }#tilde{g}, #tilde{g} #rightarrow #tilde{t}#scale[0.3]{ }t, #tilde{t} #rightarrow t#scale[0.2]{ }#tilde{#chi}^{0}}{m(#tilde{#chi}^{0})=50 GeV}";
        # scan range to plot
        self.Xmin = 875
        self.Xmax = 1400
        self.Ymin = 225
        self.Ymax = 1600
        # produce sparticle
        self.sParticle = "m(#tilde{g}) [GeV]"
        # LSP
        self.LSP = "m(#tilde{t}) [GeV]"        
        # diagonal position: 
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[0, 20000])


    def T1t1t(self):
        # model name
        self.modelname = "T1t1t"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#scale[0.2]{ }#tilde{g}, #tilde{g} #rightarrow #tilde{t}#scale[0.3]{ }t, #tilde{t} #rightarrow t#scale[0.2]{ }#tilde{#chi}^{0}, m(#tilde{g})=1 TeV";
        # scan range to plot
        #self.Xmin = 200
        self.Xmin = 400
        self.Xmax = 800
        #self.Ymin = 100
        self.Ymin = 200
        self.Ymax = 950
        # produce sparticle
        self.sParticle = "m(#tilde{t}) [GeV]"
        # LSP
        self.LSP = "m(#tilde{#chi}^{0}) [GeV]"        
        # diagonal position: 
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[0, 20000])
