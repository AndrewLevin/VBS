
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


int n_events_with_z = 0;
int n_total_events = 0;

int main(int argc, char ** argv) 
{
  if(argc < 2)
    {
      cout << "Usage:   " << argv[0] 
           << " input.lhe " << endl ;
      return -1;
    }

  std::ifstream ifs (argv[1]) ;
  LHEF::Reader reader (ifs) ;

  TH1F mll ("dielectron_mass", "dielectron_mass", 100, 0, 100) ;

  std::vector<TLorentzVector> electrons;

  //PG loop over input events
  while (reader.readEvent ()) 
    {
      n_total_events+=1;

      std::vector<TLorentzVector> leptons;
      std::vector<TLorentzVector> quarks;

      if ( reader.outsideBlock.length() ) std::cout << reader.outsideBlock;
	  std::vector<int> z_lepton_vector;

      // loop over particles in the event
      for (int iPart = 0 ; iPart < reader.hepeup.IDUP.size (); ++iPart) 
        {
           // outgoing particles          
           if (reader.hepeup.ISTUP.at (iPart) == 1)
             {

	       if (abs (reader.hepeup.IDUP.at (iPart)) == 22)
		 std::cout << "photon" << std::endl;

               if (abs (reader.hepeup.IDUP.at (iPart)) == 11 ||  abs (reader.hepeup.IDUP.at (iPart)) == 13 ||  abs (reader.hepeup.IDUP.at (iPart)) == 15) 
                 {     
		   int moth1 = reader.hepeup.IDUP.at (    (reader.hepeup.MOTHUP.at (iPart)).first -1     );
		   int moth2 = reader.hepeup.IDUP.at (    (reader.hepeup.MOTHUP.at (iPart)).second -1     );
		   //assert (moth1 == moth2);
		   std::cout << "moth1 = " << moth1 << std::endl;
		   std::cout << "moth2 = " << moth2 << std::endl;
		   if(abs(moth1) == abs(moth2) && abs(moth1)!=24){
		    z_lepton_vector.push_back(iPart);
		   }
                 }
             } // outgoing particles
        } // loop over particles in the event


  //assert(z_lepton_vector.size() == 2 || z_lepton_vector.size() == 0);

      if ( z_lepton_vector.size() > 1){
	n_events_with_z+=1;
	TLorentzVector lep1 = buildP (reader.hepeup, z_lepton_vector[0]) ;
	TLorentzVector lep2 = buildP (reader.hepeup, z_lepton_vector[1]) ;
	
	mll.Fill((lep1+lep2).M());

	std::cout << "(lep1+lep2).M() = " << (lep1+lep2).M() << std::endl;

      }

    } //PG loop over input events


  std::cout << "n_total_events = " << n_total_events << std::endl;
  std::cout << "n_events_with_z = " << n_events_with_z << std::endl;

  TFile f ("output_distributions.root", "recreate") ;
  mll.Write();
  f.Close () ;

  return 0 ;
}
