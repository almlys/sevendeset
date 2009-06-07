#!/bin/sh

find -name "*~" -exec rm -f {} \;
find -name "*.bak" -exec rm -f {} \;
find -name "*.pyc" -exec rm -f {} \;
find -name "*.class" -exec rm -f {} \;
