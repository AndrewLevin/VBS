import ROOT
import sys
from DataFormats.FWLite import Events, Handle
from math import *
import json


def isAncestor(a,p) :
        if a == p : 
                return True
        for i in xrange(0,p.numberOfMothers()) :
                if isAncestor(a,p.mother(i)) :
                         return True
        return False

f_event_list=open("/afs/cern.ch/work/a/anlevin/public/delete_this_2.txt")

event_list=json.loads(f_event_list.read())

print event_list

#events = Events('file:/afs/cern.ch/work/a/anlevin/VBS/13_tev/Merged.root')
#events = Events('file:/afs/cern.ch/work/a/anlevin/tmp/MySkim_1.electrons.root')

events = Events (['root://cms-xrd-global.cern.ch//store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/BC441FED-7662-E511-A233-C8600032C755.root'])


#events = Events(
#['root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/50000/102AAAF1-0966-E511-B871-24BE05C6D5B1.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/50000/807E47CC-0966-E511-A480-B083FED00118.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/50000/AEB5F0EF-0966-E511-833F-24BE05C616E1.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/0C9B88FC-8566-E511-A82B-782BCB284437.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/10F810F5-8566-E511-A633-009C02AABB60.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/1CD6F115-8666-E511-B523-90B11C27E141.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/26A4B5F7-8566-E511-84A5-002590593876.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/26DBC5F1-8566-E511-8C82-20CF3027A607.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/3A5140F2-8566-E511-8242-B083FED42488.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/4818A9C3-8566-E511-9BFB-008CFA11139C.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/48249135-8966-E511-A11D-0002C92A1030.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/587205F3-8566-E511-97F4-0025905A6132.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/60A6DBF4-8566-E511-9DA1-002618943975.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/7E04FAFA-8566-E511-A52F-0025907E343C.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/7EB991EF-8566-E511-938E-0025905C2CBE.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/88EF4EF2-8566-E511-8B48-0025905A608E.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/9A6290EF-8566-E511-9459-0025B3E02292.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/9E4540F4-8566-E511-B02F-842B2B758AD8.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/AC6E7EF2-8566-E511-BC65-001E670B253C.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/AE7481F1-8566-E511-88B1-842B2B296063.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/C419E6CC-8566-E511-9479-0002C90EB9D8.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/F69B98E3-8566-E511-8AD3-008CFA0A570C.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/10000/0EC87D48-E861-E511-B9FB-002590A3C97E.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/10000/1ACDCBEF-E661-E511-80A2-002590D8C7E2.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/10000/D28CBB33-E661-E511-A618-00259073E3AC.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/1A9348E8-C362-E511-A4C0-001E67A3FDF8.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/36C9568D-C362-E511-B7D4-0026B94DBDBC.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/487FBB7E-C362-E511-8769-00259073E506.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/5AA1E450-C662-E511-92EB-842B2B76653D.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/5AB4384E-C662-E511-BFE2-0002C92A1024.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/62EEDB1B-7862-E511-BDB0-0CC47A13CC7A.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/74E8BDFF-7862-E511-A8C5-B083FED12B5C.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/7AEF7437-9B62-E511-A3CA-0025905C42A6.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/92163AD0-7662-E511-BDD3-B083FED12B5C.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/AC8E7771-7E62-E511-9976-3417EBE886B2.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/B4849E4A-C662-E511-A2B8-008CFA110B08.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/BA02EE79-C362-E511-A850-6CC2173BC350.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/BC441FED-7662-E511-A233-C8600032C755.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/C8FB0F79-C362-E511-9F7F-6CC2173C4580.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/E4DF1C47-D462-E511-9A8C-549F35AD8BD6.root',
#'root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-4to60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/30000/FE050330-D462-E511-93BD-782BCB717ED1.root',
#])

#events = Events (['root://eoscms.cern.ch//eos/cms/store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_\74_V9-v1/60000/7EB991EF-8566-E511-938E-0025905C2CBE.root','root://cms-xrd-global.cern.ch//store/mc/RunIISpring15DR74/WLLJJToLNu_M-60_EWK_QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/60000/7EB991EF-8566-E511-938E-0025905C2CBE.root'])

lheinfo,lheinfoLabel = Handle("LHEEventProduct"), "externalLHEProducer"

muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"
handlePruned  = Handle ("std::vector<reco::GenParticle>")
handlePacked  = Handle ("std::vector<pat::PackedGenParticle>")

labelPruned = ("prunedGenParticles")
labelPacked = ("packedGenParticles")

# loop over events
count= 0

for event in events:

    found_event=False

    for triplet in event_list["event_list"]:
        if event.eventAuxiliary().run() == int(triplet[2]) and event.eventAuxiliary().luminosityBlock() == int(triplet[1]) and event.eventAuxiliary().event() == int(triplet[0]):
		found_event=True;

    #if event.eventAuxiliary().luminosityBlock() != 1299:
    #    continue

    #if event.eventAuxiliary().event() != 84431:
    #    continue

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

    #continue		
    
    event.getByLabel(muonLabel, muons)
    
    event.getByLabel(lheinfoLabel,lheinfo)

    for i in range(0,len(lheinfo.product().hepeup().IDUP)):
        print lheinfo.product().hepeup().IDUP.at(i)

    print "packed"	    

    event.getByLabel (labelPacked, handlePacked)

    packed = handlePacked.product()

    for p in packed :
        #print "p.numberOfMothers() = "+str(p.numberOfMothers())
	if p.mother(0) and p.mother(0).pdgId():
	    print "PdgId : %s   pt : %s  eta : %s   phi : %s  mother_pdg_id : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi(),p.mother(0).pdgId())    
        else:
	    print "PdgId : %s   pt : %s  eta : %s   phi : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi())    	    	

    print "pruned"	    
    
    for p in pruned :
	if p.mother() and p.mother().pdgId():
	    print "PdgId : %s   pt : %s  eta : %s   phi : %s  mother_pdg_id : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi(),p.mother().pdgId())    
        else:
	    print "PdgId : %s   pt : %s  eta : %s   phi : %s" %(p.pdgId(),p.pt(),p.eta(),p.phi())    	    	

    sys.exit(0)

    for i,mu in enumerate(muons.product()): 
	if mu.pt() < 5 or not mu.isLooseMuon(): continue
	print "pt : "+str(mu.pt())+ " eta : " +str(mu.eta()) + " phi : " + str(mu.phi())


