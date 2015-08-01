from ConfigurationParser import *

#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

ewk_qcd_filename="/data/blue/anlevin/ntuples/wpwpjj_ewk_qcd_v13.root"
ewk_filename="/data/blue/anlevin/ntuples/wpwpjj_ewk_v13.root"
qcd_filename="/data/blue/anlevin/ntuples/wpwpjj_qcd_v13.root"

variable = "mjj"
charge="both"
lumi=10

import selection

import parse_reweight_info

import optparse

parser = optparse.OptionParser()

parser.add_option('--config',dest='config')

(options,args) = parser.parse_args()

#cfg = ConfigurationParser(options.config)

#assert("mode" in cfg and "channel" in cfg and "lumi" in cfg)

import sys

#otherwise, root will parse the command line options, see here http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=18637
sys.argv = []

from ROOT import *

from array import array

c1 = TCanvas("c1", "c1",5,50,500,500)

#gStyle.SetOptStat(0)
gROOT.ProcessLine('#include "/afs/cern.ch/work/a/anlevin/cmssw/CMSSW_7_2_0/src/ntuple_maker/ntuple_maker/interface/enum_definition.h"')

#put the overflow in the last bin
#if (t.jet1+t.jet2).M() > hist.GetBinLowEdge(hist.GetNbinsX()):
#    hist.Fill(hist.GetBinCenter(hist.GetNbinsX()),w)
#else:
#    print (t.jet1+t.jet2).M()
#    hist.Fill((t.jet1+t.jet2).M(),w)

        


def getVariable(t):
    if variable == "mjj":
        return (t.jet1+t.jet2).M()
    elif variable == "mll":
        return (t.lep1+t.lep2).M()
    elif variable == "met":
        return t.metpt
    elif variable == "detajj":
        return abs(t.jet1.Eta() - t.jet2.Eta())
    elif variable == "jet1btag":
        return t.jet1btag
    elif variable == "jet2btag":
        return t.jet2btag
    elif variable == "nvtx":
        return t.nvtx
    elif variable == "lep1pt":
        return t.lep1.pt()
    elif variable == "lep2pt":
        return t.lep2.pt()
    elif variable == "zeppenfeld":
        return max(abs(t.lep1.Eta() - (t.jet1.Eta() + t.jet2.Eta())/2.0),abs(t.lep2.Eta() - (t.jet1.Eta() + t.jet2.Eta())/2.0))
    else:
        assert(0)    

def fillHistogram(t,hist):
    print "t.GetEntries() = " + str(t.GetEntries())

    return_hist = hist.Clone()
    
    for entry in range(t.GetEntries()):
        t.GetEntry(entry)

        if entry % 100000 == 0:
            print "entry = " + str(entry)

        if charge == "+":
            if t.lep1id > 0:
                continue
        elif charge == "-":
            if t.lep1id < 0:
                continue
        else:
            assert(charge == "both")
            
        if (abs(t.lep1id) == 13 and abs(t.lep2id) == 11) or (abs(t.lep1id) == 11 and abs(t.lep2id) == 13) :
            channel="em"
        elif abs(t.lep1id) == 13 and abs(t.lep2id) == 13:
            channel = "mm"
        elif abs(t.lep1id) == 11 and abs(t.lep2id) == 11:
            channel = "ee"
        else:
            assert(0)
            
        #if cfg["channel"] != channel and cfg["channel"] !="all":
        #    continue

        if not selection.passSelection(t):
            continue

        w=t.xsWeight*float(lumi)

        var=getVariable(t)

        #scale_factor = t.qcd_weight_mur0p5muf2/t.qcd_pdf_weight_orig
        scale_factor = 1

        if var > return_hist.GetBinLowEdge(return_hist.GetNbinsX()):
            return_hist.Fill(return_hist.GetBinCenter(return_hist.GetNbinsX()),w*scale_factor)
        else:
            return_hist.Fill(var,w*scale_factor)

    return {"hist_central" : return_hist }

if variable == "mjj":
    binning=array('f',[500,700,1100,1600,2000])
    hist = TH1F('mjj', 'mjj',4, binning )
    #hist = TH1F('mjj', 'mjj', 35, 0., 200 )
    #hist = TH1F('mjj', 'mjj', 35, 0., 3000 )
    hist.GetXaxis().SetTitle("m_{jj} (GeV)")
elif variable == "mll":
    binning = array('f',[50,100,200,300,500])
    hist = TH1F('mll', 'mll',4, binning )
    #hist = TH1F('mll', 'mll', 35, 0., 500)
    #hist = TH1F('mll', 'mll', 35, 0., 5000)
    hist.GetXaxis().SetTitle("m_{ll} (GeV)")
elif variable == "met":
    hist = TH1F('met', 'met', 35, 0., 200 )
elif variable == "detajj":
    hist = TH1F('detajj', 'detajj', 35, 0., 5 )
elif variable == "jet1btag":
    hist = TH1F('jet1btag', 'jet1btag', 35, -1., 1 )
elif variable == "jet2btag":
    hist = TH1F('jet2btag', 'jet2btag', 35, -1., 1 )
elif variable == "nvtx":
    hist = TH1F('nvtx', 'nvtx', 35, 0., 60 )
elif variable == "lep1pt":
    hist = TH1F('lep1pt', 'lep1pt', 35, 0., 100 )
elif variable == "lep2pt":
    hist = TH1F('lep2pt', 'lep2pt', 35, 0., 100 )
elif variable == "zeppenfeld":
    hist = TH1F('zeppenfeld','zeppenfeld',35,0,5)
else:
    assert(0)

#error = sqrt(sum weight^2)
hist.Sumw2()

hist.SetTitle("")
hist.SetMinimum(0)
hist.SetMaximum(12)

hist.GetXaxis().CenterTitle()
hist.GetXaxis().SetTitleSize(0.045000000149)

hist.SetLineWidth(3)

f_ewk_qcd=TFile(ewk_qcd_filename)
f_ewk=TFile(ewk_filename)
f_qcd=TFile(qcd_filename)

tree_ewk_qcd=f_ewk_qcd.Get("events")
tree_qcd=f_qcd.Get("events")
tree_ewk=f_ewk.Get("events")

ewk=fillHistogram(tree_ewk,hist)
qcd=fillHistogram(tree_qcd,hist)
ewk_qcd=fillHistogram(tree_ewk_qcd,hist)

hist_sum=ewk["hist_central"].Clone()

hist_sum.Add(qcd["hist_central"])

hist_sum.SetLineColor(kRed)
ewk_qcd["hist_central"].SetLineColor(kBlue)

ewk_qcd["hist_central"].Draw()
hist_sum.Draw("SAME")

c1.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/interference.png")
