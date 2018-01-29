#!/usr/bin/env python
''' Analysis script for gen plots
'''
#
# Standard imports and batch mode
#
import ROOT, os
ROOT.gROOT.SetBatch(True)
import itertools
from math                                import sqrt, cos, sin, pi, acos
import imp

#RootTools
from RootTools.core.standard             import *

#TopEFT
from TopEFT.Tools.user                   import skim_output_directory
from TopEFT.Tools.GenSearch              import GenSearch
from TopEFT.Tools.helpers                import deltaR2, cosThetaStar

#
# Arguments
# 
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO',          nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--small',              action='store_true', help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--targetDir',          action='store',      default='v2')
argParser.add_argument('--sample',             action='store',      default='fwlite_ttZ_ll_LO_sm')
argParser.add_argument('--nJobs',              action='store',      nargs='?', type=int, default=1,                          help="Maximum number of simultaneous jobs.")
argParser.add_argument('--job',                action='store',      nargs='?', type=int, default=0,                         help="Run only job i")
args = argParser.parse_args()

#
# Logger
#
import TopEFT.Tools.logger as logger
import RootTools.core.logger as logger_rt
logger    = logger.get_logger(   args.logLevel, logFile = None)
logger_rt = logger_rt.get_logger(args.logLevel, logFile = None)

sample_file = "./fwlite_benchmarks.py"
samples = imp.load_source( "samples", os.path.expandvars( sample_file ) )
sample = getattr( samples, args.sample )

maxN = -1
if args.small: 
    args.targetDir += "_small"
    maxN = 500
    sample.files=sample.files[:2]

output_directory = os.path.join(skim_output_directory, 'gen', args.targetDir, sample.name) 
if not os.path.exists( output_directory ): 
    os.makedirs( output_directory )
    logger.info( "Created output directory %s", output_directory )

# Run only job number "args.job" from total of "args.nJobs"
if args.nJobs>1:
    n_files_before = len(sample.files)
    sample = sample.split(args.nJobs)[args.job]
    n_files_after  = len(sample.files)
    logger.info( "Running job %i/%i over %i files from a total of %i.", args.job, args.nJobs, n_files_after, n_files_before)

products = {
    'gp':{'type':'vector<reco::GenParticle>', 'label':("genParticles")},
    'genJets':{'type':'vector<reco::GenJet>', 'label':("ak4GenJets")},
    'genMET':{'type':'vector<reco::GenMET>',  'label':("genMetTrue")},
}

def varnames( vec_vars ):
    return [v.split('/')[0] for v in vec_vars.split(',')]

# standard variables
variables  = ["run/I", "lumi/I", "evt/l"]
# MET
variables += ["GenMet_pt/F", "GenMet_phi/F"]
# jet vector
jet_read_vars       =  "pt/F,eta/F,phi/F"
jet_read_varnames   =  varnames( jet_read_vars )
jet_write_vars      = jet_read_vars+',matchBParton/I' 
jet_write_varnames  =  varnames( jet_write_vars )
variables     += ["GenJet[%s]"%jet_write_vars]
# lepton vector 
lep_vars       =  "pt/F,eta/F,phi/F,pdgId/I"
lep_extra_vars =  "motherPdgId/I"
lep_varnames   =  varnames( lep_vars ) 
lep_all_varnames = lep_varnames + varnames(lep_extra_vars)
variables     += ["GenLep[%s]"%(','.join([lep_vars, lep_extra_vars]))]
# top vector
top_vars       =  "pt/F,eta/F,phi/F,mass/F"
top_varnames   =  varnames( top_vars ) 
variables     += ["top[%s]"%top_vars]


b_vars       =  "pt/F,eta/F,phi/F,mass/F"
b_varnames   =  varnames( b_vars ) 

w_readvars   =  "pt/F,eta/F,phi/F,mass/F"
w_extravars  = 'cosThetaStar/F,daughterId/I'
w_vars       = ','.join([w_readvars, w_extravars])
w_varnames   = varnames(w_vars)

p4_vars     = "pt/F,eta/F,phi/F,mass/F"
p4_varnames = varnames( p4_vars )
variables  += ['stop[%s]'%p4_vars ]
variables  += ['LSP[%s]'%p4_vars ]
variables  += ['W[%s]'%w_vars ]
variables  += ['b[%s]'%p4_vars ]


