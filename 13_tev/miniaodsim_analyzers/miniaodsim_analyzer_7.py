#make a histogram of the mll distribution at lhe level

import ROOT
import sys
from DataFormats.FWLite import Events, Handle
events = Events ( ['root://eoscms.cern.ch//eos/cms/store/user/anlevin/data/MINIAOD/wpwpjj_dim8_v1/step4_output_601.root']) 

lheinfo,lheinfoLabel = Handle("LHEEventProduct"), "source"

n_events_run_over = 0

f=ROOT.TFile("histograms.root","recreate")

th1f=ROOT.TH1F("mll","mll",100,0,1000)

for event in events:

    if n_events_run_over % 1000 == 0:
        print n_events_run_over

    n_events_run_over=n_events_run_over+1

    event.getByLabel(lheinfoLabel,lheinfo)

    n_leptons_in_acceptance = 0
    n_leptons = 0

    #print lheinfo.product().weights()[5]

    l1=ROOT.TLorentzVector()
    l2=ROOT.TLorentzVector()

    for i in range(0,len(lheinfo.product().hepeup().IDUP)):
	v=ROOT.TLorentzVector();
        v.SetPxPyPzE(lheinfo.product().hepeup().PUP.at(i)[0],lheinfo.product().hepeup().PUP.at(i)[1],lheinfo.product().hepeup().PUP.at(i)[2],lheinfo.product().hepeup().PUP.at(i)[3])

	if abs(lheinfo.product().hepeup().IDUP.at(i)) == 11 or abs(lheinfo.product().hepeup().IDUP.at(i)) == 13:
            #print abs(lheinfo.product().hepeup().IDUP.at(i)) == 11
            #print abs(lheinfo.product().hepeup().IDUP.at(i)) == 13
            #print lheinfo.product().hepeup().IDUP.at(i)
            if n_leptons == 0:
                l1 = v
            elif n_leptons == 1:
                l2 = v
            else:
                print n_leptons
                assert(0)
            n_leptons=n_leptons+1

    if n_leptons == 2:
        mll = (l1+l2).M()
        th1f.Fill(mll)
        #print mll

f.cd()

th1f.Write()
