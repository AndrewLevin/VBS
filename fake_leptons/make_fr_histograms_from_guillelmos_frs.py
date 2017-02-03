from ROOT import *

from array import array

guillelmo_electron_frs="0.476,0.436,0.367,0.310,0.270,0.433,0.358,0.336,0.289,0.224,0.302,0.246,0.206,0.164,0.106"
guillelmo_muon_frs="0.384,0.334,0.317,0.291,0.245,0.428,0.388,0.378,0.362,0.294,0.456,0.424,0.418,0.409,0.330"

muon_ptbins=array('d', [20,25,30,35])
muon_etabins=array('d', [0,0.5,1,1.5,2.0,2.5])

electron_ptbins=array('d', [20,25,30,35])
electron_etabins=array('d', [0,0.5,1,1.5,2.0,2.5])

muon_frs=TH2F("muon_frs","muon_frs",len(muon_etabins)-1,muon_etabins,len(muon_ptbins)-1,muon_ptbins)
electron_frs=TH2F("electron_frs","electron_frs",len(electron_etabins)-1,electron_etabins,len(electron_ptbins)-1,electron_ptbins)

i=1
j=1
for fr in guillelmo_muon_frs.split(","):
    muon_frs.SetBinContent(i,j,(float(fr)))
    i=i+1
    if i == len(muon_etabins):
        i=1
        j=j+1

muon_frs.Print("all")

i=1
j=1
for fr in guillelmo_electron_frs.split(","):
    electron_frs.SetBinContent(i,j,(float(fr)))
    i=i+1
    if i == len(electron_etabins):
        i=1
        j=j+1

electron_frs.Print("all")

f=TFile("frs_guillelmo_v1.root","recreate")

muon_frs.Write()
electron_frs.Write()