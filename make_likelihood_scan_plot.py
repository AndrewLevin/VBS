from ROOT import *

gStyle.SetCanvasBorderSize( 10)
gStyle.SetCanvasDefX      ( 10)
gStyle.SetCanvasDefY      ( 10)
gStyle.SetCanvasDefH(600)
gStyle.SetCanvasDefH(550)

gStyle.SetFrameBorderSize(10)

gStyle.SetLabelOffset(0.015, "xyz")
gStyle.SetLabelSize  (0.050, "xyz")
gStyle.SetTitleOffset(  1.4,   "x")
gStyle.SetTitleOffset(  1.2,   "y")
gStyle.SetTitleSize  (0.050, "xyz")
gStyle.SetTitleFont  (   42, "xyz")


gStyle.SetPadBorderMode  (   0)
gStyle.SetPadBorderSize  (  10)
gStyle.SetPadBottomMargin(0.20)
gStyle.SetPadTopMargin   (0.08)
gStyle.SetPadLeftMargin  (0.18)
gStyle.SetPadRightMargin (0.05)

f = TFile("/afs/cern.ch/work/a/anlevin/tmp/higgsCombineTest.MultiDimFit.mH125.root","r")

t = f.Get("limit")

t.Draw("deltaNLL:r>>p","","prof")

p.SetStats(0)

p.SetTitle("")

p.SetLineWidth(3)

p.GetXaxis().SetTitle("\sigma_{W^{\pm} W^{\pm} jj}")
p.GetYaxis().SetTitle("\Delta NLL")

leg=TLegend(0.7,0.7,0.9,0.9)
leg.AddEntry(p,"expected","l")

p.Draw("hist l")

leg.Draw("same")

gPad.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/likelihood_scan.png")
