from analysisHelpers import *

ifname = '/afs/hephy.at/user/s/schoefbeck/www/pngFake2012/525_20fb_type1phiMet_minNJet6templates.root'
#ifname = '/afs/hephy.at/user/s/schoefbeck/www/pngFake2012/525_20fb_type1phiMet_templates_minNJet4.root'

htbins = [\
    [400,450   ],
    [450,500   ],
    [500,550   ],
    [550,600   ],
    [600,650   ],
    [650,700   ],
    [700,750   ],
    [750,800   ],
    [800,1000  ],
    [1000,1200 ],
    [1200,1500 ],
    [1500,2500 ]
  ]


for htb in htbins:
  template1b = getObjFromFile(ifname, 'met_shape_EleMu_b1_ht_'+str(htb[0])+'_'+str(htb[1]))
  template2 = getObjFromFile(ifname, 'met_shape_EleMu_b2_ht_'+str(htb[0])+'_'+str(htb[1]))
#  template1b = getObjFromFile(ifname, 'met_shape_b1_ht_'+str(htb[0])+'_'+str(htb[1])+'_njet_6')
#  template2 = getObjFromFile(ifname, 'met_shape_b2_ht_'+str(htb[0])+'_'+str(htb[1])+'_njet_6')

  c1 = ROOT.TCanvas()
  template1b.SetLineColor(ROOT.kBlue)
  template2.SetLineColor(ROOT.kGreen)
  template1b.SetMarkerColor(ROOT.kBlue)
  template2.SetMarkerColor(ROOT.kGreen)
  template1b.Draw()
  c1.SetLogy()
  template2.Draw("same")
  c1.Print("/afs/hephy.at/user/s/schoefbeck/www/pngFake2012/compare_fake_MET_"+str(htb[0])+'_'+str(htb[1])+".png")
  del c1
