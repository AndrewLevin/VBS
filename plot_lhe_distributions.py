#!/usr/bin/env python

from ROOT import *
from array import array
import sys
import time

gStyle.SetFillStyle(0)
gStyle.SetLegendBorderSize(0); 
gROOT.ForceStyle()

#xs1=0.008797
#xs2=0.0113
#nevents1=10000
#nevents2=10000

inputfilename1=sys.argv[1]
inputfilename2=sys.argv[2]
norm=int(sys.argv[3])
xs1=float(sys.argv[4])
xs2=float(sys.argv[5])
nevents1=float(sys.argv[6])
nevents2=float(sys.argv[7])
histname1=sys.argv[8]
histname2=sys.argv[9]
xlabel=sys.argv[10]
label1=sys.argv[11]
label2=sys.argv[12]
outputfilename=sys.argv[13]
logscale=bool(int(sys.argv[14]))

#lumi=19.365
lumi=3000.

f1=TFile(inputfilename1,"r")
f2=TFile(inputfilename2,"r")
hist_1=f1.Get(histname1)
hist_2=f2.Get(histname2)

hist_1.SetTitle("")
hist_2.SetTitle("")

#add the overflow bin to the last bin
#hist_1.SetBinContent(hist_1.GetNbinsX(), hist_1.GetBinContent(hist_1.GetNbinsX()) +hist_1.GetBinContent(hist_1.GetNbinsX()+1) )
#hist_2.SetBinContent(hist_2.GetNbinsX(),hist_2.GetBinContent(hist_2.GetNbinsX()) +hist_2.GetBinContent(hist_2.GetNbinsX()+1) )

#hist_1.SetBinContent(hist_1.GetNbinsX()+1,0)
#hist_2.SetBinContent(hist_2.GetNbinsX()+1,0)

if norm:
    hist_1.Scale(1/hist_1.Integral())
    hist_2.Scale(1/hist_2.Integral())
else:
    hist_1.Scale(lumi*xs1/nevents1)
    hist_2.Scale(lumi*xs2/nevents2)
hist_1.SetLineColor(kRed)
hist_2.SetLineColor(kBlue)
hist_1.SetLineWidth(3)
hist_2.SetLineWidth(3)

hist_1.GetXaxis().SetTitle(xlabel)
hist_2.GetXaxis().SetTitle(xlabel)

hist_1.GetXaxis().SetTitleSize(0.055)
hist_2.GetXaxis().SetTitleSize(0.055)

hist_1.GetXaxis().SetTitleOffset(0.7);
hist_2.GetXaxis().SetTitleOffset(0.7);

hist_1.GetXaxis().CenterTitle()
hist_2.GetXaxis().CenterTitle()

hist_1.SetMaximum(1.15 * hist_1.GetMaximum());
hist_2.SetMaximum(1.15 * hist_1.GetMaximum());

hist_1.SetStats(0)
hist_2.SetStats(0)

leg=TLegend(.50,.65,.75,.85)
#leg=TLegend()

leg.AddEntry(hist_1,label1,"l")
leg.AddEntry(hist_2,label2,"l")
leg.SetFillColor(0)

c1 = TCanvas()

if logscale:
    c1.SetLogy()

hist_2.Draw()
hist_1.Draw("SAME")
leg.Draw("SAME")

gPad.SaveAs(outputfilename);

#time.sleep(1)                                                                                                                                            
#raw_input("hit a key")
