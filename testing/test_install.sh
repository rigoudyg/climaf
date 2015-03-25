#!/bin/bash
# Created - S.Senesi - Feb 2015
issues=0
echo -e "\nTesting system requirements\n"
if ! python -m unittest -b -v -f test_req ; then 
    echo "You cannot run CliMAF without the binaries reported missing above"
    exit 1
fi
echo -e "\nTesting some CliMAF processing\n"
if ! python -m unittest -b -v -f test_1 ; then 
    echo "There is an issue installing CliMAF. Please report to climaf at meteo.fr, with a copy of output above"
    exit 1
fi
echo -e "\nEverything seems to be fine, you may proceed and use CliMAF - 
A beginner's guide is not yet available, but please have a look at directory examples
And don't forget to set :
\t export PYTHONPATH=$(cd ..; pwd):\$PYTHONPATH
either in your .profile or each time you want to use CliMAF\n"