fromW_vars  = p4_vars + ",pdgId/I"
fromW_varnames = varnames( fromW_vars )
variables  += ['fromW[%s]'%fromW_vars ]


fromSUSY_vars  = p4_vars + ",pdgId/I,motherPdgId/I"
fromSUSY_varnames = varnames( fromSUSY_vars )
variables  += ['fromSUSY[%s]'%fromSUSY_vars ]


# Z vector
#Z_read_varnames= [ 'pt', 'phi', 'eta', 'mass']
#varia2bles     += ["Z_pt/F", "Z_phi/F", "Z_eta/F", "Z_mass/F", "Z_cosThetaStar/F", "Z_daughterPdg/I"]
# gamma vector
#gamma_read_varnames= [ 'pt', 'phi', 'eta', 'mass']
#variables     += ["gamma_pt/F", "gamma_phi/F", "gamma_eta/F", "gamma_mass/F"]


def getVal( obj, attr):
    attr = getattr(obj,attr)
    if hasattr(attr, '__call__'):
        return attr()
    else:
        return attr


def fill_vector( event, collection_name, collection_varnames, objects):
    setattr( event, "n"+collection_name, len(objects) )
    for i_obj, obj in enumerate(objects):
        for var in collection_varnames:
            getattr(event, collection_name+"_"+var)[i_obj] = obj[var]

reader = sample.fwliteReader( products = products )

