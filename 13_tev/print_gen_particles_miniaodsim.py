import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from math import *

def isAncestor(a,p) :
        if a == p : 
                return True
        for i in xrange(0,p.numberOfMothers()) :
                if isAncestor(a,p.mother(i)) :
                         return True
        return False



events = Events (['root://cms-xrd-global.cern.ch//store/mc/Phys14DR/QCD_HT-100To250_13TeV-madgraph/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/10C40CA1-7987-E411-8C57-E0CB4E19F98A.root'])


muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"
handlePruned  = Handle ("std::vector<reco::GenParticle>")
handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")
labelPruned = ("prunedGenParticles")
labelPacked = ("packedGenParticles")

# loop over events
count= 0
for event in events:

    if event.eventAuxiliary().luminosityBlock() != 48598:
        continue

    if event.eventAuxiliary().event() != 4814521:
        continue

    print "run %6d, lumi %4d, event %12d" % (event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    
    event.getByLabel(muonLabel, muons)
    
    for i,mu in enumerate(muons.product()): 
	if mu.pt() < 5 or not mu.isLooseMuon(): continue
	print "pt : "+str(mu.pt())+ " eta : " +str(mu.eta()) + " phi : " + str(mu.phi())

    event.getByLabel (labelPacked, handlePacked)
    event.getByLabel (labelPruned, handlePruned)
    # get the product
    packed = handlePacked.product()
    pruned = handlePruned.product()
    
    for p in pruned :
	print "PdgId : %s   pt : %s  eta : %s   phi : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi())    
