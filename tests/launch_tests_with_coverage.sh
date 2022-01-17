#!/usr/bin/env bash

report_ensemble=${1:-1}
echo $report_ensemble
python_version=${2:-2}
echo $python_version
run_modules=${3:-"netcdfbasics period cache classes functions operators standard_operators operators_derive operators_scripts cmacro driver dataloc find_files html example_data_plot example_data_retrieval example_index_html mcdo"}
echo $run_modules
run_coverage=${4:-0}
echo $run_coverage

if [ $run_coverage -eq 1 ] ; then
    coverage_binary="coverage${python_version}"
    run_command_line="${coverage_binary} run --parallel-mode"
else
    run_command_line="python${python_version}"
fi

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

# Run coverage with different tests
if [ $run_coverage -eq 0 ] ; then
    ${run_command_line} "test_import.py"
fi
for module in $run_modules; do
    echo -e "\nTesting module : $module\n"
    echo $PWD
    if [ $run_coverage -eq 0 ] ; then
        ${run_command_line} "test_${module}.py"
        if [ ! $? -eq 0 ] ; then
            exit 1
        fi
    else
        if [[ "$report_ensemble" == "1" ]]; then
            ${run_command_line} --source=climaf,scripts "test_${module}.py"
            if [ ! $? -eq 0 ] ; then
                exit 1
            fi
        else
            ${run_command_line} --source="climaf.${module}" "test_${module}.py"
            if [ ! $? -eq 0 ] ; then
                exit 1
            fi
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
