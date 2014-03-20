#include "FWCore/Framework/interface/MakerMacros.h"
#include "Workspace/HEPHYCommonTools/plugins/CaloTowersTupelizer.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/CaloTowers/interface/CaloTowerCollection.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloEventSetup/interface/CaloTopologyRecord.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "Geometry/Records/interface/IdealGeometryRecord.h"


using namespace std;

namespace {
  string prefix ("[CaloTowersTupelizer] ");
}

CaloTowersTupelizer::~CaloTowersTupelizer() {}

CaloTowersTupelizer::CaloTowersTupelizer( const edm::ParameterSet & pset):
  Tupelizer(pset),
  params_ ( pset ),
  verbose_ ( pset.getUntrackedParameter< bool >("verbose") ),
  hfCaloTowers_ ( pset.getUntrackedParameter< edm::InputTag >("hfCaloTowers") )

{
  addAllVars();
}


void CaloTowersTupelizer::beginJob ( )
{
  cout << "[CaloTowersTupelizer] starting ... " << endl;
}

void CaloTowersTupelizer::endJob()
{
  cout << endl;
  cout << "[CaloTowersTupelizer] shutting down ... " << endl;
}

void CaloTowersTupelizer::beginRun ( edm::Run & iRun, edm::EventSetup const & iSetup )
{
}


void CaloTowersTupelizer::produce( edm::Event & ev, const edm::EventSetup & setup) {
  ev_ = &ev;
  int peng(0);

  edm::ESHandle<CaloGeometry> geometry;
  setup.get<CaloGeometryRecord>().get(geometry);
  // theGeometry = pG.product();

  //  ESHandle<CaloTPGTranscoder> decoder;
  //  iSetup.get<CaloTPGRecord>().get(decoder);
  //  decoder->setup(iSetup, CaloTPGTranscoder::HcalTPG);

  const CaloGeometry* geo = geometry.product();
  const CaloSubdetectorGeometry* gHB =
    geo->getSubdetectorGeometry(DetId::Hcal,HcalBarrel);
  const CaloSubdetectorGeometry* gHE =
    geo->getSubdetectorGeometry(DetId::Hcal,HcalEndcap);
  const CaloSubdetectorGeometry* gHF =
    geo->getSubdetectorGeometry(DetId::Hcal,HcalForward);

  edm::Handle<HFRecHitCollection> hfrecht;
  ev.getByLabel(hfCaloTowers_,hfrecht);
  std::vector<float> v_energy, v_eta, v_phi;
  std::vector<int> v_ieta, v_iphi, v_idepth;
  if (hfrecht.isValid()) {
    for (HFRecHitCollection::const_iterator ij=(*hfrecht).begin(); ij!=(*hfrecht).end(); ij++){
      double energy = (*ij).energy();
      if (energy <1.0) continue;
      HcalDetId id =(*ij).id();
      int ietaho = id.ieta();
      int iphiho = id.iphi();
      int idepth = id.depth();
      GlobalPoint pos = gHF->getGeometry(id)->getPosition();
      double eta = pos.eta();
      double phi = pos.phi();
      if (verbose_) cout<<"eta "<<eta<<" ietaho "<<ietaho<<" phi "<<phi<<" iphiho "<<iphiho<<" idepth "<<idepth<<" energy "<<energy<<endl;
      v_energy.push_back(energy);
      v_eta.push_back(eta);
      v_phi.push_back(phi);
      v_ieta.push_back(ietaho);
      v_iphi.push_back(iphiho);
      v_idepth.push_back(idepth);
    }
  }
  put("ctEta", v_eta); // NAN);
  put("ctPhi", v_phi); // NAN);
  put("ctIEta", v_ieta); // NAN);
  put("ctIPhi", v_iphi); // NAN);
  put("ctIDepth", v_idepth); // NAN);
  put("ctEnergy", v_energy); // NAN);
}

void CaloTowersTupelizer::addAllVars( )
{
  addVar("ctEta/F[]"); // NAN);
  addVar("ctPhi/F[]"); // NAN);
  addVar("ctIEta/I[]"); // NAN);
  addVar("ctIPhi/I[]"); // NAN);
  addVar("ctIDepth/I[]"); // NAN);
  addVar("ctEnergy/F[]"); // NAN);
}

DEFINE_FWK_MODULE(CaloTowersTupelizer);
