/**
 * \class ParserLheModelString
 *
 *
 * Description: class to retrieve the quantities from the LHE model string.
 *
 * Implementation:
 *     TODO: enter details
 *
 * Usage: see LheAnalysis
 *
 * \author: Vasile Mihai Ghete - HEPHY Vienna
 *
 *
 */

#ifndef Workspace_MonoJetModules_ParserLheModelString_h
#define Workspace_MonoJetModules_ParserLheModelString_h

// system include files
#include <string>
#include <vector>
#include <utility>
#include <type_traits>

#include <fstream>
#include <sstream>
#include <iostream>
#include "boost/lexical_cast.hpp"

// user include files
//   base classes

//   other user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Utilities/interface/Exception.h"

// forward declarations

/// class declaration
class ParserLheModelString {

public:

    /// constructor(s)
    explicit ParserLheModelString();
    explicit ParserLheModelString(const std::string&, const edm::InputTag&);

    /// destructor
    virtual ~ParserLheModelString();

public:

    /// public methods

    const bool isValid() const;

    const int getQuantityIndex(const std::string&) const;

    template<class QuantityType>
    const QuantityType getQuantityValue(const int quantityIndex);

    /// extract the LHE model string from Event and parse it
    const bool parseLheModelString(const edm::Event&);

    /// parse the LHE model string
    const bool parseLheModelString(const std::string &);

private:

    /**
     * Pattern types in the LHE model string (with examples)
     *
     * delimiter            "_"
     * fixed string         "merged"
     * variable string      "T2tt"
     * integer              "175"
     * real                 "125.6"
     */

    enum PatternType {
        DELIMITER, FIXED_STRING, STRING, INT, REAL
    };

private:

    /// private methods

    /// describe a pattern in the LHE model string and add it to the corresponding vectors
    void addPattern(const std::string&, const PatternType&);

    /// define the LHE sample, describe the LHE model string
    void initialize();

    /// get the LHE model string from LHEEventProduct
    void getLheModelString(const edm::Event&);

    /// convert a string to a integer-type number
    /// the third parameter of stringToNumber should be
    /// one of std::hex, std::dec or std::oct
    template<class T>
    bool stringToNumber(T& tmpl, const std::string& str,
            std::ios_base& (*f)(std::ios_base&));
private:

    /// private members

    /// LHE sample - must be defined in initialize
    std::string m_lheSample;

    /// true if the LHE sample is implemented in initialize()
    bool m_isValid;

    /// delimiter used in the LHE model string;
    /// it is actually set when defining the sample in initialize()
    std::string m_delimiter;

    /// pattern index, it will be assigned in initialize()
    int m_patternIndex;

    //

    /// input tag for LHEEventProduct
    edm::InputTag m_inputTagLHEEventProduct;



    std::vector<std::pair<std::string, int> > m_lheModelPatterns;
    std::vector<std::pair<std::string, int> > m_patternIndices;
    std::vector<std::pair<int, int> > m_patternIndicesTypes;

    std::vector<size_t> m_patternStartPosition;
    std::vector<size_t> m_patternEndPosition;

    /// per-event LHE model string
    std::string m_lheModelString;

};

template<class QuantityType>
const QuantityType ParserLheModelString::getQuantityValue(
        const int quantityIndex) {

    // QuantityType quantity { }; C++11
    QuantityType quantity = QuantityType();

    std::string quantityString;

    for (std::vector<std::pair<int, int> >::const_iterator cIter =
            m_patternIndicesTypes.begin(); cIter != m_patternIndicesTypes.end();
            ++cIter) {

        int qIndex = (*cIter).first;

        if (quantityIndex == qIndex) {

            quantityString = m_lheModelString.substr(
                    m_patternStartPosition[qIndex],
                    m_patternEndPosition[qIndex]
                            - m_patternStartPosition[qIndex] + 1);

            if (std::is_same<QuantityType, std::string>::value) {

                continue;

            } else if (std::is_same<QuantityType, int>::value) {

                quantity = boost::lexical_cast<int>(quantityString);

            } else if (std::is_same<QuantityType, float>::value) {

                quantity = boost::lexical_cast<float>(quantityString);

            } else if (std::is_same<QuantityType, double>::value) {

                quantity = boost::lexical_cast<double>(quantityString);

            } else {

                throw cms::Exception("ParserLheModelString")
                        << "   ParserLheModelString::getQuantityValue "
                        << "\n   Templated type not implemented. \n"
                        << std::endl;

            }

            break;
        }

    }

    return quantity;
}


#endif /* Workspace_MonoJetModules_ParserLheModelString_h */

