# lean-python-bindings
 Python Bindings to the Lean Theorem Prover http://leanprover.github.io/

## Using

Write `config.sh` with your system specifics and run
```
source config.sh
```
An example is given in `config.sh.ex`.

## Building with CMake

CMake is a portable and convenient way to build pybind11 extension. We
assume the repo has been cloned with

```
git clone --recursive https://github.com/dselsam/lean-python-bindings
```

In the root directory of the project run

```
mkdir -b build
cd build
cmake ..
make
```

The built Python extension will be in the `build/` directory.