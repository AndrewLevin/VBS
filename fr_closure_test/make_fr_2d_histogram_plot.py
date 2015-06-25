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

hist.Draw("colz")

#gPad.SetPhi( -50 )
#gPad.SetTheta( 50 )
#hist.Draw("lego")


c1.SaveAs(output_file_name)

raw_input()
