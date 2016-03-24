
// c++ -o checkMomentum_00 `root-config --glibs --cflags` -lm checkMomentum_00.cpp
#include "LHEF.h" //comes from http://home.thep.lu.se/~leif/LHEF/LHEF.h
#include <iomanip>
#include <vector>
#include <iostream>
#include <string>
#include <sstream>
#include "TH1.h"
#include "TFile.h"

#include "TLorentzVector.h"

// CINT does not understand some files included by LorentzVector
#include "Math/Vector3D.h"
#include "Math/Vector4D.h"

using namespace ROOT::Math;
using namespace std ;

TLorentzVector buildP (const LHEF::HEPEUP & event, int iPart)
{
  TLorentzVector dummy ;
  dummy.SetPxPyPzE (
      event.PUP.at (iPart).at (0), // px
      event.PUP.at (iPart).at (1), // py
      event.PUP.at (iPart).at (2), // pz
      event.PUP.at (iPart).at (3) // E
    ) ;
  return dummy ;  
}


double delta_phi(double phi1, double phi2)
{
  // Compute DeltaPhi between two given angles. Results is in [-pi/2,pi/2].
  double dphi = TMath::Abs(phi1-phi2);
  while (dphi>TMath::Pi())
    dphi = TMath::Abs(dphi - TMath::TwoPi());
  return(dphi);
}

int n_total_events = 0;
int n_events_with_two_leptons_and_two_quarks_and_two_neutrinos = 0;
int n_events_with_two_leptons_and_two_quarks_and_two_neutrinos_that_pass_cuts = 0;

