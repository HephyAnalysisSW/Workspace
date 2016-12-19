all_analysis = {}
all_analysis["StopandSbottom"] = {"name_tex":"Stop and Sbottom"}
all_analysis["EWKGauginos"] = {"name_tex":"EWK Gauginos"}
all_analysis["Gluino"] = {"name_tex":"Gluino"}
all_analysis["Squark"] = {"name_tex":"Squark"}
 
T2bb = '#tilde{b} #rightarrow b  #tilde{#chi}_{1}^{0}'
T2tt = '#tilde{t} #rightarrow t  #tilde{#chi}_{1}^{0}'
T6bbWW ='#tilde{t}#rightarrow #tilde{#chi}_{1}^{#pm} b #rightarrow W^{#pm} #tilde{#chi}_{1}^{0}'
TChiChipmSlepL = '#tilde{#chi}^{0}_{2} #tilde{#chi}^{#pm} #rightarrow lll #nu#tilde{#chi}^{0} #tilde{#chi}^{0} '
TChiChipmStauStau = '#tilde{#chi}^{0}_{2} #tilde{#chi}^{#pm} #rightarrow ll#tau #nu#tilde{#chi}^{0} #tilde{#chi}^{0} '
TChiWZ = '#tilde{#chi}^{#pm} #tilde{#chi}^{0}_{2} #rightarrow W Z #tilde{#chi}^{0} #tilde{#chi}^{0}'
TChiWH = '#tilde{#chi}^{#pm} #tilde{#chi}^{0}_{2} #rightarrow H W #tilde{#chi}^{0} #tilde{#chi}^{0}'

T1     = '#tilde{g} #rightarrow qq #tilde{#chi}^{0}' 
T2     = '#tilde{q} #rightarrow q #tilde{#chi}^{0}' 
T1tttt = '#tilde{g} #rightarrow tt #tilde{#chi}^{0}'
T1bbbb = '#tilde{g} #rightarrow bb #tilde{#chi}^{0}'

T5VV = '#tilde{g} #rightarrow qq(#tilde{#chi}^{#pm}/#tilde{#chi}^{0}_{2})#rightarrow W/Z#tilde{#chi}^{0}'
T5WW = '#tilde{g} #rightarrow qq#tilde{#chi}^{#pm}#rightarrow W#tilde{#chi}^{0}'

T6bbHH = '#tilde{b} #rightarrow b  #tilde{#chi}_{2}^{0}#rightarrow H#tilde{#chi}_{1}^{0}'
T5tctc = '#tilde{g} #rightarrow t #tilde{t}^{0} #rightarrow c #tilde{#chi}_{1}^{0} '



# NEW


lumi = 12.9


