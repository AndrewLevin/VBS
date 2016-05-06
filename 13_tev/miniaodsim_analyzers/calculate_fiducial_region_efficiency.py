#calculate the fraction of events with three leptons in the acceptance

import ROOT
import sys
from DataFormats.FWLite import Events, Handle

#the capitalization for a and b is different because a is a pat jet and b is a TLorentzVector
from math import hypot, pi
def deltaR(a,b):
    dphi = abs(a.phi()-b.Phi());
    if dphi > pi: dphi = 2*pi-dphi
    return hypot(a.eta()-b.Eta(),dphi)

#events = Events ( ['root://eoscms.cern.ch//eos/cms/store/mc/RunIIFall15MiniAODv2/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/40000/3C186689-6ED9-E511-9BDB-00259057490C.root','root://eoscms.cern.ch//eos/cms/store/mc/RunIIFall15MiniAODv2/WZJToLLLNu_TuneCUETP8M1_13TeV-amcnlo-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/80000/FA49F076-3ED9-E511-A5BA-002590A8881E.root']) 

events = Events ( ['root://eoscms.cern.ch//eos/cms/store/mc/RunIIFall15MiniAODv2/WpWpJJ_EWK-QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/20000/420FA4F7-1CB9-E511-948E-02163E013C5C.root'] )

genjets,genjetsLabel = Handle("vector<reco::GenJet>"), "slimmedGenJets"
geninfo,geninfoLabel = Handle("GenEventInfoProduct"), "generator"
lheinfo,lheinfoLabel = Handle("LHEEventProduct"), "externalLHEProducer"

n_events_run_over = 0
n_selected_gen_unweighted = 0
n_selected_lhe_unweighted = 0
n_selected_gen_pos = 0
n_selected_gen_neg = 0
n_selected_lhe_pos = 0
n_selected_lhe_neg = 0

n_selected_gen = 0
n_selected_lhe = 0


n_event = 0

for event in events:

    n_event = n_event+1

    if n_event % 1000 == 0:
        print n_event

    pass_gen = True

    pass_lhe =True

    event.getByLabel(geninfoLabel, geninfo)
    event.getByLabel(lheinfoLabel, lheinfo)
    event.getByLabel(genjetsLabel, genjets)

    if geninfo.product().weight() > 0:
        n_events_run_over=n_events_run_over+1
    else:
        n_events_run_over=n_events_run_over-1

    n_leptons_in_acceptance = 0


    lhe_quarks = []
    lhe_leptons = []

    for i in range(0,len(lheinfo.product().hepeup().IDUP)):
	v=ROOT.TLorentzVector()
        v.SetPxPyPzE(lheinfo.product().hepeup().PUP.at(i)[0],lheinfo.product().hepeup().PUP.at(i)[1],lheinfo.product().hepeup().PUP.at(i)[2],lheinfo.product().hepeup().PUP.at(i)[3])

        if lheinfo.product().hepeup().ISTUP.at(i) != 1:
            continue

	if (abs(lheinfo.product().hepeup().IDUP.at(i)) == 11 or abs(lheinfo.product().hepeup().IDUP.at(i)) == 13 or abs(lheinfo.product().hepeup().IDUP.at(i)) == 15):
                lhe_leptons.append(v)

	if (abs(lheinfo.product().hepeup().IDUP.at(i)) == 1 or abs(lheinfo.product().hepeup().IDUP.at(i)) == 2 or abs(lheinfo.product().hepeup().IDUP.at(i)) == 3 or abs(lheinfo.product().hepeup().IDUP.at(i)) == 4 or abs(lheinfo.product().hepeup().IDUP.at(i)) == 5 or abs(lheinfo.product().hepeup().IDUP.at(i)) == 6):
                lhe_quarks.append(v)


    assert(len(lhe_leptons) == 2)

    assert(len(lhe_quarks) == 2)

    cleaned_jet_indices = []
    
    for i,j in enumerate(genjets.product()):
        
        found_matching_lepton= False

        for lhe_lepton in lhe_leptons:
            if deltaR(j,lhe_lepton) < 0.4:
                found_matching_lepton = True

        if not found_matching_lepton:
            cleaned_jet_indices.append(i)
    

    if len(cleaned_jet_indices) < 2:
        pass_gen=False
    elif ( genjets.product()[cleaned_jet_indices[0]].p4() + genjets.product()[cleaned_jet_indices[1]].p4() ).M() < 500  or genjets.product()[cleaned_jet_indices[0]].pt() < 30 or genjets.product()[cleaned_jet_indices[1]].pt() < 30  or abs(genjets.product()[cleaned_jet_indices[0]].eta()) > 4.7 or abs(genjets.product()[cleaned_jet_indices[1]].eta()) > 4.7 or abs(lhe_leptons[0].Eta()) > 2.5 or abs(lhe_leptons[1].Eta()) > 2.5 or lhe_leptons[0].Pt() < 20 or lhe_leptons[1].Pt() < 20:
        pass_gen=False

    if (lhe_quarks[0]+lhe_quarks[1]).M() < 500 or lhe_quarks[0].Pt() < 30 or lhe_quarks[1].Pt() < 30 or abs(lhe_quarks[0].Eta()) > 4.7 or abs(lhe_quarks[1].Eta()) > 4.7 or abs(lhe_leptons[0].Eta()) > 2.5 or abs(lhe_leptons[1].Eta()) > 2.5 or lhe_leptons[0].Pt() < 20 or lhe_leptons[1].Pt() < 20:
        pass_lhe = False

    if pass_lhe:
        n_selected_lhe_unweighted = n_selected_lhe_unweighted + 1
        if geninfo.product().weight() > 0:
            n_selected_lhe_pos = n_selected_lhe_pos+1
        else:
            n_selected_lhe_neg = n_selected_lhe_neg+1


    if pass_gen:
        #print "run %6d, lumi %4d, event %12d" % (event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
        n_selected_gen_unweighted = n_selected_gen_unweighted + 1
        if geninfo.product().weight() > 0:
            n_selected_gen_pos = n_selected_gen_pos+1
        else:
            n_selected_gen_neg = n_selected_gen_neg+1

n_selected_gen = n_selected_gen_pos - n_selected_gen_neg
n_selected_lhe = n_selected_lhe_pos - n_selected_lhe_neg

print "n_selected_gen_unweighted = " + str(n_selected_gen_unweighted)
print "n_selected_gen_pos = " + str(n_selected_gen_pos)
print "n_selected_gen_neg = " + str(n_selected_gen_neg)
print "n_selected_lhe_pos = " + str(n_selected_lhe_pos)
print "n_selected_lhe_neg = " + str(n_selected_lhe_neg)
print "n_events_run_over = " +str(n_events_run_over)
print "n_selected_gen = " +str(n_selected_gen)
print "gen efficiency = " + str(float(n_selected_gen)/float(n_events_run_over))
print "lhe efficiency = " + str(float(n_selected_lhe)/float(n_events_run_over))
print "n_selected_events_expected = "+str(float(n_selected_gen)/float(n_events_run_over)*0.4585*1000*2.22)
print "n_selected_events_expected = "+str(float(n_selected_gen)/float(n_events_run_over)*4.740*1000*2.22)
