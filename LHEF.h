// -*- C++ -*-
#ifndef THEPEG_LHEF_H
#define THEPEG_LHEF_H
//
// This is the declaration of the Les Houches Event File classes.
//

// docs here:
// http://home.thep.lu.se/~leif/LHEF/annotated.html


#include <iostream>
#include <iomanip>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>
#include <utility>
#include <stdexcept>

namespace LHEF {

/**
 * The HEPRUP class is a simple container corresponding to the Les Houches
 * accord (<A HREF="http://arxiv.org/abs/hep-ph/0109068">hep-ph/0109068</A>)
 * common block with the same name. The members are named in the same
 * way as in the common block. However, fortran arrays are represented
 * by vectors, except for the arrays of length two which are
 * represented by pair objects.
 */
class HEPRUP {

public:

  /** @name Standard constructors and destructors. */
  //@{
  /**
   * Default constructor.
   */
  HEPRUP()
    : IDWTUP(0), NPRUP(0) {}

  /**
   * Copy-constructor.
   */
  HEPRUP(const HEPRUP & x)
    : IDBMUP(x.IDBMUP), EBMUP(x.EBMUP),
      PDFGUP(x.PDFGUP), PDFSUP(x.PDFSUP), IDWTUP(x.IDWTUP),
      NPRUP(x.NPRUP), XSECUP(x.XSECUP), XERRUP(x.XERRUP),
      XMAXUP(x.XMAXUP), LPRUP(x.LPRUP) {}


  /**
   * Assignment operator.
   */
  HEPRUP & operator=(const HEPRUP & x) {
    IDBMUP = x.IDBMUP;
    EBMUP = x.EBMUP;
    PDFGUP = x.PDFGUP;
    PDFSUP = x.PDFSUP;
    IDWTUP = x.IDWTUP;
    NPRUP = x.NPRUP;
    XSECUP = x.XSECUP;
    XERRUP = x.XERRUP;
    XMAXUP = x.XMAXUP;
    LPRUP = x.LPRUP;
    return *this;
  }

  /**
   * Destructor.
   */
  ~HEPRUP() {}
  //@}

public:

  /**
   * Set the NPRUP variable, corresponding to the number of
   * sub-processes, to \a nrup, and resize all relevant vectors
   * accordingly.
   */
  void resize(int nrup) {
    NPRUP = nrup;
    resize();
  }

  /**
   * Assuming the NPRUP variable, corresponding to the number of
   * sub-processes, is correctly set, resize the relevant vectors
   * accordingly.
   */
  void resize() {
    XSECUP.resize(NPRUP);
    XERRUP.resize(NPRUP);
    XMAXUP.resize(NPRUP);
    LPRUP.resize(NPRUP);
  }

public:

  /**
   * PDG id's of beam particles. (first/second is in +/-z direction).
   */
  std::pair<long,long> IDBMUP;

  /**
   * Energy of beam particles given in GeV.
   */
  std::pair<double,double> EBMUP;

  /**
   * The author group for the PDF used for the beams according to the
   * PDFLib specification.
   */
  std::pair<int,int> PDFGUP;

  /**
   * The id number the PDF used for the beams according to the
   * PDFLib specification.
   */
  std::pair<int,int> PDFSUP;

  /**
   * Master switch indicating how the ME generator envisages the
   * events weights should be interpreted according to the Les Houches
   * accord.
   */
  int IDWTUP;

  /**
   * The number of different subprocesses in this file.
   */
  int NPRUP;

  /**
   * The cross sections for the different subprocesses in pb.
   */
  std::vector<double> XSECUP;

  /**
   * The statistical error in the cross sections for the different
   * subprocesses in pb.
   */
  std::vector<double> XERRUP;

  /**
   * The maximum event weights (in HEPEUP::XWGTUP) for different
   * subprocesses.
   */
  std::vector<double> XMAXUP;

  /**
   * The subprocess code for the different subprocesses.
   */
  std::vector<int> LPRUP;

};


/**
 * The HEPEUP class is a simple container corresponding to the Les Houches accord
 * (<A HREF="http://arxiv.org/abs/hep-ph/0109068">hep-ph/0109068</A>)
 * common block with the same name. The members are named in the same
 * way as in the common block. However, fortran arrays are represented
 * by vectors, except for the arrays of length two which are
 * represented by pair objects.
 */
class HEPEUP {

public:

