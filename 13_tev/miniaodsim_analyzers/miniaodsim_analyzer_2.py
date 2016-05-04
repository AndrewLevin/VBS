#print out gen particles and lhe particles and electrons

import ROOT
import sys
from DataFormats.FWLite import Events, Handle

events = Events (['root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/ACE7C21B-6E6F-E511-8C2F-001E67504D2D.root'])

lheinfo,lheinfoLabel = Handle("LHEEventProduct"), "externalLHEProducer"

muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"
electrons, electronLabel = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
handlePruned  = Handle ("std::vector<reco::GenParticle>")
handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")

labelPruned = ("prunedGenParticles")
labelPacked = ("packedGenParticles")

# loop over events
count= 0

for event in events:

    if event.eventAuxiliary().luminosityBlock() != 209529:
        continue

    if event.eventAuxiliary().event() != 52570562:
        continue

    print "run %6d, lumi %4d, event %12d" % (event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    
    event.getByLabel(electronLabel, electrons)
    event.getByLabel(muonLabel, muons)

    event.getByLabel(lheinfoLabel,lheinfo)

    print "electrons\n"

    # Electrons
    for i,el in enumerate(electrons.product()):
        if el.pt() < 5: continue
        print "elec %2d: pt %4.1f, phi %+5.3f, supercluster eta %+5.3f, sigmaIetaIeta %.3f (%.3f with full5x5 shower shapes), lost hits %d, pass conv veto %d" % (i, el.pt(), el.phi(), el.superCluster().eta(), el.sigmaIetaIeta(), el.full5x5_sigmaIetaIeta(),el.gsfTrack().hitPattern().numberOfLostHits(ROOT.reco.HitPattern.MISSING_INNER_HITS), el.passConversionVeto())

    print "muons\n"

    for muon in muons.product():
        print muon.pt()
        print muon.eta()
        print muon.phi()


    print "lhe\n"

    for i in range(0,len(lheinfo.product().hepeup().IDUP)):
        print lheinfo.product().hepeup().IDUP.at(i)


    print "packed\n"	    

    event.getByLabel (labelPacked, handlePacked)

    packed = handlePacked.product()

    for p in packed :
	if p.mother(0) and p.mother(0).pdgId():
	    print "PdgId : %s   pt : %s  eta : %s   phi : %s  mother_pdg_id : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi(),p.mother(0).pdgId())    
        else:
	    print "PdgId : %s   pt : %s  eta : %s   phi : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi())    	    	

    event.getByLabel (labelPruned, handlePruned)

    pruned = handlePruned.product()

    print "pruned\n"
    
    for p in pruned :
	if p.mother() and p.mother().pdgId():
	    print "PdgId : %s   pt : %s  eta : %s   phi : %s  mother_pdg_id : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi(),p.mother().pdgId())    
        else:
	    print "PdgId : %s   pt : %s  eta : %s   phi : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi())    	    	
