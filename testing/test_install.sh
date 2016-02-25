#!/bin/bash
# Created - S.Senesi - Feb 2015
export PYTHONPATH=$(cd $(dirname $0)/..; pwd):$PYTHONPATH

if ! [[ $(python -V 2>&1) == *2.7* ]]; then
    echo "Python 2.7 is required"
    exit 1
fi

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
Consider registering to the climaf.users mailing list
(send mail to sympa@meteo.fr with body: 'sub climaf.users')\n
_____________________________________________________

Doc is at http://climaf.readthedocs.org
_____________________________________________________
\n"
