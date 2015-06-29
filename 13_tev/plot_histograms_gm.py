import style

from ROOT import *

xoffsetstart = 0.0;
yoffsetstart = 0.0;
xoffset = 0.20;
yoffset = 0.05;

xpositions = [0.65,0.65,0.65,0.65,0.65,0.65,0.40,0.40,0.40]
ypositions = [0,1,2,3,4,5,0,1,2]

style.GoodStyle().cd()

def set_axis_fonts(thstack, coordinate, title):

    if coordinate == "x":
        axis = thstack.GetHistogram().GetXaxis();
    elif coordinate == "y":
        axis = thstack.GetHistogram().GetYaxis();
    else:
        assert(0)
    
    axis.SetLabelFont  (   42)
    axis.SetLabelOffset(0.015)
    axis.SetLabelSize  (0.050)
    axis.SetNdivisions (  505)
    axis.SetTitleFont  (   42)
    axis.SetTitleOffset(  1.5)
    axis.SetTitleSize  (0.050)
    if (coordinate == "y"):
        axis.SetTitleOffset(1.6)
    axis.SetTitle(title)    



def draw_legend(x1,y1,hist,label,options):

    legend = TLegend(x1+xoffsetstart,y1+yoffsetstart,x1+xoffsetstart + xoffset,y1+yoffsetstart + yoffset)

    legend.SetBorderSize(     0)
    legend.SetFillColor (     0)
    legend.SetTextAlign (    12)
    legend.SetTextFont  (    42)
    legend.SetTextSize  ( 0.040)

    legend.AddEntry(hist,label,options)

    legend.Draw("same")

    #otherwise the legend goes out of scope and is deleted once the function finishes
    hist.label = legend

hist_file = TFile.Open("histograms.root")

gROOT.cd()

c1 = TCanvas("c1", "c1",5,50,500,500);

wpwpjjqcd = hist_file.Get("mjj;1").Clone()
wpwpjjewk = hist_file.Get("mjj;2").Clone()
ttbar = hist_file.Get("mjj;3").Clone()
gm = hist_file.Get("mjj;4").Clone()

wpwpjjqcd.SetLineColor(kMagenta)
wpwpjjewk.SetLineColor(kBlue+1)
ttbar.SetLineColor(kGreen+2)
gm.SetLineColor(kAzure-9)

wpwpjjqcd.SetFillStyle(1001)
wpwpjjewk.SetFillStyle(1001)
ttbar.SetFillStyle(1001)
gm.SetFillStyle(1001)

wpwpjjqcd.SetFillColor(kMagenta)
wpwpjjewk.SetFillColor(kBlue+1)
ttbar.SetFillColor(kGreen+2)
gm.SetFillColor(kAzure-9)

gm.SetLineWidth(3)

hstack = THStack()
hsum = wpwpjjqcd.Clone()
hsum.Scale(0.0)

hstack.Add(wpwpjjqcd)
hstack.Add(wpwpjjewk)
hstack.Add(ttbar)

hsum.Add(wpwpjjqcd)
hsum.Add(wpwpjjewk)
hsum.Add(ttbar)

ymax = max(hstack.GetMaximum(),gm.GetMaximum())

hstack.SetMaximum(1.55 * ymax)

hstack.Draw()


s="10 fb^{-1} (13 TeV)"
lumilabel = TLatex (0.95, 0.93, s)
lumilabel.SetNDC ()
lumilabel.SetTextAlign (30)
lumilabel.SetTextFont (42)
lumilabel.SetTextSize (0.040)

hstack.Draw("hist")

cmslabel = TLatex (0.18, 0.93, "#bf{CMS} (Unpublished)")
cmslabel.SetNDC ()
cmslabel.SetTextAlign (10)
cmslabel.SetTextFont (42)
cmslabel.SetTextSize (0.040)
cmslabel.Draw ("same") 

lumilabel.Draw("same")

gm.Draw("same")

j=0
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wpwpjjewk,"wpwpwjj ewk","f")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wpwpjjqcd,"wpwpwjj qcd","f")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,ttbar,"ttbar","f")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,gm,"gm","l")

set_axis_fonts(hstack,"x","m_{jj} (GeV)")
set_axis_fonts(hstack,"y","Events / bin")

hstack.GetHistogram().LabelsOption("v");

gstat = TGraphAsymmErrors(hsum);
for i in range(0,gstat.GetN()):

    gstat.SetPointEYlow (i, hsum.GetBinError(i+1));
    gstat.SetPointEYhigh(i, hsum.GetBinError(i+1));

gstat.SetFillColor(12);
gstat.SetFillStyle(3345);
gstat.SetMarkerSize(0);
gstat.SetLineWidth(0);
gstat.SetLineColor(kWhite);
gstat.Draw("E2same");

c1.Update()
c1.ForceUpdate()

c1.SaveAs("/afs/cern.ch/user/a/anlevin/www/tmp/mjj.png")

