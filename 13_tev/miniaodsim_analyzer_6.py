#prints out some information about all of the electrons and muons in an event

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
import json

#events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/BC441FED-7662-E511-A233-C8600032C755.root'])

events = Events (['root://cms-xrd-global.cern.ch//store/data/Run2015D/DoubleEG/MINIAOD/PromptReco-v4/000/258/705/00000/BCD2A2D6-6271-E511-A78E-02163E013544.root'])

muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"    
electrons, electronLabel = Handle("std::vector<pat::Electron>"), "slimmedElectrons"                                                                                                                                                                                            


#handlejets  = Handle ("std::vector<reco::GenParticle>")

# loop over events
count= 0

for event in events:

    if event.eventAuxiliary().run() != 258705 :
        continue

    if event.eventAuxiliary().luminosityBlock() != 98:
        continue

    if event.eventAuxiliary().event() != 177244452:
        continue

    print "muons:\n"

    event.getByLabel(muonLabel,muons)

    for muon in muons.product():
        print muon.pt()
        print muon.pfIsolationR04().sumChargedHadronPt
        print muon.pfIsolationR04().sumNeutralHadronEt
        print muon.pfIsolationR04().sumPhotonEt
        print muon.pfIsolationR04().sumPUPt
        print ( muon.pfIsolationR04().sumChargedHadronPt+ max(0.0,muon.pfIsolationR04().sumNeutralHadronEt + muon.pfIsolationR04().sumPhotonEt - \
0.5 * muon.pfIsolationR04().sumPUPt) )/muon.pt()

    print "electrons:\n"

    event.getByLabel(electronLabel,electrons)

    for i,el in enumerate(electrons.product()):
        print el.pt()
        print el.pfIsolationVariables().sumChargedHadronPt 
        print el.pfIsolationVariables().sumNeutralHadronEt 
        print el.pfIsolationVariables().sumPhotonEt 
        print el.pfIsolationVariables().sumPUPt 
        print (el.pfIsolationVariables().sumChargedHadronPt + max(0.0 , el.pfIsolationVariables().sumNeutralHadronEt + el.pfIsolationVariables().sumPhotonEt - 0.5 * el.pfIsolationVariables().sumPUPt))/el.pt()
        print el.userFloat("ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values")
