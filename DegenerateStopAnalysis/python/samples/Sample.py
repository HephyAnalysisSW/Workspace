import os
import ROOT
from Workspace.HEPHYPythonTools.helpers import getChain

class Sample(dict):
    def __init__(self, name,tree=None,sample=None, isSignal=0,isData=0,color=0,lineColor=0,triggers="",filters="",weight="weight",weights=None, **kwargs):
        super(Sample, self).__init__(name=name,tree=tree,sample=sample, isSignal=isSignal, isData=isData,color=color ,triggers=triggers, filters=filters,weight=weight,weights=weights,**kwargs)
        self.__dict__ = self
        self.dir    = self.sample['dir']
        self.plots = {}    
    
        # FIXME read tree only when needed
        if getattr(self, 'tree'):  
            self.chain = self.tree
        delattr(self, 'tree')  # removing the attr so the chain is added only when needed#
        hasFriend      = getattr(self, 'friend',False)
        self._getTree()

    def _getTree(self):
        if hasattr(self, 'chain'):
                #print "Will use the provided tree"
                self.tree = self.chain
        else:#if self.sample:
                self.tree = getChain(self.sample,histname='')
        self.tree.SetLineColor(self.color)

    # FIXME 
    def __getattr__(self, attr):
        if attr=='tree':
            print 'Getting %s'%attr
            self._getTree()
            self.__dict__[attr]= self.tree
            return self.tree
        else:  
            raise AttributeError, attr
    def __getitem__(self, item):
        if item=='tree':
            return getattr(self, item)
        else:
            return dict.__getitem__(self, item) 

    def findFriendTrees(self, these_to_those ):
        fileList = [x.GetTitle() for x in self.tree.GetListOfFiles()]
        friendFileList = []
        for f in fileList:
            nf = f[:]
            for this, that in these_to_those:
                nf = nf.replace(this,that)
            friendFileList.append(nf)
        return friendFileList

    def addFriendTrees(self, friendTreeName, these_to_those, alias= "", check_nevents=True):
        friendTree = ROOT.TChain(friendTreeName)
        friendFileList = self.findFriendTrees( these_to_those )
        allIsGood = True
        for f in friendFileList:
            if not os.path.isfile(f):
                print "Supposed Friend Tree does not seem to exist %s"%f
                allIsGood=False
            friendTree.Add(f)
        self.tree.AddFriend(friendTree, alias) 
        if check_nevents:
            nevts = self.tree.GetEntries()
            nfevts = friendTree.GetEntries()
            if not nevts == nfevts:
                print "!!!!!!!!!!!!!!!!!!!!!    WARNING       !!!!!!!!!!!!!!!!!!!!!!"
                print "For Sample %s Number of Events for the tree and friend tree don't match! %s vs %s"%(self.name, nevts, nfevts)
                nbadevents = self.tree.Draw("(1)", "evt!=evNumber")
                if not nbadevents:
                    print "But they seem to match event by event....seems OK, but MAKE SURE IT IS!"
                else:
                    print "There seem to a mismatch between event numbers individually... i.e. try this: %s"%'tree.Draw("(1)", "evt!==evNumber")'
                    raise Exception()
        return allIsGood

class Samples(dict):
    def __init__(self,    **kwargs):
        super(Samples, self).__init__(**kwargs)
        self.__dict__=self
        dataList= self.dataList()
        if len(dataList)>0:
            includes_data= True
            print "\nSamples include data:", dataList 

    def bkgList(self):
        return sorted([samp for samp in self.__dict__.keys() if not self[samp].isSignal and not self[samp].isData])
    def sigList(self):
        return sorted([samp for samp in self.__dict__.keys() if self[samp].isSignal and not self[samp].isData])
    def privSigList(self):
        return sorted([samp for samp in self.__dict__.keys() if self[samp].isSignal==2 and not self[samp].isData])
    def massScanList(self):
        return sorted([samp for samp in self.__dict__.keys() if self[samp].isSignal==1 and not self[samp].isData])
    def otherSigList(self):
        return sorted([samp for samp in self.__dict__.keys() if self[samp].isSignal==3 and not self[samp].isData])
    def dataList(self):
        return sorted([samp for samp in self.__dict__.keys() if not self[samp].isSignal and  self[samp].isData])
