import ROOT
from array import array

class EventHelper:

    def __init__(self,tree):
        self.tree = tree
        self.entry = 0
        self.data = { }
        self.leafLength = array('i',[0])

    def getEntry(self,entry):
        self.entry = entry

    def nextEntry(self):
        self.entry += 1
        
    def typeRootToPython(self,type):
        if type=="Double_t":
            return 'd'
        if type=="Float_t":
            return 'f'
        if type=="Int_t":
            return 'i'
        if type=="ULong64_t":
            return 'L'
        raise Exception("Unknown / unsupported ROOT data type ",type)

    def getBranchAndLeaf(self,name):
        branch = self.tree.GetBranch(name)
        if not branch:
            raise Exception("Branch not found: ",name)
        leaves = branch.GetListOfLeaves()
        if leaves.GetEntries()!=1:
            raise Exception("No or more than one leaf in branch ",name)
        return (branch,leaves[0])
        
    def get(self,name):
        if not name in self.data:
            branch, leaf = self.getBranchAndLeaf(name)
            t = self.typeRootToPython(leaf.GetTypeName())
            lc = leaf.GetLeafCounter(self.leafLength)
            if lc:
                lcbranch,lcleaf = self.getBranchAndLeaf(lc.GetName())
                lcsize = lcleaf.GetMaximum()
                buff = array(t,[0]*lcsize)
                isArray = True
            else:
                buff = array(t,[0])
                isArray = False
            self.tree.SetBranchAddress(name,buff)
            self.data[name] = ( branch, leaf, buff, isArray )
        refs = self.data[name]
        refs[0].GetEntry(self.entry)
        if refs[3]:
            return refs[2]
        else:
            return refs[2][0]
    
