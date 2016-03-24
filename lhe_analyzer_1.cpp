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

  TH1F costheta1 ("costheta1","costheta1",50,-1,1);

  std::vector<TLorentzVector> electrons;

  //PG loop over input events
  while (reader.readEvent ()) 
    {
      if (evt_num % 1000 == 0)
	std::cout << evt_num << std::endl;

      evt_num+=1;

      if (evt_num > 10000)
      	break;


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


		 //only look at positive charge events
		 if (reader.hepeup.IDUP.at (iPart) == 11 || reader.hepeup.IDUP.at (iPart) == 13 || reader.hepeup.IDUP.at (iPart) == 15){
		   break;
		 }

		 n_leptons++;
		 TLorentzVector vec = buildP (reader.hepeup, iPart) ;
		 lepton_vector.push_back(vec);
		 int moth1 = reader.hepeup.IDUP.at (    (reader.hepeup.MOTHUP.at (iPart)).first -1     );
		 int moth2 = reader.hepeup.IDUP.at (    (reader.hepeup.MOTHUP.at (iPart)).second -1     );
		 //std::cout << "moth1 = " << moth1 << std::endl;
		 //std::cout << "moth2 = " << moth2 << std::endl;

		 assert((abs(moth1) == abs(moth2)) && abs(moth1) == 24);

		 TLorentzVector vec_moth = buildP (reader.hepeup, (reader.hepeup.MOTHUP.at (iPart)).first -1) ;

		 lepton_mother_vector.push_back(vec_moth);

		 std::cout << "reader.heprup.weightIndex(1) = " << reader.heprup.weightgroup.size() << std::endl;

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

      //this means it is a negative W event
      if(lepton_vector.size() == 0 && lepton_mother_vector.size() == 0){
	continue;
      }

      assert(lepton_vector.size() == 2 && lepton_mother_vector.size() == 2);

      n_events_with_two_leptons_and_two_quarks++;	  

      if ( (quark_vector[0]+quark_vector[1]).M() < 100)
      	continue;

      TVector3 b(lepton_mother_vector[0].BoostVector());

      lepton_mother_vector[1].Boost(-b);

      lepton_vector[0].Boost(-b);

      costheta1.Fill(cos(lepton_vector[0].Angle(-lepton_mother_vector[1].Vect())));

    } //PG loop over input events

  std::cout << "n_total_events = " << n_total_events << std::endl;
  std::cout << "n_events_with_two_leptons_and_two_quarks = " << n_events_with_two_leptons_and_two_quarks << std::endl;
  std::cout << "n_events_with_two_leptons_and_two_quarks_that_pass_cuts = " << n_events_with_two_leptons_and_two_quarks_that_pass_cuts << std::endl;

  TFile f ("output_distributions.root", "recreate") ;
  costheta1.Write();
  f.Close () ;

  return 0 ;
}
