# loop looks like this: for njb in signalRegion2fb: for stb in signalRegion2fb[njb]: for htb in signalRegion2fb[njb][stb]: print signalRegion2fb[njb][stb][htb]['deltaPhi']

signalRegion40pb = {(5,5): {(250, 350): {(500, -1): {'deltaPhi': .5}},
                            (350, -1):  {(500, -1): {'deltaPhi': .5}}},
                    (6,-1):{(250, 350): {(500, -1): {'deltaPhi': .5}},
                            (350, -1):  {(500, -1): {'deltaPhi': .5}}}
                   }

signalRegionCRonly = {(5,5): {(250, -1): {(500, -1): {'deltaPhi': .5}}},
                    (6,-1):{(250, -1): {(500, -1): {'deltaPhi': .5}}}
                   }
oneRegion = {(5,5): {(250, 350): {(500, -1): {'deltaPhi': 1.}}}}

smallRegion = {(5,5): {(250, 350): {(500, -1): {'deltaPhi': 1.}}},
               (6,7):{(250, 350): {(500, 750): {'deltaPhi': 1.}}}
              }

signalRegion2fb = {(5, 5): {(250, 350): {(500, -1): {'deltaPhi': 1.0}},
                            (350, 450): {(500, -1): {'deltaPhi': 1.0}},
                            (450, -1): {(500, -1): {'deltaPhi': 1.0}}},
                   (6, 7): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
                                         (750, -1): {'deltaPhi': 1.0}},
                            (350, 450): {(500, -1): {'deltaPhi': 1.0}},
                            (450, -1): {(500, 750): {'deltaPhi': 1.0},
                                        (750, -1): {'deltaPhi': 1.0}}},
                   (8, -1): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
                                          (750, -1): {'deltaPhi': 1.0}},
                             (350, 450): {(500, -1): {'deltaPhi': 1.0}},
                             (450, -1): {(500, 750): {'deltaPhi': 1.0},
                                         (750, -1): {'deltaPhi': 1.0}}}
                  }

signalRegion3fbStaticDPhi = {(5, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}},
                            (350, 450): {(500, -1):   {'deltaPhi': 1.0}},
                            (450, -1): {(500, -1):    {'deltaPhi': 1.0}}},
                   (6, 7): {(250, 350): {(500, 750):  {'deltaPhi': 1.0},
                                         (750, -1):   {'deltaPhi': 1.0}},
                            (350, 450): {(500, 750):  {'deltaPhi': 1.0},
                                         (750, -1):   {'deltaPhi': 1.0}},
                            (450, -1): {(500, 750):   {'deltaPhi': 1.0},
                                        (750, 1250):  {'deltaPhi': 1.0},
                                        (1250, -1):   {'deltaPhi': 1.0}}},
                   (8, -1): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
                                          (750, -1):  {'deltaPhi': 1.0}},
                             (350, 450): {(500, -1):  {'deltaPhi': 1.0}},
                             (450, -1): {(500, -1):   {'deltaPhi': 1.0}}}}


#signalRegion3fb = {(5, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0}},
#                            (350, 450): {(500, -1):   {'deltaPhi': 1.0}},
#                            (450, -1): {(500, -1):    {'deltaPhi': 1.0}}},
#                   (6, 7): {(250, 350): {(500, 750):  {'deltaPhi': 1.0},
#                                         (750, -1):   {'deltaPhi': 1.0}},
#                            (350, 450): {(500, 750):  {'deltaPhi': 1.0},
#                                         (750, -1):   {'deltaPhi': 1.0}},
#                            (450, -1): {(500, 750):   {'deltaPhi': 0.75},
#                                        (750, 1250):  {'deltaPhi': 0.75},
#                                        (1250, -1):   {'deltaPhi': 0.75}}},
#                   (8, -1): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
#                                          (750, -1):  {'deltaPhi': 1.0}},
#                             (350, 450): {(500, -1):  {'deltaPhi': 0.75}},
#                             (450, -1): {(500, -1):   {'deltaPhi': 0.75}}}}

