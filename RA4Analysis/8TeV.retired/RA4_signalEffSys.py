import ROOT
import math
import pickle

def readFile(htcuts, metcuts, m0 = 0, m12 = 0):

    count_mu            = {}
    count_mu_jes_minus  = {}
    count_mu_jes_plus   = {}
    count_ele           = {}
    count_ele_jes_minus = {}
    count_ele_jes_plus  = {}
    
    for htcut in htcuts:
        count_mu           [htcut] = {}
        count_mu_jes_plus  [htcut] = {}
        count_mu_jes_minus [htcut] = {}
        count_ele          [htcut] = {}
        count_ele_jes_plus [htcut] = {}
        count_ele_jes_minus[htcut] = {}
        for metcut in metcuts:
            base_cut = "pfRA4Tupelizer_ht > " + str(htcut) + " && pfRA4Tupelizer_barepfmet > " + str(metcut)
                    
            cut = base_cut.replace("pfRA4Tupelizer_","")
            cut_jes_plus = base_cut.replace("pfRA4Tupelizer","pfRA4TupelizerJESPlus")
            cut_jes_minus = base_cut.replace("pfRA4Tupelizer","pfRA4TupelizerJESMinus")
    
            if (m0 > 0 or m12 > 0):
                cut = cut + " && msugraM0 == " + str(m0) + " && msugraM12 == " + str(m12)
                cut_jes_plus = cut_jes_plus + " && msugraM0 == " + str(m0) + " && msugraM12 == " + str(m12)
                cut_jes_minus = cut_jes_minus + " && msugraM0 == " + str(m0) + " && msugraM12 == " + str(m12)
    
            print "    -> ht>"+str(htcut)+", met>"+str(metcut)+":"
            count_mu           [htcut][metcut] = globals()["trees"]["mu"           ].GetEntries(cut)            
            count_mu_jes_plus  [htcut][metcut] = globals()["trees"]["mu_jes_plus"  ].GetEntries(cut_jes_plus)   
            count_mu_jes_minus [htcut][metcut] = globals()["trees"]["mu_jes_minus" ].GetEntries(cut_jes_minus)  
            count_ele          [htcut][metcut] = globals()["trees"]["ele"          ].GetEntries(cut)          
            count_ele_jes_plus [htcut][metcut] = globals()["trees"]["ele_jes_plus" ].GetEntries(cut_jes_plus) 
            count_ele_jes_minus[htcut][metcut] = globals()["trees"]["ele_jes_minus"].GetEntries(cut_jes_minus)
       
    return [count_mu,count_mu_jes_minus,count_mu_jes_plus,count_ele,count_ele_jes_minus,count_ele_jes_plus]
    
    
def calcSigEffSys(m0 = 0, m12 = 0):

    htcuts = [750, 1000]
    metcuts = [250, 350, 450, 550]
    
    print "    -> processing cuts..."                                                                                                        
    if (m0 > 0 and m12 > 0):
        [count_mu,count_mu_jes_minus,count_mu_jes_plus,count_ele,count_ele_jes_minus,count_ele_jes_plus] = readFile(htcuts, metcuts, m0, m12)
    else:
        [count_mu,count_mu_jes_minus,count_mu_jes_plus,count_ele,count_ele_jes_minus,count_ele_jes_plus] = readFile(htcuts, metcuts)
 
        
    for htcut in htcuts:
        globals()["sigEffSys"][m0][m12][htcut] = {}
        for metcut in metcuts:
            globals()["sigEffSys"][m0][m12][htcut][metcut] = {}
            print "    -> result of cut: ht>"+str(htcut)+", met>"+str(metcut)+":"
            count_zero      = count_mu[htcut][metcut]+count_ele[htcut][metcut]
            print "       JES0 = "+str(count_zero)
            count_jes_plus  = count_mu_jes_plus[htcut][metcut]+count_ele_jes_plus[htcut][metcut]
            print "       JES+ = "+str(count_jes_plus)
            count_jes_minus = count_mu_jes_minus[htcut][metcut]+count_ele_jes_minus[htcut][metcut]
            print "       JES- = "+str(count_jes_minus)
            if not (count_zero == 0): res = 1./2.*(count_jes_plus-count_jes_minus)/count_zero
            else: res = -1 
            globals()["sigEffSys"][m0][m12][htcut][metcut]["sys"] = res
            globals()["sigEffSys"][m0][m12][htcut][metcut]["jes+"] = count_jes_plus
            globals()["sigEffSys"][m0][m12][htcut][metcut]["jes-"] = count_jes_minus
            globals()["sigEffSys"][m0][m12][htcut][metcut]["jes0"] = count_zero
            print "       -> sig. eff. sys. = "+str(res)
    

