import style

import optparse

parser = optparse.OptionParser()

parser.add_option('--lumi',dest='lumi')
parser.add_option('--variable',dest='variable')
parser.add_option('--xaxislabel',dest='xaxislabel',default='m_{jj}')

parser.add_option('-i',dest='inputfile')
parser.add_option('-o',dest='outputfile',default="/afs/cern.ch/user/a/anlevin/www/tmp/plot.png")

(options,args) = parser.parse_args()

from ROOT import *

xoffsetstart = 0.0;
yoffsetstart = 0.0;
xoffset = 0.20;
yoffset = 0.05;

xpositions = [0.60,0.60,0.60,0.60,0.60,0.60,0.40,0.40,0.40]
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

hist_file = TFile.Open(str(options.inputfile))

gROOT.cd()

c1 = TCanvas("c1", "c1",5,50,500,500);

#variable = "mjj"

#data = hist_file.Get("data").Clone()
fake = hist_file.Get("fake_"+options.variable).Clone()
zjets = hist_file.Get("zjets_"+options.variable).Clone()
wpwpjjewk = hist_file.Get("signal_"+options.variable).Clone()
wpwpjjqcd = hist_file.Get("wpwpjjqcd_"+options.variable).Clone()
#ttbar = hist_file.Get("ttbar").Clone()
wjwjdps = hist_file.Get("wjwjdps_"+options.variable).Clone()
wzjjewk = hist_file.Get("wz_"+options.variable).Clone()
#wzjjqcd = hist_file.Get("wzjjqcd").Clone()
wgjets = hist_file.Get("wgamma_"+options.variable).Clone()

#data.SetLineColor(kBlack)
fake.SetLineColor(kMagenta)
zjets.SetLineColor(kBlue+1)
wpwpjjqcd.SetLineColor(kYellow)
wpwpjjewk.SetLineColor(kOrange)
#ttbar.SetLineColor(kGreen+2)
wjwjdps.SetLineColor(kAzure-2)
wzjjewk.SetLineColor(kRed)
#zjjqcd.SetLineColor(kRed)
wgjets.SetLineColor(kGreen+2)

fake.SetFillStyle(1001)
zjets.SetFillStyle(1001)
wpwpjjqcd.SetFillStyle(1001)
wpwpjjewk.SetFillStyle(1001)
#ttbar.SetFillStyle(1001)
wjwjdps.SetFillStyle(1001)
wgjets.SetFillStyle(1001)
wzjjewk.SetFillStyle(1001)
#wzjjqcd.SetFillStyle(1001)

fake.SetFillColor(kMagenta)
zjets.SetFillColor(kBlue+1)
wpwpjjqcd.SetFillColor(kYellow)
wpwpjjewk.SetFillColor(kOrange)
#ttbar.SetFillColor(kGreen+2)
wjwjdps.SetFillColor(kAzure-2)
wzjjewk.SetFillColor(kRed)
#wzjjqcd.SetFillColor(kRed)
wgjets.SetFillColor(kGreen+2)

#data.SetMarkerStyle(kFullCircle);

wpwpjjqcd.SetLineWidth(3)
wpwpjjewk.SetLineWidth(3)

hstack = THStack()
hsum = fake.Clone()
hsum.Scale(0.0)

hstack.Add(fake)
hstack.Add(zjets)
hstack.Add(wpwpjjqcd)
hstack.Add(wjwjdps)
#hstack.Add(ttbar)
hstack.Add(wzjjewk)
#hstack.Add(wzjjqcd)
hstack.Add(wgjets)
hstack.Add(wpwpjjewk)

hsum.Add(fake)
hsum.Add(zjets)
hsum.Add(wpwpjjqcd)

hsum.Add(wjwjdps)
#hsum.Add(ttbar)
hsum.Add(wzjjewk)
#hsum.Add(wzjjqcd)
hsum.Add(wgjets)
hsum.Add(wpwpjjewk)

ymax = hsum.GetMaximum()

hstack.SetMaximum(1.55 * ymax)

hstack.Draw()

s=str(options.lumi)+" fb^{-1} (13 TeV)"
lumilabel = TLatex (0.95, 0.93, s)
lumilabel.SetNDC ()
lumilabel.SetTextAlign (30)
lumilabel.SetTextFont (42)
lumilabel.SetTextSize (0.040)

hstack.Draw("hist")

#cmslabel = TLatex (0.18, 0.93, "#bf{CMS} (Unpublished)")
cmslabel = TLatex (0.18, 0.93, "")
cmslabel.SetNDC ()
cmslabel.SetTextAlign (10)
cmslabel.SetTextFont (42)
cmslabel.SetTextSize (0.040)
cmslabel.Draw ("same") 

lumilabel.Draw("same")

#wpwpjjewk.Draw("same")

j=0
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,fake,"fake","f")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,zjets,"Z+jets","f")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wzjjewk,"WZ+jets","f")
#j=j+1
#draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wzjjqcd,"WZ+jets","f")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wpwpjjqcd,"WWJJ QCD","f")


j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wgjets,"WGJJ","f")
j=j+1
draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,wpwpjjewk,"WWJJ","f")
#j=j+1
#draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,data,"data","lp")

#data.Draw("same")

#set_axis_fonts(hstack,"x","m_{ll} (GeV)")
#set_axis_fonts(hstack,"x","|\Delta \eta_{jj}|")
set_axis_fonts(hstack,"x",options.xaxislabel)
#set_axis_fonts(hstack,"x","pt_{l}^{max} (GeV)")
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

c1.SaveAs(options.outputfile)
