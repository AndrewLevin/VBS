
{
  // Load shared library
  gSystem->Load("lib/libExRootAnalysis.so");
  gSystem->Load("libPhysics");

  // Create chain of root trees
  TChain chain("LHCO");
  chain.Add("/data/blue/anlevin/delete_this/MG5_aMC_v2_1_1/delete_this9/Events/run_01/tag_1_pgs_events.root");
  
  // Create object of class ExRootTreeReader
  ExRootTreeReader *treeReader = new ExRootTreeReader(&chain);
  Long64_t numberOfEntries = treeReader->GetEntries();
  
  // Get pointers to branches used in this analysis
  TClonesArray *branchJet = treeReader->UseBranch("Jet");
  TClonesArray *branchElectron = treeReader->UseBranch("Electron");
  
  // Book histograms
  TH1 *histJetPT = new TH1F("jet_pt", "jet P_{T}", 100, 0.0, 100.0);
  TH1 *histMass = new TH1F("mass", "M_{inv}(e_{1}, e_{2})", 100, 40.0, 140.0);

  // Loop over all events
  for(Int_t entry = 0; entry < numberOfEntries; ++entry) {

    // Load selected branches with data from specified event
    treeReader->ReadEntry(entry);
  
    // If event contains at least 1 jet
    if(branchJet->GetEntries() > 0) {

      // Take first jet
      TRootJet *jet = (TRootJet*) branchJet->At(0);
      
      // Plot jet transverse momentum
      histJetPT->Fill(jet->PT);
      
      // Print jet transverse momentum
      cout << jet->PT << endl;
    }

    TRootElectron *elec1, *elec2;
    TLorentzVector vec1, vec2;

    // If event contains at least 2 electrons
    if(branchElectron->GetEntries() > 1) {

      // Take first two electrons
      elec1 = (TRootElectron *) branchElectron->At(0);
      elec2 = (TRootElectron *) branchElectron->At(1);

      // Create two 4-vectors for the electrons
      vec1.SetPtEtaPhiM(elec1->PT, elec1->Eta, elec1->Phi, 0.0);
      vec2.SetPtEtaPhiM(elec2->PT, elec2->Eta, elec2->Phi, 0.0);

      // Plot their invariant mass
      histMass->Fill((vec1 + vec2).M());
    }
  }

  // Show resulting histograms
  histJetPT->Draw();
  histMass->Draw();
}
