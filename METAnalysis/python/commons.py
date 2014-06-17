from math import pi
#energyBins = [[0,0.5],[0.5,1], [1,2],[2,3], [3,10], [10,-999]]
ptBins = [[0,0.5],[0.5,1], [1,2],[2,3], [3,10], [10,20], [20,-999]]
#energyBins = {\
#        'h': [[0,0.5],[0.5,1], [1,2],[2,3], [3,10], [10,-999]],
#        'h0Barrel':[[0,0.5],[0.5,1], [1,2],[2,3], [3,10], [10,-999]],

def getPtBin(pt):  
  for b in ptBins:
    if pt>=b[0] and (pt<b[1] or b[1]<0):
      return b

pfTypes = ["X", "h", "e", "mu", "gamma", "h0", "h_HF", "egamma_HF"]
label = {"X":0,"h":1, "e":2, "mu":3,"gamma":4, 'h0':5, 'h_HF':6, 'egamma_HF':7, 0:"X",1:"h", 2:"e", 3:"mu",4:"gamma", 5:'h0', 6:'h_HF', 7:'egamma_HF'}

h             = {'name':'h', 'type':'h',  'binning':[108,-2.7,2.7,160,-pi,pi]}
h0Barrel      = {'name':'h0Barrel', 'type':'h0',  'binning':[32,-1.392,1.392,72,-pi,pi]}
h0EndcapPlus  = {'name':'h0EndcapPlus', 'type':'h0',  'binning':[12,1.392,3,36/2,-pi,pi]}
h0EndcapMinus = {'name':'h0EndcapMinus', 'type':'h0',  'binning':[12,-3.000, -1.392,36/2,-pi,pi]}
gammaBarrel      = {'name':'gammaBarrel', 'type':'gamma',  'binning':[2*85,-1.479,1.479,360,-pi,pi]}
gammaEndcapPlus  = {'name':'gammaEndcapPlus', 'type':'gamma',  'binning':[20,1.479,3.,30,-pi,pi]}
gammaEndcapMinus = {'name':'gammaEndcapMinus', 'type':'gamma',  'binning':[20,-3.,-1.479, 30,-pi,pi]}
gammaForwardPlus  = {'name':'gammaForwardPlus', 'type':'gamma',  'binning':[20,3.,5.,30,-pi,pi]}
gammaForwardMinus = {'name':'gammaForwardMinus', 'type':'gamma',  'binning':[20,-5.,-3., 30,-pi,pi]}
e             = {'name':'e', 'type':'e',  'binning':[108/4,-2.7,2.7,160/4,-pi,pi]}
mu            = {'name':'mu','type':'mu', 'binning':[108/4,-2.4,2.4,160/4,-pi,pi]}

etaMaxDepth1 = 4.78
etaMinDepth1 = 2.901376
nEtaBinsHF = 11
h_HF_Minus        = {'name':'h_HFMinus', 'type':'h_HF',  'binning':[nEtaBinsHF,-etaMaxDepth1,-etaMinDepth1,18,-pi,pi]}
h_HF_Plus         = {'name':'h_HFPlus', 'type':'h_HF',   'binning':[nEtaBinsHF,etaMinDepth1,etaMaxDepth1,18,-pi,pi]}

etaMaxDepth1 = 5.2
etaMinDepth1 = 4.78
nEtaBinsHF = 2
h_HF_InnerMostRingsMinus        = {'name':'h_HFInnerMostRingsMinus', 'type':'h_HF', 'binning':[nEtaBinsHF,-etaMaxDepth1,-etaMinDepth1,18,-3.15,3]}
h_HF_InnerMostRingsPlus         = {'name':'h_HFInnerMostRingsPlus', 'type':'h_HF',  'binning':[nEtaBinsHF,etaMinDepth1,etaMaxDepth1,18,-3.15,3]}

