import jinja2
import subprocess
import os

templateLoader = jinja2.FileSystemLoader( searchpath="./templates/" )
templateEnv = jinja2.Environment( loader=templateLoader )

crabconfig=templateEnv.get_template("FastSim_crab.ja.py")
cmsswconfig=templateEnv.get_template("FastSim_filtered_cfg.ja.py")

lspmass=270

lhedir="root://hephyse.oeaw.ac.at//dpm/oeaw.ac.at/home/cms/store/user/nrad/lhe/T2tt_v2/11p8M/stop300_LSP{MASS}/".format(MASS=lspmass)


lsout = subprocess.Popen(["gfal-ls "+ lhedir ], shell = True , stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


configdir='./stop300_LSP%s/'%lspmass
os.mkdir(configdir)
for lhefile in lsout.stdout.readlines():
    lhefile = lhefile[:-1]
    if not lhefile.endswith(".lhe"):
        continue
    print lhefile
    lhetag=lhefile.replace(".lhe","")
    crabconfigout=open( configdir + "crab_%s_cfg.py"%lhetag,"w")
    cmsswconfigout=open( configdir + "FastSim_filtered_%s_cfg.py"%lhetag,"w")
    crabconfigout.write( crabconfig.render(LSPMASS=lspmass, LHETAG=lhetag) )
    cmsswconfigout.write( cmsswconfig.render(LSPMASS=lspmass, LHEFILE=lhefile) )
    crabconfigout.close()
    cmsswconfigout.close()



