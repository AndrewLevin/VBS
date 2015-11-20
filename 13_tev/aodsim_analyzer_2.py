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

events = Events (['root://cms-xrd-global.cern.ch//store/mc/Phys14DR/QCD_Pt-15to30_Tune4C_13TeV_pythia8/AODSIM/PU20bx25_trkalmb_castor_PHYS14_25_V1-v1/10000/4C152507-8174-E411-AEBC-001E67396581.root'])

#events = Events ( ['file:eos/cms/store/user/anlevin/data/AOD/wpwp_13_tev_qed_4_qcd_0/step4_output_801.root']  )

#events = Events( ['root://cms-xrd-global.cern.ch//store/user/anlevin/data/MINIAOD/sherpa_SM_v2/step5_output_9701.root'])

#events = Events( ['file:/afs/cern.ch/work/a/anlevin/tmp/sherpa_MYTEST_SM_MASTER_cff_py_GEN.root'] )

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/Phys14DR/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/AODSIM/PU20bx25_PHYS14_25_V1-v1/00000/000470E0-3B75-E411-8B90-00266CFFA604.root'])

lheeventproduct, lheeventproductLabel = Handle("LHEEventProduct"),"source"
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

    #if event.eventAuxiliary().event() != 2214912:
    #    continue

    if event.eventAuxiliary().event() != 2214912:
        continue

    event.getByLabel(muonLabel, muons)

    print "andrew debug -9"

    for muon in muons.product():
        if muon.pt() > 10:
            break

    print "andrew debug -8"

    #print "run %6d, lumi %4d, event %12d" % (event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())

    #event.getByLabel(lheeventproductLabel, lheeventproduct)    
    event.getByLabel(genParticlesLabel, genparticles)

    #for genparticle in genparticles.product():
    #    print str(deltaR(muon,genparticle))+"    "+str(genparticle.pdgId())+"    "+str(genparticle.status())+"    "+str(genparticle.pt())

    print "andrew debug -1"

    for genparticle in genparticles.product():

        if abs(genparticle.status()) == 23 or abs(genparticle.status()) == 22 or abs(genparticle.status()) == 21 or abs(genparticle.status()) == 24:
            print str(genparticle.pdgId())+" "+str(genparticle.status())+" "+str(genparticle.pt())

    print "andrew debug 0"

    sys.exit(0)

    for genparticle in genparticles.product():

        if abs(genparticle.pdgId()) == 13:

            if genparticle.pt() < 10:
                continue

            print "found muon"

            current = genparticle
            while current.numberOfMothers() > 0:
                string=str(current.pdgId())+"    "+str(current.status())
                for k in range(0,current.numberOfMothers()):
                    if current.mother(k).pdgId() == -5:
                        print "andrew debug 1"
                        print current.mother(k).numberOfMothers()
                        print current.mother(k).mother(0).pdgId()
                        print current.mother(k).mother(0).status()
                        print current.mother(k).mother(0).numberOfMothers()
                        print current.mother(k).mother(0).mother(0).pdgId()
                        print current.mother(k).mother(0).mother(0).status()
                        print current.mother(k).mother(0).mother(0).numberOfMothers()
                        print current.mother(k).mother(0).mother(0).mother(0).pdgId()
                        print current.mother(k).mother(0).mother(0).mother(0).status()
                        print current.mother(k).mother(0).mother(0).mother(0).numberOfMothers()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).pdgId()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).status()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).numberOfMothers()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).pdgId()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).status()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).numberOfMothers()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).pdgId()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).status()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).numberOfMothers()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).pdgId()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).status()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).numberOfMothers()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).pdgId()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).status()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).numberOfDaughters()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).daughter(0).pdgId()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).daughter(0).status()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).daughter(1).pdgId()
                        print current.mother(k).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).mother(0).daughter(1).status()
                        print "andrew debug 2"
                    string=string+"    "+str(current.mother(k).status())+"    "+str(current.mother(k).pdgId())
                print string    
                current = current.mother(0)

        #if genparticle.mother(0) and genparticle.mother(1):
        #    print str(genparticle.pdgId())+" "+str(genparticle.status())+" "+str(genparticle.pt())+" "+str(genparticle.mother(0).pdgId())+" "+str(genparticle.mother(0).pt())+" "+str(genparticle.mother(1).pdgId())+" "+str(genparticle.mother(1).pt())+" "+str(genparticle.numberOfMothers())
        #elif genparticle.mother(0):
        #    print str(genparticle.pdgId())+" "+str(genparticle.status())+" "+str(genparticle.pt())+" "+str(genparticle.mother(0).pdgId())+" "+str(genparticle.mother(0).pt())+" "+str(genparticle.numberOfMothers())
        #else:
        #    print str(genparticle.pdgId())+" "+str(genparticle.status())+" "+str(genparticle.pt())+" "+str(genparticle.numberOfMothers())
            

    break     
