#calculate the fraction of events with three leptons in the acceptance

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
events = Events ( ['root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/50000/807E47CC-0966-E511-A480-B083FED00118.root']) 

lheinfo,lheinfoLabel = Handle("LHEEventProduct"), "externalLHEProducer"

n_events_run_over = 0

n_events_with_three_leptons_in_acceptance = 0

n_events_with_three_leptons = 0

for event in events:

    if n_events_run_over % 1000 == 0:
        print n_events_run_over

    n_events_run_over=n_events_run_over+1

    event.getByLabel(lheinfoLabel,lheinfo)

    n_leptons_in_acceptance = 0
    n_leptons = 0

    for i in range(0,len(lheinfo.product().hepeup().IDUP)):
	v=ROOT.TLorentzVector();
        v.SetPxPyPzE(lheinfo.product().hepeup().PUP.at(i)[0],lheinfo.product().hepeup().PUP.at(i)[1],lheinfo.product().hepeup().PUP.at(i)[2],lheinfo.product().hepeup().PUP.at(i)[3])

	if v.Pt() > 10 and abs(v.Eta()) < 2.5 and (abs(lheinfo.product().hepeup().IDUP.at(i)) == 11 or abs(lheinfo.product().hepeup().IDUP.at(i)) == 13):
            n_leptons_in_acceptance=n_leptons_in_acceptance+1

	if abs(lheinfo.product().hepeup().IDUP.at(i)) == 11 or abs(lheinfo.product().hepeup().IDUP.at(i)) == 13:
            n_leptons=n_leptons+1

    assert(n_leptons_in_acceptance <= 3)
    assert(n_leptons <= 3)

    if n_leptons_in_acceptance == 3: 
        n_events_with_three_leptons_in_acceptance = n_events_with_three_leptons_in_acceptance+1   

    if n_leptons == 3:
        n_events_with_three_leptons = n_events_with_three_leptons+1

print "n_events_with_three_leptons = "+str(n_events_with_three_leptons)
print "n_events_with_three_leptons_in_acceptance = "+str(n_events_with_three_leptons_in_acceptance)
print "n_events_run_over = " +str(n_events_run_over)
print "float(n_events_with_three_leptons_in_acceptance)/float(n_events_run_over) = "+ str(float(n_events_with_three_leptons_in_acceptance)/float(n_events_run_over))
print "float(n_events_with_three_leptons)/float(n_events_run_over) = "+ str(float(n_events_with_three_leptons)/float(n_events_run_over))