  /** @name Standard constructors and destructors. */
  //@{
  /**
   * Default constructor.
   */
  HEPEUP()
    : NUP(0), IDPRUP(0), XWGTUP(0.0), XPDWUP(0.0, 0.0),
      SCALUP(0.0), AQEDUP(0.0), AQCDUP(0.0) {}

  /**
   * Copy-constructor.
   */
  HEPEUP(const HEPEUP & x)
    : NUP(x.NUP), IDPRUP(x.IDPRUP), XWGTUP(x.XWGTUP), XPDWUP(x.XPDWUP),
      SCALUP(x.SCALUP), AQEDUP(x.AQEDUP), AQCDUP(x.AQCDUP), IDUP(x.IDUP),
      ISTUP(x.ISTUP), MOTHUP(x.MOTHUP), ICOLUP(x.ICOLUP),
      PUP(x.PUP), VTIMUP(x.VTIMUP), SPINUP(x.SPINUP) {}
  
  /**
   * Assignment operator.
   */
  HEPEUP & operator=(const HEPEUP & x) {
    NUP = x.NUP;
    IDPRUP = x.IDPRUP;
    XWGTUP = x.XWGTUP;
    XPDWUP = x.XPDWUP;
    SCALUP = x.SCALUP;
    AQEDUP = x.AQEDUP;
    AQCDUP = x.AQCDUP;
    IDUP = x.IDUP;
    ISTUP = x.ISTUP;
    MOTHUP = x.MOTHUP;
    ICOLUP = x.ICOLUP;
    PUP = x.PUP;
    VTIMUP = x.VTIMUP;
    SPINUP = x.SPINUP;
    return *this;
  }


  /**
   * Destructor.
   */
  ~HEPEUP() {};
  //@}

public:

  /**
   * Set the NUP variable, corresponding to the number of particles in
   * the current event, to \a nup, and resize all relevant vectors
   * accordingly.
   */
  void resize(int nup) {
    NUP = nup;
    resize();
  }

  /**
   * Assuming the NUP variable, corresponding to the number of
   * particles in the current event, is correctly set, resize the
   * relevant vectors accordingly.
   */
  void resize() {
    IDUP.resize(NUP);
    ISTUP.resize(NUP);
    MOTHUP.resize(NUP);
    ICOLUP.resize(NUP);
    PUP.resize(NUP, std::vector<double>(5));
    VTIMUP.resize(NUP);
    SPINUP.resize(NUP);
  }

public:

  /**
   * The number of particle entries in the current event.
   */
  int NUP;

  /**
   * The subprocess code for this event (as given in LPRUP).
   */
  int IDPRUP;

  /**
   * The weight for this event.
   */
  double XWGTUP;

  /**
   * The PDF weights for the two incoming partons. Note that this
   * variable is not present in the current LesHouches accord
   * (<A HREF="http://arxiv.org/abs/hep-ph/0109068">hep-ph/0109068</A>),
   * hopefully it will be present in a future accord.
   */
  std::pair<double,double> XPDWUP;

  /**
   * The scale in GeV used in the calculation of the PDF's in this
   * event.
   */
  double SCALUP;

  /**
   * The value of the QED coupling used in this event.
   */
  double AQEDUP;

  /**
   * The value of the QCD coupling used in this event.
   */
  double AQCDUP;

  /**
   * The PDG id's for the particle entries in this event.
   */
  std::vector<long> IDUP;

  /**
   * The status codes for the particle entries in this event.
   */
  std::vector<int> ISTUP;

  /**
   * Indices for the first and last mother for the particle entries in
   * this event.
   */
  std::vector< std::pair<int,int> > MOTHUP;

  /**
   * The colour-line indices (first(second) is (anti)colour) for the
   * particle entries in this event.
   */
  std::vector< std::pair<int,int> > ICOLUP;

  /**
   * Lab frame momentum (Px, Py, Pz, E and M in GeV) for the particle
   * entries in this event.
   */
  std::vector< std::vector<double> > PUP;