etaMaxDepth1 = 4.78
etaMinDepth1 = 2.901376
nEtaBinsHF = 11
egamma_HF_Minus        = {'name':'egamma_HFMinus', 'type':'egamma_HF',  'binning':[nEtaBinsHF,-etaMaxDepth1,-etaMinDepth1,18,-pi,pi]}
egamma_HF_Plus         = {'name':'egamma_HFPlus', 'type':'egamma_HF',   'binning':[nEtaBinsHF,etaMinDepth1,etaMaxDepth1,18,-pi,pi]}

h_HF         = {'name':'h_HF', 'type':'h_HF',   'binning':[-1,-5.5,5.5,18,-pi,pi]}
egamma_HF         = {'name':'egamma_HF', 'type':'egamma_HF',   'binning':[-1,-5.5,5.5,18,-pi,pi]}

etaMaxDepth1 = 5.2
etaMinDepth1 = 4.78
nEtaBinsHF = 2
egamma_HF_InnerMostRingsMinus        = {'name':'egamma_HFInnerMostRingsMinus', 'type':'egamma_HF', 'binning':[nEtaBinsHF,-etaMaxDepth1,-etaMinDepth1,9,-pi-.1,pi]}
egamma_HF_InnerMostRingsPlus         = {'name':'egamma_HFInnerMostRingsPlus', 'type':'egamma_HF',  'binning':[nEtaBinsHF,etaMinDepth1,etaMaxDepth1,9,-pi-.1,pi]}

h['candBinning'] = [50,0,1500]
h0Barrel['candBinning'] = [50,0,50]
h0EndcapPlus['candBinning'] = [50,0,50]
h0EndcapMinus['candBinning'] = [50,0,50]
gammaBarrel['candBinning'] = [25,0,500]
gammaEndcapPlus['candBinning'] = [25,0,150]
gammaEndcapMinus['candBinning'] = [25,0,150]
gammaForwardPlus['candBinning'] = [10,0,10]
gammaForwardMinus['candBinning'] = [10,0,10]
e['candBinning'] = [10,0,10]
mu['candBinning'] = [10,0,10]
h_HF_Minus['candBinning'] = [25,0,250]
h_HF_Plus['candBinning'] = [25,0,250]
h_HF_InnerMostRingsMinus['candBinning'] = [25,0,50]
h_HF_InnerMostRingsPlus['candBinning'] = [25,0,50]
egamma_HF_Minus['candBinning'] = [25,0,250]
egamma_HF_Plus['candBinning'] = [25,0,250]
egamma_HF_InnerMostRingsMinus['candBinning'] = [25,0,50]
egamma_HF_InnerMostRingsPlus['candBinning'] = [25,0,50]
h_HF['candBinning'] = [25,0,500]
egamma_HF['candBinning'] = [25,0,500]


allMaps = [h, h0Barrel, h0EndcapPlus, h0EndcapMinus, gammaBarrel, gammaEndcapPlus, gammaEndcapMinus, gammaForwardPlus, gammaForwardMinus, e, h_HF_Minus, h_HF_Plus, \
           h_HF_InnerMostRingsMinus, h_HF_InnerMostRingsPlus, egamma_HF_Minus, egamma_HF_Plus, egamma_HF_InnerMostRingsMinus, egamma_HF_InnerMostRingsPlus]

#categories = {\
#  "gamma":[ ["gamma_mE", -99, -1.4  ],
#            ["gamma_mB", -1.4, 0.   ],
#            ["gamma_pB", 0., 1.4    ],
#            ["gamma_pE", 1.4, 99    ]],
#  "h":[ ["h_mE", -99., -1.5  ],
#        ["h_mB", -1.5, 0.   ],
#        ["h_pB", 0., 1.5    ],
#        ["h_pE", 1.5, 99    ]],
#  'h0':[["h0_mE", -99, -1.4  ],
#        ["h0_mB", -1.4, 0.   ],
#        ["h0_pB", 0., 1.4    ],
#        ["h0_pE", 1.4, 99    ]],
#  'h_HF':[["h_HF_m", -99., 0.],
#          ["h_HF_p", 0., 99.]],
#  'egamma_HF':[["egamma_HF_m", -99., 0.],
#               ["egamma_HF_p", 0., 99.]]
#}
#
