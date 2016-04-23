#!/usr/bin/env python

from ROOT import *
from array import array
import sys
import time

gStyle.SetFillStyle(0)
gStyle.SetLegendBorderSize(0); 
gROOT.ForceStyle()

inputfilename_ewk="histogram_wz_ewk.root"
inputfilename_qcd="histogram_wz_qcd.root"
inputfilename_ewk_qcd="histogram_wz_ewk_qcd.root"
histname_ewk="wpwpjjewkqcd"
histname_qcd="wpwpjjewkqcd"
histname_ewk_plus_qcd="wpwpjjewkqcd"
xlabel="m_{jj} (GeV)"

f_ewk=TFile(inputfilename_ewk,"r")
f_qcd=TFile(inputfilename_qcd,"r")
f_ewk_qcd=TFile(inputfilename_ewk_qcd,"r")
hist_ewk=f_ewk.Get(histname_ewk)
hist_qcd=f_qcd.Get(histname_qcd)
hist_ewk_plus_qcd=f_ewk_qcd.Get(histname_ewk_plus_qcd)

if type(hist_ewk) != TH1F:
    print "could not find "+histname_ewk+" in file "+inputfilename_ewk
    sys.exit(1)

print type(hist_ewk)

hist_ewk.SetTitle("")
hist_qcd.SetTitle("")
hist_ewk_plus_qcd.SetTitle("")

#add the overflow bin to the last bin
#hist_ewk.SetBinContent(hist_1.GetNbinsX(), hist_1.GetBinContent(hist_1.GetNbinsX()) +hist_1.GetBinContent(hist_1.GetNbinsX()+1) )
#hist_qcd.SetBinContent(hist_2.GetNbinsX(),hist_2.GetBinContent(hist_2.GetNbinsX()) +hist_2.GetBinContent(hist_2.GetNbinsX()+1) )

#hist_ewk.SetBinContent(hist_1.GetNbinsX()+1,0)
#hist_qcd.SetBinContent(hist_2.GetNbinsX()+1,0)

hist_combined=hist_ewk.Clone()

hist_combined.Add(hist_qcd)

hist_combined.SetLineColor(kRed)
hist_ewk_plus_qcd.SetLineColor(kBlue)
hist_qcd.SetLineColor(kRed)
hist_ewk.SetLineColor(kGreen)

hist_combined.SetMarkerColor(kRed)
hist_ewk_plus_qcd.SetMarkerColor(kBlue)
hist_qcd.SetMarkerColor(kRed)
hist_ewk.SetMarkerColor(kGreen)

hist_combined.SetLineWidth(3)
hist_ewk_plus_qcd.SetLineWidth(3)
hist_ewk.SetLineWidth(3)
hist_qcd.SetLineWidth(3)

hist_combined.GetXaxis().SetTitle(xlabel)
hist_ewk_plus_qcd.GetXaxis().SetTitle(xlabel)

hist_combined.GetXaxis().SetTitleSize(0.055)
hist_ewk_plus_qcd.GetXaxis().SetTitleSize(0.055)

hist_combined.GetXaxis().SetTitleOffset(0.7);
hist_ewk_plus_qcd.GetXaxis().SetTitleOffset(0.7);

hist_combined.GetXaxis().CenterTitle()
hist_ewk_plus_qcd.GetXaxis().CenterTitle()

hist_combined.SetStats(0)
hist_ewk_plus_qcd.SetStats(0)

leg1=TLegend(.40,.65,.90,.90)

leg1.AddEntry(hist_combined,"|EWK+QCD|^2","l")
leg1.AddEntry(hist_ewk_plus_qcd,"|EWK|^2+|QCD|^2","l")
leg1.SetFillColor(0)

hist_combined.SetMinimum(0)
hist_ewk_plus_qcd.SetMinimum(0)

hist_combined.SetMaximum(1.5 * hist_combined.GetMaximum());
hist_ewk_plus_qcd.SetMaximum(1.5 * hist_ewk_plus_qcd.GetMaximum());

#c1 = TCanvas("c1", "c1",5,50,500,500);

hist_combined.Draw("SAME")
hist_ewk_plus_qcd.Draw("SAME")

leg1.Draw("SAME")

gPad.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/ewkplusqcd_ewkqcd.png");

leg2=TLegend(.60,.65,.90,.90)

leg2.AddEntry(hist_ewk_plus_qcd,"|EWK+QCD|^2","l")
leg2.AddEntry(hist_ewk,"|EWK|^2","l")
leg2.AddEntry(hist_qcd,"|QCD|^2","l")
leg2.SetFillColor(0)

hist_ewk_plus_qcd.SetMaximum(1.5 * max(max(hist_ewk_plus_qcd.GetMaximum(),hist_ewk.GetMaximum()),hist_qcd.GetMaximum()));

hist_ewk_plus_qcd.Draw()
hist_qcd.Draw("SAME")
hist_ewk.Draw("SAME")

leg2.Draw("SAME")

gPad.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/ewk_qcd_ewkqcd.png");

leg3=TLegend(.10,.65,.90,.90)

hist_combined_clone = hist_combined.Clone()

hist_ewk_plus_qcd.Scale(-1)

hist_combined.Add(hist_ewk_plus_qcd)

hist_combined.Divide(hist_combined_clone)

#hist_combined.SetMaximum(0)

leg3.AddEntry(hist_combined,"(|EWK|^2 + |QCD|^2 - |EWK+QCD|^2)/(EWK|^2 + |QCD|^2)","l")

hist_combined.Draw()

leg3.Draw()

gPad.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/ewk_qcd_interference.png");

#time.sleep(1)                                                                                                                                            
#raw_input("hit a key")
