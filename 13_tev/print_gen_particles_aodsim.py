import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from math import *

from math import hypot, pi
def deltaR(a,b):
    dphi = abs(a.phi()-b.phi());
    if dphi > pi: dphi = 2*pi-dphi
    return hypot(a.eta()-b.eta(),dphi)

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/Phys14DR/QCD_HT-100To250_13TeV-madgraph/AODSIM/PU20bx25_PHYS14_25_V1-v1/00000/7ADC540A-BA86-E411-9B8F-002590747DEC.root'])

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/Phys14DR/QCD_HT-100To250_13TeV-madgraph/AODSIM/PU20bx25_PHYS14_25_V1-v1/00000/F61CFA31-B886-E411-935B-0025907B50D2.root'])

#events = Events( ['root://cms-xrd-global.cern.ch//store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/AODSIM/PU20bx25_PHYS14_25_V1-v1/00000/D0E76C6C-EB74-E411-97B7-0025907FD2DA.root'])

events = Events (['root://cms-xrd-global.cern.ch//store/mc/Phys14DR/QCD_Pt-30to50_Tune4C_13TeV_pythia8/AODSIM/PU20bx25_trkalmb_castor_PHYS14_25_V1-v1/00000/A4018A72-C273-E411-82BF-002590200AE4.root'])

#events = Events ( ['file:eos/cms/store/user/anlevin/data/AOD/wpwp_13_tev_qed_4_qcd_0/step4_output_801.root']  )

#events = Events( ['root://cms-xrd-global.cern.ch//store/user/anlevin/data/MINIAOD/sherpa_SM_v2/step5_output_9701.root'])

#events = Events( ['file:/afs/cern.ch/work/a/anlevin/tmp/sherpa_MYTEST_SM_MASTER_cff_py_GEN.root'] )

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/AODSIM/PU20bx25_PHYS14_25_V1-v1/00000/000470E0-3B75-E411-8B90-00266CFFA604.root'])

muons, muonLabel = Handle("std::vector<reco::Muon>"), "muons"
genparticles, genParticlesLabel = Handle("vector<reco::GenParticle>"), "genParticles"
#handlePruned  = Handle ("std::vector<reco::GenParticle>")
#handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")
#labelPruned = ("prunedGenParticles")
#labelPacked = ("packedGenParticles")

# loop over events
count= 0
for event in events:

    #if event.eventAuxiliary().luminosityBlock() != 48598:
    #    continue

    if event.eventAuxiliary().event() != 1195952 :
        continue

    #print "run %6d, lumi %4d, event %12d" % (event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    
    event.getByLabel(genParticlesLabel, genparticles)

    #for genparticle in genparticles.product():
    #    if abs(genparticle.pdgId()) == 15:
    #        for i in range(0,genparticle.numberOfDaughters()):
    #            print str(genparticle.pdgId())+" "+str(genparticle.status())+" "+str(genparticle.daughter(i).pdgId())

    for genparticle in genparticles.product():
        if abs(genparticle.pdgId()) == 13:
            print "found muon"
        if genparticle.mother(0) and genparticle.mother(1):
            print str(genparticle.pdgId())+" "+str(genparticle.status())+" "+str(genparticle.pt())+" "+str(genparticle.mother(0).pdgId())+" "+str(genparticle.mother(0).pt())+" "+str(genparticle.mother(1).pdgId())+" "+str(genparticle.mother(1).pt())+" "+str(genparticle.numberOfMothers())
        elif genparticle.mother(0):
            print str(genparticle.pdgId())+" "+str(genparticle.status())+" "+str(genparticle.pt())+" "+str(genparticle.mother(0).pdgId())+" "+str(genparticle.mother(0).pt())+" "+str(genparticle.numberOfMothers())
        else:
            print str(genparticle.pdgId())+" "+str(genparticle.status())+" "+str(genparticle.pt())+" "+str(genparticle.numberOfMothers())

    break     
