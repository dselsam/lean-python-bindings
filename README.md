# lean-python-bindings
 Python Bindings to the Lean Theorem Prover http://leanprover.github.io/

## Using

Write `config.sh` with your system specifics and run
```
source config.sh
```
An example is given in `config.sh.ex`.

## Building with setuptools

We assume the repo has been cloned with

```
git clone --recursive https://github.com/dselsam/lean-python-bindings
```

and that cmake and a C++ compiler is installed.

To install the package system wide, run

```
python setup.py install
```

and to do development in the directory run

```
python setup.py develop
```