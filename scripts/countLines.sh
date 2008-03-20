#!/bin/sh

one=`find -name "*.xml" -exec cat \{\} \; | wc -l`
two=`find -name "*.py" -exec cat \{\} \; | wc -l`
three=`find -name "*.sh" -exec cat \{\} \; | wc -l`
let res=$one+$two+$three
echo "Config lines: $one"
echo "Python lines: $two"
echo "Script lines: $three"
echo "Total: $res"

