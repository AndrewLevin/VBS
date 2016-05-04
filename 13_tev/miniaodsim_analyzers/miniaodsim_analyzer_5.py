#classify wzjj events which pass the selection

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
import json

events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/BC441FED-7662-E511-A233-C8600032C755.root'])

events = Events (['root://cms-xrd-global.cern.ch//store/data/Run2015D/DoubleMuon/MINIAOD/PromptReco-v4/000/258/159/00000/0C6D4AB0-6F6C-E511-8A64-02163E0133CD.root'])

jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"    

#handlejets  = Handle ("std::vector<reco::GenParticle>")

# loop over events
count= 0

for event in events:
    event.getByLabel(jetLabel,jets)

    maxbtagevent = 0
    for jet in jets.product():
        if jet.pt() > 20:
            if maxbtagevent < jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"):
                maxbtagevent = jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")

    print maxbtagevent
