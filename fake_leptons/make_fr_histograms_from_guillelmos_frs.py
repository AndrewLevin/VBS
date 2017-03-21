from ROOT import *

from array import array

guillelmo_electron_frs="0.360,0.354,0.331,0.277,0.258,0.245,0.317,0.378,0.314,0.279,0.263,0.243,0.352,0.384,0.318,0.290,0.262,0.236,0.366,0.298,0.264,0.230,0.198,0.162,0.221,0.176,0.150,0.117,0.100,0.084"

#guillelmo_electron_frs="0.479,0.398,0.355,0.305,0.231,0.464,0.428,0.350,0.271,0.235,0.476,0.436,0.367,0.310,0.270,0.433,0.358,0.336,0.289,0.224,0.302,0.246,0.206,0.164,0.106"

guillelmo_muon_frs="0.305,0.269,0.260,0.242,0.217,0.214,0.320,0.283,0.269,0.257,0.239,0.237,0.363,0.332,0.319,0.298,0.284,0.261,0.408,0.386,0.381,0.363,0.344,0.319,0.432,0.421,0.418,0.409,0.386,0.346"

#guillelmo_muon_frs = "0.328,0.273,0.261,0.227,0.170,0.343,0.285,0.272,0.244,0.216,0.384,0.334,0.317,0.291,0.245,0.428,0.388,0.378,0.362,0.294,0.456,0.424,0.418,0.409,0.330"

#guillelmo_electron_frs="0.476,0.436,0.367,0.310,0.270,0.433,0.358,0.336,0.289,0.224,0.302,0.246,0.206,0.164,0.106"
#guillelmo_muon_frs="0.384,0.334,0.317,0.291,0.245,0.428,0.388,0.378,0.362,0.294,0.456,0.424,0.418,0.409,0.330"

muon_ptbins=array('d', [20,25,30,40,50])
muon_etabins=array('d', [0,0.5,1,1.5,2.0,2.5])

electron_ptbins=array('d', [20,25,30,40,50])
electron_etabins=array('d', [0,0.5,1,1.5,2.0,2.5])

muon_frs=TH2F("muon_frs","muon_frs",len(muon_etabins)-1,muon_etabins,len(muon_ptbins)-1,muon_ptbins)
electron_frs=TH2F("electron_frs","electron_frs",len(electron_etabins)-1,electron_etabins,len(electron_ptbins)-1,electron_ptbins)

i=1
j=1
for fr in guillelmo_muon_frs.split(","):
    if j > 2:
        muon_frs.SetBinContent(i,j-2,(float(fr)))
    i=i+1
    if i == 6:
        i=1
        j=j+1

muon_frs.Print("all")

i=1
j=1
for fr in guillelmo_electron_frs.split(","):
    if j > 2:
        electron_frs.SetBinContent(i,j-2,(float(fr)))
    i=i+1
    if i == 6:
        i=1
        j=j+1

electron_frs.Print("all")

f=TFile("frs_guillelmo_v5.root","recreate")

muon_frs.SetStats(0)
electron_frs.SetStats(0)

muon_frs.Write()
electron_frs.Write()