  /**
   * Invariant lifetime (c*tau, distance from production to decay in
   * mm) for the particle entries in this event.
   */
  std::vector<double> VTIMUP;

  /**
   * Spin info for the particle entries in this event given as the
   * cosine of the angle between the spin vector of a particle and the
   * 3-momentum of the decaying particle, specified in the lab frame.
   */
  std::vector<double> SPINUP;

};

/**
 * The Reader class is initialized with a stream from which to read a
 * version 1.0 Les Houches Accord event file. In the constructor of
 * the Reader object the optional header information is read and then
 * the mandatory init is read. After this the whole header block
 * including the enclosing lines with tags are available in the public
 * headerBlock member variable. Also the information from the init
 * block is available in the heprup member variable and any additional
 * comment lines are available in initComments. After each successful
 * call to the readEvent() function the standard Les Houches Accord
 * information about the event is available in the hepeup member
 * variable and any additional comments in the eventComments
 * variable. A typical reading sequence would look as follows:
 *
 *
 */
class Reader {

public:

  /**
   * Initialize the Reader with a stream from which to read an event
   * file. After the constructor is called the whole header block
   * including the enclosing lines with tags are available in the
   * public headerBlock member variable. Also the information from the
   * init block is available in the heprup member variable and any
   * additional comment lines are available in initComments.
   *
   * @param is the stream to read from.
   */
  Reader(std::istream & is)
    : file(is) {
    init();
  }

  /**
   * Initialize the Reader with a filename from which to read an event
   * file. After the constructor is called the whole header block
   * including the enclosing lines with tags are available in the
   * public headerBlock member variable. Also the information from the
   * init block is available in the heprup member variable and any
   * additional comment lines are available in initComments.
   *
   * @param filename the name of the file to read from.
   */
  Reader(std::string filename)
    : intstream(filename.c_str()), file(intstream) {
    init();
  }

private:

  /**
   * Used internally in the constructors to read header and init
   * blocks.
   */
  void init() {

    bool readingHeader = false;
    bool readingInit = false;

    // Make sure we are reading a LHEF file:
    getline();
    if ( currentLine.find("<LesHouchesEvents" ) == std::string::npos )
      throw std::runtime_error
	("Tried to read a file which does not start with the "
	 "LesHouchesEvents tag.");
    if ( currentLine.find("version=\"1.0\"" ) == std::string::npos )
      throw std::runtime_error
	("Tried to read a LesHouchesEvents file which is not version 1.0.");

    // Loop over all lines until we hit the </init> tag.
    while ( getline() && currentLine.find("</init>") == std::string::npos ) {
      if ( currentLine.find("<header") != std::string::npos ) {
	// We have hit the header block, so we should dump this all
	// following lines to headerBlock until we hit the end of it.
	readingHeader = true;
	headerBlock = currentLine + "\n";
      }
      else if ( currentLine.find("<init") != std::string::npos ) {
	// We have hit the init block, so we should expect to find the
	// standard information in the following.
	readingInit = true;

	// The first line tells us how many lines to read next.
	getline();
	std::istringstream iss(currentLine);
	if ( !( iss >> heprup.IDBMUP.first >> heprup.IDBMUP.second
		    >> heprup.EBMUP.first >> heprup.EBMUP.second
	            >> heprup.PDFGUP.first >> heprup.PDFGUP.second
	            >> heprup.PDFSUP.first >> heprup.PDFSUP.second
		    >> heprup.IDWTUP >> heprup.NPRUP ) ) {
	  heprup.NPRUP = -42;
	  return;
	}
	heprup.resize();

	for ( int i = 0; i < heprup.NPRUP; ++i ) {
	  getline();
	  std::istringstream iss(currentLine);
	  if ( !( iss >> heprup.XSECUP[i] >> heprup.XERRUP[i]
	              >> heprup.XMAXUP[i] >> heprup.LPRUP[i] ) ) {
	    heprup.NPRUP = -42;
	    return;
	  }
	}
      }
      else if ( currentLine.find("</header>") != std::string::npos ) {
	// The end of the header block. Dump this line as well to the
	// headerBlock and we're done.
	readingHeader = false;
	headerBlock += currentLine + "\n";
      }
      else if ( readingHeader ) {
	// We are in the process of reading the header block. Dump the
	// line to haderBlock.
	headerBlock += currentLine + "\n";
      }
      else if ( readingInit ) {
	// Here we found a comment line. Dump it to initComments.
	initComments += currentLine + "\n";
      }
      else {
	// We found some other stuff outside the standard tags.
	outsideBlock += currentLine + "\n";
      }
    }
    if ( !file ) heprup.NPRUP = -42;
  }

public:

