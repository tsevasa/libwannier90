#########################################
# pyWannier90                           #                                
# User defines the compiling parameters #
#----------------START------------------#
W90DIR =./libwannier
LIBDIR =/opt/homebrew/opt/lapack


CPP = g++
LIBS = -L$(LIBDIR)/lib -llapack -lblas -Wl,-rpath,$(W90DIR) -L$(W90DIR) -lwannier-3.1.0-M2
CPPFLAGS = -O3 -Wall -shared -std=c++11 -fPIC -D_UF 

all: libwannier90_gf

libwannier90_gf:
	# sed -i '/#define*/c\#define gfortran' libwannier90.cpp
	$(CPP) $(CPPFLAGS) `python3 -m pybind11 --includes` libwannier90.cpp -o libwannier90`python3-config --extension-suffix` $(LIBS) -undefined dynamic_lookup

clean:
	rm -rf obj
	rm -f *.so *.o *.mod