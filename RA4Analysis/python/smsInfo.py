nfsDirectories = {}

nfsDirectories["T5tttt"] =  ["/data/mhickel/pat_130426/8TeV-T5tttt_mGo-800to1200_mStop-225to1025_mLSP_50", \
                            "/data/mhickel/pat_130426/8TeV-T5tttt_mGo-800to1200_mStop-225to1025_mLSP_50_1000_1075", \
                            "/data/mhickel/pat_130426/8TeV-T5tttt_mGo-800to1200_mStop-225to1025_mLSP_50_1075_1175", \
                            "/data/mhickel/pat_130426/8TeV-T5tttt_mGo-800to1200_mStop-225to1025_mLSP_50_1175_1200", \
                            "/data/mhickel/pat_130426/8TeV-T5tttt_mGo-800to1200_mStop-225to1025_mLSP_50_900_1000",\
                            "/data/mhickel/pat_130426/8TeV-T5tttt_mGo-800to1200_mStop-225to1025_mLSP_50_1225_1400"]

def getT5ttttMadgraphDirs(mgl=-1):
  if mgl==-1:
    return nfsDirectories["T5tttt"]
  if mgl<1000:
    return ["/data/mhickel/pat_130426/8TeV-T5tttt_mGo-800to1200_mStop-225to1025_mLSP_50"]
  if mgl>=1000 and mgl<1075:
    return ["/data/mhickel/pat_130426/8TeV-T5tttt_mGo-800to1200_mStop-225to1025_mLSP_50_1000_1075"]
  if mgl>=1075 and mgl<=1175:
    return ["/data/mhickel/pat_130426/8TeV-T5tttt_mGo-800to1200_mStop-225to1025_mLSP_50_1075_1175"]
  if mgl>=1175 and mgl<=1200:
    return ["/data/mhickel/pat_130426/8TeV-T5tttt_mGo-800to1200_mStop-225to1025_mLSP_50_1175_1200"]
  if mgl>=1225 and mgl<=1400:
    return ["/data/mhickel/pat_130426/8TeV-T5tttt_mGo-800to1200_mStop-225to1025_mLSP_50_1225_1400"]
  if mgl>=900 and mgl<=1000:
    return ["/data/mhickel/pat_130426/8TeV-T5tttt_mGo-800to1200_mStop-225to1025_mLSP_50_900_1000"]
  return []

def getT1ttttMadgraphDirs(mgl=-1, mN=-1):
  if mgl==-1 and mN==-1:
    return [\
      "/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-1025to1200-v1",
      "/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-25to500-v2",
      "/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2",
      "/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-400to750_mLSP-1_50-v1",
      "/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-400to750_mLSP-25to550-v1",
      "/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-775to1075_mLSP-25to500-v1",
      "/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-775to1075_mLSP-25to500-v3",
      "/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-775to1075_mLSP-525to875-v2",
      "/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-775to1075_mLSP-525to875-v3",
      "/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-800to1400_mLSP-1to50-v2"]

  if mgl>=400 and mgl<=750 and mN>=25 and mN<=550:
    return ["/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-400to750_mLSP-25to550-v1/"]   
  if mgl>=775  and mgl<= 1075   and mN>=  25     and mN<= 500:
    return ["/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-775to1075_mLSP-25to500-v1/", "/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-775to1075_mLSP-25to500-v3/"]
  if mgl>=775  and mgl<= 1075   and mN>=  525    and mN<= 875:
    return ["/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-775to1075_mLSP-525to875-v2/", "/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-775to1075_mLSP-525to875-v3/"]
  if mgl>=1100 and mgl<= 1400   and mN>=  1025   and mN<= 1200:
    return ["/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-1025to1200-v1/"]
  if mgl>=1100 and mgl<= 1400   and mN>=  25     and mN<= 500:
    return ["/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-25to500-v2/"]
  if mgl>=1100 and mgl<= 1400   and mN>=  525    and mN<= 1000:
    return ["/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-1100to1400_mLSP-525to1000-v2/"]
  if mgl>=400  and mgl<= 750    and mN>=  0      and mN<= 50:
    return ["/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-400to750_mLSP-1_50-v1/"]
  if mgl>=800  and mgl<= 1400   and mN>=  0      and mN<= 50:
    return ["/data/mhickel/pat_130426/8TeV-T1tttt_2J_mGo-800to1400_mLSP-1to50-v2/"]
  return []

nfsDirectories["T1tttt-madgraph"] = getT1ttttMadgraphDirs()
 
nfsDirectories["T1t1t"] = ["/data/mhickel/pat_130426/8TeV-T1t1t_2J_mGo-1000_mStop-200to750_mLSP-100to650", \
                           "/data/mhickel/pat_130426/8TeV-T1t1t_2J_mGo-1000_mStop-350to750_mLSP-100to500", \
                           "/data/mhickel/pat_130426/8TeV-T1t1t_2J_mGo-1000_mStop-775to825_mLSP-575to725", \
                            "/data/mhickel/pat_130426/8TeV-T1t1t_2J_mGo-1000_mStop-800to800_mLSP-100to550"]

nfsDirectories["T1tttt"] = ["/data/mhickel/pat_130426/8TeV-T1tttt/"]

th2Binning = {}
th2VarString = {}
xAxisTitle = {}
yAxisTitle = {}

th2Binning["T1tttt"] = [48, 400, 1600, 52, 0, 1300]
th2Binning["T1tttt_coarse"] = [48/4, 400, 1600, 52/4, 0, 1300]
th2VarString["T1tttt"] = "osetMN:osetMgl"
xAxisTitle["T1tttt"] = "m(#tilde{g}) [GeV]"
yAxisTitle["T1tttt"] = "m(#tilde{#chi}) [GeV]"

th2Binning["T1tttt-madgraph"] = [48, 400, 1600, 52, 0, 1300]
th2Binning["T1tttt-madgraph_coarse"] = [48/4, 400, 1600, 52/4, 0, 1300]
th2VarString["T1tttt-madgraph"] = "osetMN:osetMgl"
xAxisTitle["T1tttt-madgraph"] = "m(#tilde{g}) [GeV]"
yAxisTitle["T1tttt-madgraph"] = "m(#tilde{#chi}) [GeV]"

th2Binning["T1t1t"] = [29, 100, 825, 29, 100, 825]
th2VarString["T1t1t"] = "osetMN:osetMsq"
xAxisTitle["T1t1t"] = "m(#tilde{t}) [GeV]"
yAxisTitle["T1t1t"] = "m(#tilde{#chi}) [GeV]"


th2Binning["T5tttt"] = [ 25, 800, 1425, 43, 200,1275]
th2VarString["T5tttt"] = "osetMsq:osetMgl"
xAxisTitle["T5tttt"] = "m(#tilde{g}) [GeV]"
yAxisTitle["T5tttt"] = "m(#tilde{t}) [GeV]"
