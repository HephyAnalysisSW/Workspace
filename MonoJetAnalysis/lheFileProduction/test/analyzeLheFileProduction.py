# ad-hoc script 
#
# compute the number of files per stop mass and deltaMassStopLsp
# identify undecayed files not processed


undecayedLheFiles = 'T2tt_stopMass_0_500_undecayedFiles.txt'
decayedLheFiles = 'LheFiles.txt'

model = '8TeV_T2tt_2j_'
stopMassList = [100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500]
deltaMassStopLsp = [10, 20, 30, 40, 50, 60, 70, 80]

nrFilesPerStopMass = dict()
totalNumberDecayedLheFiles = 0

print '\nNumber of files for stop mass bins\n'

for stopMass in stopMassList:

    print '    stop mass = ', stopMass, ' GeV'
    findStopMass = model + str(stopMass)
    nrFiles = 0
    
    nrFilesPerdM = dict()

    for dM in deltaMassStopLsp:
        nrFilesdM = 0
        lspMass = stopMass - dM
        findDeltaMassStopLsp = str(stopMass) + '_' + str(lspMass) + '.lhe'
        
        lheFile = open(decayedLheFiles, 'r')

        for fileLine in lheFile:
            if findStopMass in fileLine:
                if findDeltaMassStopLsp in fileLine:
                    nrFilesdM += 1

        lheFile.close()

        nrFilesPerdM[dM] = nrFilesdM
        nrFiles += nrFilesdM
        
        print '        stop mass = ', stopMass, ' GeV    LSP mass = ',  lspMass, ' ( dM = ', dM, '): ', \
            nrFilesPerdM[dM], ' decayed files'
    
    nrFilesPerStopMass[stopMass] = nrFiles
    totalNumberDecayedLheFiles += nrFiles

    print '      Total: ', nrFilesPerStopMass[stopMass], ' decayed files, correspond to ', \
        float(nrFilesPerStopMass[stopMass])/float(len(deltaMassStopLsp)), " undecayed files" \
        '\n'
                
print '\nTotal number of decayed files: ', totalNumberDecayedLheFiles
    

# identify undecayed files not processed

undecLhe = open(undecayedLheFiles, 'r')

print '\nMissing decayed files:'
numberMissingFiles = 0

for undecayedFile in undecLhe:
    lheF = undecayedFile[0:undecayedFile.find("unwgt")]
    for stopMass in stopMassList:
        findStopMass = model + str(stopMass)
        if findStopMass in lheF:
            for dM in deltaMassStopLsp:
                lspMass = stopMass - dM
                
                mergedFile = lheF + 'merged_' + str(stopMass) + '_' + str(lspMass)
                fileDecayed = False
                
                lheFile = open(decayedLheFiles, 'r')

                for fileLine in lheFile:
                    if mergedFile in fileLine:
                        fileDecayed = True
                                                
                lheFile.close()
                
                if fileDecayed != True:                                            
                    print '\nstop mass = ', stopMass, ' GeV    LSP mass = ',  lspMass, ' ( dM = ', dM, '): ' 
                    print '    Missing file:', mergedFile
                    numberMissingFiles += 1
                    
print '\n\nNumber of missing files: ', numberMissingFiles


                