  /**
   * Read an event from the file and store it in the hepeup
   * object. Optional comment lines are stored i the eventComments
   * member variable.
   * @return true if the read sas successful.
   */
  bool readEvent() {

    // Check if the initialization was successful. Otherwise we will
    // not read any events.
    if ( heprup.NPRUP < 0 ) return false;
    eventComments = "";
    outsideBlock = "";
    hepeup.NUP = 0;

    // Keep reading lines until we hit the next event or the end of
    // the event block. Save any inbetween lines. Exit if we didn't
    // find an event.
    while ( getline() && currentLine.find("<event") == std::string::npos )
      outsideBlock += currentLine + "\n";
    if ( !getline()  ) return false;
    
    // We found an event. The first line determines how many
    // subsequent particle lines we have.
    std::istringstream iss(currentLine);
    if ( !( iss >> hepeup.NUP >> hepeup.IDPRUP >> hepeup.XWGTUP
	        >> hepeup.SCALUP >> hepeup.AQEDUP >> hepeup.AQCDUP ) )
      return false;
    hepeup.resize();

    // Read all particle lines.
    for ( int i = 0; i < hepeup.NUP; ++i ) {
      if ( !getline() ) return false;
      std::istringstream iss(currentLine);
      if ( !( iss >> hepeup.IDUP[i] >> hepeup.ISTUP[i]
	          >> hepeup.MOTHUP[i].first >> hepeup.MOTHUP[i].second
         	  >> hepeup.ICOLUP[i].first >> hepeup.ICOLUP[i].second
	          >> hepeup.PUP[i][0] >> hepeup.PUP[i][1] >> hepeup.PUP[i][2]
	          >> hepeup.PUP[i][3] >> hepeup.PUP[i][4]
        	  >> hepeup.VTIMUP[i] >> hepeup.SPINUP[i] ) )
	return false;
    }

    // Now read any additional comments.
    while ( getline() && currentLine.find("</event>") == std::string::npos )
      eventComments += currentLine + "\n";

    if ( !file ) return false;
    return true;

  }

protected:

  /**
   * Used internally to read a single line from the stream.
   */
  bool getline() {
    return ( std::getline(file, currentLine) );
  }

protected:

  /**
   * A local stream which is unused if a stream is supplied from the
   * outside.
   */
  std::ifstream intstream;

  /**
   * The stream we are reading from. This may be a reference to an
   * external stream or the internal intstream.
   */
  std::istream & file;

  /**
   * The last line read in from the stream in getline().
   */
  std::string currentLine;

public:

  /**
   * All lines (since the last readEvent()) outside the header, init
   * and event tags.
   */
  std::string outsideBlock;

  /**
   * All lines from the header block.
   */
  std::string headerBlock;

  /**
   * The standard init information.
   */
  HEPRUP heprup;

  /**
   * Additional comments found in the init block.
   */
  std::string initComments;

  /**
   * The standard information about the last read event.
   */
  HEPEUP hepeup;

  /**
   * Additional comments found with the last read event.
   */
  std::string eventComments;

private:

  /**
   * The default constructor should never be used.
   */
  Reader();

  /**
   * The copy constructor should never be used.
   */
  Reader(const Reader &);

  /**
   * The Reader cannot be assigned to.
   */
  Reader & operator=(const Reader &);

};

/**
 * The Writer class is initialized with a stream to which to write a
 * version 1.0 Les Houches Accord event file. In the constructor of
 * the Writer object the main XML tag is written out, with the
 * corresponding end tag is written in the destructor. After a Writer
 * object has been created, it is possible to assign standard init
 * information in the heprup member variable. In addition any XML
 * formatted information can be added to the headerBlock member
 * variable (directly or via the addHeader() function). Further
 * comment line (beginning with a <code>#</code> character) can be
 * added to the initComments variable (directly or with the
 * addInitComment() function). After this information is set, it
 * should be written out to the file with the init() function.
 *
 * Before each event is written out with the writeEvent() function,
 * the standard event information can then be assigned to the hepeup
 * variable and optional comment lines (beginning with a
 * <code>#</code> character) may be given to the eventComments
 * variable (directly or with the addEventComment() function).
 *
 */
class Writer {

public:

