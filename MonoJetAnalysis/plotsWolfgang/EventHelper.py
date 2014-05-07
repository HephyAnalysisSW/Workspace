#
# Helper class to read contents of (simple) trees (like the converted analysis tuples)
#   Handles the assignment of buffers and caches values for multiple access
#   Does not work correctly on chains (needs one instance / tree)
# Typical sequence:
# - Instantiate once / tree
# - call getEntry(entry) once / entry
# - call eh.get("<branch name>") for each branch needed
import ROOT
from array import array

class EventHelper:
    #
    # initialize buffer
    #
    def __init__(self,tree):
        self.tree = tree
        self.entry = 0
        self.data = { }
        self.leafLength = array('i',[0])
    #
    # prepare reading of "entry", reset all buffered branches to invalid
    #
    def getEntry(self,entry):
        self.entry = entry
        for v in self.data.values():
            # set length to invalid
            v[4] = -1
    #
    # prepare reading of next entry (no check for end-of-tree!!)
    #
    def nextEntry(self):
#        self.entry += 1
        self.getEntry(self.entry+1)
        
    #
    # helper function: convert root data type to character suitable for array 
    #
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
    #
    # return branch and leaf corresponding to "name" (multiple leaves are not supported)
    #
    def getBranchAndLeaf(self,name):
        branch = self.tree.GetBranch(name)
        if not branch:
            raise Exception("Branch not found: ",name)
        leaves = branch.GetListOfLeaves()
        if leaves.GetEntries()!=1:
            raise Exception("No or more than one leaf in branch ",name)
        return (branch,leaves[0])
    #
    # retrieve data for branch "name"
    #
    def get(self,name):
        #
        # create buffer on first call for this branch
        #
        if not name in self.data:
            branch, leaf = self.getBranchAndLeaf(name)
            t = self.typeRootToPython(leaf.GetTypeName())
            lc = leaf.GetLeafCounter(self.leafLength)
            if lc:
                # arrays: assign maximum leaf size to buffer
                lcbranch,lcleaf = self.getBranchAndLeaf(lc.GetName())
                lcsize = lcleaf.GetMaximum()
                buff = array(t,[0]*lcsize)
                isArray = True
            else:
                # scalar: assign one element to buffer
                buff = array(t,[0])
                isArray = False
            # set ROOT branch address and enter buffer to local store
            self.tree.SetBranchAddress(name,buff)
            self.data[name] = [ branch, leaf, buff, isArray, -1 ]
        #
        # retrieve data (from tree or cache)
        #
        refs = self.data[name]
        # if cache length is invalid: read data and leaf length from tree
        if refs[4]<0:
            refs[0].GetEntry(self.entry)
            refs[4] = refs[1].GetLen()
            assert len(refs[2])>=refs[4] # and refs[4]>0
        # for arrays: return only the first part according to the leaf length
        if refs[3]:
            return refs[2][:refs[4]]
        # else: return scalar
        else:
            assert refs[4]==1
            return refs[2][0]
    
