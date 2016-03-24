import ROOT
import sys

from DataFormats.FWLite import Events, Handle

events_powheg = Events ( ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall15MiniAODv2/WmWmJJ_13TeV-powheg-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/80000/84FEA6AF-ABED-E511-AD3F-001E67581494.root'] )

events_madgraph = Events ( ['root://cms-xrd-global.cern.ch//store/mc/RunIIFall15MiniAODv2/WpWpJJ_EWK_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/10000/4E359B07-BCB8-E511-8421-02163E012F84.root']) 

lheinfo,lheinfoLabel = Handle("LHEEventProduct"), "source"

genjets,genjetsLabel = Handle("vector<reco::GenJet>"), "slimmedGenJets"

handlePruned,labelPruned  = Handle ("std::vector<reco::GenParticle>"), "prunedGenParticles"

jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"

n_events_selected_powheg_gen = 0

n_events_selected_powheg_reco = 0

n_events_run_over_powheg = 0

for event in events_powheg:

    if n_events_run_over_powheg % 1000 == 0:
        print n_events_run_over_powheg

    n_events_run_over_powheg = n_events_run_over_powheg+1

    event.getByLabel(genjetsLabel, genjets) 
    event.getByLabel(lheinfoLabel, lheinfo) 
    event.getByLabel (labelPruned, handlePruned)
    event.getByLabel(jetLabel, jets)

    found_negative_w = True

    for i in range(0,len(lheinfo.product().hepeup().IDUP)):
        if lheinfo.product().hepeup().IDUP.at(i) == -24:
            found_negative_w = False

    if found_negative_w:
        continue

    pass_gen = True

    pass_reco = True

    if len(genjets.product()) < 2:
        pass_gen=False
    elif ( genjets.product()[0].p4() + genjets.product()[1].p4() ).M() < 500:
        pass_gen=False

    if len(jets.product()) < 2:
        pass_reco=False
    elif ( jets.product()[0].p4() + jets.product()[1].p4() ).M() < 500 or ( jets.product()[0].p4() + jets.product()[1].p4() ).M() > 1100:
        pass_reco=False

    leps = []

    pruned = handlePruned.product()

    for p in pruned :
#        if (abs(p.pdgId()) == 11 or abs(p.pdgId()) == 13 or abs(p.pdgId()) == 15) and  p.mother() and abs(p.mother().pdgId()) == 24:
        if (abs(p.pdgId()) == 11 or abs(p.pdgId()) == 13) and  p.mother() and abs(p.mother().pdgId()) == 24:
            leps.append(p)

    if len(leps) != 2:
        continue

    #assert(len(leps) == 2)

    if leps[0].p4() < 20:
        pass_gen=False

    if leps[1].p4() < 20:
        pass_gen=False

    if abs(leps[0].eta()) > 2.5:
        pass_gen=False

    if abs(leps[1].eta()) > 2.5:
        pass_gen=False

    if pass_gen:
        n_events_selected_powheg_gen = n_events_selected_powheg_gen+1

    if pass_reco:
        n_events_selected_powheg_reco = n_events_selected_powheg_reco+1

    #for i,j in enumerate(genjets.product()):
    #     if j.pt() < 20: 
    #         continue

lheinfo,lheinfoLabel = Handle("LHEEventProduct"), "externalLHEProducer"

n_events_selected_madgraph_gen = 0

n_events_selected_madgraph_reco = 0

n_events_run_over_madgraph = 0

for event in events_madgraph:

    if n_events_run_over_madgraph % 1000 == 0:
        print n_events_run_over_madgraph

    n_events_run_over_madgraph = n_events_run_over_madgraph+1

    event.getByLabel(genjetsLabel, genjets) 
    event.getByLabel(lheinfoLabel, lheinfo) 
    event.getByLabel (labelPruned, handlePruned)
    event.getByLabel(jetLabel, jets)

    found_negative_w = True

    for i in range(0,len(lheinfo.product().hepeup().IDUP)):
        if lheinfo.product().hepeup().IDUP.at(i) == -24:
            found_negative_w = False

    if found_negative_w:
        continue

    pass_gen = True

    pass_reco = True

    if len(genjets.product()) < 2:
        pass_gen=False
    elif ( genjets.product()[0].p4() + genjets.product()[1].p4() ).M() < 500:
        pass_gen=False

    if len(jets.product()) < 2:
        pass_reco=False
    elif ( jets.product()[0].p4() + jets.product()[1].p4() ).M() < 500 or ( jets.product()[0].p4() + jets.product()[1].p4() ).M() > 1100:
        pass_reco=False

    leps = []

    pruned = handlePruned.product()

    for p in pruned :
        if (abs(p.pdgId()) == 11 or abs(p.pdgId()) == 13) and  p.mother() and abs(p.mother().pdgId()) == 24:
        #if (abs(p.pdgId()) == 11 or abs(p.pdgId()) == 13 or abs(p.pdgId()) == 15) and  p.mother() and abs(p.mother().pdgId()) == 24:
            leps.append(p)

    if len(leps) != 2:
        continue

    #assert(len(leps) == 2)

    if leps[0].p4() < 20:
        pass_gen=False

    if leps[1].p4() < 20:
        pass_gen=False

    if abs(leps[0].eta()) > 2.5:
        pass_gen=False

    if abs(leps[1].eta()) > 2.5:
        pass_gen=False

    if pass_gen:
        n_events_selected_madgraph_gen = n_events_selected_madgraph_gen+1

    if pass_reco:
        n_events_selected_madgraph_reco = n_events_selected_madgraph_reco+1

    #for i,j in enumerate(genjets.product()):
    #     if j.pt() < 20: 
    #         continue

print "powheg xs:"
print 0.007868 * float(n_events_selected_powheg_gen)/float(n_events_run_over_powheg)
print 0.007868 * float(n_events_selected_powheg_reco)/float(n_events_run_over_powheg)

print "madgraph xs:"
print 0.02526 * float(n_events_selected_madgraph_gen)/float(n_events_run_over_madgraph)
print 0.02526 * float(n_events_selected_madgraph_reco)/float(n_events_run_over_madgraph)

#print "(powheg xs - madgraph xs) / (madgraph xs):"
#print (0.007868 * float(n_events_selected_powheg)/float(n_events_run_over_powheg) - 0.02526 * float(n_events_selected_madgraph)/float(n_events_run_over_madgraph))/(0.02526 * float(n_events_selected_madgraph)/float(n_events_run_over_madgraph))
