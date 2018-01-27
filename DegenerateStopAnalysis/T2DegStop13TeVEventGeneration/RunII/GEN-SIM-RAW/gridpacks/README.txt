These files need to be used by following the instructions from https://twiki.cern.ch/twiki/bin/viewauth/CMS/QuickGuideMadGraph5aMCatNLO summarised here:

We instruct users to clone the whole genproductions from git and work there. On a lxplus machine (not in a release area), you can do the following:

git clone git@github.com:cms-sw/genproductions.git genproductions
(if you need to use mg 2.6.x then do the following
git clone git@github.com:cms-sw/genproductions.git genproductions -b mg26x)
cd genproductions/bin/MadGraph5_aMCatNLO/
./gridpack_generation.sh <name of process card without _proc_card.dat> <folder containing cards relative to current location>

Cards from: https://github.com/CMS-SUS-XPAG/GenLHEfiles/tree/master/GridpackWorkflow/production/SMS-StopStop/templatecards
