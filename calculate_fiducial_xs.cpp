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

int main(int argc, char ** argv) 
{

  int n_selected_events = 0;
  int n_events = 0;

  if(argc < 2)
    {
      cout << "Usage:   " << argv[0] 
           << " input.lhe " << endl ;
      return -1;
    }

  std::ifstream ifs (argv[1]) ;
  LHEF::Reader reader (ifs) ;

  std::vector<TLorentzVector> electrons;

  //PG loop over input events
  while (reader.readEvent ()) 
    {

      std::vector<TLorentzVector> electrons;
      std::vector<TLorentzVector> muons;
      std::vector<TLorentzVector> quarks;

      if ( reader.outsideBlock.length() ) std::cout << reader.outsideBlock;

      n_events++;

      // loop over particles in the event
      for (int iPart = 0 ; iPart < reader.hepeup.IDUP.size (); ++iPart) 
        {
           // outgoing particles          
           if (reader.hepeup.ISTUP.at (iPart) == 1)
             {
               if (abs (reader.hepeup.IDUP.at (iPart)) == 11) 
                 {     
                   TLorentzVector vec = buildP (reader.hepeup, iPart) ;
		   electrons.push_back(vec);
                 }

	       if(abs (reader.hepeup.IDUP.at (iPart)) == 5 || abs (reader.hepeup.IDUP.at (iPart)) == 6)
		 std::cout << "abs (reader.hepeup.IDUP.at (iPart)) = " << abs (reader.hepeup.IDUP.at (iPart)) << std::endl;

               if (abs (reader.hepeup.IDUP.at (iPart)) == 1 || abs (reader.hepeup.IDUP.at (iPart)) == 2 || abs (reader.hepeup.IDUP.at (iPart)) == 3 || abs (reader.hepeup.IDUP.at (iPart)) == 4)
                 {
                   TLorentzVector vec = buildP (reader.hepeup, iPart) ;
                   quarks.push_back(vec);
                 }
 
             } // outgoing particles
        } // loop over particles in the event

      
      std::cout << "quarks.size() = " << quarks.size() << std::endl;
      std::cout << "electrons.size() = " << electrons.size() << std::endl;

      assert(quarks.size() == 2);
      if(electrons.size() != 2)
	continue;



      if (electrons[0].Pt() < 10)
	continue;

      if (electrons[1].Pt() < 10)
	continue;

      if (quarks[0].Pt() < 20)
	continue;

      if (quarks[1].Pt() < 20)
	continue;

      if (abs(quarks[0].Eta()) > 5.0)
	continue;

      if (abs(quarks[1].Eta()) > 5.0)
	continue;

      if (abs(electrons[0].Eta()) > 2.5)
	continue;

      if (abs(electrons[1].Eta()) > 2.5)
	continue;

      if ((quarks[0] + quarks[1]).M() < 300)
	continue;

      if(abs(quarks[0].Eta() - quarks[1].Eta()) < 2.5)
	continue;

      n_selected_events++;

    } //PG loop over input events

  std::cout << "n_selected_events = " << n_selected_events << std::endl;
  std::cout << "n_events = " << n_events << std::endl;
  std::cout << "n_selected_events/n_events = " << float(n_selected_events)/n_events << std::endl;
  std::cout << "9*n_selected_events/n_events = " << 9*float(n_selected_events)/n_events << std::endl;
  std::cout << "9*n_selected_events*0.01626/n_events = " << 9*float(n_selected_events)* 0.01626/n_events << std::endl;

  return 0 ;
}
