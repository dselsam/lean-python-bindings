#!/usr/bin/env bash

set -x
# Fail if a single command fails
set -e

mkdir -p build

pushd build
  cmake ..
  make -j4
popd
