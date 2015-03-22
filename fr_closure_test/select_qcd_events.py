#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import optparse

parser = optparse.OptionParser()

#parser.add_option('-i', '--input_filename', help='filename of the input ntuple', dest='finname', default='my_file.root')
#parser.add_option('-o', '--output_filename', help='filename of the output ntuple', dest='foutname', default='my_file.root')

(options,args) = parser.parse_args()

import sys

#otherwise, root will parse the command line options, see here http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=18637
sys.argv = []

from ROOT import *

from array import array
sys.path.append("../13_tev/")
from samples import *

gStyle.SetOptStat(0)

#gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/crab/CMSSW_7_2_0/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

#finname=options.finname
#foutname=options.foutname

#fin=TFile(finname)
#fout=TFile(foutname,"recreate")

gROOT.cd()

lumi=10

def fillMuonHistograms(t,hist):

    for entry in range(t.GetEntries()):
        t.GetEntry(entry)

        if abs(t.muon_4mom.Eta()) > 2.4:
            continue

        if not t.pass_full_muon_id:
            continue

        if t.metpt > 25:
            continue

        hist.Fill(t.muon_4mom.pt(),t.xsWeight)

def fillElectronHistograms(t,hist):
    for entry in range(t.GetEntries()):
        t.GetEntry(entry)

        if abs(t.electron_4mom.Eta()) > 2.5:
            continue

        if not t.pass_full_electron_id:
            continue

        if t.metpt > 25:
            continue

        hist.Fill(t.electron_4mom.pt(),t.xsWeight)

fwjets = TFile("/data/blue/anlevin/ntuples/fr_ntuples/wjets_phys14_v1.root")
fzjets = TFile("/data/blue/anlevin/ntuples/fr_ntuples/zjets_phys14_v1.root")
fqcd = TFile("/data/blue/anlevin/ntuples/fr_ntuples/QCD_pt_v3.root")

qcd_muon_tree=fqcd.Get("loose_muons")
qcd_electron_tree=fqcd.Get("loose_electrons")

wjets_muon_tree=fwjets.Get("loose_muons")
wjets_electron_tree=fwjets.Get("loose_electrons")

zjets_muon_tree=fzjets.Get("loose_muons")
zjets_electron_tree=fzjets.Get("loose_electrons")

hist = TH1F('', '', 35, 0., 100 )

hist.Sumw2()

hist.GetXaxis().CenterTitle()
hist.GetXaxis().SetTitle("lepton p_{T}")

qcd_muon_hist=hist.Clone()
qcd_electron_hist=hist.Clone()
wjets_muon_hist=hist.Clone()
wjets_electron_hist=hist.Clone()
zjets_muon_hist=hist.Clone()
zjets_electron_hist=hist.Clone()

fillMuonHistograms(qcd_muon_tree,qcd_muon_hist)
fillElectronHistograms(qcd_electron_tree,qcd_electron_hist)

fillMuonHistograms(wjets_muon_tree,wjets_muon_hist)
fillElectronHistograms(wjets_electron_tree,wjets_electron_hist)

fillMuonHistograms(zjets_muon_tree,zjets_muon_hist)
fillElectronHistograms(zjets_electron_tree,zjets_electron_hist)

qcd_muon_hist.SetLineColor(kBlack)
wjets_muon_hist.SetLineColor(kBlue)
zjets_muon_hist.SetLineColor(kRed)

qcd_electron_hist.SetLineColor(kBlack)
wjets_electron_hist.SetLineColor(kBlue)
zjets_electron_hist.SetLineColor(kRed)

qcd_muon_hist.SetLineWidth(3)
wjets_muon_hist.SetLineWidth(3)
zjets_muon_hist.SetLineWidth(3)

qcd_electron_hist.SetLineWidth(3)
wjets_electron_hist.SetLineWidth(3)
zjets_electron_hist.SetLineWidth(3)

leg=TLegend(.60,.65,.85,.85)
leg.SetLineWidth(3)
leg.AddEntry(qcd_electron_hist,"qcd","l")
leg.AddEntry(wjets_electron_hist,"wjets","l")
leg.AddEntry(zjets_electron_hist,"zjets","l")

c1=TCanvas("c1","c1")

c1.SetLogy()

qcd_muon_hist.Draw()
#wjets_muon_hist.Draw()
wjets_muon_hist.Draw("SAME")
zjets_muon_hist.Draw("SAME")

leg.Draw("SAME")

c1.SaveAs("muons.png")

c2=TCanvas("c2","c2")

c2.SetLogy()

qcd_electron_hist.Draw()
#wjets_electron_hist.Draw()
wjets_electron_hist.Draw("SAME")
zjets_electron_hist.Draw("SAME")

leg.Draw("SAME")

c2.SaveAs("electrons.png")

raw_input()