int main(int argc, char ** argv) 
{

  int evt_num = 0;

  if(argc < 2)
    {
      cout << "Usage:   " << argv[0] 
           << " input.lhe " << endl ;
      return -1;
    }

  std::ifstream ifs (argv[1]) ;
  LHEF::Reader reader (ifs) ;

  TH1F diquark_mass ("diquark_mass", "diquark_mass", 100, 0, 3000) ;
  TH1F dilepton_mass ("dilepton_mass", "dilepton_mass", 100, 0, 750) ;
  TH1F deltaetajj ("deltaetajj", "deltaetajj", 100, 0, 10) ;
  TH1F deltaetall ("deltaetall", "deltaetall", 100, 0, 10) ;
  TH1F deltaphijj ("deltaphijj", "deltaphijj", 100, 0, 3.5) ;
  TH1F deltaphill ("deltaphill", "deltaphill", 100, 0, 3.5) ;
  TH1F quark_pt ("quark_pt", "quark_pt", 100, 0, 400) ;
  TH1F quark_eta ("quark_eta", "quark_eta", 100, -5, 5) ;
  TH1F lepton_pt ("lepton_pt", "lepton_pt", 100, 0, 200) ;
  TH1F lepton_eta ("lepton_eta", "lepton_eta", 100, -5, 5) ;
  TH1F neutrinos_pt ("neutrinos_pt", "neutrinos_pt", 100, 0, 300) ;


  std::vector<TLorentzVector> electrons;

  //PG loop over input events
  while (reader.readEvent ()) 
    {
      if (evt_num % 1000 == 0)
	std::cout << evt_num << std::endl;

      evt_num+=1;

      //if (evt_num > 10000)
      //	break;


      n_total_events+=1;



      //if ( reader.outsideBlock.length() ) std::cout << reader.outsideBlock;
	  std::vector<TLorentzVector> lepton_vector;
	  std::vector<TLorentzVector> neutrinos_vector;
	  std::vector<TLorentzVector> quark_vector;

	  int n_quarks=0;
	  int n_leptons=0;
	  int n_neutrinos=0;

      // loop over particles in the event
      for (int iPart = 0 ; iPart < reader.hepeup.IDUP.size (); ++iPart) 
        {
           // outgoing particles          
	  if ( reader.hepeup.ISTUP.at (iPart) == 1 )
             {

	       if (abs (reader.hepeup.IDUP.at (iPart)) == 11 || abs (reader.hepeup.IDUP.at (iPart)) == 13 || abs (reader.hepeup.IDUP.at (iPart)) == 15){


		 //only look at positive charge events
		 //if (reader.hepeup.IDUP.at (iPart) == 11 || reader.hepeup.IDUP.at (iPart) == 13 || reader.hepeup.IDUP.at (iPart) == 15){
		 //  break;
		 //}

		 n_leptons++;
		 TLorentzVector vec = buildP (reader.hepeup, iPart) ;
		 lepton_vector.push_back(vec);

	       }

	       if (
		   abs (reader.hepeup.IDUP.at (iPart)) == 1 || abs (reader.hepeup.IDUP.at (iPart)) == 2 || abs (reader.hepeup.IDUP.at (iPart)) == 3 ||
		   abs (reader.hepeup.IDUP.at (iPart)) == 4 || abs (reader.hepeup.IDUP.at (iPart)) == 5 || abs (reader.hepeup.IDUP.at (iPart)) == 6
		   ){

		 n_quarks++;
		 TLorentzVector vec = buildP (reader.hepeup, iPart) ;
		 quark_vector.push_back(vec);
	       }


	       if (
		   abs (reader.hepeup.IDUP.at (iPart)) == 12 || abs (reader.hepeup.IDUP.at (iPart)) == 14 || abs (reader.hepeup.IDUP.at (iPart)) == 16
		   ){

		 n_neutrinos++;
		 TLorentzVector vec = buildP (reader.hepeup, iPart) ;
		 neutrinos_vector.push_back(vec);
	       }
             } // outgoing particles
        } // loop over particles in the event

      assert(quark_vector.size() == 2 && lepton_vector.size() == 2 && neutrinos_vector.size() == 2);

      n_events_with_two_leptons_and_two_quarks_and_two_neutrinos++;	  

      if ( (quark_vector[0]+quark_vector[1]).M() < 100)
      	continue;

      diquark_mass.Fill((quark_vector[0]+quark_vector[1]).M());
      dilepton_mass.Fill((lepton_vector[0]+lepton_vector[1]).M());
      deltaetajj.Fill(fabs(quark_vector[0].Eta() - quark_vector[1].Eta()));
      deltaphijj.Fill(delta_phi(quark_vector[0].Phi(),quark_vector[1].Phi()));
      deltaetall.Fill(fabs(lepton_vector[0].Eta() - lepton_vector[1].Eta()));
      deltaphill.Fill(delta_phi(lepton_vector[0].Phi(),lepton_vector[1].Phi()));
      quark_pt.Fill(quark_vector[0].Pt());
      quark_pt.Fill(quark_vector[1].Pt());
      lepton_pt.Fill(lepton_vector[0].Pt());
      lepton_pt.Fill(lepton_vector[1].Pt());
      quark_eta.Fill(quark_vector[0].Eta());
      quark_eta.Fill(quark_vector[1].Eta());
      lepton_eta.Fill(lepton_vector[0].Eta());
      lepton_eta.Fill(lepton_vector[1].Eta());
      neutrinos_pt.Fill((neutrinos_vector[0] + neutrinos_vector[1]).Pt());

    } //PG loop over input events

  std::cout << "n_total_events = " << n_total_events << std::endl;
  std::cout << "n_events_with_two_leptons_and_two_quarks_and_two_neutrinos = " << n_events_with_two_leptons_and_two_quarks_and_two_neutrinos << std::endl;
  std::cout << "n_events_with_two_leptons_and_two_quarks_and_two_neutrinos_that_pass_cuts = " << n_events_with_two_leptons_and_two_quarks_and_two_neutrinos_that_pass_cuts << std::endl;

  TFile f ("output_distributions.root", "recreate") ;
  diquark_mass.Write();
  dilepton_mass.Write();
  deltaetajj.Write();
  deltaetall.Write();
  deltaphijj.Write();
  deltaphill.Write();
  quark_pt.Write();
  quark_eta.Write();
  lepton_pt.Write();
  lepton_eta.Write();
  neutrinos_pt.Write();

  f.Close () ;

  return 0 ;
}
