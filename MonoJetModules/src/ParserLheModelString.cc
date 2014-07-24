/**
 * \class ParserLheModelString
 *
 *
 * Description: see header file.
 *
 *
 * \author: Vasile Mihai Ghete - HEPHY Vienna
 *
 *
 */

// this class header
#include "Workspace/MonoJetModules/interface/ParserLheModelString.h"

// system include files
#include <iostream>
#include <vector>

// user include files
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Utilities/interface/Exception.h"

#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

// constructor(s)

ParserLheModelString::ParserLheModelString() :
        m_lheSample(""),
        m_isValid(false),
        m_delimiter(""),
        m_patternIndex(-1) {

    // empty
}


ParserLheModelString::ParserLheModelString(const std::string& lheSample, const edm::InputTag& inputTagLHEEventProduct) :
        m_lheSample(lheSample),
        m_isValid(false),
        m_delimiter(""),
        m_patternIndex(-1),
        m_inputTagLHEEventProduct(inputTagLHEEventProduct) {

    initialize();

}


// destructor
ParserLheModelString::~ParserLheModelString() {

    // empty now

}

// public methods

const bool ParserLheModelString::isValid() const {

    return m_isValid;
}

const int ParserLheModelString::getQuantityIndex(
        const std::string& quantity) const {

    int quantityIndex = -1;

    for (std::vector<std::pair<std::string, int> >::const_iterator cIter =
            m_patternIndices.begin(); cIter != m_patternIndices.end();
            ++cIter) {

        if ((*cIter).first == quantity) {
            quantityIndex = (*cIter).second;

            break;
        }
    }

    if (quantityIndex <= 0) {
        edm::LogWarning("ParserLheModelString")
                << "\nParserLheModelString::getQuantityIndex: quantity '"
                << quantity << "' not defined for sample '" << m_lheSample
                << "'\n" << std::endl;
    }

    return quantityIndex;
}

const bool ParserLheModelString::parseLheModelString(const edm::Event& iEvent) {

    getLheModelString(iEvent);

    bool parseStatus = parseLheModelString(m_lheModelString);

    return parseStatus;
}

const bool ParserLheModelString::parseLheModelString(
        const std::string& lheModelString) {

    bool parseStringStatus = true;

    size_t lheModelStringSize = lheModelString.size();

    const size_t numberPatterns = m_lheModelPatterns.size();
    const size_t delimiterSize = m_delimiter.size();

    std::vector < size_t > delimiterStartPosition;
    delimiterStartPosition.reserve(numberPatterns);

    std::string::size_type startPositionDelimiter = 0;
    while ((startPositionDelimiter = lheModelString.find(m_delimiter,
            startPositionDelimiter)) != lheModelString.npos) {

        delimiterStartPosition.push_back(startPositionDelimiter);

        ++startPositionDelimiter;

    }

    size_t patternStartPosition = 0;
    size_t patternEndPosition = 0;
    size_t delimiterCounter = 0;

    for (std::vector<std::pair<int, int> >::const_iterator cIter =
            m_patternIndicesTypes.begin(); cIter != m_patternIndicesTypes.end();
            ++cIter) {

        switch ((*cIter).second) {
            case DELIMITER: {
                patternStartPosition = delimiterStartPosition[delimiterCounter];
                patternEndPosition = patternStartPosition + delimiterSize - 1;

                m_patternStartPosition[(*cIter).first] = patternStartPosition;
                m_patternEndPosition[(*cIter).first] = patternEndPosition;

                patternStartPosition = patternEndPosition + 1;
                delimiterCounter++;

            }

                break;

            case FIXED_STRING: {
                patternEndPosition = patternStartPosition
                        + ((m_patternIndices[(*cIter).first]).first).size() - 1;

                m_patternStartPosition[(*cIter).first] = patternStartPosition;
                m_patternEndPosition[(*cIter).first] = patternEndPosition;

                patternStartPosition = patternEndPosition + 1;

            }

                break;

            case STRING:
            case INT:
            case REAL: {

                size_t distanceToDelimiter = 0;

                // look for the distance to the delimiter or end of string
                for (size_t iPattern = ((*cIter).first) + 1;
                        iPattern < numberPatterns; ++iPattern) {

                    if ((m_patternIndicesTypes[iPattern]).second == DELIMITER) {

                        patternEndPosition =
                                delimiterStartPosition[delimiterCounter]
                                        - distanceToDelimiter - 1;

                        break;

                    } else if ((m_patternIndicesTypes[iPattern]).second
                            == FIXED_STRING) {

                        distanceToDelimiter +=
                                ((m_patternIndices[iPattern]).first).size();

                    } else if (iPattern == (numberPatterns - 1)) {

                        // end of string, no delimiter

                        patternEndPosition = lheModelStringSize
                                - distanceToDelimiter - 1;

                    } else {
                        throw cms::Exception("ParserLheModelString")
                                << "   ParserLheModelString::parseLheModelString "
                                << "\n  Can not resolve a substring with two variable-length patterns.\n"
                                << std::endl;
                    }

                }

                // last pattern special treatment: end of string, no delimiter
                if (int((*cIter).first) == int(numberPatterns - 1)) {

                    patternEndPosition = lheModelStringSize - 1;

                }

                m_patternStartPosition[(*cIter).first] = patternStartPosition;
                m_patternEndPosition[(*cIter).first] = patternEndPosition;

                patternStartPosition = patternEndPosition + 1;

            }

                break;

            default: {
                // should not arrive here
                parseStringStatus = false;
                break;
            }
                break;
        }

        LogTrace("ParserLheModelString")
                << "ParserLheModelString::parseLheModelString: \n pattern index "
                << ((*cIter).first) << " starting at position "
                << (m_patternStartPosition[(*cIter).first]) << " ending at "
                << m_patternEndPosition[(*cIter).first] << " has the value '"
                << lheModelString.substr(m_patternStartPosition[(*cIter).first],
                        m_patternEndPosition[(*cIter).first]
                                - m_patternStartPosition[(*cIter).first] + 1)
                << "'" << std::endl;

        // sanity checks
        if (m_patternStartPosition[(*cIter).first] >= lheModelStringSize) {
            parseStringStatus = false;
        }

        if (m_patternEndPosition[(*cIter).first] >= lheModelStringSize) {
            parseStringStatus = false;
        }

        if (m_patternEndPosition[(*cIter).first]
                >= m_patternStartPosition[(*cIter).first]) {
            parseStringStatus = false;
        }

    }

    return parseStringStatus;

}

