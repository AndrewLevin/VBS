#print out simvertex and simtrack information

import ROOT
import sys
from DataFormats.FWLite import Events, Handle

events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIIWinter15GS/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/GEN-SIM/MCRUN2_71_V1-v1/50003/F8DB58C0-E0DC-E411-9F74-001E67A3EBD8.root'])

# loop over events
count= 0
for event in events:

    if event.eventAuxiliary().luminosityBlock() != 143886:
        continue

    #if event.eventAuxiliary().event() != 2214912:
    #    continue

    if event.eventAuxiliary().event() != 36104916:
        continue

    simtracks = Handle("vector<SimTrack>")

    event.getByLabel("g4SimHits",simtracks)

    simvertices = Handle("vector<SimVertex>")

    event.getByLabel("g4SimHits",simvertices)

    #track 1 is a photon
    #vertex 252 is a conversion
    #tracks 586 and 587 have vertex 252 as their parent

    print simtracks.product()[1].vertIndex()

    print simtracks.product()[401].vertIndex()

    print simtracks.product()[1].trackId()
    print simtracks.product()[401].trackId()

    print simtracks.product()[1].momentum().pt()
    print simtracks.product()[1].momentum().eta()
    print simtracks.product()[1].momentum().phi()

    print simvertices.product()[156].processType()
    print simvertices.product()[156].parentIndex()

    print simvertices.product()[252].processType()
    print simvertices.product()[252].parentIndex()

    # positions are in cm: https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/SimG4Core/Application/src/G4SimEvent.cc
    print simvertices.product()[252].position().x()
    print simvertices.product()[252].position().y()
    print simvertices.product()[252].position().z()

    print simtracks.product()[586].momentum().pt()
    print simtracks.product()[586].momentum().eta()
    print simtracks.product()[586].momentum().phi()
    print simtracks.product()[587].momentum().pt()
    print simtracks.product()[587].momentum().eta()
    print simtracks.product()[587].momentum().phi()
    print simtracks.product()[586].type()
    print simtracks.product()[587].type()

    print "vertex 253:\n"

    print simvertices.product()[253].processType()
    print simvertices.product()[253].parentIndex()
    print simvertices.product()[253].position().x()
    print simvertices.product()[253].position().y()
    print simvertices.product()[253].position().z()

    print "vertex 254:\n"

    print simvertices.product()[254].processType()
    print simvertices.product()[254].parentIndex()
    print simvertices.product()[254].position().x()
    print simvertices.product()[254].position().y()
    print simvertices.product()[254].position().z()

    print "vertex 282:\n"

    print simvertices.product()[282].processType()
    print simvertices.product()[282].parentIndex()
    print simvertices.product()[282].position().x()
    print simvertices.product()[282].position().y()
    print simvertices.product()[282].position().z()

    print "tracks with parent vertex 254:\n"

    i = 0
    for simtrack in simtracks.product():

        if simtrack.vertIndex() == 254: 
            print i
            print simtrack.type()
            print simtrack.momentum().pt()

        i=i+1


#    j = 0
#    for simvertex in simvertices.product():
#
#        if simvertex.parentIndex() == simtracks.product()[586].trackId() or simvertex.parentIndex() == simtracks.product()[587].trackId():
#
#            print j
#            print simvertex.parentIndex()
#            print simvertex.processType()
#        j = j +1

