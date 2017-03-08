#!/usr/bin/env python

from ROOT import *
from array import array
import sys
import time

gStyle.SetFillStyle(0)
gStyle.SetLegendBorderSize(0); 
gROOT.ForceStyle()

inputfilename="histograms.root"

f=TFile(inputfilename,"read")

lumi=19.365*1000

hist_ttbar=f.Get("ttbar_cut17")
hist_fake=f.Get("fake_sample0_cut17")

hist_ttbar.SetTitle("")
hist_fake.SetTitle("")

hist_ttbar.SetLineColor(kRed)
hist_fake.SetLineColor(kBlue)

hist_ttbar.SetLineWidth(3)
hist_fake.SetLineWidth(3)

hist_ttbar.GetXaxis().SetTitle("m_{jj} (GeV)")
hist_fake.GetXaxis().SetTitle("m_{jj} (GeV)")

hist_ttbar.SetStats(0)
hist_fake.SetStats(0)

leg=TLegend(.40,.65,.85,.85)

leg.AddEntry(hist_ttbar,"ttbar","l")
leg.AddEntry(hist_fake,"fake","l")
leg.SetFillColor(0)

hist_fake.Draw()
hist_ttbar.Draw("SAME")

leg.Draw("SAME")

gPad.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/mjj.png")