// private methods

void ParserLheModelString::addPattern(const std::string& pattern,
        const ParserLheModelString::PatternType& patternType) {

    m_patternIndex++;

    m_lheModelPatterns.push_back(std::make_pair(pattern, patternType));
    m_patternIndices.push_back(std::make_pair(pattern, m_patternIndex));
    m_patternIndicesTypes.push_back(
            std::make_pair(m_patternIndex, patternType));

}

void ParserLheModelString::initialize() {

    if (m_lheSample == "T2DegenerateStop") {

        m_isValid = true;

        // 8TeV_T2tt_2j_175_25_run16892_merged_175_115

        m_delimiter = "_";
        const unsigned int lheModelSubstrings = 9;

        m_lheModelPatterns.reserve(lheModelSubstrings);
        m_patternIndices.reserve(lheModelSubstrings);

        addPattern("Energy", INT);
        addPattern("TeV", FIXED_STRING);
        addPattern(m_delimiter, DELIMITER);

        addPattern("MadModel", STRING);
        addPattern(m_delimiter, DELIMITER);

        addPattern("MadNrJets", STRING);
        addPattern(m_delimiter, DELIMITER);

        addPattern("GenStopMass", INT);
        addPattern(m_delimiter, DELIMITER);

        addPattern("GenLspMass", INT);
        addPattern(m_delimiter, DELIMITER);

        addPattern("run", FIXED_STRING);
        addPattern("RunNumber", INT);
        addPattern(m_delimiter, DELIMITER);

        addPattern("merged", FIXED_STRING);
        addPattern(m_delimiter, DELIMITER);

        addPattern("DecayStopMass", INT);
        addPattern(m_delimiter, DELIMITER);

        addPattern("DecayLspMass", INT);

        m_patternStartPosition.resize(m_lheModelPatterns.size());
        m_patternEndPosition.resize(m_lheModelPatterns.size());

        return;

    }

    m_isValid = false;
}

void ParserLheModelString::getLheModelString(const edm::Event& iEvent) {

    // reset model string
    m_lheModelString.clear();

    edm::Handle < LHEEventProduct > lheEventProduct;
    iEvent.getByLabel(m_inputTagLHEEventProduct, lheEventProduct);

    if (!(lheEventProduct.isValid())) {
        edm::LogWarning("ParserLheModelString")
                << "ParserLheModelString::getLheModelString: product LHEEventProduct with input tag "
                << m_inputTagLHEEventProduct << " does not exist." << std::endl;
    }

    LHEEventProduct::comments_const_iterator commentsBegin =
            lheEventProduct->comments_begin();
    LHEEventProduct::comments_const_iterator commentsEnd =
            lheEventProduct->comments_end();

    const std::string model = "model ";
    size_t modelSize = model.size();

    for (LHEEventProduct::comments_const_iterator cIter = commentsBegin;
            cIter != commentsEnd; ++cIter) {

        size_t foundModel = cIter->find(model);
        if (foundModel == std::string::npos) {
            continue;
        }

        LogTrace("ParserLheModelString")
                << "ParserLheModelString::getLheModelString: \n    LHE model line = '"
                << (*cIter) << "'\n" << std::endl;

        size_t lheModelBegin = foundModel + modelSize;
        size_t blankAfterLheModel = (cIter->find(' ', lheModelBegin + 1));
        size_t lheModelLength = 0;

        if (blankAfterLheModel == std::string::npos) {
            lheModelLength = cIter->size() - lheModelBegin - 1;
        } else {
            lheModelLength = blankAfterLheModel - lheModelBegin - 1;
        }

        m_lheModelString = cIter->substr(lheModelBegin, lheModelLength);

        // break if a model line was found
        break;

    }

    LogTrace("ParserLheModelString")
            << "ParserLheModelString::getLheModelString: \n    LHE model string = '"
            << m_lheModelString << "'\n" << std::endl;

}

