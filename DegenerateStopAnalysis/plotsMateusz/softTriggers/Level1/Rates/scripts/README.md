# utm-cmssw.sh
- use the following scripts to prepare codes for cms-l1t-utm/utm
  - utm-cmssw.sh for CMSSW_8_0_X
  - utm-cmssw-xsd33.sh for CMSSW_8_1_X

# genCsv.py
- use genCsv.py for generating csv file to be used with the uGT emulator (needs python binding of the UTM library)

# menu2lib.py
- use menu2lib.py for generating c++ file to be used with L1Ntuple (needs python binding of the UTM library)
- usage: `python menu2lib.py --menu <path to menu xml> [--output <output c++ file name>]`

# json2xml.py
- use json2xml.py for producing XML snippet to be included in the Level-1 trigger menu XML file.
- usage: `python json2xml.py --input <path to serialised algorithms> [--output <output file for XML snippet]`
- follow the instruction in the test/00ReadMe.txt file to serialise algorithms then to produce xml snippet for the algorithms

# makeEmptyMenu.py
- use makeEmptyMenu.py for generating menu file with empty algorithm (needs python binding of the UTM library)
- usage: `python makeEmptyMenu.py --menu <path to L1 menu xml file>`

# Follow the instruction below to install python bindings of the UTM library on lxplus [checked on 2016-11-11]
```{r, engine='bash', count_lines}
git clone https://gitlab.cern.ch/cms-l1t-utm/utm.git
cd utm
git checkout r47119-xsd330-patch
# local installation of xerces-c
wget http://linuxsoft.cern.ch/cern/slc6X/extras/x86_64/RPMS/libxerces-c-devel-3.1.2-3.1.slc6.x86_64.rpm
rpm2cpio libxerces-c-devel-3.1.2-3.1.slc6.x86_64.rpm > libxerces-c-devel-3.1.2-3.1.slc6.x86_64.cpio
cat libxerces-c-devel-3.1.2-3.1.slc6.x86_64.cpio | cpio -i -d
wget http://linuxsoft.cern.ch/cern/slc6X/extras/x86_64/RPMS/libxerces-c-3_1-3.1.2-3.1.slc6.x86_64.rpm
rpm2cpio libxerces-c-3_1-3.1.2-3.1.slc6.x86_64.rpm > libxerces-c-3_1-3.1.2-3.1.slc6.x86_64.cpio
cat libxerces-c-3_1-3.1.2-3.1.slc6.x86_64.cpio | cpio -i -d
# local installation of swig
wget http://linuxsoft.cern.ch/cern/slc6X/updates/x86_64/RPMS/swig-1.3.40-6.el6.x86_64.rpm
rpm2cpio swig-1.3.40-6.el6.x86_64.rpm > swig-1.3.40-6.el6.x86_64.cpio
cat swig-1.3.40-6.el6.x86_64.cpio | cpio -i -d
cd usr
ln -s lib64 lib
cd ..
export XERCES_LIB_DIR=`pwd`/usr/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:`pwd`/usr/lib
export XERCES_C_BASE=`pwd`/usr
export XERCES_ROOT=`pwd`/usr
export PATH=$PATH:`pwd`/usr/bin
export SWIG_LIB=`pwd`/usr/share/swig/1.3.40/
make -f Makefile.standalone
make -f Makefile.standalone python


# set base directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR

# XSD dir
export UTM_XSD_DIR=${DIR}/tmXsd

# Library path
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${DIR}/tmGrammar
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${DIR}/tmTable
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${DIR}/tmUtil
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${DIR}/tmXsd
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${DIR}/tmEventSetup
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${DIR}/usr/lib

# Python package/module paths
export PYTHONPATH=${PYTHONPATH}:${DIR}/tmTable
export PYTHONPATH=${PYTHONPATH}:${DIR}/tmGrammar
export PYTHONPATH=${PYTHONPATH}:${DIR}/tmEventSetup
```
