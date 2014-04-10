#ifndef Workspace_MonoJetAnalysis_LheAnalysis_h
#define Workspace_MonoJetAnalysis_LheAnalysis_h

/**
 * \class LheAnalysis
 * 
 * 
 * Description: analyze LHE.
 *
 * Implementation:
 *    TODO: enter details 
 *   
 * \author: Vasile Mihai Ghete - HEPHY Vienna
 * 
 *
 */

// system include files
#include <memory>
#include <string>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "Workspace/MonoJetModules/interface/ParserLheModelString.h"

// forward declarations

// class declaration

class LheAnalysis: public edm::EDAnalyzer {

public:

    /// constructor(s)
    explicit LheAnalysis(const edm::ParameterSet&);

    /// destructor
    virtual ~LheAnalysis();

private:

    /// private methods

private:

    /// standard CMSSW edm::EDAnalyzer methods

    virtual void beginJob();
    virtual void beginRun(const edm::Run&, const edm::EventSetup&);
    virtual void beginLuminosityBlock(const edm::LuminosityBlock&,
            const edm::EventSetup&);

    virtual void analyze(const edm::Event&, const edm::EventSetup&);

    virtual void endLuminosityBlock(const edm::LuminosityBlock&,
            const edm::EventSetup&);
    virtual void endRun(const edm::Run&, const edm::EventSetup&);

    virtual void endJob();

private:

    /// private members - input

    /// LHE sample
    std::string m_lheSample;

    /// input tag for LHEEventProduct
    edm::InputTag m_inputTagLHEEventProduct;


private:

    ///
    ParserLheModelString m_lheModelString;

    /// indices - use them to avoid string comparison
    int m_decayLspMass;


};

#endif /*Workspace_MonoJetAnalysis_LheAnalysis_h*/
