import os
sms = "T5tttt"

if sms == "T5tttt":
  for varX in [800,900,1000,1100,1200]:
    varY_list = [x for x in range(225,int(varX)-175,50)]
    for varY in varY_list:
      fstringMu  = "/data/schoef/convertedTuples_v18/sigCont_1100/Mu/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
      fstringEle = "/data/schoef/convertedTuples_v18/sigCont_1100/Ele/"+sms+"_"+str(varX)+"_"+str(varY)+"/histo_"+sms+"_"+str(varX)+"_"+str(varY)+".root"
      print fstringMu, fstringEle
      print os.path.isfile(fstringMu), os.path.isfile(fstringEle)

sms = "T1t1t"

if sms == "T1t1t":
  for varX in [200,300,400,500,600,700,800]:
    varY_list = [x for x in range(100,int(varX)-100+1,50)]
    for varY in varY_list:
      fstringMu  = "/data/schoef/convertedTuples_v18/copyMET/Mu/"+sms+"_"+str(varY)+"_"+str(varX)+"/histo_"+sms+"_"+str(varY)+"_"+str(varX)+".root"
      fstringEle = "/data/schoef/convertedTuples_v18/copyMET/Ele/"+sms+"_"+str(varY)+"_"+str(varX)+"/histo_"+sms+"_"+str(varY)+"_"+str(varX)+".root"

      print fstringMu, fstringEle
      print os.path.isfile(fstringMu), os.path.isfile(fstringEle)

