// #include "TH1F.h"
// #include <iostream>
// #include "ExRootAnalysis/ExRootClasses.h"
// #include "ExRootAnalysis/ExRootTreeReader.h"
// #include "TClonesArray.h"
// #include "TStyle.h"
// #include "TLorentzVector.h"
// #include "TLegend.h"
// #include "TChain.h"
// #include "TSystem.h"


float luminosity = 19.4 * 1000;

const float muon_mass = 0.000106;
const float electron_mass = 0.000511;

void fillHistogram(TH1F * hist, std::string filename, float xs){


  hist->Sumw2();

  //see https://answers.launchpad.net/mg5amcnlo/+question/200336
  int n_events_nonzero_met = 0;

    // Load shared library
  gSystem->Load("lib/libExRootAnalysis.so");
  gSystem->Load("libPhysics");

  // Create chain of root trees
  TChain chain("LHCO");
  //chain.Add("/scratch3/anlevin/MG5_aMC_v2_0_0/ww_qed_4_qcd_99_pythia_matching/Events/run_01/tag_1_pgs_events.root");
  chain.Add(filename.c_str());
  
  // Create object of class ExRootTreeReader
  ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
  Long64_t numberOfEntries = treeReader->GetEntries();
  
  // Get pointers to branches used in this analysis
  TClonesArray *branchJet = treeReader->UseBranch("Jet");
  TClonesArray *branchElectron = treeReader->UseBranch("Electron");
  TClonesArray *branchMuon = treeReader->UseBranch("Muon");
  TClonesArray *branchMET = treeReader->UseBranch("MissingET");

  
  // Loop over all events
  for(Int_t entry = 0; entry < numberOfEntries; ++entry) {

    // Load selected branches with data from specified event
    treeReader->ReadEntry(entry);
  
    if (branchMET->GetEntries() == 0)
      continue;
    else 
      assert (branchMET->GetEntries() == 1);

    n_events_nonzero_met++;

    // If event contains at least 1 jet
    if(branchJet->GetEntries() <= 2)
      continue;

    TRootJet *jet1 = 0; 
    TRootJet *jet2 = 0; 

    for (int i = 0; i < branchJet->GetEntries(); i++){
      TRootJet *jet = (TRootJet*) branchJet->At(i);
      if (jet1 == 0)
	jet1 = jet; 
      else if (jet2 == 0 )
	jet2 = jet;
      else if (jet->PT > jet1->PT)
	jet1 = jet;
      else if (jet->PT > jet2->PT)
	jet2 = jet;
    }
    
    if (!jet1 || !jet2 )
      continue;

    if (jet1->PT < 30)
      continue;

    if (jet2->PT < 30)
      continue;

    TLorentzVector vec1, vec2;
    bool found1 = false;
    bool found2 = false;
    int charge1 = 0;
    int charge2 = 0;

    for (int i = 0; i < branchMuon->GetEntries(); i++){
      TRootMuon * muon = (TRootMuon*) branchJet->At(i);
      TLorentzVector vec;
      vec.SetPtEtaPhiM(muon->PT, muon->Eta, muon->Phi, muon_mass);

      if (!found1){
	found1 = true;
	vec1 = vec;
	charge1=muon->Charge;
      }
      else if (!found2){
	found2 = true;
	vec2 = vec;
	charge2=muon->Charge;
      }
      else if (vec.Pt() > vec1.Pt()) {
	vec1 = vec;
	charge1=muon->Charge;
      }
      else if (vec.Pt() > vec2.Pt()) {
	vec2 = vec;
	charge2=muon->Charge;
      }

    }

    for (int i = 0; i < branchElectron->GetEntries(); i++){
      TRootElectron *electron = (TRootElectron*) branchElectron->At(i);
      TLorentzVector vec;
      vec.SetPtEtaPhiM(electron->PT, electron->Eta, electron->Phi, electron_mass);

       if (!found1){
	found1 = true;
	vec1 = vec;
	charge1=electron->Charge;
      }
      else if (!found2){
	found2 = true;
	vec2 = vec;
	charge2=electron->Charge;
      }
      else if (vec.Pt() > vec1.Pt()) {
	vec1 = vec;
	charge1=electron->Charge;
      }
      else if (vec.Pt() > vec2.Pt()) {
	vec2 = vec;
	charge2=electron->Charge;
      }

    }




    if (!found1 || !found2)
      continue;
    
    if (vec1.Pt() < 20)
      continue;
    
    if (vec2.Pt() < 20)
      continue;
    
    if (charge1 * charge2 < 0)
      continue;
    
    TLorentzVector vec1_jet, vec2_jet;
    
    vec1_jet.SetPtEtaPhiM(jet1->PT, jet1->Eta, jet1->Phi, jet1->Mass);
    vec2_jet.SetPtEtaPhiM(jet2->PT, jet2->Eta, jet2->Phi, jet2->Mass);


    if (abs(jet1->Eta - jet2->Eta)  < 2.5)
      continue;
    
    if((vec1_jet + vec2_jet).M() < 500)
      continue;
    
    TRootMissingET * met =(TRootMissingET *) branchMET->At(0);

    if (met->MET < 30)
      continue;
    
    hist->Fill( (vec1_jet + vec2_jet).M());
    
  }


  std::cout << "n_events_nonzero_met = " << n_events_nonzero_met << std::endl;



  hist->Scale(xs * luminosity/ n_events_nonzero_met);

}


