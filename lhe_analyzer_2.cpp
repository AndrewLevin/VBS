
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


int n_total_events = 0;
int n_events_with_two_leptons_and_two_quarks = 0;
int n_events_with_two_leptons_and_two_quarks_that_pass_cuts = 0;

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
	  std::vector<TLorentzVector> lepton_mother_vector;
	  std::vector<TLorentzVector> quark_vector;

	  int n_quarks=0;
	  int n_leptons=0;

      // loop over particles in the event
      for (int iPart = 0 ; iPart < reader.hepeup.IDUP.size (); ++iPart) 
        {
           // outgoing particles          
	  if ( reader.hepeup.ISTUP.at (iPart) == 1 )
             {

	       if (abs (reader.hepeup.IDUP.at (iPart)) == 11 || abs (reader.hepeup.IDUP.at (iPart)) == 13 || abs (reader.hepeup.IDUP.at (iPart)) == 15){


		 n_leptons++;
		 TLorentzVector vec = buildP (reader.hepeup, iPart) ;
		 lepton_vector.push_back(vec);
		 int moth1 = reader.hepeup.IDUP.at (    (reader.hepeup.MOTHUP.at (iPart)).first -1     );
		 int moth2 = reader.hepeup.IDUP.at (    (reader.hepeup.MOTHUP.at (iPart)).second -1     );

	       }

	       if (
		   abs (reader.hepeup.IDUP.at (iPart)) == 1 || abs (reader.hepeup.IDUP.at (iPart)) == 2 || abs (reader.hepeup.IDUP.at (iPart)) == 3 ||
		   abs (reader.hepeup.IDUP.at (iPart)) == 4 || abs (reader.hepeup.IDUP.at (iPart)) == 5 || abs (reader.hepeup.IDUP.at (iPart)) == 6
		   ){

		 n_quarks++;
		 TLorentzVector vec = buildP (reader.hepeup, iPart) ;
		 quark_vector.push_back(vec);
	       }
             } // outgoing particles
        } // loop over particles in the event

      assert(quark_vector.size() == 2 && lepton_vector.size() == 2);

      n_events_with_two_leptons_and_two_quarks++;	  

      if ( (quark_vector[0]+quark_vector[1]).M() < 100)
      	continue;

      diquark_mass.Fill((quark_vector[0]+quark_vector[1]).M());

    } //PG loop over input events

  std::cout << "n_total_events = " << n_total_events << std::endl;
  std::cout << "n_events_with_two_leptons_and_two_quarks = " << n_events_with_two_leptons_and_two_quarks << std::endl;
  std::cout << "n_events_with_two_leptons_and_two_quarks_that_pass_cuts = " << n_events_with_two_leptons_and_two_quarks_that_pass_cuts << std::endl;

  TFile f ("output_distributions.root", "recreate") ;
  diquark_mass.Write();
  f.Close () ;

  return 0 ;
}
