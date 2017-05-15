from ROOT import *
import sys


if len(sys.argv) != 4:
    print "len(sys.argv) != 4, exiting"
    sys.exit(0)

f=TFile(sys.argv[1],"r")
hist_name=sys.argv[2]
output_file_name=sys.argv[3]

hist=f.Get(hist_name)

c1=TCanvas("c1")

hist.SetTitle("")

gStyle.SetPaintTextFormat("4.2f")

hist.GetYaxis().SetTitle("p_{T} (GeV)")
hist.GetXaxis().SetTitle("|\eta|")

#hist.Draw("colz")
hist.Draw("texte colz")

#hist.Draw("legoe")

#gPad.SetPhi( -50 )
#gPad.SetTheta( 50 )
#hist.Draw("lego")


c1.SaveAs(output_file_name)

#raw_input()
