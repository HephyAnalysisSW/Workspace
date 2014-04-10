/**
 * \class LheAnalysis
 * 
 * 
 * Description: see header file.
 *
 * \author: Vasile Mihai Ghete - HEPHY Vienna
 * 
 *
 */

// this class header
#include "Workspace/MonoJetModules/interface/LheAnalysis.h"

// system include files
#include <memory>
#include <iostream>

// user include files
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/Exception.h"

// constructor(s)
LheAnalysis::LheAnalysis(const edm::ParameterSet& paramSet) :

        m_lheSample(paramSet.getParameter<std::string>("LheSample")),
        m_inputTagLHEEventProduct(paramSet.getParameter<edm::InputTag>("InputTagLHEEventProduct")),
        m_lheModelString(ParserLheModelString(m_lheSample, m_inputTagLHEEventProduct)) {

    //
    if (!(m_lheModelString.isValid())) {
        throw cms::Exception("FailModule")
                << "  LheAnalysis::LheAnalysis LHE Sample '" << m_lheSample
                << "' does not exist."
                << "\n  Check the input string; if correct, add sample to ParserLheModelString class.\n"
                << std::endl;
    }

    m_decayLspMass = m_lheModelString.getQuantityIndex("DecayLspMass");

}

// destructor
LheAnalysis::~LheAnalysis() {
    // empty
}

void LheAnalysis::beginJob() {
    // empty
}

void LheAnalysis::beginRun(const edm::Run& iRun,
        const edm::EventSetup& evSetup) {
    // empty
}

void LheAnalysis::beginLuminosityBlock(const edm::LuminosityBlock& iLumBlock,
        const edm::EventSetup& evSetup) {
    // empty
}

void LheAnalysis::analyze(const edm::Event& iEvent,
        const edm::EventSetup& evSetup) {

    const unsigned int runNumber = iEvent.run();
    const unsigned int lsNumber = iEvent.luminosityBlock();
    const unsigned int eventNumber = iEvent.id().event();

    LogTrace("LheAnalysis") << "LheAnalysis::analyze: " << "Run: " << runNumber
            << " LS: " << lsNumber << " Event: " << eventNumber << "\n\n"
            << std::endl;

    // parse the LHE model string (once per event)
    m_lheModelString.parseLheModelString(iEvent);

    float decayLspMass = 0.;
    if (m_decayLspMass >= 0) {
        decayLspMass = m_lheModelString.getQuantityValue<float>(m_decayLspMass);

        LogTrace("LheAnalysis") << "\ndecayLspMass index = " << m_decayLspMass
                << "\n" << "decayLspMass = " << decayLspMass << "\n"
                << std::endl;
    }

}

void LheAnalysis::endLuminosityBlock(const edm::LuminosityBlock& iLumBlock,
        const edm::EventSetup& evSetup) {
}

void LheAnalysis::endRun(const edm::Run& iRun, const edm::EventSetup& evSetup) {
}

void LheAnalysis::endJob() {
}

