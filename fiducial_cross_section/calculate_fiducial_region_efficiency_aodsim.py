#this runs over AOD and calculates the efficiency to enter the fiducial region

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from math import *

from math import hypot, pi
def deltaR(a,b):
    dphi = abs(a.phi()-b.phi());
    if dphi > pi: dphi = 2*pi-dphi
    return hypot(a.eta()-b.eta(),dphi)

events = Events (['file:/afs/cern.ch/work/a/anlevin/data/AOD/wpwp_13_tev_qed_4_qcd_0.root'])

lheeventproduct, lheeventproductLabel = Handle("LHEEventProduct"),"source"
genparticles, genParticlesLabel = Handle("vector<reco::GenParticle>"), "genParticles"
genjets, genJetsLabel = Handle("vector<reco::GenJet>"), "ak4GenJets"

n_events=0
n_events_fiducial=0
# loop over events
count= 0
for i,event in enumerate(events):

    #set the number of events to run over
    if i == 5000:
        break

    if i % 100 == 0:
        print str(i)

    #if event.eventAuxiliary().luminosityBlock() != 2001:
    #    continue

    #if event.eventAuxiliary().event() != 1:
    #    continue

    #print "run %6d, lumi %4d, event %12d" % (event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())
    
    event.getByLabel(genParticlesLabel, genparticles)
    event.getByLabel(genJetsLabel, genjets)
    event.getByLabel(lheeventproductLabel, lheeventproduct)

    lhejet1 = ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')()
    lhejet2 = ROOT.Math.LorentzVector('ROOT::Math::PxPyPzE4D<double>')()

    foundjet1=False
    for i in range(0,lheeventproduct.product().hepeup().NUP):
        if (abs(lheeventproduct.product().hepeup().IDUP[i]) == 1 or abs(lheeventproduct.product().hepeup().IDUP[i]) == 2 or abs(lheeventproduct.product().hepeup().IDUP[i]) == 3 or abs(lheeventproduct.product().hepeup().IDUP[i]) == 4 or abs(lheeventproduct.product().hepeup().IDUP[i]) == 5) and lheeventproduct.product().hepeup().ISTUP[i] == 1:
            if not foundjet1:
                lhejet1.SetPxPyPzE(lheeventproduct.product().hepeup().PUP[i][0],lheeventproduct.product().hepeup().PUP[i][1],lheeventproduct.product().hepeup().PUP[i][2],lheeventproduct.product().hepeup().PUP[i][3])
                foundjet1 = True
            else:    
                lhejet2.SetPxPyPzE(lheeventproduct.product().hepeup().PUP[i][0],lheeventproduct.product().hepeup().PUP[i][1],lheeventproduct.product().hepeup().PUP[i][2],lheeventproduct.product().hepeup().PUP[i][3])

    #make sure the genjets are sorted by pt

    for (i,genjet) in enumerate(genjets.product()):
        #print genjet.pt()
	if i != 0 and genjet.pt() > previousgenjetpt:
            print "the gen jets are not sorted by pt"
            sys.exit(0)
	previousgenjetpt=genjet.pt()

    selected_electrons = []
    selected_muons = []
    selected_electron_neutrinos = []
    selected_muon_neutrinos = []

    gen_leptons = []

    for p in genparticles.product():
        if abs(p.pdgId()) == 11 and p.status() == 3:
            gen_leptons.append(p)
        elif abs(p.pdgId()) == 13 and p.status() == 3:
            gen_leptons.append(p)
        elif abs(p.pdgId()) == 15 and p.status() == 3:
            gen_leptons.append(p)

    gen_quarks = []

    #don't consider tau to electron and muon decays
    if abs(gen_leptons[0].pdgId()) == 15 or abs(gen_leptons[1].pdgId()) == 15:
        continue

    n_events=n_events+1

    for p in genparticles.product():
	if abs(p.pdgId()) == 13 and p.status() == 1:
            current=p
            mother = False
            if current.mother():
                mother = True
                mother_pdg_id = current.mother().pdgId()
                while mother_pdg_id == p.pdgId() or abs(mother_pdg_id) == 15:
                    current = current.mother()
                    mother_pdg_id = current.mother().pdgId()
            if mother and abs(mother_pdg_id) == 24:        
                selected_muons.append(p)
	if abs(p.pdgId()) == 14 and p.status() == 1:
            current=p
            mother = False
            if current.mother():
                mother = True
                mother_pdg_id = current.mother().pdgId()
                while mother_pdg_id == p.pdgId() or abs(mother_pdg_id) == 15:
                    current = current.mother()
                    mother_pdg_id = current.mother().pdgId()
            if mother and abs(mother_pdg_id) == 24:        
                selected_muon_neutrinos.append(p)
	if abs(p.pdgId()) == 11 and p.status() == 1:
            current=p
            mother = False
            if current.mother():
                mother = True
                mother_pdg_id = current.mother().pdgId()
                while mother_pdg_id == p.pdgId() or abs(mother_pdg_id) == 15:
                    current = current.mother()
                    mother_pdg_id = current.mother().pdgId()
            if mother and abs(mother_pdg_id) == 24:        
                selected_electrons.append(p)
	if abs(p.pdgId()) == 12 and p.status() == 1:
            current=p
            mother = False
            if current.mother():
                mother = True
                mother_pdg_id = current.mother().pdgId()
                while mother_pdg_id == p.pdgId() or abs(mother_pdg_id) == 15:
                    current = current.mother()
                    mother_pdg_id = current.mother().pdgId()
            if mother and abs(mother_pdg_id) == 24:        
                selected_electron_neutrinos.append(p)

    dressed_muons = []
    dressed_electrons = []

    for selected_muon in selected_muons:
        dressed_lepton = [selected_muon, selected_muon.p4()]
        for p in genparticles.product():
            if abs(p.pdgId()) == 22 and p.status() == 1 and deltaR(p.p4(),selected_muon.p4()) < 0.1:
                #print "found photon"
                dressed_lepton[1] = dressed_lepton[1] + p.p4()
        dressed_muons.append(dressed_lepton)        

    for selected_electron in selected_electrons:
        dressed_lepton = [selected_electron, selected_electron.p4()]
        for p in genparticles.product():
            if abs(p.pdgId()) == 22 and p.status() == 1 and deltaR(p.p4(),selected_electron.p4()) < 0.1:
                #print "found photon"
                dressed_lepton[1] = dressed_lepton[1] + p.p4()
        dressed_electrons.append(dressed_lepton)

    two_muon_event = len(dressed_muons) >= 2 and dressed_muons[0][0].charge() == dressed_muons[1][0].charge() and dressed_muons[0][1].pt() > 10 and dressed_muons[1][1].pt() > 10 and abs(selected_muons[0].eta()) < 2.5 and abs(selected_muons[1].eta()) < 2.5

    two_electron_event = len(dressed_electrons) >= 2 and dressed_electrons[0][0].charge() == dressed_electrons[1][0].charge() and dressed_electrons[0][1].pt() > 10 and dressed_electrons[1][1].pt() > 10 and abs(selected_electrons[0].eta()) < 2.5 and abs(selected_electrons[1].eta()) < 2.5

    muon_electron_event = len(dressed_muons) >= 1 and len(dressed_electrons) >=1 and dressed_muons[0][0].charge() == dressed_electrons[0][0].charge() and dressed_muons[0][1].pt() > 10 and dressed_electrons[0][1].pt() > 10 and abs(selected_muons[0].eta()) < 2.5 and abs(selected_electrons[0].eta()) < 2.5
    
    if two_muon_event:
        lep1_p4 = dressed_muons[0][1]
        lep2_p4 = dressed_muons[1][1]
    elif two_electron_event:
        lep1_p4 = dressed_electrons[0][1]
        lep2_p4 = dressed_electrons[1][1]
    elif muon_electron_event:
        lep1_p4 = dressed_muons[0][1]
        lep2_p4 = dressed_electrons[0][1]
    else:
        continue

    #if not two_muon_event and not two_electron_event and not muon_electron_event:
    #    continue

    cleanedgenjets = []

    for genjet in genjets.product():
        if deltaR(genjet.p4(),lep1_p4) < 0.5:
            continue
        if deltaR(genjet.p4(),lep2_p4) < 0.5:
            continue
        match_to_neutrino=False
        for muon_neutrino in selected_muon_neutrinos:
            if deltaR(genjet.p4(),muon_neutrino.p4()) < 0.5:
                match_to_neutrino=True
        for electron_neutrino in selected_electron_neutrinos:
            if deltaR(genjet.p4(),electron_neutrino.p4()) < 0.5:
                match_to_neutrino=True
        if match_to_neutrino:
            continue
        cleanedgenjets.append(genjet)

    if len(cleanedgenjets) < 2:
	    continue        

    genjet1=cleanedgenjets[0]	    
    genjet2=cleanedgenjets[1]	            


    if genjet1.pt() < 20:
	continue

    if genjet2.pt() < 20:
	continue

    if abs(genjet1.eta()) > 5.0:
	continue

    if abs(genjet2.eta()) > 5.0:
	continue

    #if (lhejet1+lhejet2).mass() < 500:
    #    continue

    #if abs(lhejet1.eta() - lhejet2.eta()) < 2.5:
    #    continue

    #if (gen_leptons[0].p4() + gen_leptons[1].p4()).mass() < 500:
    #    continue

    #if abs(gen_leptons[0].eta() - gen_leptons[1].eta()) < 2.5:
    #    continue

    if (genjet1.p4() + genjet2.p4()).mass() < 500:
     	continue

    if abs(genjet1.eta() - genjet2.eta()) < 2.5:
     	continue

    n_events_fiducial=n_events_fiducial+1

print "n_events = "+str(n_events)
print "n_events_fiducial = "+str(n_events_fiducial)
print "n_events_fiducial/n_events = "+str(float(n_events_fiducial)/float(n_events))

