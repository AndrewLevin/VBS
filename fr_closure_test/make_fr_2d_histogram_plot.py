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

gPad.SetPhi( -50 )
gPad.SetTheta( 50 )

hist.SetTitle("")

#hist.Draw("colz")
hist.Draw("lego")

#v= TGLViewer  (gPad.GetViewer3D())

#fov=30
#dollyStep=2.5
#hRotateStep = 0.015
#vRotateStep = 0.025;
#center=0.5

#v.SetPerspectiveCamera(TGLViewer.ECameraType(), fov, dollyStep, center, hRotateStep,vRotateStep);

c1.SaveAs(output_file_name)

raw_input()
