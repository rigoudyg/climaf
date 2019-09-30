#!/usr/bin/env bash

report_ensemble=${1:-1}
echo $report_ensemble
run_modules=${2:-"netcdfbasics period cache classes functions operators standard_operators cmacro html"}
echo $run_modules

# Remove old results
coverage erase
rm -rf $PWD/htmlcov

# Run coverage with different tests
# coverage run --parallel-mode --source=climaf,scripts test_import.py

if [[ "$report_ensemble" == "1" ]]; then
    for module in $run_modules; do
        coverage run --parallel-mode --source=climaf,scripts "test_${module}.py"
        if [[ $? -neq 0 ]] ; then
            exit 1
        fi
    done
else
    for module in $run_modules; do
        coverage run --parallel-mode --source="climaf.${module}" "test_${module}.py"
        if [[ $? -neq 0 ]] ; then
            exit 1
        fi
    done
fi

# Assemble results
coverage combine

# Make html results
coverage html --title "CliMAF unitests coverage" -d $PWD/htmlcov

# Open html coverage
# firefox file://$PWD/htmlcov/index.html