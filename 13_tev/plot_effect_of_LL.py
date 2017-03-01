#!/usr/bin/env python

from ROOT import *
from array import array
import sys
import time

gStyle.SetFillStyle(0)
gStyle.SetLegendBorderSize(0); 
gROOT.ForceStyle()

inputfilename1="histograms_2016.root.nofailfail"
inputfilename2="histograms_2016.root.failfail"

f1=TFile(inputfilename1,"read")
f2=TFile(inputfilename2,"read")

hist_fake1=f1.Get("fake")
hist_fake2=f2.Get("fake")

hist_fake1.SetTitle("")
hist_fake2.SetTitle("")

hist_fake1.SetLineColor(kRed)
hist_fake2.SetLineColor(kBlue)

hist_fake1.SetLineWidth(3)
hist_fake2.SetLineWidth(3)

hist_fake1.GetXaxis().SetTitle("m_{jj} (GeV)")
hist_fake2.GetXaxis().SetTitle("m_{jj} (GeV)")

hist_fake1.SetStats(0)
hist_fake2.SetStats(0)

leg=TLegend(.40,.65,.85,.85)

leg.AddEntry(hist_fake1,"fake, estimated using only TL","l")
leg.AddEntry(hist_fake2,"fake, estimated using TL and LL events","l")
leg.SetFillColor(0)

hist_fake1.Draw()
hist_fake2.Draw("SAME")

leg.Draw("SAME")

gPad.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/mjj.png")