  /**
   * Create a Writer object giving a stream to write to.
   * @param os the stream where the event file is written.
   */
  Writer(std::ostream & os)
    : file(os) {
    // Write out the standard XML tag for the event file.
    file << "<LesHouchesEvents version=\"1.0\">\n";
  }

  /**
   * Create a Writer object giving a filename to write to.
   * @param filename the name of the event file to be written.
   */
  Writer(std::string filename)
    : intstream(filename.c_str()), file(intstream) {
    // Write out the standard XML tag for the event file.
    file << "LesHouchesEvents version=\"1.0\">\n";
  }

  /**
   * The destructor writes out the final XML end-tag.
   */
  ~Writer() {
    file << "</LesHouchesEvents>" << std::endl;
  }

  /**
   * Add header lines consisting of XML code with this stream.
   */
  std::ostream & headerBlock() {
    return headerStream;
  }

  /**
   * Add comment lines to the init block with this stream.
   */
  std::ostream & initComments() {
    return initStream;
  }

  /**
   * Add comment lines to the next event to be written out with this stream.
   */
  std::ostream & eventComments() {
    return eventStream;
  }

  /**
   * Write out an optional header block followed by the standard init
   * block information together with any comment lines.
   */
  void init() {

    file << std::setprecision(8);

    using std::setw;

    std::string headerBlock = headerStream.str();
    if ( headerBlock.length() ) {
      if ( headerBlock.find("<header>") == std::string::npos )
	file << "<header>\n";
      if ( headerBlock[headerBlock.length() - 1] != '\n' )
	headerBlock += '\n';
      file << headerBlock;
      if ( headerBlock.find("</header>") == std::string::npos )
	file << "</header>\n";
    }
    file << "<init>\n"
	 << " " << setw(8) << heprup.IDBMUP.first
	 << " " << setw(8) << heprup.IDBMUP.second
	 << " " << setw(14) << heprup.EBMUP.first
	 << " " << setw(14) << heprup.EBMUP.second
	 << " " << setw(4) << heprup.PDFGUP.first
	 << " " << setw(4) << heprup.PDFGUP.second
	 << " " << setw(4) << heprup.PDFSUP.first
	 << " " << setw(4) << heprup.PDFSUP.second
	 << " " << setw(4) << heprup.IDWTUP
	 << " " << setw(4) << heprup.NPRUP << std::endl;
    heprup.resize();
    for ( int i = 0; i < heprup.NPRUP; ++i )
      file << " " << setw(14) << heprup.XSECUP[i]
	   << " " << setw(14) << heprup.XERRUP[i]
	   << " " << setw(14) << heprup.XMAXUP[i]
	   << " " << setw(6) << heprup.LPRUP[i] << std::endl;
    file << hashline(initStream.str()) << "</init>" << std::endl;
    eventStream.str("");
  }

  /**
   * Write out the event stored in hepeup, followed by optional
   * comment lines.
   */
  bool writeEvent() {

    using std::setw;

    file << "<event>\n";
    file << " " << setw(4) << hepeup.NUP
	 << " " << setw(6) << hepeup.IDPRUP
	 << " " << setw(14) << hepeup.XWGTUP
	 << " " << setw(14) << hepeup.SCALUP
	 << " " << setw(14) << hepeup.AQEDUP
	 << " " << setw(14) << hepeup.AQCDUP << "\n";
    hepeup.resize();

    for ( int i = 0; i < hepeup.NUP; ++i )
      file << " " << setw(8) << hepeup.IDUP[i]
	   << " " << setw(2) << hepeup.ISTUP[i]
	   << " " << setw(4) << hepeup.MOTHUP[i].first
	   << " " << setw(4) << hepeup.MOTHUP[i].second
	   << " " << setw(4) << hepeup.ICOLUP[i].first
	   << " " << setw(4) << hepeup.ICOLUP[i].second
	   << " " << setw(14) << hepeup.PUP[i][0]
	   << " " << setw(14) << hepeup.PUP[i][1]
	   << " " << setw(14) << hepeup.PUP[i][2]
	   << " " << setw(14) << hepeup.PUP[i][3]
	   << " " << setw(14) << hepeup.PUP[i][4]
	   << " " << setw(1) << hepeup.VTIMUP[i]
	   << " " << setw(1) << hepeup.SPINUP[i] << std::endl;

    file << hashline(eventStream.str()) << "</event>\n";

    eventStream.str("");

    if ( !file ) return false;

    return true;

  }

protected:

