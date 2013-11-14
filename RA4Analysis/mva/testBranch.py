import ROOT, ctypes
bufNewVal = ctypes.c_float(0.)
newTree = ROOT.TTree("Events", "Events")
newTree.Branch("var1", ctypes.addressof(bufNewVal), "var1/F")
#bufNewVal.value = vtxWeight*MCWeight
#newTree.Fill()

