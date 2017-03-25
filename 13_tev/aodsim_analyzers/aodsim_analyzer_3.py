import ROOT
import sys
from DataFormats.FWLite import Events, Handle

events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISpring15DR74/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/Asympt25ns_MCRUN2_74_V9-v3/10000/6E643F29-A213-E511-ACC5-0002C90F8088.root'])

electrons, electronsLabel = Handle("vector<reco::GsfElectron>"),"gedGsfElectrons"
#genparticles, genParticlesLabel = Handle("vector<reco::GenParticle>"), "genParticles"

rho, rhoLabel = Handle("double"),"fixedGridRhoFastjetAll"

# loop over events
count= 0
for event in events:

    if count == 10:
        break

    count=count+1

    #if event.eventAuxiliary().luminosityBlock() != 2918:
    #    continue

    #if event.eventAuxiliary().event() != 734862:
    #    continue

    print "rho\n"

    event.getByLabel(rhoLabel,rho)
    print rho.product()[0]

    event.getByLabel(electronsLabel, electrons)

    for el in electrons.product():
        print "el.pt() = " +str(el.pt())
        print el.pfIsolationVariables().sumPhotonEt
        print el.pfIsolationVariables().sumNeutralHadronEt
        print el.pfIsolationVariables().sumChargedHadronPt
        print el.superCluster().eta()
        print (el.pfIsolationVariables().sumChargedHadronPt + max(0.0 , el.pfIsolationVariables().sumNeutralHadronEt + el.pfIsolationVariables().sumPhotonEt - 0.1862 *rho.product()[0]))/el.pt()
        
