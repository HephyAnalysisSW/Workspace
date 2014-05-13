from commons import label, allMaps
import ROOT
c = ROOT.TChain('Events')
c.Add('/data/schoef/convertedMETTuples_v2//inc/dy53X_dy53X_rwTo_flat/histo_dy53X_from0To1.root')
c1 = ROOT.TCanvas()
c.Draw('candPt', 'candId=='+str(label['h_HF']))
c.Draw('candPt', 'candId=='+str(label['h']),'same')
