#!/usr/bin/env bash

report_ensemble=${1:-1}
echo $report_ensemble
python_version=${2:-2}
echo $python_version
run_modules=${3:-"netcdfbasics period cache classes functions operators standard_operators operators_derive operators_scripts cmacro html example_data_plot example_data_retrieval example_index_html mcdo"}
echo $run_modules

coverage_binary="coverage${python_version}"

# Add CliMAF path to environment
export PYTHONPATH=$PWD/..:$PYTHONPATH

# Remove old results
$coverage_binary erase
rm -rf $PWD/htmlcov
climaf_macros="$PWD/.climaf.macros_tests"
rm -f ${climaf_macros}
export CLIMAF_MACROS=${climaf_macros}

# Run coverage with different tests
# coverage run --parallel-mode --source=climaf,scripts test_import.py

if [[ "$report_ensemble" == "1" ]]; then
    for module in $run_modules; do
        $coverage_binary run --parallel-mode --source=climaf,scripts "test_${module}.py"
        if [ ! $? -eq 0 ] ; then
            exit 1
        fi
    done
else
    for module in $run_modules; do
        $coverage_binary run --parallel-mode --source="climaf.${module}" "test_${module}.py"
        if [ ! $? -eq 0 ] ; then
            exit 1
        fi
    done
fi

rm -f ${climaf_macros}

# Assemble results
$coverage_binary combine

# Make html results
$coverage_binary html --title "CliMAF unitests coverage" -d $PWD/htmlcov

# Open html coverage
# firefox file://$PWD/htmlcov/index.html