def runSigEffSys(lm = "LM6"):
    ROOT.gSystem.Load("EventLoop_cc.so")
    loop = ROOT.EventLoop()
    
    txt = ROOT.TLatex()
    txt.SetTextSize(0.03)
    

    fpath = "/data/schoef/pat_111201/"
    fpath_mu = fpath+"Mu/"    
    fpath_ele = fpath+"EG/"    
      
    if (lm == "msugra"):
        fpath_mu  = fpath_mu +"msugra/"    
        fpath_ele = fpath_ele+"msugra/"    
    else: 
        fpath_mu  = fpath_mu +lm+"/"    
        fpath_ele = fpath_ele+lm+"/"    
    
    print fpath_mu  
    print fpath_ele
                                                                                                    
    fpath_mu  = fpath_mu +"histo_*.root"    
    fpath_ele = fpath_ele+"histo_*.root"    

    c_mu = ROOT.TChain("Events","muons")
    c_mu.Add(fpath_mu)
 
    c_ele = ROOT.TChain("Events","electrons")
    c_ele.Add(fpath_ele)
    
    cut_mu  = "pfRA4Tupelizer_singleMuonic && pfRA4Tupelizer_leptonPt > 20 && pfRA4Tupelizer_jet2pt > 40 && pfRA4Tupelizer_nvetoMuons == 1 && pfRA4Tupelizer_nvetoElectrons == 0 && pfRA4Tupelizer_ht > " + str(750) + " && pfRA4Tupelizer_barepfmet > " + str(250)
    cut_ele = "pfRA4Tupelizer_singleElectronic && pfRA4Tupelizer_leptonPt > 20 && pfRA4Tupelizer_jet2pt > 40 && pfRA4Tupelizer_nvetoMuons == 0 && pfRA4Tupelizer_nvetoElectrons == 1 && pfRA4Tupelizer_ht > " + str(750) + " && pfRA4Tupelizer_barepfmet > " + str(250)

    base_cut_mu = cut_mu.replace("pfRA4Tupelizer_","")
    base_cut_mu_jes_plus  = cut_mu.replace("pfRA4Tupelizer","pfRA4TupelizerJESPlus")
    base_cut_mu_jes_minus = cut_mu.replace("pfRA4Tupelizer","pfRA4TupelizerJESMinus")
    base_cut_ele = cut_ele.replace("pfRA4Tupelizer_","")
    base_cut_ele_jes_plus  = cut_ele.replace("pfRA4Tupelizer","pfRA4TupelizerJESPlus")
    base_cut_ele_jes_minus = cut_ele.replace("pfRA4Tupelizer","pfRA4TupelizerJESMinus")

    print "generating reduced trees:"
    print "    -> mu:"
    t_mu            = c_mu .CopyTree(base_cut_mu)
    print "    -> mu_jes_plus:"
    t_mu_jes_plus   = c_mu .CopyTree(base_cut_mu_jes_plus)
    print "    -> mu_jes_minus:"
    t_mu_jes_minus  = c_mu .CopyTree(base_cut_mu_jes_minus)
    print "    -> ele:"
    t_ele           = c_ele.CopyTree(base_cut_ele)
    print "    -> ele_jes_plus:"
    t_ele_jes_plus  = c_ele.CopyTree(base_cut_ele_jes_plus)
    print "    -> ele_jes_minus:"
    t_ele_jes_minus = c_ele.CopyTree(base_cut_ele_jes_minus)
  
    globals()["trees"] = {}
    globals()["trees"]["mu"           ] = t_mu
    globals()["trees"]["mu_jes_plus"  ] = t_mu_jes_plus
    globals()["trees"]["mu_jes_minus" ] = t_mu_jes_minus
    globals()["trees"]["ele"          ] = t_ele
    globals()["trees"]["ele_jes_plus" ] = t_ele_jes_plus
    globals()["trees"]["ele_jes_minus"] = t_ele_jes_minus

