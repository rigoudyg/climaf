#!/bin/bash
#
Usage="clean_pdf.sh [ last_changed_time ]"
#
# Remove pdf files without CliMAF Reference Syntax (CRS) 
# which status was last changed LAST_CHANGED_TIME*24 hours ago
# (see documentation of 'find' command at '-ctime' argument
# for more information about LAST_CHANGED_TIME argument)

set -x

age=$1

if [ "$age" ] ; then 
    find_cmd=$(find . -name '*.pdf' -ctime $age)
else
    find_cmd=$(find . -name '*.pdf')
fi

for file in $find_cmd 
do
  cmd=$(pdfinfo "$file" | grep "Keywords")

  if [ "$cmd" = "" ]; then
      rm $file
      echo 'file' $file 'was removed' 
  fi

done
