import sys
import ROOT

gname = "graph_smoothed_Obs"
if len(sys.argv)>2:
    gname = sys.argv[2]
tf = ROOT.TFile(sys.argv[1])
tf.ls()
g = tf.Get(gname)
n = g.GetN()
x = ROOT.Double(0.)
y = ROOT.Double(0.)
g.GetPoint(0,x,y)
print 0,x,y
g.GetPoint(n-1,x,y)
print n-1,x,y

