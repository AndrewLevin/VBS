# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.AutoLibraryLoader.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

# open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)
events = Events([
"root://eoscms//eos/cms/store/user/anlevin/data/MINIAOD/qed_4_qcd_99_sm_14_tev/Merged.root"
#"file:/afs/cern.ch/work/a/anlevin/tmp/Merged.root"
])

muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"
mets, metLabel = Handle("std::vector<pat::MET>"), "slimmedMETs"
electrons, electronLabel = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"
vertices, vertexLabel = Handle("std::vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices"

n_events=0
n_selected_events=0

for ievent,event in enumerate(events):

    n_events=n_events+1
    if ievent % 1000 == 0:
        print "Event", ievent

    if ievent > 10000: break

    event.getByLabel(jetLabel,jets)
    event.getByLabel(electronLabel,electrons)
    event.getByLabel(metLabel,mets)
    event.getByLabel(vertexLabel, vertices)
    event.getByLabel(muonLabel, muons)

    if len(mets.product()) != 1:
        print "not exactly one met in the event, exiting"
        sys.exit(1)

    if mets.product()[0].pt() < 40:
        continue

    selected_electrons = []
    selected_muons = []
    selected_jets = []

    PV = vertices.product()[0]

    for i,electron in enumerate(electrons.product()):
        if electron.pt() < 20:
            continue
        selected_electrons.append(electron)

    for i,mu in enumerate(muons.product()):
        if mu.pt() < 20 or not mu.isTightMuon(PV) or abs(mu.eta()) > 2.4 or not mu.isGlobalMuon():
            continue
        selected_muons.append(mu)    

    for i,jet in enumerate(jets.product()):
        if jet.pt() < 30:
            continue
        
        #use the cuts here https://github.com/latinos/UserCode-CMG-CMGTools-External/blob/master/python/JetIdParams_cfi.py
        if abs(jet.eta()) < 2.5:
            if jet.userFloat("pileupJetId:fullDiscriminant") < 0.1:
                continue
        elif abs(jet.eta()) > 2.5 and abs(jet.eta()) < 2.75:
            if jet.userFloat("pileupJetId:fullDiscriminant") < -0.36:
                continue
        elif abs(jet.eta()) > 2.75 and abs(jet.eta()) < 3.0:
            if jet.userFloat("pileupJetId:fullDiscriminant") < -0.54:
                continue
        elif abs(jet.eta()) > 3.0 and abs(jet.eta()) < 5.0:
            if jet.userFloat("pileupJetId:fullDiscriminant") < -0.54:
                continue

        selected_jets.append(jet)

    if len(selected_electrons) != 0:
        continue

    if len(selected_muons) != 2:
        continue

    if len(selected_jets) < 2:
        continue    

    if selected_muons[0].charge() != selected_muons[1].charge():
        continue
    
#    print "Event", ievent

#    print len(selected_muons)
#    print len(selected_electrons)
#    print len(selected_jets)

    n_selected_events=n_selected_events+1
        
        #print "muon %2d: pt %4.1f, dz(PV) %+5.3f, POG loose id %d, tight id %d." % (
        #    i, mu.pt(), mu.muonBestTrack().dz(PV.position()), mu.isLooseMuon(), mu.isTightMuon(PV))

print "n_selected_events/n_events = " + str(float(n_selected_events)/float(n_events))