  /**
   * Make sure that each line in the string \a s starts with a
   * #-character and that the string ends with a new-line.
   */
  std::string hashline(std::string s) {
    std::string ret;
    std::istringstream is(s);
    std::string ss;
    while ( getline(is, ss) ) {
      if ( ss.find('#') == std::string::npos ||
	   ss.find('#') != ss.find_first_not_of(" \t") ) ss = "# " + ss;
      ret += ss + '\n';
    }
    return ret;
  }

protected:

  /**
   * A local stream which is unused if a stream is supplied from the
   * outside.
   */
  std::ofstream intstream;

  /**
   * The stream we are writing to. This may be a reference to an
   * external stream or the internal intstream.
   */
  std::ostream & file;

public:

  /**
   * Stream to add all lines in the header block.
   */
  std::ostringstream headerStream;

  /**
   * The standard init information.
   */
  HEPRUP heprup;

  /**
   * Stream to add additional comments to be put in the init block.
   */
  std::ostringstream initStream;

  /**
   * The standard information about the event we will write next.
   */
  HEPEUP hepeup;

  /**
   * Stream to add additional comments to be written together the next event.
   */
  std::ostringstream eventStream;

private:

  /**
   * The default constructor should never be used.
   */
  Writer();

  /**
   * The copy constructor should never be used.
   */
  Writer(const Writer &);

  /**
   * The Writer cannot be assigned to.
   */
  Writer & operator=(const Writer &);

};

}

/** \example LHEFReadEx.cc An example function which reads from a Les
    Huches Event File: */
/** \example LHEFWriteEx.cc An example function which writes out a Les
    Huches Event File: */
/** \example LHEFCat.cc This is a main function which simply reads a
    Les Houches Event File from the standard input and writes it again
    to the standard output. 
    This file can be downloaded from
    <A HREF="http://www.thep.lu.se/~leif/LHEF/LHEFCat.cc">here</A>. 
    There is also a sample
    <A HREF="http://www.thep.lu.se/~leif/LHEF/ttbar.lhef">event file</A>
    to try it on.
*/

/**\mainpage Les Houches Event File

Why isn't any doxygen output generated by this text?

Here are some example classes for reading and writing Les Houches
Event Files according to the
<A HREF="http://www.thep.lu.se/~torbjorn/lhef/lhafile2.pdf">proposal</A>
by Torbj&ouml;rn Sj&ouml;strand discussed at the
<A HREF="http://mc4lhc06.web.cern.ch/mc4lhc06/">MC4LHC</A>
workshop at CERN 2006.

In total there are four classes which are all available in a single
header file called
<A HREF="http://www.thep.lu.se/~leif/LHEF/LHEF.h">LHEF.h</A>.

The two classes LHEF::HEPRUP and LHEF::HEPEUP are simple container
classes which contain the same information as the Les Houches standard
Fortran common blocks with the same names. The other two classes are
called LHEF::Reader and LHEF::Writer and are used to read and write
Les Houches Event Files

Here are a few <A HREF="examples.html">examples</A> of how to use the
classes:

\namespace LHEF The LHEF namespace contains some example classes for reading and writing Les Houches
Event Files according to the
<A HREF="http://www.thep.lu.se/~torbjorn/lhef/lhafile2.pdf">proposal</A>
by Torbj&ouml;rn Sj&ouml;strand discussed at the
<A HREF="http://mc4lhc06.web.cern.ch/mc4lhc06/">MC4LHC</A>
workshop at CERN 2006.



 */


#endif /* THEPEG_LHEF_H */
