# Path to Lean standard library (MODIFY ME)
export MY_PATH_TO_LEAN_STDLIB=/usr/local/lib/lean/library

# Path to Lean includes (MODIFY ME)
export MY_PATH_TO_LEAN_INC=/usr/local/include/lean
# Path to Lean shared library
export MY_PATH_TO_LEAN_LIB=/usr/local/lib
# Update shared library load path to include Lean
export LD_LIBRARY_PATH=$MY_PATH_TO_LEAN_LIB

# Path to pybind11
export MY_PATH_TO_PYBIND11_INC=/usr/local/include/pybind11

# Activate virtualenv (UNCOMMENT AND MODIFY if using virtualenv)
#MY_PATH_TO_PYENV=<path/to/pyenv>
#source $MY_PATH_TO_PYENV/bin/activate