# Gluino production
all_analysis["Gluino"]['empty']        = {'max'  : {'050': [0.0, ''           , 0 , 0   ]}, 'min': {}, 'decay': ''  ,     'delta': {'050': [0.0,''         , 0 , 0]}}
all_analysis["Gluino"]['16-014-T5VV']     = {'max'  : {'050': [1625, 'SUS-16-014',  13, lumi]}, 'min': {}, 'decay': T5VV,    'delta': {'050': [0, 'SUS-16-014',  13, lumi]},}
all_analysis["Gluino"]['16-014-T1']       = {'max'  : {'050': [1675, 'SUS-16-014',  13, lumi]}, 'min': {}, 'decay': T1,      'delta': {'050': [0, 'SUS-16-014',  13, lumi]},}
all_analysis["Gluino"]['16-014-T1tttt']   = {'max'  : {'050': [1620, 'SUS-16-014',  13, lumi]}, 'min': {}, 'decay': T1tttt,  'delta': {'050': [0, 'SUS-16-014',  13, lumi]},}
all_analysis["Gluino"]['16-015-T1bbbb']    = {'max'  : {'050': [1750, 'SUS-16-015',  13, lumi]}, 'min': {}, 'decay': T1bbbb, 'delta': {'050': [0, 'SUS-16-015',  13, lumi]},}
all_analysis["Gluino"]['16-015-T1tttt']    = {'max'  : {'050': [1700, 'SUS-16-015',  13, lumi]}, 'min': {}, 'decay': T1tttt, 'delta': {'050': [0, 'SUS-16-015',  13, lumi]},}
all_analysis["Gluino"]['16-015-T1']        = {'max'  : {'050': [1650, 'SUS-16-015',  13, lumi]}, 'min': {}, 'decay': T1,     'delta': {'050': [0, 'SUS-16-015',  13, lumi]},}
all_analysis["Gluino"]['16-016-T1bbbb']    = {'max'  : {'050': [1720, 'SUS-16-016',  13, lumi]}, 'min': {}, 'decay': T1bbbb, 'delta': {'050': [0, 'SUS-16-016',  13, lumi]},}
all_analysis["Gluino"]['16-016-T1tttt']    = {'max'  : {'050': [1380, 'SUS-16-016',  13, lumi]}, 'min': {}, 'decay': T1tttt, 'delta': {'050': [0, 'SUS-16-016',  13, lumi]},}
all_analysis["Gluino"]['16-019-T5WW']     = {'max'  : {'050': [1600, 'SUS-16-019',  13, lumi]}, 'min': {}, 'decay': T5WW,    'delta': {'050': [0, 'SUS-16-019',  13, lumi]},}
all_analysis["Gluino"]['16-019-T1tttt']   = {'max'  : {'050': [1630, 'SUS-16-019',  13, lumi]}, 'min': {}, 'decay': T1tttt,  'delta': {'050': [0, 'SUS-16-019',  13, lumi]},}
all_analysis["Gluino"]['16-020-T1tttt']   = {'max'  : {'050': [1370, 'SUS-16-020',  13, lumi]}, 'min': {}, 'decay': T5tctc,  'delta': {'050': [0, 'SUS-16-020',  13, lumi]},}
all_analysis["Gluino"]['16-020-T5WW']     = {'max'  : {'050': [1100, 'SUS-16-020',  13, lumi]}, 'min': {}, 'decay': T5tctc,  'delta': {'050': [0, 'SUS-16-020',  13, lumi]},}
all_analysis["Gluino"]['16-030-T1tttt']   = {'max'  : {'050': [1760, 'SUS-16-030',  13, lumi]}, 'min': {}, 'decay': T1tttt,  'delta': {'050': [0, 'SUS-16-030',  13, lumi]},}
all_analysis["Gluino"]['16-030-T5tctc']   = {'max'  : {'050': [1500, 'SUS-16-030',  13, lumi]}, 'min': {}, 'decay': T5tctc,  'delta': {'050': [0, 'SUS-16-030',  13, lumi]},}

#Squark
all_analysis["Squark"]['empty']        = {'max'  : {'050': [0.0, ''           , 0 , 0   ]}, 'min': {}, 'decay': ''  ,     'delta': {'050': [0.0,''         , 0 , 0]}}
all_analysis["Squark"]['16-015-T2']        = {'max'  : {'050': [1350, 'SUS-16-015',  13, lumi]}, 'min': {}, 'decay': T2,    'delta': {'050': [0, 'SUS-16-015',   13, lumi]},}
all_analysis["Squark"]['16-014-T2']        = {'max'  : {'050': [1160, 'SUS-16-014',  13, lumi]}, 'min': {}, 'decay': T2,     'delta': {'050': [0, 'SUS-16-014',  13, lumi]},}



