import ROOT

c = ROOT.TChain('Events')

##TTJEts
#c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2/hard/TTJets/TTJets_*.root')
#c.Add('/data/schoef/cmgTuples/postProcessed_v5_Phys14V2/soft/TTJets/TTJets_*.root')
#c.Add('/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/TTJets/TTJets_*.root')
##WJetsToLNu
#c.Add('/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/WJetsToLNu_HT100to200/*.root')
#c.Add('/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/WJetsToLNu_HT200to400/*.root')
#c.Add('/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/WJetsToLNu_HT400to600/*.root')
c.Add('/data/schoef/cmgTuples/postProcessed_v6_Phys14V2/hard/WJetsToLNu_HT600toInf/*.root')

#c.GetEntries()

#htBin = [(600,1000),(1000,1500),(1500,2000),(2000,5000)]
#htBin = [(600,900),(900,1300),(1300,1800),(1800,5000)]
htBin = [(600,800),(800,1000),(1000,1200),(1200,5000)]

histo = ROOT.TH1F('histo','histo',5000,0,5000)

c.Draw('Sum$(Jet_pt)>>histo')

xsec = 23.1363
Lumi = 4000
tot = histo.Integral()

print 'Full:' , tot
for bin in htBin:
  print bin
  Area = histo.Integral(bin[0],bin[1])
  print 'Area:' , Area , 'Area/tot:' , Area/tot , 'xsec*(Area/tot):' , xsec*(Area/tot)  , 'weightSim:' , xsec*(Area/tot)*Lumi/Area
   

