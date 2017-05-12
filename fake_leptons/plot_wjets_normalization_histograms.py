from ROOT import *

fin = TFile("distributions_electrons_v50.root","read")

muon_or_electron="electron"

prescale_rate = 0.0005

mc_met = fin.Get(muon_or_electron+"_mc_met")
data_met = fin.Get(muon_or_electron+"_data_met")

c = TCanvas()

mc_met.SetTitle("")
data_met.SetTitle("")

mc_met.GetXaxis().SetTitle("MET (GeV)")
data_met.GetXaxis().SetTitle("MET (GeV)")


mc_met.SetLineWidth(2)
data_met.SetLineWidth(2)

data_met.Draw()

c.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/wjets_normalization_check_"+muon_or_electron+"s_data.png")

mc_met.Draw()

c.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/wjets_normalization_check_"+muon_or_electron+"s_mc.png")

mc_met.Scale(prescale_rate)

mc_met.SetLineColor(kRed)
data_met.SetLineColor(kBlue)

data_met.Draw()
mc_met.Draw("same")

leg=TLegend(.60,.65,.85,.85)
leg.AddEntry(mc_met,"W+jets MC","l")
leg.AddEntry(data_met,"data","l")

leg.Draw("same")

c.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/wjets_normalization_check_"+muon_or_electron+"s.png")
