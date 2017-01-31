from copy import deepcopy

# loop looks like this: for njb in signalRegion2fb: for stb in signalRegion2fb[njb]: for htb in signalRegion2fb[njb][stb]: print signalRegion2fb[njb][stb][htb]['deltaPhi']

signalRegion40pb = {(5,5): {(250, 350): {(500, -1): {'deltaPhi': .5}},
                            (350, -1):  {(500, -1): {'deltaPhi': .5}}},
                    (6,-1):{(250, 350): {(500, -1): {'deltaPhi': .5}},
                            (350, -1):  {(500, -1): {'deltaPhi': .5}}}
                   }

signalRegionCRonly = {(5,5): {(250, -1): {(500, -1): {'deltaPhi': .5}}},
                    (6,-1):{(250, -1): {(500, -1): {'deltaPhi': .5}}}
                   }
oneRegion = {(5,5): {(250, 350): {(500, 750): {'deltaPhi': 1., 'njet':'5j','LT':'LT1','HT': 'HT1',      'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}}

smallRegion = {(5,5): {(250, 350): {(500, -1): {'deltaPhi': 1., 'njet':'5j','LT':'LT1','HT': 'HTi',      'tex':'\\textrm{LT1}, \\textrm{HTi}'}}},
               (6,7):{(250, 350): {(500, 750): {'deltaPhi': 1., 'njet':'6-7j','LT':'LT1','HT': 'HT1',      'tex':'\\textrm{LT1}, \\textrm{HTi}'}}}
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


signalRegions2016 = {(5,5): {(250, 350): {(500, 750):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},
                             (350, 450): {(500, 750):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                             (450, -1):  {(500, 750):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'},
                                          (750, 1000):  {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT2', 'tex':'\\textrm{LT3}, \\textrm{HT2}'},
                                          (1000, -1):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT3', 'tex':'\\textrm{LT3}, \\textrm{HT3}'}}},
                     (6,7): {(250, 350): {(500, 750):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},
                             (350, 450): {(500, 750):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                             (450, -1):  {(500, 750):   {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'},
                                          (750, 1000):  {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT2', 'tex':'\\textrm{LT3}, \\textrm{HT2}'},
                                          (1000, -1):   {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT3', 'tex':'\\textrm{LT3}, \\textrm{HT3}'}}},
                     (8,-1): {(250, 350):{(500, 750):   {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},
                              (350, 450):{(500, 750):   {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                              (450, -1): {(500, 1000):  {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT3','HT': 'HT1', 'tex':'\\textrm{LT3}, \\textrm{HT1}'},
                                          (1000, -1):   {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT3','HT': 'HT23', 'tex':'\\textrm{LT3}, \\textrm{HT23}'}}}}
signalRegions2016_onebyone =[\
{(5, 5): {(250, 350): {(500, 750): {'tex': '\\textrm{LT1}, \\textrm{HT1}', 'LT': 'LT1', 'njet': '5j', 'HT': 'HT1', 'deltaPhi': 1.0}}}} ,\
{(5, 5): {(250, 350): {(750, -1): {'tex': '\\textrm{LT1}, \\textrm{HT23}', 'LT': 'LT1', 'njet': '5j', 'HT': 'HT23', 'deltaPhi': 1.0}}}} ,\
{(5, 5): {(350, 450): {(500, 750): {'tex': '\\textrm{LT2}, \\textrm{HT1}', 'LT': 'LT2', 'njet': '5j', 'HT': 'HT1', 'deltaPhi': 1.0}}}} ,\
{(5, 5): {(350, 450): {(750, -1): {'tex': '\\textrm{LT2}, \\textrm{HT23}', 'LT': 'LT2', 'njet': '5j', 'HT': 'HT23', 'deltaPhi': 1.0}}}} ,\
{(5, 5): {(450, -1): {(500, 750): {'tex': '\\textrm{LT3}, \\textrm{HT1}', 'LT': 'LT3', 'njet': '5j', 'HT': 'HT1', 'deltaPhi': 0.75}}}} ,\
{(5, 5): {(450, -1): {(750, 1000): {'tex': '\\textrm{LT3}, \\textrm{HT2}', 'LT': 'LT3', 'njet': '5j', 'HT': 'HT2', 'deltaPhi': 0.75}}}} ,\
{(5, 5): {(450, -1): {(1000, -1): {'tex': '\\textrm{LT3}, \\textrm{HT3}', 'LT': 'LT3', 'njet': '5j', 'HT': 'HT3', 'deltaPhi': 0.75}}}} ,\
{(6, 7): {(250, 350): {(500, 750): {'tex': '\\textrm{LT1}, \\textrm{HT1}', 'LT': 'LT1', 'njet': '6-7j', 'HT': 'HT1', 'deltaPhi': 1.0}}}} ,\
{(6, 7): {(250, 350): {(750, -1): {'tex': '\\textrm{LT1}, \\textrm{HT23}', 'LT': 'LT1', 'njet': '6-7j', 'HT': 'HT23', 'deltaPhi': 1.0}}}} ,\
{(6, 7): {(350, 450): {(500, 750): {'tex': '\\textrm{LT2}, \\textrm{HT1}', 'LT': 'LT2', 'njet': '6-7j', 'HT': 'HT1', 'deltaPhi': 1.0}}}} ,\
{(6, 7): {(350, 450): {(750, -1): {'tex': '\\textrm{LT2}, \\textrm{HT23}', 'LT': 'LT2', 'njet': '6-7j', 'HT': 'HT23', 'deltaPhi': 1.0}}}} ,\
{(6, 7): {(450, -1): {(500, 750): {'tex': '\\textrm{LT3}, \\textrm{HT1}', 'LT': 'LT3', 'njet': '6-7j', 'HT': 'HT1', 'deltaPhi': 0.75}}}} ,\
{(6, 7): {(450, -1): {(750, 1000): {'tex': '\\textrm{LT3}, \\textrm{HT2}', 'LT': 'LT3', 'njet': '6-7j', 'HT': 'HT2', 'deltaPhi': 0.75}}}} ,\
{(6, 7): {(450, -1): {(1000, -1): {'tex': '\\textrm{LT3}, \\textrm{HT3}', 'LT': 'LT3', 'njet': '6-7j', 'HT': 'HT3', 'deltaPhi': 0.75}}}} ,\
{(8, -1): {(250, 350): {(500, 750): {'tex': '\\textrm{LT1}, \\textrm{HT1}', 'LT': 'LT1', 'njet': '#geq8j', 'HT': 'HT1', 'deltaPhi': 1.0}}}} ,\
{(8, -1): {(250, 350): {(750, -1): {'tex': '\\textrm{LT1}, \\textrm{HT23}', 'LT': 'LT1', 'njet': '#geq8j', 'HT': 'HT23', 'deltaPhi': 1.0}}}} ,\
{(8, -1): {(350, 450): {(500, 750): {'tex': '\\textrm{LT2}, \\textrm{HT1}', 'LT': 'LT2', 'njet': '#geq8j', 'HT': 'HT1', 'deltaPhi': 1.0}}}} ,\
{(8, -1): {(350, 450): {(750, -1): {'tex': '\\textrm{LT2}, \\textrm{HT23}', 'LT': 'LT2', 'njet': '#geq8j', 'HT': 'HT23', 'deltaPhi': 1.0}}}} ,\
{(8, -1): {(450, -1): {(500, 1000): {'tex': '\\textrm{LT3}, \\textrm{HT1}', 'LT': 'LT3', 'njet': '#geq8j', 'HT': 'HT1', 'deltaPhi': 0.75}}}} ,\
{(8, -1): {(450, -1): {(1000, -1): {'tex': '\\textrm{LT3}, \\textrm{HT23}', 'LT': 'LT3', 'njet': '#geq8j', 'HT': 'HT23', 'deltaPhi': 0.75}}}} ,\
                            ]

validation2016    = {(4,4): {(250, 350): {(500, 750):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT1','HT': 'HT1'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'4j','LT':'LT1','HT': 'HT23'}},
                             (350, 450): {(500, 750):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT2','HT': 'HT1'},
                                          (750, -1):    {'deltaPhi': 1.0, 'njet':'4j','LT':'LT2','HT': 'HT23'}},
                             (450, -1):  {(500, 750):   {'deltaPhi': 0.75, 'njet':'4j','LT':'LT3','HT': 'HT1'},
                                          (750, -1):    {'deltaPhi': 0.75, 'njet':'4j','LT':'LT3','HT': 'HT23'}}}}


signalRegions2016VR = {(5,5): { (250, 350): {(500, -1):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT1','HT': 'HTi',      'tex':'\\textrm{LT1}, \\textrm{HTi}'}},
                                (350, -1):  {(500, -1):   {'deltaPhi': 0.75, 'njet':'5j','LT':'LT2i','HT': 'HTi',     'tex':'\\textrm{LT2i}, \\textrm{HTi}'}}},
                       (6,-1):{ (250, 350): {(500, -1):   {'deltaPhi': 0.75, 'njet':'#geq6j','LT':'LT1','HT': 'HTi',  'tex':'\\textrm{LT1}, \\textrm{HTi}'}},
                                (350, -1):  {(500, -1):   {'deltaPhi': 0.75, 'njet':'#geq6j','LT':'LT2i','HT': 'HTi', 'tex':'\\textrm{LT2i}, \\textrm{HTi}'}}}}


signalRegion3fb = {(5, 5):  {(250, 350): {(500, -1):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HTi',      'tex':'\\textrm{LT1}, \\textrm{HTi}'}},
                             (350, 450): {(500, -1):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HTi',      'tex':'\\textrm{LT2}, \\textrm{HTi}'}},
                             (450, -1):  {(500, -1):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT3','HT': 'HTi',      'tex':'\\textrm{LT3}, \\textrm{HTi}'}}},
                   (6, 7):  {(250, 350): {(500, 750):  {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT1',    'tex':'\\textrm{LT1}, \\textrm{HT1}'},
                                          (750, -1):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT23',   'tex':'\\textrm{LT1}, \\textrm{HT23}'}},
                             (350, 450): {(500, 750):  {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT1',    'tex':'\\textrm{LT2}, \\textrm{HT1}'},
                                          (750, -1):   {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT23',   'tex':'\\textrm{LT2}, \\textrm{HT23}'}},
                             (450, -1):  {(500, 1000): {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT12',  'tex':'\\textrm{LT3}, \\textrm{HT12}'},
                                          (1000, -1):  {'deltaPhi': 0.75, 'njet':'6-7j','LT':'LT3','HT': 'HT3',   'tex':'\\textrm{LT3}, \\textrm{HT3}'}}},
                   (8, -1): {(250, 350): {(500, 750):  {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'},
                                          (750, -1):   {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}},
                             (350, 450): {(500, -1):   {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT2','HT': 'HTi', 'tex':'\\textrm{LT2}, \\textrm{HTi}'}},
                             (450, -1):  {(500, -1):   {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT3','HT': 'HTi', 'tex':'\\textrm{LT3}, \\textrm{HTi}'}}}}

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

validationRegionAll = {(4, 4):  {(250, 350): {(500, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT1','HT': 'HTi'},
                                              (500, 750):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT1','HT': 'HT1'},
                                              (750, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT1','HT': 'HT23'}},
                                 (350, 450): {(500, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT2','HT': 'HTi'},
                                              (500, 750):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT2','HT': 'HT1'},
                                              (750, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT2','HT': 'HT23'}},
                                 (450, -1):  {(500, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT3','HT': 'HTi'},
                                              (500, 1000): {'deltaPhi': 0.75, 'njet':'4j','LT':'LT3','HT': 'HT12'},
                                              (1000, -1):  {'deltaPhi': 0.75, 'njet':'4j','LT':'LT3','HT': 'HT3'}}}}

validationRegion_Moriond_All = {(4, 4):  {(250, 350): {\
                                                        #(500, 750):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT0'    ,'HT': 'HT0' },
                                                        #(750, -1):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT0'     ,'HT': 'HT1i'},
                                                        #(750, 1250):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT0'   ,'HT': 'HT12'},
                                                        (500, 1000):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT0'   ,'HT': 'HT01', 'tex':'\\textrm{LT0},  \\textrm{HT01}'},
                                                        (1000, -1):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT0'    ,'HT': 'HT2i', 'tex':'\\textrm{LT0},  \\textrm{HT2i}'}},
                                                        #(1250, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT0'   ,'HT': 'HT3i'}},
                                           (350, 450):  {\
                                                          #(500, 750):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT1'  ,'HT': 'HT0' },
                                                          #(750, -1):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT1'   ,'HT': 'HT1i'},
                                                         # (750, 1250):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT1' ,'HT': 'HT12'},
                                                          (500, 1000):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT1' ,'HT': 'HT01', 'tex':'\\textrm{LT1},  \\textrm{HT01}'},
                                                          (1000, -1):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT1'  ,'HT': 'HT2i', 'tex':'\\textrm{LT1},  \\textrm{HT2i}'}},
                                                         # (1250, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT1' ,'HT': 'HT3i'}},
                                           (450, 650): {\
                                                         #(500, 750):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT2'   ,'HT': 'HT0' },
                                                         #(750, -1):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT2'    ,'HT': 'HT1i'},
                                                         #(750, 1250):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT2'  ,'HT': 'HT12'},
                                                         (500, 1000):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT2'  ,'HT': 'HT01', 'tex':'\\textrm{LT2},  \\textrm{HT01}'},
                                                         (1000, -1):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT2'   ,'HT': 'HT2i', 'tex':'\\textrm{LT2},  \\textrm{HT2i}'}},
                                                         #(1250, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT2'  ,'HT': 'HT3i'}},
                                           (650, -1): {\
                                                        #(500, 750):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT3i'   ,'HT': 'HT0' },
                                                        #(750, -1):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT3i'    ,'HT': 'HT1i'},
                                                        #(750, 1250):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT3i'  ,'HT': 'HT12'},
                                                        (500, 1000):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT3i'  ,'HT': 'HT01', 'tex':'\\textrm{LT3i},  \\textrm{HT01}'},
                                                        (1000, -1):  {'deltaPhi': 1.0, 'njet':'4j','LT':'LT3i'   ,'HT': 'HT2i', 'tex':'\\textrm{LT3i},  \\textrm{HT2i}'}}}}
                                                        #(1250, -1):   {'deltaPhi': 1.0, 'njet':'4j','LT':'LT3i'  ,'HT': 'HT3i'}}}}

validationRegion_Moriond_onebyone = [\
                                    {(4, 4):  {(250, 350): {(500, 750):   {'deltaPhi': 1.0 , 'njet':'4j','LT':'LT0' ,'HT': 'HT0' }}}},
                                    {(4, 4):  {(250, 350): {(750, -1):    {'deltaPhi': 1.0 , 'njet':'4j','LT':'LT0' ,'HT': 'HT1i'}}}},
                                    {(4, 4):  {(250, 350): {(750, 1250):  {'deltaPhi': 1.0 , 'njet':'4j','LT':'LT0' ,'HT': 'HT12'}}}},
                                    {(4, 4):  {(250, 350): {(500, 1000):  {'deltaPhi': 1.0 , 'njet':'4j','LT':'LT0' ,'HT': 'HT01'}}}},
                                    {(4, 4):  {(250, 350): {(1000, -1):   {'deltaPhi': 1.0 , 'njet':'4j','LT':'LT0' ,'HT': 'HT2i'}}}},
                                    {(4, 4):  {(250, 350): {(1250, -1):   {'deltaPhi': 1.0 , 'njet':'4j','LT':'LT0' ,'HT': 'HT3i'}}}},
                                    {(4, 4):  {(350, 450): {(500, 750):   {'deltaPhi': 1.0 , 'njet':'4j','LT':'LT1' ,'HT': 'HT0' }}}},
                                    {(4, 4):  {(350, 450): {(750, -1):    {'deltaPhi': 1.0 , 'njet':'4j','LT':'LT1' ,'HT': 'HT1i'}}}},
                                    {(4, 4):  {(350, 450): {(750, 1250):  {'deltaPhi': 1.0 , 'njet':'4j','LT':'LT1' ,'HT': 'HT12'}}}},
                                    {(4, 4):  {(350, 450): {(500, 1000):  {'deltaPhi': 1.0 , 'njet':'4j','LT':'LT1' ,'HT': 'HT01'}}}},
                                    {(4, 4):  {(350, 450): {(1000, -1):   {'deltaPhi': 1.0 , 'njet':'4j','LT':'LT1' ,'HT': 'HT2i'}}}},
                                    {(4, 4):  {(350, 450): {(1250, -1):   {'deltaPhi': 1.0 , 'njet':'4j','LT':'LT1' ,'HT': 'HT3i'}}}},
                                    {(4, 4):  {(450, 650): {(500, 750):   {'deltaPhi': 0.75, 'njet':'4j','LT':'LT2' ,'HT': 'HT0' }}}},
                                    {(4, 4):  {(450, 650): {(750, -1):    {'deltaPhi': 0.75, 'njet':'4j','LT':'LT2' ,'HT': 'HT1i'}}}},
                                    {(4, 4):  {(450, 650): {(750, 1250):  {'deltaPhi': 0.75, 'njet':'4j','LT':'LT2' ,'HT': 'HT12'}}}},
                                    {(4, 4):  {(450, 650): {(500, 1000):  {'deltaPhi': 0.75, 'njet':'4j','LT':'LT2' ,'HT': 'HT01'}}}},
                                    {(4, 4):  {(450, 650): {(1000, -1):   {'deltaPhi': 0.75, 'njet':'4j','LT':'LT2' ,'HT': 'HT2i'}}}},
                                    {(4, 4):  {(450, 650): {(1250, -1):   {'deltaPhi': 0.75, 'njet':'4j','LT':'LT2' ,'HT': 'HT3i'}}}},
                                    {(4, 4):  {(650, -1):  {(500, 750):   {'deltaPhi': 0.5 , 'njet':'4j','LT':'LT3i','HT': 'HT0' }}}},
                                    {(4, 4):  {(650, -1):  {(750, -1):    {'deltaPhi': 0.5 , 'njet':'4j','LT':'LT3i','HT': 'HT1i'}}}},
                                    {(4, 4):  {(650, -1):  {(750, 1250):  {'deltaPhi': 0.5 , 'njet':'4j','LT':'LT3i','HT': 'HT12'}}}},
                                    {(4, 4):  {(650, -1):  {(500, 1000):  {'deltaPhi': 0.5 , 'njet':'4j','LT':'LT3i','HT': 'HT01'}}}},
                                    {(4, 4):  {(650, -1):  {(1000, -1):   {'deltaPhi': 0.5 , 'njet':'4j','LT':'LT3i','HT': 'HT2i'}}}},
                                    {(4, 4):  {(650, -1):  {(1250, -1):   {'deltaPhi': 0.5 , 'njet':'4j','LT':'LT3i','HT': 'HT3i'}}}}
                                ]

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



signalRegions_Moriond2017 = {(5,5): {(250, 350): {(500, 750): {'deltaPhi': 1.0,   'njet':'5j'    ,'LT':'LT0'  ,'HT': 'HT0',  'tex':'\\textrm{LT0},   \\textrm{HT0}'   },
                                          (750, -1):          {'deltaPhi': 1.0,   'njet':'5j'    ,'LT':'LT0'  ,'HT': 'HT1i', 'tex':'\\textrm{LT0},   \\textrm{HT1i}'  }},
                             (350, 450): {(500, 750):         {'deltaPhi': 1.0,   'njet':'5j'    ,'LT':'LT1'  ,'HT': 'HT0',  'tex':'\\textrm{LT1},   \\textrm{HT0}'  },
                                          (750, -1):          {'deltaPhi': 1.0,   'njet':'5j'    ,'LT':'LT1'  ,'HT': 'HT1i', 'tex':'\\textrm{LT1},   \\textrm{HT1i}'  }},
                             (450, 650): {(500, 750):         {'deltaPhi': 0.75,  'njet':'5j'    ,'LT':'LT2'  ,'HT': 'HT0',  'tex':'\\textrm{LT2},   \\textrm{HT0}'  },
                                          (750, 1250):         {'deltaPhi': 0.75, 'njet':'5j'    ,'LT':'LT2'  ,'HT': 'HT12', 'tex':'\\textrm{LT2},   \\textrm{HT12}'  },
                                          (1250, -1):          {'deltaPhi': 0.75, 'njet':'5j'    ,'LT':'LT2'  ,'HT': 'HT3i', 'tex':'\\textrm{LT2},   \\textrm{HT3i}'  }},
                             (650, -1): {(500, 750):         {'deltaPhi': 0.5,    'njet':'5j'    ,'LT':'LT3i' ,'HT': 'HT0',  'tex':'\\textrm{LT3i},  \\textrm{HT0}'  },
                                          (750, 1250):         {'deltaPhi': 0.5,  'njet':'5j'    ,'LT':'LT3i' ,'HT': 'HT12', 'tex':'\\textrm{LT3i},  \\textrm{HT12}'  },
                                          (1250, -1):          {'deltaPhi': 0.5,  'njet':'5j'    ,'LT':'LT3i' ,'HT': 'HT3i', 'tex':'\\textrm{LT3i},  \\textrm{HT3i}'  }}},
                     (6,7): {(250, 350): {(500, 1000):         {'deltaPhi': 1.0,  'njet':'6-7j'  ,'LT':'LT0'  ,'HT': 'HT01', 'tex':'\\textrm{LT0},   \\textrm{HT01}'  },
                                          (1000, -1):          {'deltaPhi': 1.0,  'njet':'6-7j'  ,'LT':'LT0'  ,'HT': 'HT2i', 'tex':'\\textrm{LT0},   \\textrm{HT2i}'  }},
                             (350, 450): {(500, 1000):         {'deltaPhi': 1.0,  'njet':'6-7j'  ,'LT':'LT1'  ,'HT': 'HT01', 'tex':'\\textrm{LT1},   \\textrm{HT01}'  },
                                          (1000, -1):          {'deltaPhi': 1.0,  'njet':'6-7j'  ,'LT':'LT1'  ,'HT': 'HT2i', 'tex':'\\textrm{LT1},   \\textrm{HT2i}'  }},
                             (450, 650): {(500, 750):         {'deltaPhi': 0.75,  'njet':'6-7j'    ,'LT':'LT2'  ,'HT': 'HT0',  'tex':'\\textrm{LT2},   \\textrm{HT0}'  },
                                          (750, 1250):         {'deltaPhi': 0.75, 'njet':'6-7j'    ,'LT':'LT2'  ,'HT': 'HT12', 'tex':'\\textrm{LT2},   \\textrm{HT12}'  },
                                          (1250, -1):          {'deltaPhi': 0.75, 'njet':'6-7j'    ,'LT':'LT2'  ,'HT': 'HT3i', 'tex':'\\textrm{LT2},   \\textrm{HT3i}'  }},
                             (650, -1): {(500, 750):         {'deltaPhi': 0.5,    'njet':'6-7j'    ,'LT':'LT3i' ,'HT': 'HT0',  'tex':'\\textrm{LT3i},  \\textrm{HT0}'  },
                                          (750, 1250):         {'deltaPhi': 0.5,  'njet':'6-7j'    ,'LT':'LT3i' ,'HT': 'HT12', 'tex':'\\textrm{LT3i},  \\textrm{HT12}'  },
                                          (1250, -1):          {'deltaPhi': 0.5,  'njet':'6-7j'    ,'LT':'LT3i' ,'HT': 'HT3i', 'tex':'\\textrm{LT3i},  \\textrm{HT3i}'  }}},
                     (8,-1): {(250, 350):{(500, 1000):         {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT0'  ,'HT': 'HT01', 'tex':'\\textrm{LT0},   \\textrm{HT01}'  },
                                          (1000, -1):          {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT0'  ,'HT': 'HT2i', 'tex':'\\textrm{LT0},   \\textrm{HT2i}'  }},
                              (350, 450):{(500, 1000):         {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT1'  ,'HT': 'HT01', 'tex':'\\textrm{LT1},   \\textrm{HT01}'  },
                                          (1000, -1):          {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT1'  ,'HT': 'HT2i', 'tex':'\\textrm{LT1},   \\textrm{HT2i}'  }},
                             (450, 650): {(500, 1250):         {'deltaPhi': 0.75, 'njet':'#geq8j'    ,'LT':'LT2'  ,'HT': 'HT02', 'tex':'\\textrm{LT2},   \\textrm{HT02}'  },
                                          (1250, -1):          {'deltaPhi': 0.75, 'njet':'#geq8j'    ,'LT':'LT2'  ,'HT': 'HT3i', 'tex':'\\textrm{LT2},   \\textrm{HT3i}'  }},
                             (650, -1): {(500, 1250):         {'deltaPhi': 0.5,   'njet':'#geq8j'    ,'LT':'LT3i' ,'HT': 'HT02', 'tex':'\\textrm{LT3i},  \\textrm{HT02}'  },
                                          (1250, -1):          {'deltaPhi': 0.5,  'njet':'#geq8j'    ,'LT':'LT3i' ,'HT': 'HT3i', 'tex':'\\textrm{LT3i},  \\textrm{HT3i}'  }}}}

aggregateRegions_Moriond2017 =  {(5,5): {(650, -1): {(750, -1):    {'deltaPhi': 0.5,  'njet':'5j'    ,'LT':'LT3i' ,'HT': 'HT1i', 'tex':'\\textrm{LT3i},  \\textrm{HT1i}'  }}},
                                 (6,7): {(450, 650): {(500, 1250):   {'deltaPhi': 0.75,  'njet':'6-7j'    ,'LT':'LT2'  ,'HT': 'HT02',  'tex':'\\textrm{LT2},   \\textrm{HT02}'  },
                                                      (1250, -1):    {'deltaPhi': 0.75, 'njet':'6-7j'    ,'LT':'LT2'  ,'HT': 'HT3i', 'tex':'\\textrm{LT2},   \\textrm{HT3i}'  }},
                                         (650, -1): {(1250, -1):    {'deltaPhi': 0.5,  'njet':'6-7j'    ,'LT':'LT3i' ,'HT': 'HT3i', 'tex':'\\textrm{LT3i},  \\textrm{HT3i}'  }}},
                                 (8,-1): {(250, 450):{(500, 1000):   {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT01'  ,'HT': 'HT01', 'tex':'\\textrm{LT01},   \\textrm{HT01}'  },
                                                      (1000, -1):    {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT01'  ,'HT': 'HT2i', 'tex':'\\textrm{LT01},   \\textrm{HT2i}'  }},
                                          (450, -1): {(500, 1250):   {'deltaPhi': 0.75, 'njet':'#geq8j'    ,'LT':'LT2i'  ,'HT': 'HT02', 'tex':'\\textrm{LT2i},   \\textrm{HT02}'  },
                                                      (1250, -1):    {'deltaPhi': 0.75, 'njet':'#geq8j'    ,'LT':'LT2i'  ,'HT': 'HT3i', 'tex':'\\textrm{LT2i},   \\textrm{HT3i}'  }}}}

aggregateRegions_Moriond2017_onebyone = [ {(5,5):   {(650, -1):   {(750, -1):     {'deltaPhi': 0.5,  'njet':'5j'    ,'LT':'LT3i' ,'HT': 'HT1i', 'tex':'\\textrm{LT3i},  \\textrm{HT1i}'  }}}},
                                          {(6,7):   {(450, 650):  {(500, 1250):   {'deltaPhi': 0.75, 'njet':'6-7j'  ,'LT':'LT2'  ,'HT': 'HT02',  'tex':'\\textrm{LT2},   \\textrm{HT02}' }}}},
                                          {(6,7):   {(450, 650):  {(1250, -1):    {'deltaPhi': 0.75, 'njet':'6-7j'  ,'LT':'LT2'  ,'HT': 'HT3i', 'tex':'\\textrm{LT2},   \\textrm{HT3i}'  }}}},
                                          {(6,7):   {(650, -1):   {(1250, -1):    {'deltaPhi': 0.5,  'njet':'6-7j'  ,'LT':'LT3i' ,'HT': 'HT3i', 'tex':'\\textrm{LT3i},  \\textrm{HT3i}'  }}}},
                                          {(8,-1):  {(250, 450):  {(500, 1000):   {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT01'  ,'HT': 'HT01', 'tex':'\\textrm{LT01},   \\textrm{HT01}'}}}},
                                          {(8,-1):  {(250, 450):  {(1000, -1):    {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT01'  ,'HT': 'HT2i', 'tex':'\\textrm{LT01},   \\textrm{HT2i}'}}}},
                                          {(8,-1):  {(450, -1):   {(500, 1250):   {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT2i'  ,'HT': 'HT02', 'tex':'\\textrm{LT2i},   \\textrm{HT02}'}}}},
                                          {(8,-1):  {(450, -1):   {(1250, -1):    {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT2i'  ,'HT': 'HT3i', 'tex':'\\textrm{LT2i},   \\textrm{HT3i}'}}}}]

aggregateRegions_Moriond2017_Test1_onebyone = [ {(5,-1):   {(250, -1):   {(750, -1):     {'deltaPhi': 1.0,  'njet':'#geq5j'    ,'LT':'LT0i' ,'HT': 'HT1i', 'tex':'\\textrm{LT0i},  \\textrm{HT1i}'  }}}},
                                                {(5,-1):   {(450, -1):   {(750, -1):     {'deltaPhi': 0.75, 'njet':'#geq5j'    ,'LT':'LT1i' ,'HT': 'HT1i', 'tex':'\\textrm{LT1i},  \\textrm{HT1i}'  }}}},
                                                {(5,-1):   {(650, -1):   {(750, -1):     {'deltaPhi': 0.5,  'njet':'#geq5j'    ,'LT':'LT2i' ,'HT': 'HT1i', 'tex':'\\textrm{LT2i},  \\textrm{HT1i}'  }}}},
                                                {(6,-1):   {(250, -1):   {(1000, -1):    {'deltaPhi': 1.0,  'njet':'#geq6j'  ,'LT':'LT0i' ,'HT': 'HT2i', 'tex':'\\textrm{LT0i},  \\textrm{HT2i}' }}}},
                                                {(6,-1):   {(450, -1):   {(1000, -1):    {'deltaPhi': 0.75, 'njet':'#geq6j'  ,'LT':'LT1i' ,'HT': 'HT2i', 'tex':'\\textrm{LT1i},  \\textrm{HT2i}'  }}}},
                                                {(6,-1):   {(650, -1):   {(1000, -1):    {'deltaPhi': 0.5,  'njet':'#geq6j'  ,'LT':'LT2i' ,'HT': 'HT2i', 'tex':'\\textrm{LT2i},  \\textrm{HT2i}'  }}}},
                                                {(6,-1):   {(250, -1):   {(500, -1):     {'deltaPhi': 1.0,  'njet':'#geq6j'  ,'LT':'LT0i' ,'HT': 'HT0i', 'tex':'\\textrm{LT0i},  \\textrm{HT0i}' }}}},
                                                {(6,-1):   {(450, -1):   {(500, -1):     {'deltaPhi': 0.75, 'njet':'#geq6j'  ,'LT':'LT1i' ,'HT': 'HT0i', 'tex':'\\textrm{LT1i},  \\textrm{HT0i}'  }}}},
                                                {(6,-1):   {(650, -1):   {(500, -1):     {'deltaPhi': 0.5,  'njet':'#geq6j'  ,'LT':'LT2i' ,'HT': 'HT0i', 'tex':'\\textrm{LT2i},  \\textrm{HT0i}'  }}}},
                                                {(7,-1):   {(250, -1):   {(1000, -1):    {'deltaPhi': 1.0,  'njet':'#geq7j'  ,'LT':'LT0i' ,'HT': 'HT2i', 'tex':'\\textrm{LT0i},  \\textrm{HT2i}' }}}},
                                                {(7,-1):   {(450, -1):   {(1000, -1):    {'deltaPhi': 0.75, 'njet':'#geq7j'  ,'LT':'LT1i' ,'HT': 'HT2i', 'tex':'\\textrm{LT1i},  \\textrm{HT2i}'  }}}},
                                                {(7,-1):   {(650, -1):   {(1000, -1):    {'deltaPhi': 0.5,  'njet':'#geq7j'  ,'LT':'LT2i' ,'HT': 'HT2i', 'tex':'\\textrm{LT2i},  \\textrm{HT2i}'  }}}},
                                                {(7,-1):   {(250, -1):   {(500, -1):     {'deltaPhi': 1.0,  'njet':'#geq7j'  ,'LT':'LT0i' ,'HT': 'HT0i', 'tex':'\\textrm{LT0i},  \\textrm{HT0i}' }}}},
                                                {(7,-1):   {(450, -1):   {(500, -1):     {'deltaPhi': 0.75, 'njet':'#geq7j'  ,'LT':'LT1i' ,'HT': 'HT0i', 'tex':'\\textrm{LT1i},  \\textrm{HT0i}'  }}}},
                                                {(7,-1):   {(650, -1):   {(500, -1):     {'deltaPhi': 0.5,  'njet':'#geq7j'  ,'LT':'LT2i' ,'HT': 'HT0i', 'tex':'\\textrm{LT2i},  \\textrm{HT0i}'  }}}},
                                                {(8,-1):  {(250, -1):   {(1000, -1):    {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT0i' ,'HT': 'HT1i', 'tex':'\\textrm{LT0i},  \\textrm{HT1i}'}}}},
                                                {(8,-1):  {(450, -1):   {(1000, -1):    {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT1i' ,'HT': 'HT1i', 'tex':'\\textrm{LT1i},  \\textrm{HT1i}'}}}},
                                                {(8,-1):  {(650, -1):   {(1000, -1):    {'deltaPhi': 0.5,  'njet':'#geq8j','LT':'LT2i' ,'HT': 'HT1i', 'tex':'\\textrm{LT2i},  \\textrm{HT1i}'}}}},
                                                {(8,-1):  {(250, -1):   {(1250, -1):    {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT0i' ,'HT': 'HT3i', 'tex':'\\textrm{LT0i},  \\textrm{HT3i}'}}}},
                                                {(8,-1):  {(450, -1):   {(1250, -1):    {'deltaPhi': 0.75, 'njet':'#geq8j','LT':'LT1i' ,'HT': 'HT3i', 'tex':'\\textrm{LT1i},  \\textrm{HT3i}'}}}},
                                                {(8,-1):  {(650, -1):   {(1250, -1):    {'deltaPhi': 0.5,  'njet':'#geq8j','LT':'LT2i' ,'HT': 'HT3i', 'tex':'\\textrm{LT2i},  \\textrm{HT3i}'}}}}
                                              ]

aggregateRegions_Moriond2017_Test2_onebyone = [\
                                                {(5,-1):   {(650, -1):   {(750, -1):     {'deltaPhi': 0.5,  'njet':'#geq5j'    ,'LT':'LT2i' ,'HT': 'HT1i', 'tex':'\\textrm{LT2i},  \\textrm{HT1i}'  }}}},
                                                {(6,-1):   {(650, -1):   {(1000, -1):    {'deltaPhi': 0.5,  'njet':'#geq6j'  ,'LT':'LT2i' ,'HT': 'HT2i', 'tex':'\\textrm{LT2i},  \\textrm{HT2i}'  }}}},
                                                {(6,-1):   {(450, -1):   {(500, -1):     {'deltaPhi': 0.75, 'njet':'#geq6j'  ,'LT':'LT1i' ,'HT': 'HT0i', 'tex':'\\textrm{LT1i},  \\textrm{HT0i}'  }}}},
                                                {(7,-1):   {(450, -1):   {(500, -1):     {'deltaPhi': 0.75, 'njet':'#geq7j'  ,'LT':'LT1i' ,'HT': 'HT0i', 'tex':'\\textrm{LT1i},  \\textrm{HT0i}'  }}}},
                                                {(7,-1):   {(650, -1):   {(500, -1):     {'deltaPhi': 0.5,  'njet':'#geq7j'  ,'LT':'LT2i' ,'HT': 'HT0i', 'tex':'\\textrm{LT2i},  \\textrm{HT0i}'  }}}},
                                                {(8,-1):  {(250, -1):   {(1250, -1):    {'deltaPhi': 1.0,  'njet':'#geq8j','LT':'LT0i' ,'HT': 'HT3i', 'tex':'\\textrm{LT0i},  \\textrm{HT3i}'}}}},
                                            ]
#aggregateRegions_Moriond2017_Test1 = {(8, -1): {(450, -1): {(1000, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT1i}', 'LT': 'LT1i', 'njet': '#geq8j', 'HT': 'HT1i', 'deltaPhi': 0.75}, (1250, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT3i}', 'LT': 'LT1i', 'njet': '#geq8j', 'HT': 'HT3i', 'deltaPhi': 0.75}}, (650, -1): {(1000, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT1i}', 'LT': 'LT2i', 'njet': '#geq8j', 'HT': 'HT1i', 'deltaPhi': 0.5}, (1250, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT3i}', 'LT': 'LT2i', 'njet': '#geq8j', 'HT': 'HT3i', 'deltaPhi': 0.5}}, (250, -1): {(1000, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT1i}', 'LT': 'LT0i', 'njet': '#geq8j', 'HT': 'HT1i', 'deltaPhi': 1.0}, (1250, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT3i}', 'LT': 'LT0i', 'njet': '#geq8j', 'HT': 'HT3i', 'deltaPhi': 1.0}}}, (6, 7): {(450, -1): {(1000, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT2i}', 'LT': 'LT1i', 'njet': '6-7j', 'HT': 'HT2i', 'deltaPhi': 0.75}, (500, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT0i}', 'LT': 'LT1i', 'njet': '6-7j', 'HT': 'HT0i', 'deltaPhi': 0.75}}, (650, -1): {(1000, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT2i}', 'LT': 'LT2i', 'njet': '6-7j', 'HT': 'HT2i', 'deltaPhi': 0.5}, (500, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT0i}', 'LT': 'LT2i', 'njet': '6-7j', 'HT': 'HT0i', 'deltaPhi': 0.5}}, (250, -1): {(1000, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT2i}', 'LT': 'LT0i', 'njet': '6-7j', 'HT': 'HT2i', 'deltaPhi': 1.0}, (500, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT0i}', 'LT': 'LT0i', 'njet': '6-7j', 'HT': 'HT0i', 'deltaPhi': 1.0}}}, (5, 5): {(450, -1): {(750, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT1i}', 'LT': 'LT1i', 'njet': '5j', 'HT': 'HT1i', 'deltaPhi': 0.75}}, (650, -1): {(750, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT1i}', 'LT': 'LT2i', 'njet': '5j', 'HT': 'HT1i', 'deltaPhi': 0.5}}, (250, -1): {(750, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT1i}', 'LT': 'LT0i', 'njet': '5j', 'HT': 'HT1i', 'deltaPhi': 1.0}}}}
aggregateRegions_Moriond2017_Test1 = {(5, -1): {(450, -1): {(750, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT1i}', 'LT': 'LT1i', 'njet': '#geq5j', 'HT': 'HT1i', 'deltaPhi': 0.75}}, (650, -1): {(750, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT1i}', 'LT': 'LT2i', 'njet': '#geq5j', 'HT': 'HT1i', 'deltaPhi': 0.5}}, (250, -1): {(750, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT1i}', 'LT': 'LT0i', 'njet': '#geq5j', 'HT': 'HT1i', 'deltaPhi': 1.0}}}, (8, -1): {(450, -1): {(1000, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT1i}', 'LT': 'LT1i', 'njet': '#geq8j', 'HT': 'HT1i', 'deltaPhi': 0.75}, (1250, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT3i}', 'LT': 'LT1i', 'njet': '#geq8j', 'HT': 'HT3i', 'deltaPhi': 0.75}}, (650, -1): {(1000, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT1i}', 'LT': 'LT2i', 'njet': '#geq8j', 'HT': 'HT1i', 'deltaPhi': 0.5}, (1250, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT3i}', 'LT': 'LT2i', 'njet': '#geq8j', 'HT': 'HT3i', 'deltaPhi': 0.5}}, (250, -1): {(1000, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT1i}', 'LT': 'LT0i', 'njet': '#geq8j', 'HT': 'HT1i', 'deltaPhi': 1.0}, (1250, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT3i}', 'LT': 'LT0i', 'njet': '#geq8j', 'HT': 'HT3i', 'deltaPhi': 1.0}}}, (7, -1): {(450, -1): {(1000, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT2i}', 'LT': 'LT1i', 'njet': '#geq7j', 'HT': 'HT2i', 'deltaPhi': 0.75}, (500, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT0i}', 'LT': 'LT1i', 'njet': '#geq7j', 'HT': 'HT0i', 'deltaPhi': 0.75}}, (650, -1): {(1000, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT2i}', 'LT': 'LT2i', 'njet': '#geq7j', 'HT': 'HT2i', 'deltaPhi': 0.5}, (500, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT0i}', 'LT': 'LT2i', 'njet': '#geq7j', 'HT': 'HT0i', 'deltaPhi': 0.5}}, (250, -1): {(1000, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT2i}', 'LT': 'LT0i', 'njet': '#geq7j', 'HT': 'HT2i', 'deltaPhi': 1.0}, (500, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT0i}', 'LT': 'LT0i', 'njet': '#geq7j', 'HT': 'HT0i', 'deltaPhi': 1.0}}}, (6, -1): {(450, -1): {(1000, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT2i}', 'LT': 'LT1i', 'njet': '#geq6j', 'HT': 'HT2i', 'deltaPhi': 0.75}, (500, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT0i}', 'LT': 'LT1i', 'njet': '#geq6j', 'HT': 'HT0i', 'deltaPhi': 0.75}}, (650, -1): {(1000, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT2i}', 'LT': 'LT2i', 'njet': '#geq6j', 'HT': 'HT2i', 'deltaPhi': 0.5}, (500, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT0i}', 'LT': 'LT2i', 'njet': '#geq6j', 'HT': 'HT0i', 'deltaPhi': 0.5}}, (250, -1): {(1000, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT2i}', 'LT': 'LT0i', 'njet': '#geq6j', 'HT': 'HT2i', 'deltaPhi': 1.0}, (500, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT0i}', 'LT': 'LT0i', 'njet': '#geq6j', 'HT': 'HT0i', 'deltaPhi': 1.0}}}}
aggregateRegions_Moriond2017_Test2 = {(5, -1): {(650, -1): {(750, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT1i}', 'LT': 'LT2i', 'njet': '#geq5j', 'HT': 'HT1i', 'deltaPhi': 0.5}}}, (8, -1): {(250, -1): {(1250, -1): {'tex': '\\textrm{LT0i},  \\textrm{HT3i}', 'LT': 'LT0i', 'njet': '#geq8j', 'HT': 'HT3i', 'deltaPhi': 1.0}}}, (7, -1): {(650, -1): {(500, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT0i}', 'LT': 'LT2i', 'njet': '#geq7j', 'HT': 'HT0i', 'deltaPhi': 0.5}}, (450, -1): {(500, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT0i}', 'LT': 'LT1i', 'njet': '#geq7j', 'HT': 'HT0i', 'deltaPhi': 0.75}}}, (6, -1): {(650, -1): {(1000, -1): {'tex': '\\textrm{LT2i},  \\textrm{HT2i}', 'LT': 'LT2i', 'njet': '#geq6j', 'HT': 'HT2i', 'deltaPhi': 0.5}}, (450, -1): {(500, -1): {'tex': '\\textrm{LT1i},  \\textrm{HT0i}', 'LT': 'LT1i', 'njet': '#geq6j', 'HT': 'HT0i', 'deltaPhi': 0.75}}}}

signalRegions_Moriond2017_onebyone = [{(5,5): {(250, 350): {(500, 750):   {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}},
                                      {(5,5): {(250, 350): {(750, -1):          {'deltaPhi': 1.0, 'njet':'5j','LT':'LT1','HT': 'HT2', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}}}},
                                      {(5,5): {(350, 450): {(500, 750):         {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                             {(5,5): {(350, 450): {(750, -1):     {'deltaPhi': 1.0, 'njet':'5j','LT':'LT2','HT': 'HT2', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
                             {(5,5): {(450, 650): {(500, 750):    {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                             {(5,5): {(450, 650): {(750, 1250):    {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT23',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                             {(5,5): {(450, 650): {(1250, -1):     {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT3', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
                             {(5,5): {(650, -1): {(500, 750):    {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                             {(5,5): {(650, -1): {(750, 1250):    {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT23',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                             {(5,5): {(650, -1): {(1250, -1):     {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT3', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
                     {(6,7): {(250, 350): {(500, 1000):         {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}},
                      {(6,7): {(250, 350): {(1000, -1):          {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}}}},
                            {(6,7): { (350, 450): {(500, 1000):         {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                                         {(6,7): { (350, 450): { (1000, -1):          {'deltaPhi': 1.0, 'njet':'6-7j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
                            {(6,7): { (450, 650): {(500, 750):         {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                                          {(6,7): { (450, 650): {(750, 1250):         {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                                          {(6,7): { (450, 650): {(1250, -1):          {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
                            {(6,7): { (650, -1): {(500, 750):         {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                                          {(6,7): { (650, -1): {(750, 1250):         {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                                          {(6,7): { (650, -1): {(1250, -1):          {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
                     {(8,-1): {(250, 350):{(500, 1000):         {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT1',  'tex':'\\textrm{LT1}, \\textrm{HT1}'}}}},
                                          {(8,-1): {(250, 350):{ (1000, -1):          {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT1','HT': 'HT23', 'tex':'\\textrm{LT1}, \\textrm{HT23}'}}}},
                                {(8,-1): {(350, 450):{(500, 1000):         {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                                         {(8,-1): {(350, 450):{ (1000, -1):          {'deltaPhi': 1.0, 'njet':'#geq8j','LT':'LT2','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
                               {(8,-1): {(450, 650): {(500, 1250):         {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                                          {(8,-1): {(450, 650): {(1250, -1):          {'deltaPhi': 0.75, 'njet':'5j','LT':'LT3','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}},
                               {(8,-1): {(650, -1): {(500, 1250):         {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT1',  'tex':'\\textrm{LT2}, \\textrm{HT1}'}}}},
                                          {(8,-1): {(650, -1): {(1250, -1):          {'deltaPhi': 0.5, 'njet':'5j','LT':'LT4','HT': 'HT23', 'tex':'\\textrm{LT2}, \\textrm{HT23}'}}}}]

def addKey(d, newDict='deltaPhiCut'):
  for k, v in d.iteritems():
    if k == newDict:
      d = {d[k]:d}
      return d
    elif isinstance(v, dict):
      d[k] = addKey(v, newDict)
  return d


def makeQCDsignalRegions(d2, QCDSB = (3,4), ttSB = (4,5)):
  d = deepcopy(d2)
  #del d2
  dQCD = addKey(d, newDict='deltaPhi')

  for njet in sorted(d):
    for lt in sorted(d[njet]):
      for ht in sorted(d[njet][lt]):
        dPhi = d2[njet][lt][ht]['deltaPhi']
        try: dQCD[njet][lt][ht][dPhi]['sys']
        except KeyError:
          sys = 0.025
          if ht[1]<0 and ht[0]>700: sys = 0.05
          if njet[0]>5: sys = 0.05
          if njet[0]>7: sys = 0.1
          dQCD[njet][lt][ht][dPhi] = {'deltaPhi':dPhi,'sys': sys}
        try: dQCD[QCDSB][lt][ht][dPhi]
        #  print 'QCD SB with LT',lt,', HT',ht, ' and dPhi', dPhi, ' already exists'
        except KeyError:
          sys = 0.025
          if ht[1]<0 and ht[0]>700: sys = 0.05
          #if njet[0]>7: sys = 0.1
          try: dQCD[QCDSB]
          except KeyError: dQCD[QCDSB] = {}
          try: dQCD[QCDSB][lt]
          except KeyError: dQCD[QCDSB][lt] = {}
          try: dQCD[QCDSB][lt][ht]
          except KeyError: dQCD[QCDSB][lt][ht] = {}
          try: dQCD[QCDSB][lt][ht][dPhi]
          except KeyError: dQCD[QCDSB][lt][ht][dPhi] = {'deltaPhi':dPhi, 'sys':sys}
          #dQCD[(3,4)][lt][ht][dPhi] = {'deltaPhi':dPhi, 'sys':sys}}}}
        try: dQCD[ttSB][lt][ht][dPhi]
        except KeyError:
          sys = 0.025
          if ht[1]<0 and ht[0]>700: sys = 0.05
          #if njet[0]>7: sys = 0.1
          try: dQCD[ttSB]
          except KeyError: dQCD[ttSB] = {}
          try: dQCD[ttSB][lt]
          except KeyError: dQCD[ttSB][lt] = {}
          try: dQCD[ttSB][lt][ht]
          except KeyError: dQCD[ttSB][lt][ht] = {}
          try: dQCD[ttSB][lt][ht][dPhi]
          except KeyError: dQCD[ttSB][lt][ht][dPhi] = {'deltaPhi':dPhi, 'sys':sys}
          #dQCD[(4,5)] = {lt:{ht:{dPhi:{'deltaPhi':dPhi, 'sys':sys}}}}
  return dQCD
