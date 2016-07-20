''' Sample definition file for CMG tuples of background MC samples.


Note: samples which have extended datasets have the key "ext" which is a list of all datasets
contributing to the sample, including the dataset which is defined.

Example: 
    "ext": [WJetsToLNu_HT200to400, WJetsToLNu_HT200to400_ext] 
    appears in both WJetsToLNu_HT200to400 and WJetsToLNu_HT200to400_ext definition.
'''
def wikiPrint(sample):
    
    sampleName = sample['cmgComp'].name
    dasString = "https://cmsweb.cern.ch/das/request?view=list&limit=50&instance=prod%2Fglobal&input=dataset%3D%2F"
    dbsString = sample['dbsName'][1:]
    datasetShort = sample['dbsName'].replace("RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0", "*")
    
    print "|-"
    print "|| {0} || {1} || - || [{2}{3} {4}]".format(sampleName, sample['xsec'], dasString, dbsString, datasetShort)
    print "|| Done || Done || DIRECTORY ||  ||"




if __name__ == "__main__":
   import sys
   if "printWiki" in sys.argv:
       for comp in allComponents:
           wikiPrint(comp)