signalRegion3fb = {(5, 5):  {(250, 350): {(500, -1):   {'deltaPhi': 1.0, 'njet':'5j','LT':'L_{T}1','HT': 'H_{T}i',      'tex':'\\textrm{5j}, \\textrm{L}_T1, \\textrm{H}_Ti'}},
                             (350, 450): {(500, -1):   {'deltaPhi': 1.0, 'njet':'5j','LT':'L_{T}2','HT': 'H_{T}i',      'tex':'\\textrm{5j}, \\textrm{L}_T2, \\textrm{H}_Ti'}},
                             (450, -1):  {(500, -1):   {'deltaPhi': 1.0, 'njet':'5j','LT':'L_{T}3','HT': 'H_{T}i',      'tex':'\\textrm{5j}, \\textrm{L}_T3, \\textrm{H}_Ti'}}},
                   (6, 7):  {(250, 350): {(500, 750):  {'deltaPhi': 1.0, 'njet':'6-7j','LT':'L_{T}1','HT': 'H_{T}1',    'tex':'\\textrm{6-7j}, \\textrm{L}_T1, \\textrm{H}_T1'},
                                          (750, -1):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'L_{T}1','HT': 'H_{T}23',   'tex':'\\textrm{6-7j}, \\textrm{L}_T1, \\textrm{H}_T23'}},
                             (350, 450): {(500, 750):  {'deltaPhi': 1.0, 'njet':'6-7j','LT':'L_{T}2','HT': 'H_{T}1',    'tex':'\\textrm{6-7j}, \\textrm{L}_T2, \\textrm{H}_T1'},
                                          (750, -1):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'L_{T}2','HT': 'H_{T}23',   'tex':'\\textrm{6-7j}, \\textrm{L}_T2, \\textrm{H}_T23'}},
                             (450, -1):  {(500, 1000): {'deltaPhi': 0.75, 'njet':'6-7j','LT':'L_{T}3','HT': 'H_{T}12',  'tex':'\\textrm{6-7j}, \\textrm{L}_T3, \\textrm{H}_T12'},
                                          (1000, -1):  {'deltaPhi': 0.75, 'njet':'6-7j','LT':'L_{T}3','HT': 'H_{T}3',   'tex':'\\textrm{6-7j}, \\textrm{L}_T3, \\textrm{H}_T3'}}},
                   (8, -1): {(250, 350): {(500, 750):  {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'L_{T}1','HT': 'H_{T}1',  'tex':'\geq\\textrm{8j}, \\textrm{L}_T1, \\textrm{H}_T1'},
                                          (750, -1):   {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'L_{T}1','HT': 'H_{T}23', 'tex':'\geq\\textrm{8j}, \\textrm{L}_T1, \\textrm{H}_T23'}},
                             (350, 450): {(500, -1):   {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'L_{T}2','HT': 'H_{T}i', 'tex':'\geq\\textrm{8j}, \\textrm{L}_T2, \\textrm{H}_Ti'}},
                             (450, -1):  {(500, -1):   {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'L_{T}3','HT': 'H_{T}i', 'tex':'\geq\\textrm{8j}, \\textrm{L}_T3, \\textrm{H}_Ti'}}}}

signalRegion3fbMerge = {(5, 5):  {(450, -1):  {(500, -1):   {'deltaPhi': 0.75, 'njet':'5j','LT':'L_{T}3','HT': 'H_{T}i'}}},
                        (6, 7):  {(450, -1):  {(500, 750):  {'deltaPhi': 0.75, 'njet':'6-7j','LT':'L_{T}3','HT': 'H_{T}12'},
                                               (750, -1):   {'deltaPhi': 0.75, 'njet':'6-7j','LT':'L_{T}3','HT': 'H_{T}3'}}},
                        (8, -1): {(350, 450): {(500, -1):   {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'L_{T}2','HT': 'H_{T}i'}}}}

signalRegion3fbReduced = {(5, 5):  {(250, 350): {(500, -1):  {'deltaPhi': 1.0, 'name':'5j, L_{Tl}, H_{Ti}'}},
                                    (350, 450): {(500, -1):  {'deltaPhi': 1.0, 'name':'5j, L_{Tm}, H_{Ti}'}},
                                    (450, -1):  {(500, -1):  {'deltaPhi': 0.75, 'name':'5j, L_{Th}, H_{Ti}'}}},
                          (6, 7):  {(250, 350): {(500, 750): {'deltaPhi': 1.0, 'name':'6-7j, L_{Tl}, H_{Tl}'},
                                                 (750, -1):  {'deltaPhi': 1.0, 'name':'6-7j, L_{Tl}, H_{Tmh}'}},
                                    (350, 450): {(500, 750): {'deltaPhi': 1.0, 'name':'6-7j, L_{Tm}, H_{Tl}'},
                                                 (750, -1):  {'deltaPhi': 1.0, 'name':'6-7j, L_{Tm}, H_{Tmh}'}},
                                    (450, -1):  {(500, 750): {'deltaPhi': 0.75, 'name':'6-7j, L_{Th}, H_{Tl}'},
                                                 (750, -1):  {'deltaPhi': 0.75, 'name':'6-7j, L_{Th}, H_{Tmh}'}}},
                          (8, -1): {(250, 350): {(500, 750): {'deltaPhi': 1.0, 'name':'#geq8j, L_{Tl}, H_{Tl}'},
                                                 (750, -1):  {'deltaPhi': 1.0, 'name':'#geq8j, L_{Tl}, H_{Tmh}'}},
                                    (350, -1):  {(500, -1):  {'deltaPhi': 0.75, 'name':'#geq8j, L_{Tmh}, H_{Ti}'}}}}

