#classify wzjj events which pass the selection

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
import json

#here is an example of how the event list should look like (for the case of one event):

#{"event_list":
#[
#[190767,2219,1]
#]
#}

f_event_list=open("/afs/cern.ch/work/a/anlevin/public/delete_this_2.txt")

event_list=json.loads(f_event_list.read())

print event_list

events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/BC441FED-7662-E511-A233-C8600032C755.root'])

lheinfo,lheinfoLabel = Handle("LHEEventProduct"), "externalLHEProducer"

handlePruned  = Handle ("std::vector<reco::GenParticle>")

labelPruned = ("prunedGenParticles")

# loop over events
count= 0

for event in events:

    found_event=False

    for triplet in event_list["event_list"]:
        if event.eventAuxiliary().run() == int(triplet[2]) and event.eventAuxiliary().luminosityBlock() == int(triplet[1]) and event.eventAuxiliary().event() == int(triplet[0]):
		found_event=True;

    if not found_event:
        continue   

    print "run %6d, lumi %4d, event %12d" % (event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())

    event.getByLabel (labelPruned, handlePruned)

    pruned = handlePruned.product()

    case1 = False
    case2 = False
    case3 = False
    case4 = False
    case5 = False

    for p in pruned :
	if (abs(p.pdgId()) == 11) and  p.mother() and (abs(p.mother().pdgId()) == 23 or abs(p.mother().pdgId()) == 24 or abs(p.mother().pdgId()) == 21):
	    if p.pt() < 10:
		case1 = True    

    for p in pruned :
	if (abs(p.pdgId()) == 11) and  p.mother() and (abs(p.mother().pdgId()) == 23 or abs(p.mother().pdgId()) == 24 or abs(p.mother().pdgId()) == 21):
	    if abs(p.eta()) > 2.4:
		case2 = True    

    for p in pruned :
	if (abs(p.pdgId()) == 13) and  p.mother() and (abs(p.mother().pdgId()) == 23 or abs(p.mother().pdgId()) == 24 or abs(p.mother().pdgId()) == 21):
	    if p.pt() < 10:
		case3 = True    

    for p in pruned :
	if (abs(p.pdgId()) == 13) and  p.mother() and (abs(p.mother().pdgId()) == 23 or abs(p.mother().pdgId()) == 24 or abs(p.mother().pdgId()) == 21):
	    if abs(p.eta()) > 2.4:
		case4 = True    

    for p in pruned :
	if abs(p.pdgId()) == 15 and (abs(p.mother().pdgId()) == 23 or abs(p.mother().pdgId()) == 24) and p.daughter(1) and abs(p.daughter(1).pdgId()) != 16 and abs(p.daughter(1).pdgId()) != 15 and abs(p.daughter(1).pdgId()) != 14 and abs(p.daughter(1).pdgId()) != 13 and abs(p.daughter(1).pdgId()) != 12 and abs(p.daughter(1).pdgId()) != 11:
                case5 = True

    print str(case1)+" "+str(case2)+" "+str(case3)+" "+str(case4)+" "+str(case5)

    #print (not case1 and not case1 and not case3 and case4 and not case5)

    assert( (case1 and case2 and not case3 and not case4 and not case5) or (not case1 and not case2 and case3 and case4 and not case5) or (case1 and not case2 and not case3 and not case4 and not case5) or (not case1 and case2 and not case3 and not case4 and not case5) or (not case1 and not case1 and case3 and not case4 and not case5) or (not case1 and not case1 and not case3 and case4 and not case5) or (not case1 and not case1 and not case3 and not case4 and case5) or (not case1 and not case2 and not case3 and not case4 and not case5) or (not case1 and not case2 and case3 and case4 and case5) or (case1 and not case2 and not case3 and not case4 and case5) or (case1 and not case2 and case3 and not case4 and not case5))

    if not case1 and not case2 and case3 and case4 and case5:
	print "cases 3, 4, and 5"    
    elif case1 and not case2 and not case3 and not case4 and case5:
        print "cases 1 and 5"	
    elif case1 and not case2 and case3 and not case4 and not case5:
        print "cases 1 and 3"	
    elif case1 and case2 and not case5:
        print "cases 1 and 2"
    elif case3 and case4 and not case5:
        print "cases 3 and 4"
    elif case1 and not case5:
        print "case 1"
    elif case2 and not case5:
        print "case 2"
    elif case3 and not case5:
        print "case 3"
    elif case4 and not case5:
        print "case 4"
    elif case5:
        print "case 5"
    else:
        print "none of the cases"

