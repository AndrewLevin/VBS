import ROOT
import sys
from DataFormats.FWLite import Events, Handle

events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/AODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/8024A63E-A161-E511-9377-B083FECFC6ED.root'])

genparticles, genParticlesLabel = Handle("vector<reco::GenParticle>"), "genParticles"

# loop over events
count= 0
for event in events:

    if event.eventAuxiliary().luminosityBlock() != 2219:
        continue

    if event.eventAuxiliary().event() != 190767:
        continue

    event.getByLabel(genParticlesLabel, genparticles)

    for genparticle in genparticles.product():

        if genparticle.mother(0) and genparticle.mother(1):
            print str(genparticle.status())+" "+str(genparticle.pdgId())+" "+str(genparticle.status())+" "+str(genparticle.pt())+" "+" "+str(genparticle.eta())+str(genparticle.mother(0).pdgId())+" "+str(genparticle.mother(0).pt())+" "+str(genparticle.mother(1).pdgId())+" "+str(genparticle.mother(1).pt())+" "+str(genparticle.numberOfMothers())
        elif genparticle.mother(0):
            print str(genparticle.status())+" "+str(genparticle.pdgId())+" "+str(genparticle.status())+" "+str(genparticle.pt())+" "+str(genparticle.mother(0).pdgId())+" "+str(genparticle.mother(0).pt())+" "+str(genparticle.numberOfMothers())
        else:
            print str(genparticle.status())+" "+str(genparticle.pdgId())+" "+str(genparticle.status())+" "+str(genparticle.pt())+" "+str(genparticle.numberOfMothers())