def filler( event ):

    event.evt, event.lumi, event.run = reader.evt

    if reader.position % 100==0: logger.info("At event %i/%i", reader.position, reader.nEvents)

    # All gen particles
    gp      = reader.products['gp']

    # for searching
    search  = GenSearch( gp )

    # find heavy objects before they decay
    tops = map( lambda t:{var: getattr(t, var)() for var in p4_varnames}, filter( lambda p:abs(p.pdgId())==6  and search.isLast(p),  gp) )
    bs   = map( lambda b:{var: getattr(b, var)() for var in p4_varnames}, filter( lambda p:abs(p.pdgId())==5  and search.isLast(p),  gp) )
    ws   = map( lambda t:{var: getattr(t, var)() for var in p4_varnames}, filter( lambda p:abs(p.pdgId())==24 and search.isLast(p),  gp) )
    stops= map( lambda t:{var: getattr(t, var)() for var in p4_varnames}, filter( lambda p:abs(p.pdgId())==1000006  and search.isLast(p),  gp) )
    lsps = map( lambda t:{var: getattr(t, var)() for var in p4_varnames}, filter( lambda p:abs(p.pdgId())==1000022  and search.isLast(p),  gp) )

    for col in [tops, bs, ws, stops, lsps]:
        col.sort( key = lambda p:-p['pt']  )
    fill_vector( event, "top" , p4_varnames, tops ) 
    fill_vector( event, "b"   , p4_varnames, tops ) 
    fill_vector( event, "W"   , p4_varnames, tops ) 
    fill_vector( event, "stop", p4_varnames, tops ) 
    fill_vector( event, "LSP" , p4_varnames, tops ) 

    #gen_Ws = filter( lambda p:abs(p.pdgId())==24 and search.isLast(p), gp)
    #gen_Ws.sort( key = lambda p: -p.pt() )
    #if len(gen_Ws)>0: 
    #    gen_W = gen_Ws[0]
    #    for var in p4_varnames:
    #       setattr( event, "W_"+var,  getattr(gen_W, var)() )
    #else:
    #    gen_W = None
    #
    #if gen_W is not None:

    #    d1, d2 = gen_W.daughter(0), gen_W.daughter(1)
    #    if d1.pdgId()>0: 
    #        lm, lp = d1, d2
    #    else:
    #        lm, lp = d2, d1
    #    event.W_daughterPdg = lm.pdgId()
    #    event.W_cosThetaStar = cosThetaStar(gen_W.mass(), gen_W.pt(), gen_W.eta(), gen_W.phi(), lm.pt(), lm.eta(), lm.phi())

    #gen_Gammas = filter( lambda p:abs(p.pdgId())==22 and search.isLast(p), gp)
    #gen_Gammas.sort( key = lambda p: -p.pt() )
    #if len(gen_Gammas)>0: 
    #    gen_Gamma = gen_Gammas[0]
    #    for var in gamma_read_varnames:
    #       setattr( event, "gamma_"+var,  getattr(gen_Gamma, var)() )
    #else:
    #    gen_Gamma = None
    #
    # find all leptons
    final_state_particles = filter( lambda p: search.isLast(p), gp )
    fromW = []
    fromSUSY = []
    for p in final_state_particles:
        pdgId, pt, eta, phi, mass = p.pdgId(), p.pt(), p.eta(), p.phi(), p.mass()
        #if abs(pdgId) in [6]:
        #    tops.append(p)
        #elif abs(pdgId) in [5]:
        #    bs.append(p)
        #elif abs(pdgId) in [24]:
        #    ws.append(p)
        #elif abs(pdgId) in [1000022]:
        #    lsps.append(p)
        #elif abs(pdgId) in [1000006]:
        #    stops.append(p)
     
        firstMother = search.ascend(p).mother().pdgId() if search.ascend(p).mother() else -1           
        p.motherPdgId = firstMother 
        if abs(firstMother) in [24]:
            fromW.append(p)
        if abs(firstMother) >= 1E6:
            fromSUSY.append(p)


    

    for col_name, col, col_vars in ( ('fromSUSY',fromSUSY, fromSUSY_varnames), ):
        col_dicts = [ {var: getVal(p_,var) for var in col_vars} for p_ in col ]
        col_dicts.sort( key = lambda p:-p['pt']  )
        fill_vector( event, col_name , col_vars, col_dicts ) 


    #from_w = [ (search.ascend(l), l) for l in filter( lambda p:abs(  ) in [11, 13] and search.isLast(p) and p.pt()>=0,  gp) ]
    


    leptons = [ (search.ascend(l), l) for l in filter( lambda p:abs(p.pdgId()) in [11, 13] and search.isLast(p) and p.pt()>=0,  gp) ]
    leps    = []
    for first, last in leptons:
        mother_pdgId = first.mother(0).pdgId() if first.numberOfMothers()>0 else -1
        if not abs(mother_pdgId) in [24]: continue
        leps.append( {var: getattr(last, var)() for var in lep_varnames} )
        leps[-1]['motherPdgId'] = mother_pdgId

    leps.sort( key = lambda p:-p['pt'] )
    fill_vector( event, "GenLep", lep_all_varnames, leps)

    # MET
    event.GenMet_pt = reader.products['genMET'][0].pt()
    event.GenMet_phi = reader.products['genMET'][0].phi()

    # jets
    jets = map( lambda t:{var: getattr(t, var)() for var in jet_read_varnames}, filter( lambda j:j.pt()>30, reader.products['genJets']) )

    # jet/lepton disambiguation
    jets = filter( lambda j: (min([999]+[deltaR2(j, l) for l in leps if l['pt']>10]) > 0.3**2 ), jets )

    # find b's from tops:
    b_partons = [ b for b in filter( lambda p:abs(p.pdgId())==5 and p.numberOfMothers()==1 and abs(p.mother(0).pdgId())==6,  gp) ]

    for jet in jets:
        jet['matchBParton'] = ( min([999]+[deltaR2(jet, {'eta':b.eta(), 'phi':b.phi()}) for b in b_partons]) < 0.2**2 )

    jets.sort( key = lambda p:-p['pt'] )
    fill_vector( event, "GenJet", jet_write_varnames, jets)

tmp_dir     = ROOT.gDirectory
#post_fix = '_%i'%args.job if args.nJobs > 1 else ''
output_filename =  os.path.join(output_directory, sample.name+'.root') 
output_file = ROOT.TFile( output_filename, 'recreate')
output_file.cd()
maker = TreeMaker(
    sequence  = [ filler ],
    variables = [ TreeVariable.fromString(x) for x in variables ],
    treeName = "Events"
    )

tmp_dir.cd()

counter = 0
reader.start()
maker.start()

while reader.run( ):
    #if abs(map( lambda p: p.daughter(0).pdgId(), filter( lambda p: p.pdgId()==23 and p.numberOfDaughters()==2, reader.products['gp']))[0])==13: 
    #    maker.run()
    #    break
    maker.run()

    counter += 1
    if counter == maxN:  break

logger.info( "Done with running over %i events.", reader.nEvents )

output_file.cd()
maker.tree.Write()
output_file.Close()

logger.info( "Written output file %s", output_filename )
