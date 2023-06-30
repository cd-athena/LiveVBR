# Building instructions

The software is tested mostly in Linux and Windows OS. It requires some pre-requisite software to be installed before compiling. The steps to build the project in Linux and Windows are explained below.

## Prerequisites
 1. [Python](https://www.python.org/) version 3.7 or higher.
 2. [Pandas](https://pandas.pydata.org/) version 1.2.5 or higher.

## Prerequisites for VCA

 1. [CMake](https://cmake.org) version 3.13 or higher.
 2. [Git](https://git-scm.com/).
 3. C++ compiler with C++11 support
 4. [NASM](https://nasm.us/) assembly compiler (for x86 SIMD support)

The following C++11 compilers have been known to work:

 * Visual Studio 2015 or later
 * GCC 4.8 or later
 * Clang 3.3 or later
 
 ## Instructions to run 
  1. Execute the following commands to checkout the VCA source code and place the compiler output inside the folder \build:
  
     $ cd build

  2. cmake is then used to generate build files and compile the VCA binaries

	 $ cmake ..\VCA\
	 $ cmake --build .
	 
  3. Ensure that VCA is built and that vca binary exists in the location \build\source\apps\.
  4. Run the following command:
  
	 $ python main.py --video <Video-location> --inputres <Resolution: w x h> --codec <Codec name> --minbr <Minimum bitrate> --maxbr <Maximum bitrate> --jnd <Target average perceptual difference> --output <Desired output file name>
	 
	 Sample command line:

	 $ python main.py --video AncientThought_s000.yuv --inputres 3840x2160 --codec x265 --minbr 145 --maxbr 16800 --jnd 6 --output result.csv