validationRegion = {(4, 4):  {(250, 350): {(500, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}1','HT': 'H_{T}i'}},
                             (350, 450): {(500, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}2','HT': 'H_{T}i'}},
                             (450, -1):  {(500, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}3','HT': 'H_{T}i'}}}}

validationRegion2 = {(4, 4):  {(250, -1): {(500, 750):   {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}i','HT': 'H_{T}1'},
                                           (750, 1000):  {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}i','HT': 'H_{T}2'},
                                           (1000, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}i','HT': 'H_{T}3'}}}}

validationRegionAll = {(4, 4):  {(250, 350): {(500, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}1','HT': 'H_{T}i'},
                                              (500, 750):  {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}1','HT': 'H_{T}1'},
                                              (750, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}1','HT': 'H_{T}23'}},
                                 (350, 450): {(500, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}2','HT': 'H_{T}i'},
                                              (500, 750):  {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}2','HT': 'H_{T}1'},
                                              (750, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}2','HT': 'H_{T}23'}},
                                 (450, -1):  {(500, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'L_{T}3','HT': 'H_{T}i'},
                                              (500, 1000): {'deltaPhi': 0.75, 'njet':'4j','LT':'L_{T}3','HT': 'H_{T}12'},
                                              (1000, -1):  {'deltaPhi': 0.75, 'njet':'4j','LT':'L_{T}3','HT': 'H_{T}3'}}}}

newBins3fb = {(5, 5):  {(450, -1): {(500, -1):    {'deltaPhi': 0.75}}},
              (6, 7):  {(450, -1): {(500, 750):   {'deltaPhi': 0.75},
                                    (750, -1):    {'deltaPhi': 0.75}}},
              (8, -1): {(350, -1): {(500, -1):    {'deltaPhi': 0.75}}}}


sideBand3fb =     {(4, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0},
                                         (500, 750):  {'deltaPhi': 1.0},
                                         (750, -1):   {'deltaPhi': 1.0}},
                            (350, 450): {(500, -1):   {'deltaPhi': 1.0},
                                         (500, 750):  {'deltaPhi': 1.0},
                                         (750, -1):   {'deltaPhi': 1.0}},
                            (450, -1): {(500, 1000):   {'deltaPhi': 0.75},
                                        (1000, -1):   {'deltaPhi': 0.75},
                                        (500, -1):   {'deltaPhi': 0.75}}}}

#sideBand3fb =     {(4, 5): {(250, 350): {(500, -1):   {'deltaPhi': 1.0},
#                                         (500, 750):  {'deltaPhi': 1.0},
#                                         (750, -1):   {'deltaPhi': 1.0}},
#                            (350, 450): {(500, -1):   {'deltaPhi': 1.0},
#                                         (500, 750):  {'deltaPhi': 1.0},
#                                         (750, -1):   {'deltaPhi': 1.0}},
#                            (450, -1): {(500, 750):   {'deltaPhi': 0.75},
#                                        (750, 1250):  {'deltaPhi': 0.75},
#                                        (1250, -1):   {'deltaPhi': 0.75},
#                                        (500, -1):   {'deltaPhi': 0.75}}}}

#signalRegion3fb = {(5, 5): {(250, 350): {(500, -1): {'deltaPhi': 1.0}},
#                            (350, 450): {(500, -1): {'deltaPhi': 1.0}},
#                            (450, -1): {(500, -1): {'deltaPhi': 1.0}}},
#                   (6, 7): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
#                                         (750, -1): {'deltaPhi': 1.0}},
#                            (350, 450): {(500, 750): {'deltaPhi': 1.0},
#                                         (750, -1): {'deltaPhi': 1.0}},
#                            (450, -1): {(500, 750): {'deltaPhi': 0.75},
#                                        (750, 1250): {'deltaPhi': 0.75},
#                                        (1250, -1): {'deltaPhi': 0.75}}},
#                   (8, -1): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
#                                          (750, -1): {'deltaPhi': 1.0}},
#                             (350, 450): {(500, 750): {'deltaPhi': 0.75},
#                                          (750, -1): {'deltaPhi': 0.75}},
#                             (450, -1): {(500, 1000): {'deltaPhi': 0.75},
#                                         (1000, -1): {'deltaPhi': 0.75}}}}

signalRegion10fb =  {(5, 5): {(250, 350): {(500, 750):    {'deltaPhi': 1.0},
                                           (750, 1000):   {'deltaPhi': 1.0},
                                           (1000, -1):    {'deltaPhi': 1.0}},
                              (350, 450): {(500, 750):    {'deltaPhi': 1.0},
                                           (750, 1000):   {'deltaPhi': 1.0},
                                           (1000, -1):    {'deltaPhi': 1.0}},
                              (450, -1): {(500, 750):     {'deltaPhi': 1.0},
                                          (750, 1000):    {'deltaPhi': 1.0},
                                          (1000, -1):     {'deltaPhi': 1.0}}},

                     (6, 7): {(250, 350): {(500, 750):    {'deltaPhi': 1.0},
                                           (750, 1000):   {'deltaPhi': 1.0},
                                           (1000, -1):    {'deltaPhi': 1.0}},
                              (350, 450): {(500, 750):    {'deltaPhi': 1.0},
                                           (750, 1000):   {'deltaPhi': 1.0},
                                           (1000, -1):    {'deltaPhi': 1.0}},
                              (450, -1): {(500, 750):     {'deltaPhi': 0.75},
                                          (750, 1000):    {'deltaPhi': 0.75},
                                          (1000, -1):     {'deltaPhi': 0.75}}},

                     (8, -1): {(250, 350): {(500, 750):   {'deltaPhi': 1.0},
                                            (750, 1000):  {'deltaPhi': 1.0},
                                            (1000, -1):   {'deltaPhi': 1.0}},
                               (350, 450): {(500, 750):   {'deltaPhi': 0.75},
                                            (750, 1000):  {'deltaPhi': 0.75},
                                            (1000, -1):   {'deltaPhi': 0.75}},
                               (450, -1): {(500, 750):    {'deltaPhi': 0.75},
                                           (750, 1000):   {'deltaPhi': 0.75},
                                           (1000, -1):    {'deltaPhi': 0.75}}}
                    }

sideBand10fb =  {(4, 5):     {(250, 350): {(500, 750):    {'deltaPhi': 1.0},
                                           (750, 1000):   {'deltaPhi': 1.0},
                                           (1000, -1):    {'deltaPhi': 1.0}},
                              (350, 450): {(500, 750):    {'deltaPhi': 1.0},
                                           (750, 1000):   {'deltaPhi': 1.0},
                                           (1000, -1):    {'deltaPhi': 1.0}},
                              (450, -1): {(500, 750):     {'deltaPhi': 1.0},
                                          (750, 1000):    {'deltaPhi': 1.0},
                                          (1000, -1):     {'deltaPhi': 1.0}}}}

signalRegion10fbStaticDPhi =  {(5, 5): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
                                           (750, 1000): {'deltaPhi': 1.0},
                                           (1000, 1250): {'deltaPhi': 1.0},
                                           (1250, -1): {'deltaPhi': 1.0}},
                              (350, 450): {(500, 750): {'deltaPhi': 1.0},
                                           (750, 1000): {'deltaPhi': 1.0},
                                           (1000, 1250): {'deltaPhi': 1.0},
                                           (1250, -1): {'deltaPhi': 1.0}},
                              (450, -1): {(500, 750): {'deltaPhi': 1.0},
                                          (750, 1000): {'deltaPhi': 1.0},
                                          (1000, 1250): {'deltaPhi': 1.0},
                                          (1250, -1): {'deltaPhi': 1.0}}},
                     (6, 7): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
                                           (750, 1000): {'deltaPhi': 1.0},
                                           (1000, 1250): {'deltaPhi': 1.0},
                                           (1250, -1): {'deltaPhi': 1.0}},
                              (350, 450): {(500, 750): {'deltaPhi': 1.0},
                                           (750, 1000): {'deltaPhi': 1.0},
                                           (1000, 1250): {'deltaPhi': 1.0},
                                           (1250, -1): {'deltaPhi': 1.0}},
                              (450, -1): {(500, 750): {'deltaPhi': 1.0},
                                          (750, 1000): {'deltaPhi': 1.0},
                                          (1000, 1250): {'deltaPhi': 1.0},
                                          (1250, -1): {'deltaPhi': 1.0}}},
                     (8, -1): {(250, 350): {(500, 750): {'deltaPhi': 1.0},
                                            (750, 1000): {'deltaPhi': 1.0},
                                            (1000, 1250): {'deltaPhi': 1.0},
                                            (1250, -1): {'deltaPhi': 1.0}},
                               (350, 450): {(500, 750): {'deltaPhi': 1.0},
                                            (750, 1000): {'deltaPhi': 1.0},
                                            (1000, 1250): {'deltaPhi': 1.0},
                                            (1250, -1): {'deltaPhi': 1.0}},
                               (450, -1): {(500, 750): {'deltaPhi': 1.0},
                                           (750, 1000): {'deltaPhi': 1.0},
                                           (1000, 1250): {'deltaPhi': 1.0},
                                           (1250, -1): {'deltaPhi': 1.0}}}
                    }
