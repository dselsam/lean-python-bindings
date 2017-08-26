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

FIXME: We also assume that the Lean Theorem Prover is installed to /usr/local/<...>. 

1. Activate a virtualenv (optional).

2. Install the requirements.
```
pip install -r requirements.txt
```

3. Install the package.

Install system wide:
```
python setup.py install
```
Install for development:
```
python setup.py develop
```
