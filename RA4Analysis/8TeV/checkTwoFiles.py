import ROOT
c = ROOT.TChain("Events")
d = ROOT.TChain("Events")
c.Add("/data/schoef/pat_120905/data8TeV/DoubleMu-Run2012B-13Jul2012/histo_134_1_UF8.root")
d.Add("/data/schoef/pat_120905/data8TeV/DoubleMu-Run2012B-13Jul2012/histo_77_1_pln.root")

events_c = []
for i in range(c.GetEntries()):
  c.GetEntry(i)
  events_c.append([c.GetLeaf(c.GetAlias("run")).GetValue(), c.GetLeaf(c.GetAlias("lumi")).GetValue(), c.GetLeaf(c.GetAlias("event")).GetValue()])
events_d = []
for i in range(d.GetEntries()):
  d.GetEntry(i)
  events_d.append([d.GetLeaf(d.GetAlias("run")).GetValue(), d.GetLeaf(d.GetAlias("lumi")).GetValue(), d.GetLeaf(d.GetAlias("event")).GetValue()])

for ev in events_d:
  if ev in events_c:
    print ev,"in both!!(A)"
for ev in events_c:
  if ev in events_d:
    print ev,"in both!!(B)"
