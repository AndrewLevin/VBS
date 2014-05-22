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

inputfilename=sys.argv[1]
norm=int(sys.argv[2])
xs1=float(sys.argv[3])
xs2=float(sys.argv[4])
nevents1=float(sys.argv[5])
nevents2=float(sys.argv[6])
histname1=sys.argv[7]
histname2=sys.argv[8]
xlabel=sys.argv[9]
label1=sys.argv[10]
label2=sys.argv[11]
outputfilename=sys.argv[12]

lumi=19.365

f=TFile(inputfilename,"r")
hist_1=f.Get(histname1)
hist_2=f.Get(histname2)

hist_1.SetTitle("")
hist_2.SetTitle("")

#add the overflow bin to the last bin
hist_1.SetBinContent(hist_1.GetNbinsX(), hist_1.GetBinContent(hist_1.GetNbinsX()) +hist_1.GetBinContent(hist_1.GetNbinsX()+1) )
hist_2.SetBinContent(hist_2.GetNbinsX(),hist_2.GetBinContent(hist_2.GetNbinsX()) +hist_2.GetBinContent(hist_2.GetNbinsX()+1) )

hist_1.SetBinContent(hist_1.GetNbinsX()+1,0)
hist_2.SetBinContent(hist_2.GetNbinsX()+1,0)

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

hist_1.SetStats(0)
hist_2.SetStats(0)

leg=TLegend(.40,.45,.95,.95)

leg.AddEntry(hist_1,label1,"l")
leg.AddEntry(hist_2,label2,"l")
leg.SetFillColor(0)

hist_2.Draw()
hist_1.Draw("SAME")
leg.Draw("SAME")

gPad.SaveAs(outputfilename);

#time.sleep(1)                                                                                                                                            
#raw_input("hit a key")