# Stop
all_analysis["StopandSbottom"]['empty']        = {'max'  : {'050': [0.0, ''           , 0 , 0   ]}, 'min': {}, 'decay': ''  ,     'delta': {'050': [0.0,''         , 0 , 0]}}
all_analysis["StopandSbottom"]['16-014-T2tt']  = {'max'  : {'050': [840, 'SUS-16-014', 13, lumi]}, 'min': {}, 'decay': T2tt,     'delta': {'050': [0, 'SUS-16-014', 13, lumi]},}
all_analysis["StopandSbottom"]['16-015-T2tt']  = {'max'  : {'050': [900, 'SUS-16-015', 13, lumi]}, 'min': {},  'decay': T2tt,   'delta': {'050': [0, 'SUS-16-015', 13, lumi]},}
all_analysis["StopandSbottom"]['16-028-T2tt']              = {'max'  : {'050': [860, 'SUS-16-028', 13, lumi]}, 'min': {}, 'decay': T2tt,   'delta': {'050': [0, 'SUS-16-028', 13, lumi]}}
all_analysis["StopandSbottom"]['16-028-T6bbWW']            = {'max'  : {'050': [760, 'SUS-16-028', 13, lumi]}, 'min': {}, 'decay': T6bbWW, 'delta': {'050': [0, 'SUS-16-028', 13, lumi]}}
all_analysis["StopandSbottom"]['16-029-T2tt']              = {'max'  : {'050': [825, 'SUS-16-029', 13, lumi]}, 'min': {}, 'decay': T2tt,   'delta': {'050': [0, 'SUS-16-029', 13, lumi]}}
all_analysis["StopandSbottom"]['16-029-T6bbWW']            = {'max'  : {'050': [710, 'SUS-16-029', 13, lumi]}, 'min': {}, 'decay': T6bbWW, 'delta': {'050': [0, 'SUS-16-029', 13, lumi]}}
all_analysis["StopandSbottom"]['16-030-T2tt']  = {'max'  : {'050': [900, 'SUS-16-030', 13, lumi]},  'min': {}, 'decay': T2tt,    'delta': {'050': [0, 'SUS-16-030', 13, lumi]},}

#Sbottom
all_analysis["StopandSbottom"]['16-014-T2bb']  = {'max'  : {'050': [790,  'SUS-16-014', 13, lumi]}, 'min': {}, 'decay': T2bb,     'delta': {'050': [0, 'SUS-16-014', 13, lumi]},}
all_analysis["StopandSbottom"]['16-016-T2bb']  = {'max'  : {'050': [1050, 'SUS-16-016', 13, lumi]}, 'min': {}, 'decay': T2bb,     'delta': {'050': [0, 'SUS-16-016', 13, lumi]},}
all_analysis["StopandSbottom"]['16-015-T2bb']  = {'max'  : {'050': [1030, 'SUS-16-015', 13, lumi]}, 'min': {}, 'decay': T2bb,     'delta': {'050': [0, 'SUS-16-015', 13, lumi]},}

#EW Gauginos
#all_analysis["EWKGauginos"]['empty']        = {'max'  : {'050': [0.0, ''           , 0 , 0   ]}, 'min': {}, 'decay': ''  ,     'delta': {'050': [0.0,''         , 0 , 0]}}
all_analysis["EWKGauginos"]['16-024-TChiChipmSlepL']       = {'max'  : {'050': [1000, 'SUS-16-024', 13, lumi]},'min': {}, 'decay': TChiChipmSlepL, 'delta': {'050': [0, 'SUS-16-024', 13, lumi] }}
all_analysis["EWKGauginos"]['16-024-TChiChipmStauStau']    = {'max'  : {'050': [460, 'SUS-16-024', 13, lumi]}, 'min': {}, 'decay': TChiChipmStauStau, 'delta': {'050': [0, 'SUS-16-024', 13, lumi]}}
all_analysis["EWKGauginos"]['16-024-TChiWZ']               = {'max'  : {'050': [375, 'SUS-16-024', 13, lumi]}, 'min': {}, 'decay': TChiWZ, 'delta': {'050': [0, 'SUS-16-024', 13, lumi]},}
all_analysis["EWKGauginos"]['16-024-TChiWH']               = {'max'  : {'050': [150, 'SUS-16-024', 13, lumi]}, 'min': {}, 'decay': TChiWH, 'delta': {'050': [0, 'SUS-16-024', 13, lumi]},}