void select_pgs()
{


  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(0);
  gStyle->SetLineWidth(2);

  Float_t bins[5] = {500, 700,  1100, 1600, 2000};
  
//   TH1 *histMjjNoMatching = new TH1F("mjj_no_matching", "m_jj", 10, 0.0, 1000.);
//   TH1 *histMjjMatching = new TH1F("mjj_matching", "m_jj", 10, 0.0, 1000.);
//   TH1 *histMjjNoMatchingDown = new TH1F("mjj_no_matching_down", "m_jj", 10, 0.0, 1000.);
//   TH1 *histMjjNoMatchingUp = new TH1F("mjj_no_matching_up", "m_jj", 10, 0.0, 1000.);
//   TH1 *histMjjMatchingDown = new TH1F("mjj_matching_down", "m_jj", 10, 0.0, 1000.);
//   TH1 *histMjjMatchingUp = new TH1F("mjj_matching_up", "m_jj", 10, 0.0, 1000.);

  TH1F *histMjjNoMatching = new TH1F("mjj_no_matching", "m_jj", 4, bins);
  TH1F *histMjjMatching = new TH1F("mjj_matching", "m_jj", 4, bins);
  TH1F *histMjjNoMatchingDown = new TH1F("mjj_no_matching_down", "m_jj", 4, bins);
  TH1F *histMjjNoMatchingUp = new TH1F("mjj_no_matching_up", "m_jj", 4, bins);
  TH1F *histMjjMatchingDown = new TH1F("mjj_matching_down", "m_jj", 4, bins);
  TH1F *histMjjMatchingUp = new TH1F("mjj_matching_up", "m_jj", 4, bins);


  fillHistogram(histMjjMatching, "/scratch3/anlevin/MG5_aMC_v2_0_0/ww_qed_4_qcd_99_pythia_matching/Events/run_01/tag_1_pgs_events.root",0.0215);
  fillHistogram(histMjjMatchingUp, "/scratch3/anlevin/MG5_aMC_v2_0_0/ww_qed_4_qcd_99_pythia_matching_up/Events/run_01/tag_1_pgs_events.root",0.01852);
  fillHistogram(histMjjMatchingDown, "/scratch3/anlevin/MG5_aMC_v2_0_0/ww_qed_4_qcd_99_pythia_matching_down/Events/run_01/tag_1_pgs_events.root",0.02547);
  fillHistogram(histMjjNoMatching, "/scratch3/anlevin/MG5_aMC_v2_0_0/ww_qed_4_qcd_99_pythia_no_matching/Events/run_01/tag_1_pgs_events.root",0.01625);
  fillHistogram(histMjjNoMatchingUp,"/scratch3/anlevin/MG5_aMC_v2_0_0/ww_qed_4_qcd_99_pythia_no_matching_up/Events/run_01/tag_1_pgs_events.root",0.01386);
  fillHistogram(histMjjNoMatchingDown, "/scratch3/anlevin/MG5_aMC_v2_0_0/ww_qed_4_qcd_99_pythia_no_matching_down/Events/run_01/tag_1_pgs_events.root",0.01939 );


  histMjjNoMatching->SetLineColor(kBlack);
  histMjjMatching->SetLineColor(kBlue);
  histMjjNoMatchingDown->SetLineColor(kBlack);
  histMjjNoMatchingUp->SetLineColor(kBlack);
  histMjjMatchingDown->SetLineColor(kBlue);
  histMjjMatchingUp->SetLineColor(kBlue);

  histMjjNoMatching->SetLineWidth(2);
  histMjjMatching->SetLineWidth(2);
  histMjjNoMatchingDown->SetLineWidth(2);
  histMjjNoMatchingUp->SetLineWidth(2);
  histMjjMatchingDown->SetLineWidth(2);
  histMjjMatchingUp->SetLineWidth(2);


    


  histMjjMatchingDown->SetMinimum(0);



  histMjjMatchingDown->GetXaxis()->SetTitle("m_{jj} (GeV)");

  histMjjMatchingDown->Draw("E");

  histMjjNoMatchingDown->Draw("ESAME");
  histMjjNoMatchingUp->Draw("ESAME");
  histMjjNoMatching->Draw("ESAME");
  histMjjMatching->Draw("ESAME");
  histMjjMatchingUp->Draw("ESAME");

  TLegend *legend = new TLegend(0.532,0.64,0.874,0.86);
  legend->AddEntry(histMjjMatching,"with matching","L");
  legend->AddEntry(histMjjNoMatching,"without matching","L");
  legend->SetFillStyle(0);
  legend->Draw("SAME");

}
