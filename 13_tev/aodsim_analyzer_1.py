#for each electron, print out the pt and the pt of the gsf track

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from math import *

events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/Asympt25ns_MCRUN2_74_V9-v3/70001/6A07150B-2D14-E511-A784-001E6739811F.root'])

electrons, electronLabel = Handle("std::vector<reco::GsfElectron>"), "gedGsfElectrons"

# loop over events
count= 0
for event in events:

    if event.eventAuxiliary().luminosityBlock() != 143886:
        continue

    if event.eventAuxiliary().event() != 36104916:
        continue

    event.getByLabel(electronLabel, electrons)

    for electron in electrons.product():
        if electron.pt() > 10:
            print electron.pt()
            print electron.gsfTrack().pt()
