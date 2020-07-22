#!/usr/bin/env bash

version=${1:-2}
report_ensemble=${2:-1}
echo $report_ensemble
run_modules=${3:-"netcdfbasics period cache classes functions operators standard_operators operators_derive operators_scripts cmacro html example_data_plot example_data_retrieval example_index_html mcdo"}
echo $run_modules

# Add CliMAF path to environment
export PYTHONPATH=$PYTHONPATH:$PWD/..

# Remove old results
coverage erase
rm -rf $PWD/htmlcov
climaf_macros="$PWD/.climaf.macros_tests"
rm -f ${climaf_macros}
export CLIMAF_MACROS=${climaf_macros}

# Run coverage with different tests
# coverage run --parallel-mode --source=climaf,scripts test_import.py

if [[ "$version" == "2" ]]; then
    for module in $run_modules; do
        python2 "test_${module}.py"
        if [ ! $? -eq 0 ] ; then
            exit 1
        fi
    done
else
    for module in $run_modules; do
        python3 "test_${module}.py"
        if [ ! $? -eq 0 ] ; then
            exit 1
        fi
    done
fi

rm -f ${climaf_macros}

# Assemble results
coverage combine

# Make html results
coverage html --title "CliMAF unitests coverage" -d $PWD/htmlcov

# Open html coverage
# firefox file://$PWD/htmlcov/index.html
