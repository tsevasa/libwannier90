W90DIR =../wannier90-3.1.0
LIBDIR =/opt/homebrew/opt/lapack

CPP = g++
LIBS = -L$(LIBDIR)/lib -llapack -lblas -Wl,-rpath,$(W90DIR) -L$(W90DIR) -lwannier
CPPFLAGS = -O3 -Wall -shared -std=c++11 -fPIC -D_UF

all: libwannier90
libwannier90:
	$(CPP) $(CPPFLAGS) `python3 -m pybind11 --includes` libwannier90.cpp -o libwannier90`python3-config --extension-suffix` $(LIBS) -undefined dynamic_lookup

clean:
	rm -rf obj
	rm -f *.so *.o *.mod
