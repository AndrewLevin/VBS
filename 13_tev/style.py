from ROOT import *

def GoodStyle():
    GoodStyle = TStyle("GoodStyle", "GoodStyle");
    
    ##----------------------------------------------------------------------------
    ## Canvas
    ##----------------------------------------------------------------------------
    GoodStyle.SetCanvasBorderMode(  0);
    GoodStyle.SetCanvasBorderSize( 10);
    GoodStyle.SetCanvasColor     (  0);
    GoodStyle.SetCanvasDefH      (600);
    GoodStyle.SetCanvasDefW      (550);
    GoodStyle.SetCanvasDefX      ( 10);
    GoodStyle.SetCanvasDefY      ( 10);
    
    
    ##----------------------------------------------------------------------------
    ## Pad
    ##----------------------------------------------------------------------------
    GoodStyle.SetPadBorderMode  (   0);
    GoodStyle.SetPadBorderSize  (  10);
    GoodStyle.SetPadColor       (   0);
    GoodStyle.SetPadBottomMargin(0.20);
    GoodStyle.SetPadTopMargin   (0.08);
    GoodStyle.SetPadLeftMargin  (0.18);
    GoodStyle.SetPadRightMargin (0.05);
    
    
    ##----------------------------------------------------------------------------
    ## Frame
    ##----------------------------------------------------------------------------
    GoodStyle.SetFrameFillStyle ( 0);
    GoodStyle.SetFrameFillColor ( 0);
    GoodStyle.SetFrameLineColor ( 1);
    GoodStyle.SetFrameLineStyle ( 0);
    GoodStyle.SetFrameLineWidth ( 2);
    GoodStyle.SetFrameBorderMode( 0);
    GoodStyle.SetFrameBorderSize(10);
    
    
    ##----------------------------------------------------------------------------
    ## Hist
    ##---------------------------------------------------------------------------
    GoodStyle.SetHistFillColor(0);
    GoodStyle.SetHistFillStyle(1);
    GoodStyle.SetHistLineColor(1);
    GoodStyle.SetHistLineStyle(0);
    GoodStyle.SetHistLineWidth(1);
    
    
    ##----------------------------------------------------------------------------
    ## Axis
    ##----------------------------------------------------------------------------
    GoodStyle.SetLabelFont  (   42, "xyz");
    GoodStyle.SetLabelOffset(0.015, "xyz");
    GoodStyle.SetLabelSize  (0.050, "xyz");
    GoodStyle.SetNdivisions (  505, "xyz");
    GoodStyle.SetTitleFont  (   42, "xyz");
    GoodStyle.SetTitleSize  (0.050, "xyz");
    
    ##  GoodStyle->SetNdivisions ( -503, "y");
    
    GoodStyle.SetTitleOffset(  1.4,   "x");
    GoodStyle.SetTitleOffset(  1.2,   "y");
    GoodStyle.SetPadTickX   (           1);  ## Tick marks on the opposite side of the frame
    GoodStyle.SetPadTickY   (           1);  ## Tick marks on the opposite side of the frame
    
    
    ##----------------------------------------------------------------------------
    ## Title
    ##----------------------------------------------------------------------------
    GoodStyle.SetTitleBorderSize(    0);
    GoodStyle.SetTitleFillColor (   10);
    GoodStyle.SetTitleAlign     (   12);
    GoodStyle.SetTitleFontSize  (0.045);
    GoodStyle.SetTitleX         (0.560);
    GoodStyle.SetTitleY         (0.860);
    
    GoodStyle.SetTitleFont(42, "");
    
    
    ##----------------------------------------------------------------------------
    ## Stat
    ##----------------------------------------------------------------------------
    GoodStyle.SetOptStat       (1110);
    GoodStyle.SetStatBorderSize(   0);
    GoodStyle.SetStatColor     (  10);
    GoodStyle.SetStatFont      (  42);
    GoodStyle.SetStatX         (0.94);
    GoodStyle.SetStatY         (0.91);

    return GoodStyle
