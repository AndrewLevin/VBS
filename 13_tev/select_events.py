#if running on a dtmit machine, you need to move to root version 5.34.20 or higher
#source /afs/cern.ch/sw/lcg/external/gcc/4.7.2/x86_64-slc5-gcc47-opt/setup.sh
#source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.20/x86_64-slc5-gcc47-opt/root/bin/thisroot.sh

import optparse
from ROOT import *
import sys

gStyle.SetOptStat(0)

def fillHistograms(t,hist):
    for entry in range(t.GetEntries()):
        t.GetEntry(entry)

        if t.lep1q == t.lep2q:
            continue

        #if (t.jet1+t.jet2).M() < 500:
        #    continue
        #if abs(t.jet1.Eta() - t.jet2.Eta()) < 2.5:
        #    continue

        lep1passfullid = bool(t.cuts & 1<<2)
        lep2passfullid = bool(t.cuts & 1<<9)

        if not lep1passfullid:
            continue

        if not lep2passfullid:
            continue

        if options.variable == "mjj":
            hist.Fill((t.jet1+t.jet2).M())
        elif options.variable == "mll":    
            hist.Fill((t.lep1+t.lep2).M())
        elif options.variable == "met":    
            hist.Fill(t.metpt)
        elif options.variable == "detajj":
            hist.Fill(abs(t.jet1.Eta() - t.jet2.Eta()))
        elif options.variable == "jet1btag":
            hist.Fill(t.jet1btag)    
        elif options.variable == "jet2btag":            
            hist.Fill(t.jet2btag)    
        else:
            assert(0)
        

parser = optparse.OptionParser()

parser.add_option('-v', '--variable', help='which variable to plot', dest='variable', default='mjj')

(options,args) = parser.parse_args()


#signal_fname="/data/blue/anlevin/ntuples/wpwp_13_tev_qed_4_qcd_0_v3.root"
signal_fname="/data/blue/anlevin/ntuples/ttbar_normal_mixing.root"
#background_fname="/data/blue/anlevin/ntuples/wpwp_13_tev_qed_4_qcd_0_v3.root"
background_fname="/data/blue/anlevin/ntuples/ttbar_pre_mixing.root"
#background_fname="/afs/cern.ch/user/a/anlevin/merged.root"

c=TCanvas("c", "c",0,0,600,500)
c.Range(0,0,1,1)

f_signal=TFile(signal_fname)
f_background=TFile(background_fname)

tree_signal=f_signal.Get("demo/events")
tree_background=f_background.Get("demo/events")

if options.variable == "mjj":
    hist = TH1F('mjj', 'mjj', 35, 0., 2000 )
elif options.variable == "mll":    
    hist = TH1F('mll', 'mll', 35, 0., 500)
elif options.variable == "met":
    hist = TH1F('met', 'met', 35, 0., 200 )
elif options.variable == "detajj":
    hist = TH1F('detajj', 'detajj', 35, 0., 5 )
elif options.variable == "jet1btag":
    hist = TH1F('detajj', 'jet1btag', 35, -1., 1 )
elif options.variable == "jet2btag":
    hist = TH1F('detajj', 'jet2btag', 35, -1., 1 )        
else:
    assert(0)

hist_signal=hist.Clone()
hist_background=hist.Clone()

hist_signal.GetXaxis().SetTitleSize(0.00)
hist_signal.GetYaxis().SetLabelSize(0.07)
hist_signal.GetYaxis().SetTitleSize(0.08)
hist_signal.GetYaxis().SetTitleOffset(0.76)
hist_signal.GetXaxis().SetLabelSize(0.0)

hist_background.GetXaxis().SetTitleSize(0.00)
hist_background.GetYaxis().SetLabelSize(0.07)
hist_background.GetYaxis().SetTitleSize(0.08)
hist_background.GetYaxis().SetTitleOffset(0.76)
hist_background.GetXaxis().SetLabelSize(0.0)

fillHistograms(tree_signal,hist_signal)
fillHistograms(tree_background,hist_background)

hist_signal.Sumw2()
hist_background.Sumw2()

hist_signal.Scale(1/hist_signal.Integral())
hist_background.Scale(1/hist_background.Integral())

hist_signal.SetLineColor(kRed)
hist_background.SetLineColor(kBlue)

reldiffhist = hist_signal.Clone()

reldiffhist.SetTitle("")
reldiffhist.Scale(-1)
reldiffhist.Add(hist_background)
reldiffhist.Divide(hist_background)

pbottom=TPad("bottom tpad","bottom tpad",0.01,0.01,0.99,0.32)
pbottom.Draw()
pbottom.cd()
pbottom.SetTopMargin(0.03)
pbottom.SetBottomMargin(0.3)
pbottom.SetRightMargin(0.1)
pbottom.SetFillStyle(0)

reldiffhist.Draw()
reldiffhist.SetLineWidth(1)
reldiffhist.GetYaxis().SetNdivisions(5)
reldiffhist.GetXaxis().SetTitleSize(0.14)
reldiffhist.GetXaxis().SetLabelSize(0.14)
reldiffhist.GetYaxis().SetLabelSize(0.11)
reldiffhist.GetYaxis().SetTitleSize(0.14)
reldiffhist.GetYaxis().SetTitleOffset(0.28)
reldiffhist.SetMaximum(0.99)
reldiffhist.SetMinimum(-0.99)

#b={}
#
#for i in range(1,reldiffhist.GetNbinsX()+1):
#    b[i]=TBox(reldiffhist.GetBinLowEdge(i),0.1,reldiffhist.GetBinLowEdge(i+1),-0.1)
#    b[i].SetFillStyle(3001)
#    b[i].SetFillColor(kBlue)
#    b[i].SetLineColor(kBlue)
#    b[i].Draw("SAME")

c.cd()
ptop=TPad("top tpad","top tpad",0.01,0.33,0.99,0.99)
ptop.Draw()
ptop.cd()
ptop.SetTopMargin(0.1)
ptop.SetBottomMargin(0.03)
ptop.SetRightMargin(0.1)
ptop.SetFillStyle(0)

hist_background.Draw()
hist_signal.Draw("SAME")

pbottom.Update()
ptop.Update()
c.Update()

c.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/"+options.variable+".png")

raw_input()

