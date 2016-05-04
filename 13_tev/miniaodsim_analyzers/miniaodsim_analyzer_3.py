#print out the lhe and the gen weights

import ROOT
import sys
from DataFormats.FWLite import Events, Handle

events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISpring15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/00759690-D16E-E511-B29E-00261894382D.root'])

geninfo,geninfoLabel = Handle("GenEventInfoProduct"), "generator"
lheinfo,lheinfoLabel = Handle("LHEEventProduct"), "externalLHEProducer"

# loop over events
count= 0

for event in events:

    print "run %6d, lumi %4d, event %12d" % (event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())

    event.getByLabel(geninfoLabel,geninfo)
    event.getByLabel(lheinfoLabel,lheinfo)

    print geninfo.product().weight()
    print lheinfo.product().originalXWGTUP()



