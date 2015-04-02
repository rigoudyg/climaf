# Computig and plotting an annual cycle 

from climaf.api import *

# Define a dataset
dataloc(experiment="AMIPV6ALB2G", organization="example",
        url=[cpath+"/../examples/data/AMIPV6ALB2G"])
dg=ds(experiment="AMIPV6ALB2G", variable="tas", period="1980-1981", frequency="monthly")

# Compute annual cycle, using swiss knife operator 'ccdo', and look at it
anncycle=ccdo(dg,operator='ymonavg')
ncview(anncycle)

# Define the average annual cycle over a latlon box
extract=llbox(anncycle, latmin=30, latmax=60, lonmin=-30, lonmax=30)
space_average=ccdo(extract,operator='fldavg')

# Show it (this triggers computation)
ncview(space_average)

# Creating a figure with standard operator timeplot
fig_avg=timeplot(space_average, title="Annual cycle")

# Get the figure computed, and get its filename in CliMAF file cache
figfile=cfile(fig_avg)


