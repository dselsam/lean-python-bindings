# Based off of code from:
# http://www.shocksolution.com/python-basics-tutorials-and-examples/linking-python-and-c-with-boostpython/


# location of the Python header files
PYTHON_VERSION = 2.7
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)

# location of the Boost Python include files and library
BOOST_INC = /usr/local/include
BOOST_LIB = /usr/local/lib

# location of LEAN
LEAN_INC = path/to/lean/src 
LEAN_LIB = path/to/lean/build/release

# compile classes
TARGET = lean
 
$(TARGET).so: $(TARGET).o
	g++ -shared $(TARGET).o -L$(LEAN_LIB) -lleanshared -L$(BOOST_LIB) -lboost_python -L/usr/lib/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) -o $(TARGET).so -v
 
$(TARGET).o: $(TARGET).cpp
	g++ -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -I$(LEAN_INC) -fPIC -c $(TARGET).cpp

.PHONY: clean
clean:
	 -rm $(TARGET).o $(TARGET).so
