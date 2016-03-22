import ROOT
import math
#from Plot import Plot, Plots
from Workspace.HEPHYPythonTools.helpers import getChain


class Sample(dict):
    #def __init__(self, *args, **kwargs):
    #    super(Sample, self).__init__(*args, **kwargs)
    def __init__(self, name,tree=None,sample=None, isSignal=0,isData=0,color=0,lineColor=0,triggers="",filters="",weight="weight", **kwargs):
        super(Sample, self).__init__(name=name,tree=tree,sample=sample, isSignal=isSignal, isData=isData,color=color ,triggers=triggers, filters=filters,weight=weight,**kwargs)
        self.__dict__ = self 
        #print self
        #bool(self.tree) ^ bool(self.sample) , "Provide either a tree, or sampleDic in the form of {'bins'=[], 'dir':/path/to/bins/, 'name':SampleName}"
        if self.tree:
                pass
        if self.sample:
                if not self.tree:
                        self.tree = getChain(self.sample,histname='')
                else:
                        print "Will use the provided tree"
                self.dir    = self.sample['dir']
        self.tree.SetLineColor(self.color)
        #self.plots=Plots()
        self.plots={}



class Samples(dict):
    def __init__(self,    **kwargs):
        super(Samples, self).__init__(**kwargs)
        self.__dict__=self
        dataList= [samp for samp in self.__dict__ if    self[samp].isData ]
        if len(dataList)>0:
            includes_data= True
            print "--------- Samples include data,", dataList 
            for d in dataList:
                if self[d].isSignal:
                    assert False, ("A sample is Signal and Data??!... nice try, but NO! ", d)
                data_name = self[d]['name']
                data_lumi = self[d]['lumi']
                weight_name = data_name +"_weight"
                print "--------- %s will be created for MC samples using the data lumi:    %s fb-1 "%(weight_name, data_lumi)
                for samp in self:
                    if not self[samp].isData:
                        self[samp][weight_name] = "({w})*({dlumi})/({mclumi})".format(w=self[samp].weight, dlumi=data_lumi, mclumi=self[samp].lumi)
            

    def addWeight(self, weight, sampleList=[]):
        if not sampleList:
            bkgList = self.bkgList()
            sigList = self.sigList()
            sampleList = bkgList + sigList

        for samp in sampleList:
            if not hasattr(self[samp],"weight"):
                new_weight  = weight
            else:
                new_weight = "(%s *  %s)"%(self[samp]["weight"], weight)
            self[samp]["weight"] = new_weight
    


    def bkgList(self):
        return [samp for samp in self.__dict__.keys() if not self[samp].isSignal and not self[samp].isData ] 
    def sigList(self):
        return [samp for samp in self.__dict__.keys() if self[samp].isSignal and not self[samp].isData ] 
    def privSigList(self):
        return [samp for samp in self.__dict__.keys() if self[samp].isSignal==2 and not self[samp].isData ] 
    def massScanList(self):
        return [samp for samp in self.__dict__.keys() if self[samp].isSignal==1 and not self[samp].isData ] 
    def dataList(self):
        return [samp for samp in self.__dict__.keys() if not self[samp].isSignal and  self[samp].isData ] 


 
        #self.iterall = self.all.itervalues
    def doStuff(self):        #### not sure how to add these without messing with the class/dict structre    
        print [ self[samp].isData for samp in self.__dict__ ]
        self.all = [samp for samp in self.__dict__ ] 
        self.bkgs = [samp for samp in self.all if not self[samp].isData and not self[samp].isSignal ]
        self.sigs = [samp for samp in self.all if self[samp].isSignal ]
        self.data= [samp for samp in self.all if    self[samp].isData ]
        if any( [self[samp].isData and self[samp].isSignal for samp in self.all ] ):
            assert "A sample is Signal and Data??!... nice try, but no!"

        if len(ndata)>0:
            print "Samples include data", "MC will be reweighted based on data lumi"
            self.includes_data= True
            
        else:
            self.includes_data= False
  




