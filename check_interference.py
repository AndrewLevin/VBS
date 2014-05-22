#!/usr/bin/env python

from ROOT import *
from array import array
import sys
import time

gStyle.SetFillStyle(0)
gStyle.SetLegendBorderSize(0); 
gROOT.ForceStyle()

inputfilename=sys.argv[1]
xs_ewk=float(sys.argv[2])
xs_qcd=float(sys.argv[3])
xs_ewk_plus_qcd=float(sys.argv[4])
nevents_ewk=float(sys.argv[5])
nevents_qcd=float(sys.argv[6])
nevents_ewk_plus_qcd=float(sys.argv[7])
histname_ewk=sys.argv[8]
histname_qcd=sys.argv[9]
histname_ewk_plus_qcd=sys.argv[10]
xlabel=sys.argv[11]
label_combined=sys.argv[12]
label_ewk_plus_qcd=sys.argv[13]
outputfilename=sys.argv[14]

lumi=19.365*1000

f=TFile(inputfilename,"r")
hist_ewk=f.Get(histname_ewk)
hist_qcd=f.Get(histname_qcd)
hist_ewk_plus_qcd=f.Get(histname_ewk_plus_qcd)

if type(hist_ewk) != TH1F:
    print "could not find "+histname_ewk+" in file "+inputfilename
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


hist_ewk.Scale(lumi*xs_ewk/nevents_ewk)
hist_qcd.Scale(lumi*xs_qcd/nevents_qcd)
hist_ewk_plus_qcd.Scale(lumi*xs_ewk_plus_qcd/nevents_ewk_plus_qcd)


hist_combined=hist_ewk.Clone()

hist_combined.Add(hist_qcd)

hist_combined.SetLineColor(kRed)
hist_ewk_plus_qcd.SetLineColor(kBlue)
hist_combined.SetLineWidth(3)
hist_ewk_plus_qcd.SetLineWidth(3)

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

leg=TLegend(.40,.65,.85,.85)

leg.AddEntry(hist_combined,label_combined,"l")
leg.AddEntry(hist_ewk_plus_qcd,label_ewk_plus_qcd,"l")
leg.SetFillColor(0)

hist_combined.Draw()
hist_ewk_plus_qcd.Draw("SAME")


leg.Draw("SAME")

gPad.SaveAs(outputfilename);

#time.sleep(1)                                                                                                                                            
#raw_input("hit a key")
