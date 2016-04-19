
from ROOT import *

fin = TFile("distributions_electrons_v8.root","read")

mc_met = fin.Get("electron_mc_mt")
data_met = fin.Get("electron_data_mt")

c = TCanvas()

mc_met.SetTitle("")
data_met.SetTitle("")

mc_met.GetXaxis().SetTitle("MET (GeV)")
data_met.GetXaxis().SetTitle("MET (GeV)")

mc_met.SetLineColor(kRed)
data_met.SetLineColor(kBlue)

mc_met.SetLineWidth(2)
data_met.SetLineWidth(2)

data_met.Draw()
mc_met.Draw("same")

leg=TLegend(.60,.65,.85,.85)
leg.AddEntry(mc_met,"W+jets MC","l")
leg.AddEntry(data_met,"data","l")

leg.Draw("same")


c.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/wjets_normalization_check_electrons.png")
