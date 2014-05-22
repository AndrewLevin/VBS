// c++ -o checkMomentum_00 `root-config --glibs --cflags` -lm checkMomentum_00.cpp
#include "LHEF.h"
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

double DeltaPhi(double phi1, double phi2)
{
  // Compute DeltaPhi between two given angles. Results is in [-pi/2,pi/2].
  double dphi = TMath::Abs(phi1-phi2);
  while (dphi>TMath::Pi())
    dphi = TMath::Abs(dphi - TMath::TwoPi());
  return(dphi);
}

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


int main(int argc, char ** argv) 
{
  if(argc < 2)
    {
      cout << "Usage:   " << argv[0] 
           << " input1.lhe input2.lhe" << endl ;
      return -1;
    }

  std::ifstream ifs1 (argv[1]) ;
  LHEF::Reader reader1 (ifs1) ;

  std::ifstream ifs2 (argv[2]) ;
  LHEF::Reader reader2 (ifs2) ;

  TH1F mjjll_1 ("mjjll_1", "mjjll_1", 10, 500, 3000) ;
  TH1F mjjll_2 ("mjjll_2", "mjjll_2", 10, 500, 3000) ;
  TH1F mt_1 ("mt_1", "mt_1", 10, 000, 600) ;
  TH1F mt_2 ("mt_2", "mt_2", 10, 000, 600) ;
  TH1F mll_1 ("mll_1", "mll_1", 10, 0, 300) ;
  TH1F mll_2 ("mll_2", "mll_2", 10, 0, 300) ;
  TH1F mjj_1 ("mjj_1", "mjj_1", 10, 500, 3000) ;
  TH1F mjj_2 ("mjj_2", "mjj_2", 10, 500, 3000) ;

  //PG loop over input events
  while (reader1.readEvent ()) 
    {

      std::vector<TLorentzVector> electrons;
      std::vector<TLorentzVector> quarks;
      std::vector<TLorentzVector> electron_neutrinos;

      if ( reader1.outsideBlock.length() ) std::cout << reader1.outsideBlock;

      // loop over particles in the event
      for (int iPart = 0 ; iPart < reader1.hepeup.IDUP.size (); ++iPart) 
        {
           // outgoing particles          
           if (reader1.hepeup.ISTUP.at (iPart) == 1)
             {
               if (abs (reader1.hepeup.IDUP.at (iPart)) == 11) 
                 {     
                   TLorentzVector vec = buildP (reader1.hepeup, iPart) ;
		   electrons.push_back(vec);
                 }

	       if(abs (reader1.hepeup.IDUP.at (iPart)) == 5 || abs (reader1.hepeup.IDUP.at (iPart)) == 6)
		 std::cout << "abs (reader1.hepeup.IDUP.at (iPart)) = " << abs (reader1.hepeup.IDUP.at (iPart)) << std::endl;

	       if(abs (reader1.hepeup.IDUP.at (iPart)) == 12 ){
		 TLorentzVector vec = buildP(reader1.hepeup,iPart);
		 electron_neutrinos.push_back(vec);
	       }

               if (abs (reader1.hepeup.IDUP.at (iPart)) == 1 || abs (reader1.hepeup.IDUP.at (iPart)) == 2 || abs (reader1.hepeup.IDUP.at (iPart)) == 3 || abs (reader1.hepeup.IDUP.at (iPart)) == 4)
                 {
                   TLorentzVector vec = buildP (reader1.hepeup, iPart) ;
                   quarks.push_back(vec);
                 }
 
             } // outgoing particles
        } // loop over particles in the event

      if(quarks.size() != 2){
	std::cout << "found event without exactly two quarks 1" << std::endl;
	continue;
      }
      if(electrons.size() != 2)
	continue;

      assert(electron_neutrinos.size() == 2);

      mjjll_1.Fill( (quarks[0] + quarks[1]+electrons[0]+electrons[1]).M() );
      mjj_1.Fill( (quarks[0] + quarks[1]).M() );
      mll_1.Fill( (electrons[0]+electrons[1]).M() );
      mt_1.Fill( sqrt(2 * (electrons[0]+electrons[1]).Pt() * (electron_neutrinos[0] + electron_neutrinos[1]).Et()
		      * (1-cos(DeltaPhi((electrons[0]+electrons[1]).Phi(),(electron_neutrinos[0] + electron_neutrinos[1]).Phi())))) );

    } //PG loop over input events

  //PG loop over input events
  while (reader2.readEvent ()) 
    {

      std::vector<TLorentzVector> electrons;
      std::vector<TLorentzVector> quarks;
      std::vector<TLorentzVector> electron_neutrinos;

      if ( reader2.outsideBlock.length() ) std::cout << reader2.outsideBlock;

      // loop over particles in the event
      for (int iPart = 0 ; iPart < reader2.hepeup.IDUP.size (); ++iPart) 
        {
           // outgoing particles          
           if (reader2.hepeup.ISTUP.at (iPart) == 1)
             {
               if (abs (reader2.hepeup.IDUP.at (iPart)) == 11) 
                 {     
                   TLorentzVector vec = buildP (reader2.hepeup, iPart) ;
		   electrons.push_back(vec);
                 }

	       if(abs (reader2.hepeup.IDUP.at (iPart)) == 12 ){
		 TLorentzVector vec = buildP(reader2.hepeup,iPart);
		 electron_neutrinos.push_back(vec);
	       }

	       if(abs (reader2.hepeup.IDUP.at (iPart)) == 5 || abs (reader2.hepeup.IDUP.at (iPart)) == 6)
		 std::cout << "abs (reader2.hepeup.IDUP.at (iPart)) = " << abs (reader2.hepeup.IDUP.at (iPart)) << std::endl;

               if (abs (reader2.hepeup.IDUP.at (iPart)) == 1 || abs (reader2.hepeup.IDUP.at (iPart)) == 2 || abs (reader2.hepeup.IDUP.at (iPart)) == 3 || abs (reader2.hepeup.IDUP.at (iPart)) == 4)
                 {
                   TLorentzVector vec = buildP (reader2.hepeup, iPart) ;
                   quarks.push_back(vec);
                 }
 
             } // outgoing particles
        } // loop over particles in the event

      if(quarks.size() != 2){
	std::cout << "found event without exactly two quarks 2" << std::endl;
	continue;
      }
	
      if(electrons.size() != 2)
	continue;

      assert(electron_neutrinos.size() == 2);

      mjjll_2.Fill( (quarks[0] + quarks[1]+electrons[0]+electrons[1]).M() );
      mjj_2.Fill( (quarks[0] + quarks[1]).M() );
      mll_2.Fill( (electrons[0]+electrons[1]).M() );
      mt_2.Fill( sqrt(2 * (electrons[0]+electrons[1]).Pt() * (electron_neutrinos[0] + electron_neutrinos[1]).Et() 
		      * (1-cos(DeltaPhi((electrons[0]+electrons[1]).Phi(),(electron_neutrinos[0] + electron_neutrinos[1]).Phi())))) );

    } //PG loop over input events


  TFile f ("output_distributions.root", "recreate") ;
  mjjll_2.Write();
  mjjll_1.Write();
  mjj_1.Write();
  mjj_2.Write();
  mll_1.Write();
  mll_2.Write();
  mt_1.Write();
  mt_2.Write();
  f.Close () ;

  return 0 ;
}