#    f_trees = open('./cutTrees_sigEffSys_'+lm+'_inc'+'.pickle', 'w')
#    pickle.dump(trees, f_trees)
#    f_trees.close()
#
    
    globals()["sigEffSys"] = {}
    if (lm == "msugra"):
        for m0 in range(100, 1701, 20):
            globals()["sigEffSys"][m0] = {}
            for m12 in range(100, 701, 20):
                print " -> m0="+str(m0)+", m12="+str(m12)+":"
                globals()["sigEffSys"][m0][m12] = {}
                calcSigEffSys(m0, m12)
            print globals()["sigEffSys"][m0]
    else:
        globals()["sigEffSys"][0] = {}
        globals()["sigEffSys"][0][0] = {}
        calcSigEffSys()

    f = open('/afs/hephy.at/user/k/kwolf/www/RA4_Study/SigEffSys/sigEffSysFast_'+lm+'_inc'+'.pickle', 'w')
    sigEffSys = globals()["sigEffSys"]
    pickle.dump(sigEffSys, f)
    f.close()
    return sigEffSys


def plotSigEffSys(fname = "/afs/hephy.at/user/k/kwolf/www/RA4_Study/SigEffSys/sigEffSysFull_msugra_inc.pickle"):
    ROOT.gSystem.Load("EventLoop_cc.so")
    loop = ROOT.EventLoop()
    
    txt = ROOT.TLatex()
    txt.SetTextSize(0.03)
    
    f = open(fname,'r')
    d = pickle.load(f)

    htcuts = [750, 1000]
    metcuts = [250, 350, 450, 550]
 
    h_sigEff = {}  
    h_sigEff_Err = {}  
    h_sigEff_j0jplus = {}  
    h_sigEff_j0jminus = {}  
    for htcut in htcuts:
        h_sigEff[htcut] = {}
        h_sigEff_Err[htcut] = {}
        h_sigEff_j0jplus[htcut] = {}
        h_sigEff_j0jminus[htcut] = {}
        for metcut in metcuts:
            h_sigEff[htcut][metcut] = ROOT.TH2F("h_sigEff"+str(htcut)+"_"+str(metcut), "H_{T}>"+str(htcut)+", #slash{E}_{T}>"+str(metcut)+", b-inclusive",           (1710-90)/20, 90, 1710, (710-90)/20, 90, 710)
            h_sigEff_Err[htcut][metcut] = ROOT.TH2F("h_sigEff_Err"+str(htcut)+"_"+str(metcut), "H_{T}>"+str(htcut)+", #slash{E}_{T}>"+str(metcut)+", b-inclusive",           (1710-90)/20, 90, 1710, (710-90)/20, 90, 710)
            h_sigEff_j0jplus[htcut][metcut] = ROOT.TH2F("h_sigEff_j0jplus"+str(htcut)+"_"+str(metcut), "H_{T}>"+str(htcut)+", #slash{E}_{T}>"+str(metcut)+", b-inclusive",           (1000)/50, 0, 1000, int(0.1/0.005), 0., 100)
            h_sigEff_j0jminus[htcut][metcut] = ROOT.TH2F("h_sigEff_j0jminus"+str(htcut)+"_"+str(metcut), "H_{T}>"+str(htcut)+", #slash{E}_{T}>"+str(metcut)+", b-inclusive",           (1000)/50, 0, 1000, int(0.1/0.005), 0., 100)
    
    for m0 in range(120, 1681, 20):
        for m12 in range(120, 681, 20):
            if d.has_key(m0):
                if d[m0].has_key(m12):    
                        for htcut in htcuts:
                            for metcut in metcuts:
                                bin = h_sigEff[htcut][metcut].FindBin(m0,m12)
                                if d[m0][m12][htcut][metcut]["jes0"] == 0: continue                                
                                jes0 = d[m0][m12][htcut][metcut]["jes0"]+d[m0+20][m12][htcut][metcut]["jes0"]+d[m0-20][m12][htcut][metcut]["jes0"]+d[m0][m12+20][htcut][metcut]["jes0"]+d[m0][m12-20][htcut][metcut]["jes0"]+d[m0+20][m12+20][htcut][metcut]["jes0"]+d[m0+20][m12-20][htcut][metcut]["jes0"]+d[m0-20][m12+20][htcut][metcut]["jes0"]+d[m0-20][m12-20][htcut][metcut]["jes0"]
                                jesplus = d[m0][m12][htcut][metcut]["jes+"]+d[m0+20][m12][htcut][metcut]["jes+"]+d[m0-20][m12][htcut][metcut]["jes+"]+d[m0][m12+20][htcut][metcut]["jes+"]+d[m0][m12-20][htcut][metcut]["jes+"]+d[m0+20][m12+20][htcut][metcut]["jes+"]+d[m0+20][m12-20][htcut][metcut]["jes+"]+d[m0-20][m12+20][htcut][metcut]["jes+"]+d[m0-20][m12-20][htcut][metcut]["jes+"]
                                jesminus = d[m0][m12][htcut][metcut]["jes-"]+d[m0+20][m12][htcut][metcut]["jes-"]+d[m0-20][m12][htcut][metcut]["jes-"]+d[m0][m12+20][htcut][metcut]["jes-"]+d[m0][m12-20][htcut][metcut]["jes-"]+d[m0+20][m12+20][htcut][metcut]["jes-"]+d[m0+20][m12-20][htcut][metcut]["jes-"]+d[m0-20][m12+20][htcut][metcut]["jes-"]+d[m0-20][m12-20][htcut][metcut]["jes-"]     
                                syserr = math.sqrt((jesplus-jes0 + jes0-jesminus)**2/(4.*jes0**3) + (jesplus-jes0)/(4.*jes0**2) + (jes0-jesminus)/(4.*jes0**2))
                                sys = 1./2.*(jesplus-jesminus)/jes0
                                if (sys > 0 and syserr/sys < 0.5): h_sigEff[htcut][metcut].SetBinContent(bin, sys)
                                if (sys > 0): h_sigEff_Err[htcut][metcut].SetBinContent(bin, syserr/sys)
                                h_sigEff_j0jplus[htcut][metcut].Fill(jes0, (jesplus-jes0))
                                h_sigEff_j0jminus[htcut][metcut].Fill(jes0, (jes0-jesminus))
    c_sigEff = {}  
    for htcut in htcuts:
        c_sigEff[htcut] = {}
        for metcut in metcuts:
            c_sigEff[htcut][metcut] = ROOT.TCanvas("c_sigEff"+str(htcut)+"_"+str(metcut), "H_{T}>"+str(htcut)+", #slash{E}_{T}>"+str(metcut)+", b-inclusive", 800,600)
            c_sigEff[htcut][metcut].Divide(2,2)   

            h_sigEff[htcut][metcut].SetMinimum(0)
            h_sigEff[htcut][metcut].SetMaximum(0.30)
            h_sigEff[htcut][metcut].Draw("colz")
            h_sigEff[htcut][metcut].GetXaxis().SetTitle("m_{0}")
            h_sigEff[htcut][metcut].GetYaxis().SetTitle("m_{1/2}")

            c_sigEff[htcut][metcut].SaveAs("/afs/hephy.at/user/k/kwolf/www/RA4_Study/SigEffSys_test/"+h_sigEff[htcut][metcut].GetName()+"_exclude0p5RelError.pdf")    

    return [h_sigEff, h_sigEff_Err, h_sigEff_j0jplus, h_sigEff_j0jminus]