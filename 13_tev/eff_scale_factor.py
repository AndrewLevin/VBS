from ROOT import *

#from https://twiki.cern.ch/twiki/bin/view/CMS/EgammaIDRecipesRun2#Efficiencies_and_scale_factors and https://twiki.cern.ch/twiki/bin/view/CMS/MuonWorkInProgressAndPagResults

electron_id_sf_filename = "egammaEffi.txt_EGM2D.root.id"

electron_id_sf_file = TFile(electron_id_sf_filename,"read")

electron_id_sf = electron_id_sf_file.Get("EGamma_SF2D")

electron_reco_sf_filename = "egammaEffi.txt_EGM2D.root.reco"

electron_reco_sf_file = TFile(electron_reco_sf_filename,"read")

electron_reco_sf = electron_reco_sf_file.Get("EGamma_SF2D")

muon_iso_sf_filename = "EfficienciesAndSF_GH.root.iso"

muon_iso_sf_file = TFile(muon_iso_sf_filename,"read")

muon_iso_sf_file.cd("TightISO_TightID_pt_eta")

muon_iso_sf = muon_iso_sf_file.Get("TightISO_TightID_pt_eta/abseta_pt_ratio")

muon_id_sf_filename = "EfficienciesAndSF_GH.root.id"

muon_id_sf_file = TFile(muon_id_sf_filename,"read")

muon_id_sf_file.cd("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta")

muon_id_sf = muon_id_sf_file.Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio")


def electron_efficiency_scale_factor(pt,eta):
    #the reoc 2D histogram is really a 1D histogram
    return electron_id_sf.GetBinContent(electron_id_sf.GetXaxis().FindFixBin(eta),electron_id_sf.GetYaxis().FindFixBin(pt))* electron_reco_sf.GetBinContent(electron_reco_sf.GetXaxis().FindFixBin(eta),1)

def muon_efficiency_scale_factor(pt,eta):
    return muon_iso_sf.GetBinContent(muon_iso_sf.GetXaxis().FindFixBin(abs(eta)),muon_iso_sf.GetYaxis().FindFixBin(pt))*muon_id_sf.GetBinContent(muon_id_sf.GetXaxis().FindFixBin(abs(eta)),muon_id_sf.GetYaxis().FindFixBin(pt))

#print electron_efficiency_scale_factor(25,0.7)
