#!/bin/sh

rm -rf build_hex
mkdir build_hex
PYTHONPATH=`pwd`/../.. ../../bin/pycc test.p test.hex build_hex/
rm -rf build_hex
rm ../../pycc/*pyc
