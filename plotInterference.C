
#include "TROOT.h"
#include "TSystem.h"
#include "TInterpreter.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TStyle.h"
#include "TPad.h"
#include "Math/QuantFuncMathCore.h"
#include "TMath.h"
#include "TGraphAsymmErrors.h"
#include "StandardPlotVBS.C"

 //.x finalPlotVBS.C+(0,1,"m_{jj} (GeV)","GeV","histo_nice8TeV.root","wwss_mjj",0,19.4)


void plotInterference(){

  gStyle->SetFillStyle(0);
  gStyle->SetLegendBorderSize(0); 
gROOT->ForceStyle();


  TFile* file_ewk = new TFile("histo_nice8TeV_ewk_wz.root", "read");
  TFile* file_qcd = new TFile("histo_nice8TeV_qcd_wz.root", "read");
  TFile* file_ewk_plus_qcd = new TFile("histo_nice8TeV_ewk_plus_qcd_wz.root", "read");

  TH1F* hSignalEwk = (TH1F*)file_ewk->Get("histo1");
  TH1F* hSignalQCD = (TH1F*)file_qcd->Get("histo1");
  TH1F* hSignalEwkPlusQCD = (TH1F*)file_ewk_plus_qcd->Get("histo1");

  //TCanvas* c2 = new TCanvas("c2", "c2",700,50,500,500);
  //c2->cd(1);

  TH1F * hSum= (TH1F*)hSignalEwk->Clone();
  hSum->Add(hSignalQCD);

  TLegend* legend = new TLegend(0.5,0.74,0.8,0.9);
  legend->AddEntry(hSum,"sum of EWK and QCD");
  legend->AddEntry(hSignalEwkPlusQCD,"EWK and QCD with interference");

  legend->SetBorderSize(     0);                                                                                                                            
  legend->SetFillColor (     0);                                                                                                                            
  legend->SetTextAlign (    12);                                                                                                                            
  legend->SetTextFont  (    42);                                                                                                                            
  legend->SetTextSize(0.03);

  hSum->SetLineWidth(3);
  hSignalEwkPlusQCD->SetLineWidth(3);
  hSum->SetStats(0);

  hSum->SetTitle("");
  hSum->SetLineColor(kRed);

  hSum->Draw("e");
  hSum->GetYaxis()->SetRangeUser(0,1);  
  hSum->GetXaxis()->SetTitle("m_{jj} (GeV)}");

  hSignalEwkPlusQCD->Draw("eSAME");
  legend->Draw("SAME");
}
