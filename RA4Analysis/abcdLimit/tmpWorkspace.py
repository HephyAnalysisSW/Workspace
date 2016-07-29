import sys
import ROOT

ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit.so")
tf = ROOT.TFile(sys.argv[1])
w = tf.Get("w")
vars = w.allVars()
iv = vars.createIterator()
v = iv.Next()
while v:
    assert v.getVal()==v.getValV()
    print "{0:30s} {1:10.2g} {2:10.2g} {3:10.2g} {4:10.2g}".format(v.GetName(),v.getVal(),v.getValV(),v.getMin(),v.getMax())
    v = iv.Next()
    
