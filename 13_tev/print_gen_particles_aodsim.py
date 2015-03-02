import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from math import *

from math import hypot, pi
def deltaR(a,b):
    dphi = abs(a.phi()-b.phi());
    if dphi > pi: dphi = 2*pi-dphi
    return hypot(a.eta()-b.eta(),dphi)

events = Events (['root://cms-xrd-global.cern.ch//store/mc/Phys14DR/QCD_HT-100To250_13TeV-madgraph/AODSIM/PU20bx25_PHYS14_25_V1-v1/00000/7ADC540A-BA86-E411-9B8F-002590747DEC.root'])

muons, muonLabel = Handle("std::vector<reco::Muon>"), "muons"
genparticles, genParticlesLabel = Handle("vector<reco::GenParticle>"), "genParticles"
#handlePruned  = Handle ("std::vector<reco::GenParticle>")
#handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")
#labelPruned = ("prunedGenParticles")
#labelPacked = ("packedGenParticles")

# loop over events
count= 0
for event in events:

    if event.eventAuxiliary().luminosityBlock() != 48598:
        continue

    if event.eventAuxiliary().event() != 4814521:
        continue

    print "run %6d, lumi %4d, event %12d" % (event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    
    event.getByLabel(muonLabel, muons)
    event.getByLabel(genParticlesLabel, genparticles)

    mu=muons.product()[1]

    #print mu.isLooseMuon()
    print mu.isGlobalMuon()
    print mu.isTrackerMuon()
    print mu.isStandAloneMuon()
    print mu.pt()
    print mu.innerTrack().pt()
    print mu.outerTrack().pt()
    print mu.globalTrack().pt()
    print mu.globalTrack().normalizedChi2()

    #mu.
    
    #for i,mu in enumerate(muons.product()): 
    #	print "pt : "+str(mu.pt())+ " eta : " +str(mu.eta()) + " phi : " + str(mu.phi())

    for genparticle in genparticles.product():
        if genparticle.pt() < 5:
            continue

        if deltaR(genparticle,mu) < 1.0:
	    print str(deltaR(genparticle,mu))+" "+str(genparticle.pt())+" "+str(genparticle.pdgId())
