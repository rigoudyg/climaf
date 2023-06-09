#!/usr/bin/env bash
# -*- coding: utf-8 -*-

#####
# Launch the unitary tests for CliMAF
# args:
#     - report_ensemble (if run_coverage is 1), default 1: if 1, coverage is computed for the whole CliMAF package, if 0 by module
#     - python_version, default 3: the python version to be used
#     - run_modules, default all: the list of test modules to be launched
#     - run_coverage, default 0: 1 coverage is on, 0 coverage is off
#     - plot_config, default default: the set of config used to generate plots, there is a set by default but it could not be the good one depending on the system install
#####
set -e

report_ensemble=${1:-1}
echo $report_ensemble
python_version=${2:-3}
echo $python_version
run_modules=${3:-"netcdfbasics period cache classes functions operators standard_operators operators_derive operators_scripts cmacro driver dataloc find_files html example_data_plot example_data_retrieval example_index_html mcdo"}
echo $run_modules
run_coverage=${4:-0}
echo $run_coverage
plot_config=${5:-"default"}
echo $plot_config

if [ $run_coverage -eq 1 ] ; then
    coverage_binary="coverage${python_version}"
    run_command_line="${coverage_binary} run --parallel-mode"
else
    run_command_line="python${python_version}"
fi

run_command_line="$run_command_line -W ignore::DeprecationWarning:pycompat"

# Add CliMAF path to environment
export PYTHONPATH=$PWD/..:$PYTHONPATH

# Remove old results
if [ $run_coverage -eq 1 ] ; then
    $coverage_binary erase
    rm -rf $PWD/htmlcov
fi
climaf_macros="$PWD/.climaf.macros_tests"
rm -f ${climaf_macros}
export CLIMAF_MACROS=${climaf_macros}

export CLIMAF_TEST_PLOT_CONFIG=${plot_config}

# Run coverage with different tests
if [ $run_coverage -eq 0 ] ; then
    ${run_command_line} "test_import.py"
fi
for module in $run_modules; do
    echo -e "\nTesting module : $module\n"
    echo $PWD
    if [ $run_coverage -eq 0 ] ; then
        ${run_command_line} "test_${module}.py"
    else
        if [[ "$report_ensemble" == "1" ]]; then
            ${run_command_line} --source=climaf,scripts "test_${module}.py"
        else
            ${run_command_line} --source="climaf.${module}" "test_${module}.py"
        fi
    fi
done

rm -f ${climaf_macros}

if [ $run_coverage -eq 1 ] ; then
    # Assemble results
    $coverage_binary combine

    # Make html results
    $coverage_binary html --title "CliMAF unitests coverage" -d $PWD/htmlcov

    # Open html coverage
    # firefox file://$PWD/htmlcov/index.html
fi
