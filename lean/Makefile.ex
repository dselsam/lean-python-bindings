# Based off of code from:
# http://www.shocksolution.com/python-basics-tutorials-and-examples/linking-python-and-c-with-boostpython/

# Magic to make it work on osx
CC = clang++ --std=c++11 -stdlib=libc++


# location of the Python header files
PYTHON_VERSION = 2.7
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)


# location of Pybind11 includes
PYBIND11_INC = <path/to/pybind11/include> 


# location of LEAN
LEAN_INC = <path/to/lean/src>
LEAN_LIB = <path/to/lean/build/release>


# compile classes
TARGET = lean
 
$(TARGET).so: $(TARGET).o
	$(CC) -shared $(TARGET).o -L$(LEAN_LIB) -lleanshared -L/usr/lib/python$(PYTHON_VERSION)/config -lpython$(PYTHON_VERSION) -o $(TARGET).so -v
 
$(TARGET).o: $(TARGET).cpp
	$(CC) -I$(PYTHON_INCLUDE) -I$(PYBIND11_INC) -I$(LEAN_INC) -fPIC -c $(TARGET).cpp

.PHONY: clean
clean:
	 -rm $(TARGET).o $(TARGET).so
