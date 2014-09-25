import ROOT
import math

f = ROOT.TFile("/afs/hephy.at/scratch/k/kwolf/CMSSW_5_2_4_patch1/src/Workspace/MTF2012_6j/output/erfFit_genmet_MuonElectron_jet5pt40_intLumi-20p0_convertedTuples_v16_with_weight_weight_130319_1032/ttjets_nonlin_hesseresult.root")
fitres = f.Get("nonlin_hesseResult")
params = f.Get("floatParsFinal")
C = ROOT.TMatrixDSym(2)
mu = ROOT.TMatrixD(2,1)
paramNames = ["erfMean2_ttjets", "erfScale2_ttjets"]
n = fitres.covarianceMatrix().GetNcols()
cv = fitres.covarianceMatrix()
for i in range( n):
  mu[i][0] = fitres.floatParsFinal().find(paramNames[i]).getVal() 
  for j in range( n):
    C[i][j] = cv[i][j]

f.Close()
#C[0][0] = 3.;
#C[1][0] = 2.;C[1][1] = 8.;
#C[2][0] = 0.;C[2][1] = 0.;C[2][2] = 11.;
#C[3][0] = 0.;C[3][1] = .1;C[3][2] = .2;C[3][3] = 7;
print "Correlation matrix:"
fitres.correlationMatrix().Print()


eigensys = ROOT.TMatrixDSymEigen(C)
O = ROOT.TMatrixD(eigensys.GetEigenVectors())
OT = ROOT.TMatrixD(ROOT.TMatrixD.kTransposed, O)
Lambda = ROOT.TMatrixDSym(2)
for i in range(2):
  Lambda[i][i] = eigensys.GetEigenValues()[i]

print "Should be zero:"
(C - ROOT.TMatrixD(ROOT.TMatrixD(O, ROOT.TMatrixD.kMult, Lambda), ROOT.TMatrixD.kMult, OT)).Print()

#mu = ROOT.TMatrixD(4,1)
#mu[0][0] = 1.
#mu[1][0] = 2.
#mu[2][0] = 3.
#mu[3][0] = 4.
#print "if (signErfcVar == 0) {"
#for j in range(0,4):
#  print "  "+cstring[j]+str((mu[j][0]))+');'
#print "}"
for i in range(2):
  LM = ROOT.TMatrixD(2, 1)
  LM[i][0] = math.sqrt(Lambda[i][i])
  shift = ROOT.TMatrixD(O,ROOT.TMatrixD.kMult, LM)
  for sign in [+1, -1]:
    print "Variation ",i,"sign",sign
    for j in range(2):
      print str((mu[j][0] + sign*shift[j][0]))

#for i in range(0,4):
#  LM = ROOT.TMatrixD(4,1)
#  LM[i][0] = math.sqrt(Lambda[i][i])
#  shift = ROOT.TMatrixD(O,ROOT.TMatrixD.kMult, LM)
#  sign = +1
#  offset=0
#  if mode=="WJets":
#    offset=8
#  print "if (modeErfcVar == "+str(offset+2*i)+") {"
#  for j in range(0,4):
#    print "  "+cstring[j]+str((mu[j][0] + sign*shift[j][0]))+' );'
#  print "}"
#  sign = -1
#  print "if (modeErfcVar == "+str(offset+2*i+1)+"){"
#  for j in range(0,4):
#    print "  "+cstring[j]+str((mu[j][0] + sign*shift[j][0]))+' );'
#  print "}"

